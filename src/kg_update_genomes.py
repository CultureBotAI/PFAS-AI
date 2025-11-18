#!/usr/bin/env python3
"""
Update taxa_and_genomes table using Knowledge Graph mining

This script queries both kg-microbe and kg-microbe-function to find:
- Related taxa from the same genus/family
- Taxa with similar functional profiles
- Taxa with phenotypic data in kg-microbe

All new records are labeled with source='kg_update'.
Repeatable: Deduplication prevents duplicate entries on repeated runs.
"""

from pathlib import Path
from typing import Dict, List, Set, Optional, Tuple
import pandas as pd
import argparse
from src.kg_mining_utils import (
    KGMiningSession,
    load_taxon_ids,
    save_extended_table,
    summarize_extraction,
    format_source_label
)


def get_existing_taxa(
    taxa_file: str = "data/txt/sheet/BER_CMM_Data_for_AI_taxa_and_genomes.tsv"
) -> Set[str]:
    """
    Load existing NCBITaxon IDs from taxa table.

    Args:
        taxa_file: Path to taxa TSV file

    Returns:
        Set of existing NCBITaxon IDs (formatted as "NCBITaxon:12345")
    """
    if not Path(taxa_file).exists():
        print(f"⚠️  File not found: {taxa_file}")
        return set()

    df = pd.read_csv(taxa_file, sep='\t')

    existing_ids = set()
    for idx, row in df.iterrows():
        taxon_id = row.get("NCBITaxon id")
        if pd.notna(taxon_id):
            tid = f"NCBITaxon:{int(float(taxon_id))}"
            existing_ids.add(tid)

    print(f"Loaded {len(existing_ids)} existing taxon IDs from {taxa_file}")
    return existing_ids


def query_related_taxa_from_phenotype_kg(
    session: KGMiningSession,
    taxon_ids: List[str],
    limit: int = 500
) -> pd.DataFrame:
    """
    Query kg-microbe for taxa with phenotypic data.

    Args:
        session: Active KG mining session
        taxon_ids: List of target NCBITaxon IDs
        limit: Maximum taxa to retrieve

    Returns:
        DataFrame with taxon_id, taxon_name, phenotype info
    """
    if not session.phenotype_kg:
        raise RuntimeError("Phenotypic KG not enabled in session")

    print(f"\nQuerying kg-microbe for related taxa...")

    # Query for taxa with phenotypic annotations
    sql = f"""
    SELECT DISTINCT
        n.id as taxon_id,
        n.name as taxon_name,
        n.category as taxon_category
    FROM nodes n
    WHERE n.id LIKE 'NCBITaxon:%'
      AND (n.name LIKE '%Methylobacterium%'
           OR n.name LIKE '%Methylorubrum%'
           OR n.name LIKE '%Paracoccus%'
           OR n.name LIKE '%Bradyrhizobium%'
           OR n.name LIKE '%methylotroph%')
    LIMIT {limit}
    """

    df = session.phenotype_kg.query(sql)
    print(f"Retrieved {len(df)} related taxa from kg-microbe")

    return df


def query_taxa_with_functions_from_function_kg(
    session: KGMiningSession,
    function_ids: List[str],
    limit: int = 500
) -> pd.DataFrame:
    """
    Query function KG for taxa with specific functions (e.g., methanol metabolism).

    Args:
        session: Active KG mining session
        function_ids: List of function IDs to search for (EC, GO, etc.)
        limit: Maximum taxa to retrieve

    Returns:
        DataFrame with taxon_id, function associations
    """
    if not session.function_kg:
        raise RuntimeError("Function KG not enabled in session")

    print(f"\nQuerying function KG for taxa with relevant functions...")

    # Build query for taxa with methanol/methylotrophy functions
    functions_list = ", ".join([f"'{fid}'" for fid in function_ids])

    sql = f"""
    WITH function_proteins AS (
        -- Get proteins with target functions
        SELECT DISTINCT
            e.subject as protein_id,
            e.object as function_id
        FROM edges e
        WHERE e.object IN ({functions_list})
          AND e.predicate IN ('biolink:enables', 'biolink:participates_in')
    )
    SELECT DISTINCT
        e2.object as taxon_id,
        COUNT(DISTINCT fp.protein_id) as protein_count,
        GROUP_CONCAT(DISTINCT fp.function_id) as functions
    FROM function_proteins fp
    JOIN edges e2 ON fp.protein_id = e2.subject
    WHERE e2.predicate = 'biolink:derives_from'
      AND e2.object LIKE 'NCBITaxon:%'
    GROUP BY e2.object
    HAVING protein_count >= 2
    ORDER BY protein_count DESC
    LIMIT {limit}
    """

    df = session.function_kg.query(sql)
    print(f"Retrieved {len(df)} taxa with relevant functions from kg-microbe-function")

    return df


def get_taxon_names_from_function_kg(
    session: KGMiningSession,
    taxon_ids: List[str]
) -> Dict[str, str]:
    """
    Get taxon names from function KG nodes.

    Args:
        session: Active KG mining session
        taxon_ids: List of NCBITaxon IDs

    Returns:
        Dictionary mapping taxon_id to taxon_name
    """
    if not session.function_kg:
        raise RuntimeError("Function KG not enabled in session")

    taxa_list = ", ".join([f"'{tid}'" for tid in taxon_ids])

    sql = f"""
    SELECT id, name
    FROM nodes
    WHERE id IN ({taxa_list})
    """

    df = session.function_kg.query(sql)
    return dict(zip(df['id'], df['name']))


