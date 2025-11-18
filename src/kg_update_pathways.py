#!/usr/bin/env python3
"""
Update pathways table using Knowledge Graph mining

This script queries kg-microbe-function to extract:
- KEGG pathways (map* IDs)
- MetaCyc pathways (PWY-* IDs)
- Associated proteins and genes

All new records are labeled with source='kg_update'.
Repeatable: Deduplication prevents duplicate entries on repeated runs.
"""

from pathlib import Path
from typing import Dict, List, Set, Optional
import pandas as pd
import argparse
from src.kg_mining_utils import (
    KGMiningSession,
    load_taxon_ids,
    load_existing_pathway_ids,
    deduplicate_and_merge,
    save_extended_table,
    summarize_extraction,
    format_source_label
)


def query_pathways_from_function_kg(
    session: KGMiningSession,
    taxon_ids: List[str]
) -> pd.DataFrame:
    """
    Query function KG for pathways from target taxa.

    Uses three-hop path: NCBITaxon <- derives_from <- UniProtKB -> participates_in -> Pathway

    Args:
        session: Active KG mining session
        taxon_ids: List of NCBITaxon IDs

    Returns:
        DataFrame with pathway_id, pathway_name, protein_id, taxon_id
    """
    if not session.function_kg:
        raise RuntimeError("Function KG not enabled in session")

    print(f"\nQuerying pathways for {len(taxon_ids)} taxa...")

    taxa_list = ", ".join([f"'{tid}'" for tid in taxon_ids])

    # Three-hop query: Taxa -> Proteins -> Pathways
    sql = f"""
    WITH taxon_proteins AS (
        -- Get proteins from target taxa
        SELECT DISTINCT
            e.subject as protein_id,
            e.object as taxon_id
        FROM edges e
        WHERE e.object IN ({taxa_list})
          AND e.predicate = 'biolink:derives_from'
          AND e.subject LIKE 'UniProtKB:%'
    )
    SELECT DISTINCT
        e2.object as pathway_id,
        n.name as pathway_name,
        tp.protein_id,
        tp.taxon_id,
        COUNT(DISTINCT tp.protein_id) OVER (PARTITION BY e2.object) as protein_count
    FROM taxon_proteins tp
    JOIN edges e2 ON tp.protein_id = e2.subject
    JOIN nodes n ON e2.object = n.id
    WHERE (e2.object LIKE 'KEGG:%' OR e2.object LIKE 'MetaCyc:%'
           OR e2.object LIKE 'path:%' OR e2.object LIKE 'PWY-%')
      AND e2.predicate IN ('biolink:participates_in', 'biolink:actively_involved_in',
                            'biolink:related_to')
    ORDER BY protein_count DESC, pathway_id
    """

    df = session.function_kg.query(sql)
    print(f"Retrieved {len(df)} pathway associations")

    # Count unique pathways
    unique_pathways = df['pathway_id'].nunique()
    print(f"Found {unique_pathways} unique pathways")

    return df


def format_pathway_records(
    df: pd.DataFrame,
    source_label: str = "kg_update"
) -> pd.DataFrame:
    """
    Format KG query results into pathways table schema.

    Schema:
    - pathway name
    - pathway id
    - organism
    - genes (from genes and proteins tab)
    - genes (from genes & proteins tab)  [duplicate column]
    - Source

    Args:
        df: Raw KG query results
        source_label: Source label for new records

    Returns:
        Formatted DataFrame matching pathways table schema
    """
    # Group by pathway_id and taxon_id to aggregate proteins per organism
    records = []

    for (pathway_id, taxon_id), group in df.groupby(['pathway_id', 'taxon_id']):
        pathway_name = group.iloc[0]['pathway_name']

        # Extract protein IDs (remove "UniProtKB:" prefix)
        protein_ids = group['protein_id'].str.replace('UniProtKB:', '', regex=False).unique()
        proteins_str = "; ".join(protein_ids)

        # Format pathway ID (remove prefixes for consistency)
        formatted_id = pathway_id
        if pathway_id.startswith('KEGG:'):
            formatted_id = pathway_id.replace('KEGG:', '')
        elif pathway_id.startswith('path:'):
            formatted_id = pathway_id.replace('path:', '')

        records.append({
            "pathway name": pathway_name,
            "pathway id": formatted_id,
            "organism": taxon_id,  # Will be mapped to organism name
            "genes (from genes and proteins tab)": proteins_str,
            "genes (from genes & proteins tab)": proteins_str,  # Duplicate column
            "Source": source_label
        })

    result_df = pd.DataFrame(records)
    print(f"Formatted {len(result_df)} pathway-organism records")

    return result_df


