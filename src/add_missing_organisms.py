#!/usr/bin/env python3
"""
Add missing organism references to genomes table.

This script identifies organisms referenced in genes/proteins table
that are not present in the genomes table, then queries NCBI to get
their taxonomy IDs and genome information.
"""

import argparse
import pandas as pd
from pathlib import Path
from typing import List, Dict, Optional
import time
from Bio import Entrez

# Configure Entrez
Entrez.email = "your.email@example.com"


def normalize_organism_name(name: str) -> str:
    """Normalize organism name for matching."""
    if pd.isna(name):
        return ""

    # Remove strain info in parentheses for base matching
    name_str = str(name).strip()
    if "(" in name_str:
        name_str = name_str.split("(")[0].strip()

    return name_str


def get_ncbi_taxon_id(organism_name: str) -> Optional[int]:
    """Query NCBI Taxonomy to get taxon ID for organism.

    Args:
        organism_name: Scientific name of organism

    Returns:
        NCBITaxon ID or None if not found
    """
    def try_search(search_term: str) -> Optional[int]:
        """Try searching with a specific term."""
        try:
            time.sleep(0.5)  # Rate limiting

            # Search taxonomy database
            search_handle = Entrez.esearch(
                db="taxonomy",
                term=search_term,
                retmax=1
            )
            search_results = Entrez.read(search_handle)
            search_handle.close()

            if not search_results["IdList"]:
                return None

            taxon_id = int(search_results["IdList"][0])

            # Fetch taxonomy details to verify
            time.sleep(0.5)
            fetch_handle = Entrez.efetch(
                db="taxonomy",
                id=taxon_id,
                retmode="xml"
            )
            fetch_results = Entrez.read(fetch_handle)
            fetch_handle.close()

            if fetch_results:
                scientific_name = fetch_results[0]["ScientificName"]
                print(f"    ✓ Found: {scientific_name} (NCBITaxon:{taxon_id})")
                return taxon_id

            return None

        except Exception as e:
            print(f"    ❌ Error querying NCBI Taxonomy: {e}")
            return None

    # Try full name first
    print(f"  Searching NCBI Taxonomy for: {organism_name}")
    taxon_id = try_search(organism_name)
    if taxon_id:
        return taxon_id

    # If not found and has strain info, try without strain designation
    if "(" in organism_name or "strain" in organism_name.lower():
        # Extract genus and species only
        parts = organism_name.split("(")[0].strip().split()
        if len(parts) >= 2:
            genus_species = f"{parts[0]} {parts[1]}"
            print(f"    Trying without strain info: {genus_species}")
            taxon_id = try_search(genus_species)
            if taxon_id:
                return taxon_id

    print(f"    ⚠️  No taxonomy match found")
    return None


def get_ncbi_assembly_info(taxon_id: int) -> Optional[Dict[str, str]]:
    """Query NCBI Assembly database for genome info.

    Args:
        taxon_id: NCBITaxon ID

    Returns:
        Dictionary with genome info or None if not found
    """
    try:
        print(f"  Searching NCBI Assembly for taxon {taxon_id}")
        time.sleep(0.5)  # Rate limiting

        # Search assembly database
        search_handle = Entrez.esearch(
            db="assembly",
            term=f"txid{taxon_id}[Organism:exp]",
            retmax=1,
            sort="relevance"
        )
        search_results = Entrez.read(search_handle)
        search_handle.close()

        if not search_results["IdList"]:
            print(f"    ⚠️  No assembly found")
            return None

        assembly_id = search_results["IdList"][0]

        # Fetch assembly details
        time.sleep(0.5)
        summary_handle = Entrez.esummary(
            db="assembly",
            id=assembly_id,
            retmode="xml"
        )
        summary_results = Entrez.read(summary_handle)
        summary_handle.close()

        if not summary_results["DocumentSummarySet"]["DocumentSummary"]:
            return None

        assembly_doc = summary_results["DocumentSummarySet"]["DocumentSummary"][0]

        # Extract genome info
        genome_id = assembly_doc.get("AssemblyAccession", "")
        ftp_path = assembly_doc.get("FtpPath_RefSeq") or assembly_doc.get("FtpPath_GenBank", "")

        # Generate annotation download URL
        annotation_url = ""
        if ftp_path and genome_id:
            # Format: ftp://ftp.ncbi.nlm.nih.gov/genomes/all/GCF/xxx/xxx/xxx/GCF_xxx_*_genomic.gff.gz
            annotation_url = f"{ftp_path}/{genome_id}_*_genomic.gff.gz"

        print(f"    ✓ Found assembly: {genome_id}")

        return {
            "genome_id": genome_id,
            "annotation_url": annotation_url
        }

    except Exception as e:
        print(f"    ❌ Error querying NCBI Assembly: {e}")
        return None