def format_taxa_records(
    df: pd.DataFrame,
    source_label: str,
    taxon_name_map: Optional[Dict[str, str]] = None
) -> pd.DataFrame:
    """
    Format KG query results into taxa_and_genomes table schema.

    Schema:
    - Scientific name
    - NCBITaxon id
    - Genome identifier (GenBank, IMG etc)
    - source

    Args:
        df: Raw KG query results with taxon_id column
        source_label: Source label for new records
        taxon_name_map: Optional mapping of taxon_id to taxon_name

    Returns:
        Formatted DataFrame matching taxa table schema
    """
    records = []

    for idx, row in df.iterrows():
        taxon_id = row['taxon_id']

        # Extract numeric ID
        numeric_id = taxon_id.replace("NCBITaxon:", "")

        # Get taxon name (try from row first, then from map)
        taxon_name = ""
        if 'taxon_name' in row and pd.notna(row['taxon_name']):
            taxon_name = row['taxon_name']
        elif taxon_name_map and taxon_id in taxon_name_map:
            taxon_name = taxon_name_map[taxon_id]

        records.append({
            "Scientific name": taxon_name,
            "NCBITaxon id": float(numeric_id),
            "Genome identifier (GenBank, IMG etc)": "",  # Will be filled by NCBI search later
            "source": source_label
        })

    result_df = pd.DataFrame(records)
    print(f"Formatted {len(result_df)} taxa records")

    return result_df


def extend_genomes_from_kg(
    output_file: str = "data/txt/sheet/extended/BER_CMM_Data_for_AI_taxa_and_genomes_extended.tsv",
    append: bool = True
) -> pd.DataFrame:
    """
    Main workflow: Extend taxa table using KG mining.

    Args:
        output_file: Output TSV file path
        append: If True, append to existing file

    Returns:
        DataFrame with new taxa records
    """
    print("=" * 80)
    print("KG-UPDATE: Knowledge Graph Mining for Taxa/Genomes")
    print("=" * 80)

    # Load existing taxa to avoid duplicates
    existing_ids = get_existing_taxa()

    all_new_records = []

    with KGMiningSession(use_function_kg=True, use_phenotype_kg=True) as session:
        # 1. Query phenotypic KG for related methylotrophs
        phenotype_taxa = query_related_taxa_from_phenotype_kg(
            session,
            list(existing_ids),
            limit=500
        )

        if not phenotype_taxa.empty:
            # Filter out existing taxa
            phenotype_taxa = phenotype_taxa[
                ~phenotype_taxa['taxon_id'].isin(existing_ids)
            ]

            if not phenotype_taxa.empty:
                pheno_records = format_taxa_records(
                    phenotype_taxa,
                    source_label="kg_update"
                )
                all_new_records.append(pheno_records)
                print(f"Found {len(pheno_records)} new taxa from phenotypic KG")

        # 2. Query function KG for taxa with methanol metabolism
        methanol_functions = [
            "EC:1.1.2.7",  # methanol dehydrogenase
            "EC:1.2.1.46",  # formaldehyde dehydrogenase
            "GO:0018525",  # methanol metabolic process
        ]

        function_taxa = query_taxa_with_functions_from_function_kg(
            session,
            methanol_functions,
            limit=500
        )

        if not function_taxa.empty:
            # Filter out existing taxa
            function_taxa = function_taxa[
                ~function_taxa['taxon_id'].isin(existing_ids)
            ]

            if not function_taxa.empty:
                # Get taxon names from function KG
                taxon_ids = function_taxa['taxon_id'].unique().tolist()
                taxon_name_map = get_taxon_names_from_function_kg(session, taxon_ids)

                func_records = format_taxa_records(
                    function_taxa,
                    source_label="kg_update",
                    taxon_name_map=taxon_name_map
                )
                all_new_records.append(func_records)
                print(f"Found {len(func_records)} new taxa from function KG")

    # Combine all records
    if not all_new_records:
        print("⚠️  No new taxa found in KG")
        return pd.DataFrame()

    combined_records = pd.concat(all_new_records, ignore_index=True)

    # Deduplicate by NCBITaxon id
    combined_records = combined_records.drop_duplicates(subset=["NCBITaxon id"])

    if combined_records.empty:
        print("⚠️  No new unique taxa to add (all duplicates)")
        return pd.DataFrame()

    # Save results
    save_extended_table(combined_records, output_file, append=append)

    # Summary
    summarize_extraction(
        "taxa_and_genomes",
        len(existing_ids),
        len(combined_records),
        "kg_update"
    )

    return combined_records


def main():
    """Command-line interface."""
    parser = argparse.ArgumentParser(
        description="Extend taxa/genomes table using Knowledge Graph mining"
    )
    parser.add_argument(
        "--output",
        default="data/txt/sheet/extended/BER_CMM_Data_for_AI_taxa_and_genomes_extended.tsv",
        help="Output TSV file path"
    )
    parser.add_argument(
        "--no-append",
        action="store_true",
        help="Overwrite instead of append"
    )

    args = parser.parse_args()

    extend_genomes_from_kg(
        output_file=args.output,
        append=not args.no_append
    )


if __name__ == "__main__":
    main()
