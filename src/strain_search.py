"""Strain search functions for microbial culture collection and procurement information.

This module queries KG-Microbe (DuckDB), NCBI Taxonomy, and BacDive APIs to extract
standardized strain information including culture collection IDs, type strain designation,
and procurement details.
"""

import time
import re
from typing import Dict, List, Optional, Tuple
import pandas as pd
import requests
from pathlib import Path
from Bio import Entrez
import sys

# Import KG-Microbe database interface
try:
    from kg_analysis.kg_database import KnowledgeGraphDB
except (ImportError, AttributeError) as e:
    print(f"Warning: Could not import KnowledgeGraphDB: {e}")
    print("KG-Microbe queries will be unavailable.")
    KnowledgeGraphDB = None

# Configure Entrez
Entrez.email = "your.email@example.com"  # Should be configured


def parse_strain_from_name(scientific_name: str) -> Tuple[str, str]:
    """Parse strain designation from scientific name.

    Args:
        scientific_name: Full scientific name potentially including strain info

    Returns:
        Tuple of (species_name, strain_designation)

    Examples:
        >>> parse_strain_from_name("Methylosinus sp. C49")
        ('Methylosinus sp.', 'C49')
        >>> parse_strain_from_name("Methylobacterium aquaticum Strain 22A")
        ('Methylobacterium aquaticum', '22A')
        >>> parse_strain_from_name("Paracoccus denitrificans")
        ('Paracoccus denitrificans', '')
    """
    # Handle None, NaN, or empty values
    if not scientific_name or (isinstance(scientific_name, float) and pd.isna(scientific_name)):
        return '', ''

    name = str(scientific_name).strip()

    # Pattern 1: "Genus sp. STRAIN"
    match = re.match(r'(.+?sp\.)\s+([A-Z0-9\-_]+)$', name)
    if match:
        return match.group(1).strip(), match.group(2).strip()

    # Pattern 2: "Genus species Strain XXX" or "Genus species STRAIN"
    match = re.match(r'(.+?)\s+(?:Strain|strain)\s+([A-Z0-9\-_]+.*?)$', name)
    if match:
        return match.group(1).strip(), match.group(2).strip()

    # Pattern 3: Culture collection IDs in name (e.g., "CCM : 7218 , CECT : 5998")
    if re.search(r'[A-Z]{2,6}\s*:\s*\d+', name):
        # Extract base name before first collection ID
        match = re.match(r'(.+?)\s+[A-Z]{2,6}\s*:', name)
        if match:
            return match.group(1).strip(), ''

    # Pattern 4: "Genus species PROJECT-CODE"
    match = re.match(r'(.+?)\s+([A-Z]+\d+|[A-Z]+\-\d+)$', name)
    if match:
        return match.group(1).strip(), match.group(2).strip()

    # No strain found
    return name, ''


def extract_culture_collection_ids(text: str) -> List[str]:
    """Extract culture collection IDs from text.

    Args:
        text: Text containing potential culture collection IDs

    Returns:
        List of culture collection IDs in format "COLLECTION:ID"

    Examples:
        >>> extract_culture_collection_ids("ATCC 14718 / DSM 1338 / JCM 2805")
        ['ATCC:14718', 'DSM:1338', 'JCM:2805']
        >>> extract_culture_collection_ids("CCM : 7218 , CECT : 5998")
        ['CCM:7218', 'CECT:5998']
    """
    # Handle None, NaN, or empty values
    if not text or (isinstance(text, float) and pd.isna(text)):
        return []

    # Convert to string safely
    text = str(text)

    collection_ids = []

    # Pattern: COLLECTION : NUMBER or COLLECTION NUMBER or COLLECTION:NUMBER
    pattern = r'([A-Z]{2,10})\s*:?\s*(\d+)'
    matches = re.findall(pattern, text)

    for collection, number in matches:
        # Filter known culture collections
        known_collections = {
            'ATCC', 'DSM', 'DSMZ', 'JCM', 'NCIMB', 'NBRC', 'CCM', 'CECT',
            'CIP', 'BCRC', 'IAM', 'LMG', 'NCPPB', 'CFBP', 'USDA', 'NCTC'
        }
        if collection in known_collections:
            collection_ids.append(f"{collection}:{number}")

    return collection_ids


