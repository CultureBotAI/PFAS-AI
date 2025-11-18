#!/usr/bin/env python3
"""
Annotate existing sheet rows with kg-microbe and kg-microbe-function node IDs

This script adds kg_node_id columns to existing TSV sheets by:
1. Querying KG databases for matching node IDs
2. Adding new columns with semicolon-delimited KG node IDs
3. Preserving all existing data

Tables annotated:
- Taxa/Genomes: NCBITaxon ID → kg-microbe + kg-microbe-function nodes
- Genes/Proteins: UniProt/Gene ID → kg-microbe-function nodes
- Pathways: KEGG/MetaCyc ID → kg-microbe-function nodes
- Chemicals: CHEBI ID → kg-microbe-function nodes
"""

import argparse
import pandas as pd
from pathlib import Path
from typing import Dict, List, Set
from src.kg_mining_utils import KGMiningSession


def annotate_taxa_with_kg_nodes(
    input_file: str,
    output_file: str
) -> None:
    """
    Annotate taxa/genomes table with KG node IDs.

    Adds column: kg_node_ids (NCBITaxon nodes from both KGs)
    """
    print("\n" + "=" * 80)
    print("Annotating Taxa/Genomes with KG Node IDs")
    print("=" * 80)

    # Read existing data
    df = pd.read_csv(input_file, sep='\t')
    print(f"Loaded {len(df)} taxa records")

    # Add kg_node_ids column if it doesn't exist
    if 'kg_node_ids' not in df.columns:
        df['kg_node_ids'] = ""

    # Query both KGs for node IDs
    with KGMiningSession(use_function_kg=True, use_phenotype_kg=True) as session:
        for idx, row in df.iterrows():
            taxon_id = row.get("NCBITaxon id")
            if pd.isna(taxon_id):
                continue

            # Format as NCBITaxon:12345
            ncbi_taxon = f"NCBITaxon:{int(float(taxon_id))}"

            # Check if node exists in either KG
            nodes_found = set()

            # Query function KG
            if session.function_kg:
                sql = f"SELECT id FROM nodes WHERE id = '{ncbi_taxon}' LIMIT 1"
                result = session.function_kg.query(sql)
                if not result.empty:
                    nodes_found.add(f"{ncbi_taxon}|kg-microbe-function")

            # Query phenotype KG
            if session.phenotype_kg:
                sql = f"SELECT id FROM nodes WHERE id = '{ncbi_taxon}' LIMIT 1"
                result = session.phenotype_kg.query(sql)
                if not result.empty:
                    nodes_found.add(f"{ncbi_taxon}|kg-microbe")

            if nodes_found:
                df.at[idx, 'kg_node_ids'] = "; ".join(sorted(nodes_found))

    # Save annotated data
    df.to_csv(output_file, sep='\t', index=False)

    # Report
    annotated = df['kg_node_ids'].notna() & (df['kg_node_ids'] != "")
    print(f"✓ Annotated {annotated.sum()}/{len(df)} taxa with KG node IDs")
    print(f"✓ Saved to {output_file}")


def annotate_genes_with_kg_nodes(
    input_file: str,
    output_file: str
) -> None:
    """
    Annotate genes/proteins table with KG node IDs.

    Adds column: kg_node_ids (KEGG Orthology or UniProt nodes from function KG)
    """
    print("\n" + "=" * 80)
    print("Annotating Genes/Proteins with KG Node IDs")
    print("=" * 80)

    # Read existing data
    df = pd.read_csv(input_file, sep='\t')
    print(f"Loaded {len(df)} gene/protein records")

    # Add kg_node_ids column if it doesn't exist
    if 'kg_node_ids' not in df.columns:
        df['kg_node_ids'] = ""

    # Query function KG for node IDs
    with KGMiningSession(use_function_kg=True, use_phenotype_kg=False) as session:
        for idx, row in df.iterrows():
            gene_id = row.get("gene or protein id")
            if pd.isna(gene_id):
                continue

            gene_id_str = str(gene_id).strip()
            nodes_found = []

            # Handle KEGG Orthology IDs (K12345 format)
            if gene_id_str.startswith("K") and len(gene_id_str) >= 5 and gene_id_str[1:6].isdigit():
                kegg_id = f"KEGG.ORTHOLOGY:{gene_id_str}"
                if session.function_kg:
                    sql = f"SELECT id FROM nodes WHERE id = '{kegg_id}' LIMIT 1"
                    result = session.function_kg.query(sql)
                    if not result.empty:
                        nodes_found.append(f"{kegg_id}|kg-microbe-function")

            # Handle UniProt IDs
            elif gene_id_str.startswith("UniProtKB:"):
                uniprot_id = gene_id_str
                if session.function_kg:
                    sql = f"SELECT id FROM nodes WHERE id = '{uniprot_id}' LIMIT 1"
                    result = session.function_kg.query(sql)
                    if not result.empty:
                        nodes_found.append(f"{uniprot_id}|kg-microbe-function")
            elif "UniProtKB:" in gene_id_str:
                # Extract from pipe-delimited string
                parts = gene_id_str.split("|")
                for part in parts:
                    if part.strip().startswith("UniProtKB:"):
                        uniprot_id = part.strip()
                        if session.function_kg:
                            sql = f"SELECT id FROM nodes WHERE id = '{uniprot_id}' LIMIT 1"
                            result = session.function_kg.query(sql)
                            if not result.empty:
                                nodes_found.append(f"{uniprot_id}|kg-microbe-function")
                        break

            if nodes_found:
                df.at[idx, 'kg_node_ids'] = "; ".join(nodes_found)

    # Save annotated data
    df.to_csv(output_file, sep='\t', index=False)

    # Report
    annotated = df['kg_node_ids'].notna() & (df['kg_node_ids'] != "")
    print(f"✓ Annotated {annotated.sum()}/{len(df)} genes with KG node IDs")
    print(f"✓ Saved to {output_file}")