def map_taxon_ids_to_organisms(
    df: pd.DataFrame,
    taxa_file: str = "data/txt/sheet/BER_CMM_Data_for_AI_taxa_and_genomes.tsv"
) -> pd.DataFrame:
    """
    Map NCBITaxon IDs to organism names from taxa table.

    Args:
        df: DataFrame with "organism" column containing NCBITaxon:* IDs
        taxa_file: Path to taxa TSV file

    Returns:
        DataFrame with taxon IDs replaced by organism names
    """
    # Load taxa mapping
    taxa_df = pd.read_csv(taxa_file, sep='\t')

    # Create mapping dict: NCBITaxon:12345 -> Scientific name
    taxon_to_organism = {}
    for idx, row in taxa_df.iterrows():
        taxon_id = row.get("NCBITaxon id")
        organism = row.get("Scientific name")
        if pd.notna(taxon_id) and pd.notna(organism):
            tid = f"NCBITaxon:{int(float(taxon_id))}"
            taxon_to_organism[tid] = organism

    # Map taxon IDs to organism names
    df = df.copy()
    df["organism"] = df["organism"].map(
        lambda x: taxon_to_organism.get(x, x)
    )

    print(f"Mapped {len(taxon_to_organism)} taxon IDs to organism names")
    return df


def create_pathway_id_column(df: pd.DataFrame) -> pd.DataFrame:
    """
    Create unique pathway IDs combining pathway_id and organism.

    This ensures each pathway-organism combination is unique.

    Args:
        df: DataFrame with pathway_id and organism columns

    Returns:
        DataFrame with pathway_unique_id column added
    """
    df = df.copy()
    df["pathway_unique_id"] = df["pathway id"] + "_" + df["organism"].str.replace(" ", "_")
    return df


def extend_pathways_from_kg(
    output_file: str = "data/txt/sheet/extended/BER_CMM_Data_for_AI_pathways_extended.tsv",
    source_label: str = "kg_update",
    append: bool = True
) -> pd.DataFrame:
    """
    Main workflow: Extend pathways table using function KG mining.

    Args:
        output_file: Output TSV file path
        source_label: Source label for new records
        append: If True, append to existing file

    Returns:
        DataFrame with new pathway records
    """
    print("=" * 80)
    print("KG-UPDATE: Knowledge Graph Mining for Pathways")
    print("=" * 80)

    # Load target taxa
    taxon_ids = load_taxon_ids()
    if not taxon_ids:
        print("❌ No taxon IDs found!")
        return pd.DataFrame()

    # Load existing pathway IDs to avoid duplicates
    existing_ids = load_existing_pathway_ids(output_file)

    # Query function KG
    with KGMiningSession(use_function_kg=True, use_phenotype_kg=False) as session:
        # Get pathways and associated proteins
        pathway_df = query_pathways_from_function_kg(session, taxon_ids)

        if pathway_df.empty:
            print("⚠️  No pathways found in KG for target taxa")
            return pd.DataFrame()

        # Format into pathways table schema
        pathway_records = format_pathway_records(pathway_df, source_label)

        # Map taxon IDs to organism names
        pathway_records = map_taxon_ids_to_organisms(pathway_records)

        # Create unique IDs for deduplication
        pathway_records = create_pathway_id_column(pathway_records)

        # Deduplicate against existing pathway IDs
        # Note: Using pathway_unique_id for dedup, then dropping it
        pathway_records = deduplicate_and_merge(
            pathway_records,
            existing_ids,
            id_column="pathway id"
        )

        # Drop temporary unique ID column
        if "pathway_unique_id" in pathway_records.columns:
            pathway_records = pathway_records.drop(columns=["pathway_unique_id"])

        if pathway_records.empty:
            print("⚠️  No new unique pathways to add (all duplicates)")
            return pd.DataFrame()

        # Save results
        save_extended_table(pathway_records, output_file, append=append)

        # Summary
        summarize_extraction(
            "pathways",
            len(existing_ids),
            len(pathway_records),
            source_label
        )

        return pathway_records


def main():
    """Command-line interface."""
    parser = argparse.ArgumentParser(
        description="Extend pathways table using Knowledge Graph mining"
    )
    parser.add_argument(
        "--output",
        default="data/txt/sheet/extended/BER_CMM_Data_for_AI_pathways_extended.tsv",
        help="Output TSV file path"
    )
    parser.add_argument(
        "--source-label",
        default="kg_update",
        help="Source label for new records"
    )
    parser.add_argument(
        "--no-append",
        action="store_true",
        help="Overwrite instead of append"
    )

    args = parser.parse_args()

    extend_pathways_from_kg(
        output_file=args.output,
        source_label=args.source_label,
        append=not args.no_append
    )


if __name__ == "__main__":
    main()