def query_kg_microbe_for_strain(taxon_id: int, organism_name: str) -> Dict:
    """Query KG-Microbe DuckDB for strain information.

    Args:
        taxon_id: NCBITaxon ID
        organism_name: Scientific name of organism

    Returns:
        Dictionary with strain information from KG-Microbe
    """
    if KnowledgeGraphDB is None:
        return {}

    try:
        kg = KnowledgeGraphDB("data/kgm/kg-microbe.duckdb")

        # Query for strain nodes related to this taxon
        strain_query = f"""
            SELECT DISTINCT n.id, n.name, n.category
            FROM nodes n
            JOIN edges e ON n.id = e.subject
            WHERE e.object = 'NCBITaxon:{taxon_id}'
              AND (n.category LIKE '%strain%' OR n.category LIKE '%OrganismTaxon%')
            LIMIT 10
        """

        strain_nodes = kg.query(strain_query)

        if strain_nodes.empty:
            return {}

        # Get the first strain node
        strain_id = strain_nodes.iloc[0]['id']
        strain_name = strain_nodes.iloc[0]['name']

        # Query for culture collection identifiers
        collection_query = f"""
            SELECT e.object, n.name
            FROM edges e
            LEFT JOIN nodes n ON e.object = n.id
            WHERE e.subject = '{strain_id}'
              AND e.predicate = 'biolink:has_identifier'
        """

        collections = kg.query(collection_query)

        # Extract culture collection IDs
        culture_ids = []
        for _, row in collections.iterrows():
            if pd.notna(row['object']):
                # Check if object is a culture collection ID
                extracted = extract_culture_collection_ids(str(row['object']))
                culture_ids.extend(extracted)

        # Query for phenotypes (growth requirements)
        phenotype_query = f"""
            SELECT n.name, e.predicate
            FROM edges e
            JOIN nodes n ON e.object = n.id
            WHERE e.subject = 'NCBITaxon:{taxon_id}'
              AND e.predicate IN ('biolink:has_phenotype', 'biolink:capable_of')
            LIMIT 5
        """

        phenotypes = kg.query(phenotype_query)

        growth_reqs = []
        for _, row in phenotypes.iterrows():
            if pd.notna(row['name']):
                growth_reqs.append(row['name'])

        kg.close()

        return {
            'strain_id': strain_id if strain_id else '',
            'culture_collection_ids': culture_ids,
            'growth_requirements': '; '.join(growth_reqs[:3]) if growth_reqs else '',
            'kg_microbe_name': strain_name
        }

    except Exception as e:
        print(f"  Error querying KG-Microbe for {organism_name}: {e}")
        return {}


def query_kg_microbe_nodes_for_strain(taxon_id: int, organism_name: str) -> List[str]:
    """Query KG-Microbe for nodes matching the strain.

    Searches for strain: and NCBITaxon: node types.

    Args:
        taxon_id: NCBITaxon ID
        organism_name: Scientific name of organism

    Returns:
        List of matching KG-Microbe node IDs
    """
    if KnowledgeGraphDB is None:
        return []

    try:
        kg = KnowledgeGraphDB("data/kgm/kg-microbe.duckdb")
        matched_nodes = []

        # Query 1: Match by NCBITaxon ID
        if taxon_id:
            taxon_node = f"NCBITaxon:{taxon_id}"
            taxon_query = f"""
                SELECT DISTINCT id, name
                FROM nodes
                WHERE id = '{taxon_node}'
                   OR id LIKE '%NCBITaxon:{taxon_id}%'
                LIMIT 5
            """
            results = kg.query(taxon_query)
            if not results.empty:
                for _, row in results.iterrows():
                    matched_nodes.append(row['id'])

        # Query 2: Match by organism name for strain: nodes
        if organism_name and len(matched_nodes) < 10:
            strain_query = f"""
                SELECT DISTINCT id, name
                FROM nodes
                WHERE id LIKE 'strain:%'
                  AND (LOWER(name) LIKE LOWER('%{organism_name}%')
                       OR LOWER(name) LIKE LOWER('%{organism_name.split()[0]}%'))
                LIMIT 10
            """
            results = kg.query(strain_query)
            if not results.empty:
                for _, row in results.iterrows():
                    node_id = row['id']
                    if node_id not in matched_nodes:
                        matched_nodes.append(node_id)

        kg.close()
        return matched_nodes[:10]  # Limit to 10 nodes

    except Exception as e:
        print(f"  Warning: KG-Microbe node query failed for {organism_name}: {e}")
        return []