def annotate_pathways_with_kg_nodes(
    input_file: str,
    output_file: str
) -> None:
    """
    Annotate pathways table with KG node IDs.

    Adds column: kg_node_ids (KEGG/MetaCyc pathway nodes from function KG)
    """
    print("\n" + "=" * 80)
    print("Annotating Pathways with KG Node IDs")
    print("=" * 80)

    # Read existing data
    df = pd.read_csv(input_file, sep='\t')
    print(f"Loaded {len(df)} pathway records")

    # Add kg_node_ids column if it doesn't exist
    if 'kg_node_ids' not in df.columns:
        df['kg_node_ids'] = ""

    # Query function KG for pathway node IDs
    with KGMiningSession(use_function_kg=True, use_phenotype_kg=False) as session:
        for idx, row in df.iterrows():
            pathway_id = row.get("pathway id")
            if pd.isna(pathway_id):
                continue

            pathway_id_str = str(pathway_id).strip()
            nodes_found = []

            # Extract individual pathway IDs from complex strings
            # Handle formats like: "ko00680 (Methane metabolism); PWY-5506; PWY-6966"
            pathway_ids = []
            if ";" in pathway_id_str:
                # Split by semicolon and extract IDs
                for part in pathway_id_str.split(";"):
                    part = part.strip()
                    # Extract ID from parenthetical descriptions
                    if "(" in part:
                        part = part.split("(")[0].strip()
                    if part:
                        pathway_ids.append(part)
            else:
                pathway_ids = [pathway_id_str]

            # Process each pathway ID
            for pid in pathway_ids:
                pid = pid.strip()
                if not pid or pid.startswith("Custom_"):
                    # Skip custom IDs
                    continue

                node_ids_to_check = []

                # Handle KEGG pathway formats
                if pid.startswith("path:map"):
                    # Format: "path:map00680" → "KEGG.PATHWAY:map00680"
                    kegg_id = pid.replace("path:", "")
                    node_ids_to_check.append(f"KEGG.PATHWAY:{kegg_id}")
                elif pid.startswith("ko"):
                    # Format: "ko00680" → "KEGG.PATHWAY:ko00680"
                    node_ids_to_check.append(f"KEGG.PATHWAY:{pid}")
                elif pid.startswith("map"):
                    # Format: "map00680" → "KEGG.PATHWAY:map00680"
                    node_ids_to_check.append(f"KEGG.PATHWAY:{pid}")

                # Handle MetaCyc pathways
                elif pid.startswith("PWY"):
                    # Format: "PWY-5506" → "MetaCyc:PWY-5506"
                    node_ids_to_check.append(f"MetaCyc:{pid}")

                # Handle KEGG gene-pathway format (probably not in KG)
                elif ":" in pid and not pid.startswith("KEGG"):
                    # Skip KEGG gene-pathway format like "mca:MCA0779"
                    continue

                # Check if any node exists in function KG
                if session.function_kg:
                    for node_id in node_ids_to_check:
                        sql = f"SELECT id FROM nodes WHERE id = '{node_id}' LIMIT 1"
                        result = session.function_kg.query(sql)
                        if not result.empty:
                            nodes_found.append(f"{node_id}|kg-microbe-function")

            if nodes_found:
                df.at[idx, 'kg_node_ids'] = "; ".join(sorted(set(nodes_found)))

    # Save annotated data
    df.to_csv(output_file, sep='\t', index=False)

    # Report
    annotated = df['kg_node_ids'].notna() & (df['kg_node_ids'] != "")
    print(f"✓ Annotated {annotated.sum()}/{len(df)} pathways with KG node IDs")
    print(f"✓ Saved to {output_file}")