def find_missing_organisms(genes_file: str, genomes_file: str) -> List[str]:
    """Find organisms in genes table that are not in genomes table.

    Args:
        genes_file: Path to genes/proteins TSV file
        genomes_file: Path to genomes TSV file

    Returns:
        List of missing organism names
    """
    genes_df = pd.read_csv(genes_file, sep='\t')
    genomes_df = pd.read_csv(genomes_file, sep='\t')

    # Get all organism names from genomes table
    genome_organisms = set()
    for _, row in genomes_df.iterrows():
        name = row.get("Scientific name", "")
        if pd.notna(name):
            genome_organisms.add(normalize_organism_name(name))

    # Find organisms in genes table not in genomes table
    missing_organisms = set()
    for _, row in genes_df.iterrows():
        org = row.get("organism (from taxa and genomes tab)", "")
        if pd.isna(org):
            continue

        org_str = str(org).strip()
        org_normalized = normalize_organism_name(org_str)

        # Check if organism exists (fuzzy match on genus)
        genus = org_normalized.split()[0] if org_normalized else ""
        matched = any(genus in genome_org for genome_org in genome_organisms)

        # Skip generic or placeholder names
        if genus in ["Various", "Methylotroph", ""]:
            continue

        if not matched:
            missing_organisms.add(org_str)

    return sorted(missing_organisms)


def add_missing_organisms_to_genomes(
    genes_file: str,
    genomes_file: str,
    output_file: str = None
) -> int:
    """Add missing organisms from genes table to genomes table.

    Args:
        genes_file: Path to genes/proteins TSV file
        genomes_file: Path to genomes TSV file
        output_file: Path to output TSV file (defaults to genomes_file)

    Returns:
        Number of organisms added
    """
    if output_file is None:
        output_file = genomes_file

    print("\n" + "=" * 80)
    print("Adding Missing Organisms to Genomes Table")
    print("=" * 80)

    # Find missing organisms
    print("\nIdentifying missing organisms...")
    missing_organisms = find_missing_organisms(genes_file, genomes_file)

    if not missing_organisms:
        print("✓ No missing organisms found")
        return 0

    print(f"Found {len(missing_organisms)} missing organisms:")
    for org in missing_organisms:
        print(f"  • {org}")

    # Load genomes table
    genomes_df = pd.read_csv(genomes_file, sep='\t')

    # Query NCBI for each missing organism
    print("\nQuerying NCBI for organism information...")
    added_count = 0

    for organism_name in missing_organisms:
        print(f"\nProcessing: {organism_name}")

        # Get taxon ID
        taxon_id = get_ncbi_taxon_id(organism_name)
        if not taxon_id:
            continue

        # Get assembly info
        assembly_info = get_ncbi_assembly_info(taxon_id)

        # Create new row
        new_row = {
            "Scientific name": organism_name,
            "NCBITaxon id": taxon_id,
            "Genome identifier (GenBank, IMG etc)": assembly_info["genome_id"] if assembly_info else "",
            "Annotation download URL": assembly_info["annotation_url"] if assembly_info else "",
            "source": "fix_validation"
        }

        # Add any other columns that exist in genomes table
        for col in genomes_df.columns:
            if col not in new_row:
                new_row[col] = ""

        # Append to dataframe
        genomes_df = pd.concat([genomes_df, pd.DataFrame([new_row])], ignore_index=True)
        added_count += 1
        print(f"  ✓ Added to genomes table")

    # Save updated genomes table
    genomes_df.to_csv(output_file, sep='\t', index=False)

    print("\n" + "=" * 80)
    print(f"✓ Added {added_count} organisms to genomes table")
    print(f"✓ Saved to: {output_file}")
    print("=" * 80)

    return added_count


def main():
    """Command-line interface."""
    parser = argparse.ArgumentParser(
        description="Add missing organism references to genomes table",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Add missing organisms to extended genomes table
  python src/add_missing_organisms.py

  # Add to specific files
  python src/add_missing_organisms.py --genes-file data/txt/sheet/BER_CMM_Data_for_AI_genes_and_proteins.tsv --genomes-file data/txt/sheet/BER_CMM_Data_for_AI_taxa_and_genomes.tsv
"""
    )

    parser.add_argument(
        "--genes-file",
        default="data/txt/sheet/BER_CMM_Data_for_AI_genes_and_proteins_extended.tsv",
        help="Path to genes/proteins TSV file"
    )
    parser.add_argument(
        "--genomes-file",
        default="data/txt/sheet/BER_CMM_Data_for_AI_taxa_and_genomes_extended.tsv",
        help="Path to genomes TSV file"
    )
    parser.add_argument(
        "--output-file",
        help="Path to output TSV file (defaults to genomes-file)"
    )

    args = parser.parse_args()

    # Check if files exist
    if not Path(args.genes_file).exists():
        print(f"Error: Genes file not found: {args.genes_file}")
        return 1

    if not Path(args.genomes_file).exists():
        print(f"Error: Genomes file not found: {args.genomes_file}")
        return 1

    # Add missing organisms
    try:
        added_count = add_missing_organisms_to_genomes(
            args.genes_file,
            args.genomes_file,
            args.output_file
        )

        if added_count > 0:
            print("\nRecommended next steps:")
            print("  1. Run validation again: make validate-consistency")
            print("  2. Review the newly added organisms")
            print("  3. Run crosslink to update gene-genome references: make crosslink")

        return 0

    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    import sys
    sys.exit(main())