def query_ncbi_taxonomy(taxon_id: int) -> Dict:
    """Query NCBI Taxonomy for strain and type strain information.

    Args:
        taxon_id: NCBITaxon ID

    Returns:
        Dictionary with taxonomy information
    """
    try:
        # Fetch taxonomy record
        handle = Entrez.efetch(db="taxonomy", id=str(taxon_id), retmode="xml")
        records = Entrez.read(handle)
        handle.close()

        if not records:
            return {}

        record = records[0]

        # Extract culture collection IDs from OtherNames -> Name with ClassCDE='type material'
        other_names = record.get('OtherNames', {})
        name_list = other_names.get('Name', [])

        culture_ids = []
        is_type_strain = False

        for name_entry in name_list:
            if isinstance(name_entry, dict):
                class_cde = name_entry.get('ClassCDE', '')
                disp_name = name_entry.get('DispName', '')

                # Extract culture collection IDs from type material entries
                if class_cde == 'type material':
                    is_type_strain = True
                    # Extract IDs using the extraction function
                    extracted = extract_culture_collection_ids(disp_name)
                    culture_ids.extend(extracted)

        # Deduplicate while preserving order
        culture_ids = list(dict.fromkeys(culture_ids))

        # Extract alternative names from synonyms and equivalent names
        synonyms = other_names.get('Synonym', [])
        equivalent_names = other_names.get('EquivalentName', [])

        all_names = []
        if isinstance(synonyms, list):
            all_names.extend(synonyms)
        elif synonyms:
            all_names.append(synonyms)
        if isinstance(equivalent_names, list):
            all_names.extend(equivalent_names)
        elif equivalent_names:
            all_names.append(equivalent_names)

        return {
            'type_strain': 'yes' if is_type_strain else 'no',
            'culture_collection_ids': culture_ids,
            'alternative_names': '; '.join(all_names[:5]) if all_names else '',
            'lineage': record.get('Lineage', '')
        }

    except Exception as e:
        print(f"  Error querying NCBI for taxon {taxon_id}: {e}")
        return {}


def query_bacdive(organism_name: str, culture_id: str = None) -> Dict:
    """Query BacDive API for strain information (requires API key).

    Args:
        organism_name: Scientific name of organism
        culture_id: Culture collection ID (e.g., "DSM 1338")

    Returns:
        Dictionary with BacDive information (empty if API unavailable)
    """
    # BacDive requires API key - skip for now unless configured
    # TODO: Implement BacDive API once credentials available
    # https://api.bacdive.dsmz.de/doc/

    return {}


def generate_procurement_urls(culture_ids: List[str]) -> List[str]:
    """Generate procurement URLs from culture collection IDs.

    Args:
        culture_ids: List of culture collection IDs (e.g., ["ATCC:14718", "DSM:1338"])

    Returns:
        List of URLs to culture collection pages
    """
    url_templates = {
        'ATCC': 'https://www.atcc.org/products/{}',
        'DSM': 'https://www.dsmz.de/collection/catalogue/details/culture/DSM-{}',
        'DSMZ': 'https://www.dsmz.de/collection/catalogue/details/culture/DSM-{}',
        'JCM': 'https://jcm.brc.riken.jp/cgi-bin/jcm/jcm_number?JCM={}',
        'NCIMB': 'https://www.ncimb.com/product/NCIMB{}',
        'NBRC': 'https://www.nite.go.jp/nbrc/catalogue/NBRCCatalogueDetailServlet?ID=NBRC&CAT={}',
        'CCM': 'https://ccm.sci.muni.cz/detail.php?id={}',
        'CECT': 'https://www.uv.es/uvweb/spanish-type-culture-collection/en/spanish-type-culture-collection/catalogue-cect/bacterial-catalogue/detail-1285872530871/Catalogo.html?id={}',
    }

    urls = []
    for cid in culture_ids:
        if ':' in cid:
            collection, number = cid.split(':', 1)
            if collection in url_templates:
                url = url_templates[collection].format(number)
                urls.append(url)

    return urls