def annotate_chemicals_with_kg_nodes(
    input_file: str,
    output_file: str
) -> None:
    """
    Annotate chemicals table with KG node IDs.

    Adds column: kg_node_ids (CHEBI nodes from function KG)
    """
    print("\n" + "=" * 80)
    print("Annotating Chemicals with KG Node IDs")
    print("=" * 80)

    # Read existing data
    df = pd.read_csv(input_file, sep='\t')
    print(f"Loaded {len(df)} chemical records")

    # Add kg_node_ids column if it doesn't exist
    if 'kg_node_ids' not in df.columns:
        df['kg_node_ids'] = ""

    # Query function KG for CHEBI node IDs
    with KGMiningSession(use_function_kg=True, use_phenotype_kg=False) as session:
        for idx, row in df.iterrows():
            chebi_id = row.get("chebi_id")
            if pd.isna(chebi_id):
                continue

            chebi_id_str = str(chebi_id).strip()

            # Ensure CHEBI: prefix
            if not chebi_id_str.startswith("CHEBI:"):
                chebi_id_str = f"CHEBI:{chebi_id_str}"

            # Check if node exists in function KG
            if session.function_kg:
                sql = f"SELECT id FROM nodes WHERE id = '{chebi_id_str}' LIMIT 1"
                result = session.function_kg.query(sql)
                if not result.empty:
                    df.at[idx, 'kg_node_ids'] = f"{chebi_id_str}|kg-microbe-function"

    # Save annotated data
    df.to_csv(output_file, sep='\t', index=False)

    # Report
    annotated = df['kg_node_ids'].notna() & (df['kg_node_ids'] != "")
    print(f"✓ Annotated {annotated.sum()}/{len(df)} chemicals with KG node IDs")
    print(f"✓ Saved to {output_file}")


def main():
    """Command-line interface."""
    parser = argparse.ArgumentParser(
        description="Annotate existing sheet rows with kg-microbe node IDs",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Annotate all tables
  python src/annotate_kg_identifiers.py --all

  # Annotate specific table
  python src/annotate_kg_identifiers.py --table taxa

Tables:
  taxa      - Taxa/Genomes (NCBITaxon IDs)
  genes     - Genes/Proteins (UniProt IDs)
  pathways  - Pathways (KEGG/MetaCyc IDs)
  chemicals - Chemicals (CHEBI IDs)
"""
    )

    parser.add_argument(
        "--table",
        choices=["taxa", "genes", "pathways", "chemicals"],
        help="Specific table to annotate"
    )
    parser.add_argument(
        "--all",
        action="store_true",
        help="Annotate all tables"
    )
    parser.add_argument(
        "--data-dir",
        default="data/txt/sheet",
        help="Data directory (default: data/txt/sheet)"
    )

    args = parser.parse_args()

    data_dir = Path(args.data_dir)

    if not args.all and not args.table:
        parser.error("Must specify either --table or --all")

    # Define table mappings
    tables = {
        "taxa": {
            "input": data_dir / "BER_CMM_Data_for_AI_taxa_and_genomes.tsv",
            "output": data_dir / "BER_CMM_Data_for_AI_taxa_and_genomes.tsv",
            "func": annotate_taxa_with_kg_nodes
        },
        "genes": {
            "input": data_dir / "BER_CMM_Data_for_AI_genes_and_proteins.tsv",
            "output": data_dir / "BER_CMM_Data_for_AI_genes_and_proteins.tsv",
            "func": annotate_genes_with_kg_nodes
        },
        "pathways": {
            "input": data_dir / "BER_CMM_Data_for_AI_pathways.tsv",
            "output": data_dir / "BER_CMM_Data_for_AI_pathways.tsv",
            "func": annotate_pathways_with_kg_nodes
        },
        "chemicals": {
            "input": data_dir / "BER_CMM_Data_for_AI_chemicals.tsv",
            "output": data_dir / "BER_CMM_Data_for_AI_chemicals.tsv",
            "func": annotate_chemicals_with_kg_nodes
        }
    }

    # Process tables
    if args.all:
        tables_to_process = tables.keys()
    else:
        tables_to_process = [args.table]

    print("=" * 80)
    print("KG IDENTIFIER ANNOTATION")
    print("=" * 80)
    print(f"Data directory: {data_dir}")
    print(f"Tables to annotate: {', '.join(tables_to_process)}")
    print("=" * 80)

    for table_name in tables_to_process:
        table_info = tables[table_name]
        table_info["func"](
            str(table_info["input"]),
            str(table_info["output"])
        )

    print("\n" + "=" * 80)
    print("✓ KG ANNOTATION COMPLETE")
    print("=" * 80)


if __name__ == "__main__":
    main()
