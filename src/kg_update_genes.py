#!/usr/bin/env python3
"""
Update genes_and_proteins table using Knowledge Graph mining

This script queries kg-microbe-function to extract:
- UniProt protein IDs for target taxa
- EC numbers (enzymes)
- GO terms (molecular functions, biological processes)
- RHEA reactions
- CHEBI cofactors and substrates

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
    load_existing_gene_ids,
    deduplicate_and_merge,
    save_extended_table,
    summarize_extraction,
    format_source_label
)


def query_proteins_from_function_kg(
    session: KGMiningSession,
    taxon_ids: List[str],
    limit: int = 2000
) -> pd.DataFrame:
    """
    Query function KG for proteins from target taxa with functional annotations.

    Uses two-hop path: NCBITaxon <- derives_from <- UniProtKB -> enables/participates_in -> Function

    Args:
        session: Active KG mining session
        taxon_ids: List of NCBITaxon IDs
        limit: Maximum proteins to retrieve per taxon

    Returns:
        DataFrame with protein_id, taxon_id, function_id, function_name, function_type
    """
    if not session.function_kg:
        raise RuntimeError("Function KG not enabled in session")

    print(f"\nQuerying proteins for {len(taxon_ids)} taxa...")

    taxa_list = ", ".join([f"'{tid}'" for tid in taxon_ids])

    # Two-hop query: Get proteins and their functions
    sql = f"""
    WITH taxon_proteins AS (
        -- Get proteins from target taxa (UniProtKB -> derives_from -> NCBITaxon)
        SELECT DISTINCT
            e.subject as protein_id,
            e.object as taxon_id
        FROM edges e
        WHERE e.object IN ({taxa_list})
          AND e.predicate = 'biolink:derives_from'
          AND e.subject LIKE 'UniProtKB:%'
        LIMIT {limit}
    )
    SELECT
        tp.protein_id,
        tp.taxon_id,
        e2.object as function_id,
        n.name as function_name,
        n.category as function_category,
        e2.predicate,
        CASE
            WHEN e2.object LIKE 'EC:%' THEN 'EC'
            WHEN e2.object LIKE 'GO:%' AND n.category LIKE '%BiologicalProcess%' THEN 'GO_BP'
            WHEN e2.object LIKE 'GO:%' AND n.category LIKE '%MolecularActivity%' THEN 'GO_MF'
            WHEN e2.object LIKE 'RHEA:%' THEN 'RHEA'
            WHEN e2.object LIKE 'CHEBI:%' THEN 'CHEBI'
            ELSE 'Other'
        END as function_type
    FROM taxon_proteins tp
    JOIN edges e2 ON tp.protein_id = e2.subject
    JOIN nodes n ON e2.object = n.id
    WHERE (e2.object LIKE 'EC:%' OR e2.object LIKE 'GO:%'
           OR e2.object LIKE 'RHEA:%' OR e2.object LIKE 'CHEBI:%')
      AND e2.predicate IN ('biolink:enables', 'biolink:participates_in',
                            'biolink:has_input', 'biolink:has_output',
                            'biolink:related_to')
    """

    df = session.function_kg.query(sql)
    print(f"Retrieved {len(df)} protein-function associations")

    return df


def format_gene_records(
    df: pd.DataFrame,
    source_label: str = "kg_update"
) -> pd.DataFrame:
    """
    Format KG query results into genes_and_proteins table schema.

    Schema:
    - gene or protein id
    - organism (from taxa and genomes tab)
    - annotation
    - EC
    - GO
    - CHEBI
    - Source

    Args:
        df: Raw KG query results
        source_label: Source label for new records

    Returns:
        Formatted DataFrame matching genes table schema
    """
    # Group by protein_id to aggregate functions
    records = []

    for protein_id, group in df.groupby('protein_id'):
        # Extract UniProt accession (remove "UniProtKB:" prefix)
        accession = protein_id.replace("UniProtKB:", "")

        # Get taxon (convert NCBITaxon:12345 to organism name - we'll use taxon ID for now)
        taxon_id = group.iloc[0]['taxon_id']
        organism = taxon_id  # Will be mapped to organism name in post-processing

        # Aggregate EC numbers
        ec_numbers = group[group['function_type'] == 'EC']['function_id'].str.replace('EC:', '', regex=False).unique()
        ec_str = ", ".join(ec_numbers) if len(ec_numbers) > 0 else ""

        # Aggregate GO terms
        go_terms = group[group['function_type'].str.startswith('GO')]['function_id'].unique()
        go_str = ", ".join(go_terms) if len(go_terms) > 0 else ""

        # Aggregate CHEBI terms
        chebi_terms = group[group['function_type'] == 'CHEBI']['function_id'].unique()
        chebi_str = ", ".join(chebi_terms) if len(chebi_terms) > 0 else ""

        # Use first function name as annotation (prioritize EC, then GO, then others)
        ec_rows = group[group['function_type'] == 'EC']
        if not ec_rows.empty:
            annotation = ec_rows.iloc[0]['function_name']
        else:
            go_rows = group[group['function_type'].str.startswith('GO')]
            if not go_rows.empty:
                annotation = go_rows.iloc[0]['function_name']
            else:
                annotation = group.iloc[0]['function_name']

        records.append({
            "gene or protein id": accession,
            "organism (from taxa and genomes tab)": organism,
            "annotation": annotation,
            "EC": ec_str,
            "GO": go_str,
            "CHEBI": chebi_str,
            "Source": source_label
        })

    result_df = pd.DataFrame(records)
    print(f"Formatted {len(result_df)} unique protein records")

    return result_df


def map_taxon_ids_to_organisms(
    df: pd.DataFrame,
    taxa_file: str = "data/txt/sheet/BER_CMM_Data_for_AI_taxa_and_genomes.tsv"
) -> pd.DataFrame:
    """
    Map NCBITaxon IDs to organism names from taxa table.

    Args:
        df: DataFrame with "organism (from taxa and genomes tab)" column containing NCBITaxon:* IDs
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
    df["organism (from taxa and genomes tab)"] = df["organism (from taxa and genomes tab)"].map(
        lambda x: taxon_to_organism.get(x, x)
    )

    print(f"Mapped {len(taxon_to_organism)} taxon IDs to organism names")
    return df