def create_extended_strains_table(
    input_file: str = "data/txt/sheet/PFAS_Data_for_AI_taxa_and_genomes_extended.tsv",
    output_dir: str = "data/txt/sheet",
    max_rows: int = 100
) -> None:
    """Create extended strains table from taxa_and_genomes data.

    Args:
        input_file: Path to taxa_and_genomes TSV file
        output_dir: Directory to save extended table
        max_rows: Maximum number of rows to process from taxa sheet (default: 100)
    """
    print("=" * 80)
    print("STRAINS DATA EXTENSION")
    print("=" * 80)
    print()

    # Read taxa and genomes data
    print(f"Reading taxa data from {input_file}...")
    taxa_df = pd.read_csv(input_file, sep='\t', nrows=max_rows)
    print(f"  Found {len(taxa_df)} organisms")
    print()

    # Process each organism
    all_strains = []
    skipped_count = 0

    for idx, row in taxa_df.iterrows():
        scientific_name = row['Scientific name']
        taxon_id = int(row['NCBITaxon id']) if pd.notna(row['NCBITaxon id']) else None

        print(f"[{idx+1}/{len(taxa_df)}] Processing: {scientific_name}")

        # Skip invalid scientific names (NaN, None, empty)
        if not scientific_name or (isinstance(scientific_name, float) and pd.isna(scientific_name)):
            print(f"  ⊗ Skipped: Invalid scientific name")
            skipped_count += 1
            continue

        if not taxon_id:
            print(f"  ⊗ Skipped: No NCBITaxon ID")
            skipped_count += 1
            continue

        # Parse strain designation from name
        species_name, strain_designation = parse_strain_from_name(scientific_name)

        # Extract any culture IDs from the name itself
        name_culture_ids = extract_culture_collection_ids(scientific_name)

        # Step 1: Query KG-Microbe (primary source)
        print(f"  → Querying KG-Microbe...")
        kg_data = query_kg_microbe_for_strain(taxon_id, scientific_name)

        culture_ids = list(set(name_culture_ids + kg_data.get('culture_collection_ids', [])))
        growth_reqs = kg_data.get('growth_requirements', '')

        # Step 2: Query NCBI Taxonomy if KG-Microbe incomplete
        if not culture_ids or kg_data.get('type_strain') is None:
            print(f"  → Querying NCBI Taxonomy...")
            ncbi_data = query_ncbi_taxonomy(taxon_id)

            if ncbi_data:
                culture_ids.extend(ncbi_data.get('culture_collection_ids', []))
                culture_ids = list(set(culture_ids))  # Deduplicate

                if 'type_strain' in ncbi_data:
                    type_strain = ncbi_data['type_strain']
                else:
                    type_strain = 'no'

                alternative_names = ncbi_data.get('alternative_names', '')
            else:
                type_strain = 'no'
                alternative_names = ''

            time.sleep(0.5)  # Rate limiting for NCBI
        else:
            type_strain = 'no'
            alternative_names = ''

        # Special handling for key PFAS degraders
        # IMPORTANT: This must come BEFORE the skip check so we can add culture IDs
        if 'plecoglossicida' in scientific_name.lower() and '2.4-D' in scientific_name:
            # Pseudomonas plecoglossicida 2.4-D (PFAS degrader)
            if not strain_designation:
                strain_designation = '2.4-D'
            if '2.4-D' not in alternative_names:
                alternative_names = 'Pseudomonas sp. 2.4-D' + ('; ' + alternative_names if alternative_names else '')
            print(f"  ★ Enhanced Pseudomonas plecoglossicida 2.4-D (PFAS degrader)")

        elif 'acidimicrobium' in scientific_name.lower() and 'A6' in scientific_name:
            # Acidimicrobium sp. A6 (PFAS degrader)
            if not strain_designation:
                strain_designation = 'A6'
            print(f"  ★ Enhanced Acidimicrobium sp. A6 (acid-tolerant PFAS degrader)")

        # Skip if no culture collection IDs found
        if not culture_ids:
            print(f"  ⊗ Skipped: No culture collection IDs found")
            skipped_count += 1
            continue

        # Generate procurement URLs
        procurement_urls = generate_procurement_urls(culture_ids)

        # Query KG-Microbe for matching nodes
        kg_nodes = query_kg_microbe_nodes_for_strain(taxon_id, species_name)

        # Create strain record
        strain_record = {
            'strain_id': culture_ids[0] if culture_ids else f"STRAIN_{idx+1:03d}",
            'species_taxon_id': taxon_id,
            'scientific_name': species_name,
            'strain_designation': strain_designation,
            'type_strain': type_strain,
            'culture_collection_ids': '; '.join(culture_ids),
            'procurement_urls': '; '.join(procurement_urls),
            'availability_status': 'available' if culture_ids else 'unknown',
            'alternative_names': alternative_names,
            'biosafety_level': 1,  # Default BSL-1 for most environmental bacteria
            'growth_requirements': growth_reqs,
            'kg_microbe_nodes': '; '.join(kg_nodes) if kg_nodes else '',
            'notes': '',
            'source': 'extend1'
        }

        all_strains.append(strain_record)
        print(f"  ✓ Added strain with {len(culture_ids)} culture collection IDs")
        print()

    print("=" * 80)
    print(f"Total strains with culture collection IDs: {len(all_strains)}")
    print(f"Skipped (no culture collection IDs): {skipped_count}")
    print("=" * 80)
    print()

    # Convert to DataFrame
    strains_df = pd.DataFrame(all_strains)

    # Save to file
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    output_file = output_dir / "PFAS_Data_for_AI_strains_extended.tsv"
    strains_df.to_csv(output_file, sep='\t', index=False)

    print(f"Extended strains table saved: {output_file}")
    print(f"  Total strains: {len(strains_df)}")
    print()

    # Summary by genus
    print("Strains by genus:")
    for genus in strains_df['scientific_name'].str.split().str[0].value_counts().head(10).items():
        print(f"  {genus[0]}: {genus[1]} strains")


if __name__ == "__main__":
    """Run strain search when executed directly."""
    create_extended_strains_table()