def extend_genes_from_kg(
    output_file: str = "data/txt/sheet/extended/BER_CMM_Data_for_AI_genes_and_proteins_extended.tsv",
    source_label: str = "kg_update",
    limit_per_taxon: int = 2000,
    append: bool = True
) -> pd.DataFrame:
    """
    Main workflow: Update genes table using function KG mining.

    Args:
        output_file: Output TSV file path
        source_label: Source label for new records
        limit_per_taxon: Max proteins to retrieve per taxon
        append: If True, append to existing file

    Returns:
        DataFrame with new gene records
    """
    print("=" * 80)
    print("KG-UPDATE: Knowledge Graph Mining for Genes/Proteins")
    print("=" * 80)

    # Load target taxa
    taxon_ids = load_taxon_ids()
    if not taxon_ids:
        print("❌ No taxon IDs found!")
        return pd.DataFrame()

    # Load existing gene IDs to avoid duplicates
    existing_ids = load_existing_gene_ids(output_file)

    # Query function KG
    with KGMiningSession(use_function_kg=True, use_phenotype_kg=False) as session:
        # Get proteins and their functions
        protein_df = query_proteins_from_function_kg(
            session,
            taxon_ids,
            limit=limit_per_taxon
        )

        if protein_df.empty:
            print("⚠️  No proteins found in KG for target taxa")
            return pd.DataFrame()

        # Format into genes table schema
        gene_records = format_gene_records(protein_df, source_label)

        # Map taxon IDs to organism names
        gene_records = map_taxon_ids_to_organisms(gene_records)

        # Deduplicate against existing IDs
        gene_records = deduplicate_and_merge(
            gene_records,
            existing_ids,
            id_column="gene or protein id"
        )

        if gene_records.empty:
            print("⚠️  No new unique genes to add (all duplicates)")
            return pd.DataFrame()

        # Save results
        save_extended_table(gene_records, output_file, append=append)

        # Summary
        summarize_extraction(
            "genes_and_proteins",
            len(existing_ids),
            len(gene_records),
            source_label
        )

        return gene_records


def main():
    """Command-line interface."""
    parser = argparse.ArgumentParser(
        description="Extend genes/proteins table using Knowledge Graph mining"
    )
    parser.add_argument(
        "--output",
        default="data/txt/sheet/extended/BER_CMM_Data_for_AI_genes_and_proteins_extended.tsv",
        help="Output TSV file path"
    )
    parser.add_argument(
        "--source-label",
        default="kg_update",
        help="Source label for new records"
    )
    parser.add_argument(
        "--limit",
        type=int,
        default=2000,
        help="Maximum proteins per taxon"
    )
    parser.add_argument(
        "--no-append",
        action="store_true",
        help="Overwrite instead of append"
    )

    args = parser.parse_args()

    extend_genes_from_kg(
        output_file=args.output,
        source_label=args.source_label,
        limit_per_taxon=args.limit,
        append=not args.no_append
    )


if __name__ == "__main__":
    main()
