#!/usr/bin/env python3
"""Merge duplicate sheets: genes → genes_and_proteins, organisms → taxa_and_genomes.

This script consolidates:
1. PFAS_Data_for_AI_genes.tsv → PFAS_Data_for_AI_genes_and_proteins.tsv
2. PFAS_Data_for_AI_genes_extended.tsv → PFAS_Data_for_AI_genes_and_proteins_extended.tsv
3. PFAS_Data_for_AI_organisms_extended.tsv → PFAS_Data_for_AI_taxa_and_genomes_extended.tsv
"""

import argparse
from pathlib import Path
import pandas as pd


def normalize_column_names(df, target_columns):
    """Normalize column names to match target schema."""
    # Create mapping of normalized names
    column_mapping = {}
    df_cols_lower = {col.lower().replace(' ', '_').replace('/', '_or_'): col for col in df.columns}

    for target_col in target_columns:
        target_lower = target_col.lower().replace(' ', '_').replace('/', '_or_')
        if target_lower in df_cols_lower:
            column_mapping[df_cols_lower[target_lower]] = target_col

    return df.rename(columns=column_mapping)


def merge_genes(data_dir: Path, backup: bool = True):
    """Merge genes.tsv into genes_and_proteins.tsv."""
    print("="*60)
    print("Merging genes → genes_and_proteins")
    print("="*60)

    # File paths
    genes_base = data_dir / "PFAS_Data_for_AI_genes.tsv"
    genes_ext = data_dir / "PFAS_Data_for_AI_genes_extended.tsv"
    gap_base = data_dir / "PFAS_Data_for_AI_genes_and_proteins.tsv"
    gap_ext = data_dir / "PFAS_Data_for_AI_genes_and_proteins_extended.tsv"

    # === Merge base files ===
    print("\n1. Merging base files...")
    genes_df = pd.read_csv(genes_base, sep='\t', dtype=str, keep_default_na=False)
    gap_df = pd.read_csv(gap_base, sep='\t', dtype=str, keep_default_na=False)

    print(f"   genes.tsv: {len(genes_df)} rows")
    print(f"   genes_and_proteins.tsv: {len(gap_df)} rows")

    # Normalize genes columns to match genes_and_proteins
    target_cols = list(gap_df.columns)
    genes_normalized = normalize_column_names(genes_df, target_cols)

    # Add missing columns with empty values
    for col in gap_df.columns:
        if col not in genes_normalized.columns:
            genes_normalized[col] = ''

    # Reorder columns to match
    genes_normalized = genes_normalized[gap_df.columns]

    # Merge
    if backup and gap_base.exists():
        backup_path = gap_base.with_suffix('.tsv.backup')
        gap_base.rename(backup_path)
        print(f"   Backed up to: {backup_path}")

    merged_base = pd.concat([gap_df, genes_normalized], ignore_index=True)
    merged_base.to_csv(gap_base, sep='\t', index=False)
    print(f"   ✓ Merged base: {len(merged_base)} rows")

    # === Merge extended files ===
    print("\n2. Merging extended files...")
    genes_ext_df = pd.read_csv(genes_ext, sep='\t', dtype=str, keep_default_na=False)
    gap_ext_df = pd.read_csv(gap_ext, sep='\t', dtype=str, keep_default_na=False)

    print(f"   genes_extended.tsv: {len(genes_ext_df)} rows")
    print(f"   genes_and_proteins_extended.tsv: {len(gap_ext_df)} rows")

    # Normalize
    target_cols_ext = list(gap_ext_df.columns)
    genes_ext_normalized = normalize_column_names(genes_ext_df, target_cols_ext)

    # Add missing columns
    for col in gap_ext_df.columns:
        if col not in genes_ext_normalized.columns:
            genes_ext_normalized[col] = ''

    genes_ext_normalized = genes_ext_normalized[gap_ext_df.columns]

    # Merge
    if backup and gap_ext.exists():
        backup_path = gap_ext.with_suffix('.tsv.backup')
        gap_ext.rename(backup_path)
        print(f"   Backed up to: {backup_path}")

    merged_ext = pd.concat([gap_ext_df, genes_ext_normalized], ignore_index=True)
    merged_ext.to_csv(gap_ext, sep='\t', index=False)
    print(f"   ✓ Merged extended: {len(merged_ext)} rows")

    print("\n✓ Genes merge complete!")
    return genes_base, genes_ext


def merge_organisms(data_dir: Path, backup: bool = True):
    """Merge organisms_extended.tsv into taxa_and_genomes_extended.tsv."""
    print("\n" + "="*60)
    print("Merging organisms → taxa_and_genomes")
    print("="*60)

    # File paths
    organisms_ext = data_dir / "PFAS_Data_for_AI_organisms_extended.tsv"
    taxa_base = data_dir / "PFAS_Data_for_AI_taxa_and_genomes.tsv"
    taxa_ext = data_dir / "PFAS_Data_for_AI_taxa_and_genomes_extended.tsv"

    # Only organisms_extended exists (no base organisms file with data)
    print("\n1. Merging organisms_extended → taxa_and_genomes_extended...")
    organisms_df = pd.read_csv(organisms_ext, sep='\t', dtype=str, keep_default_na=False)
    taxa_ext_df = pd.read_csv(taxa_ext, sep='\t', dtype=str, keep_default_na=False)

    print(f"   organisms_extended.tsv: {len(organisms_df)} rows")
    print(f"   taxa_and_genomes_extended.tsv: {len(taxa_ext_df)} rows")

    # Normalize column names
    target_cols = list(taxa_ext_df.columns)
    organisms_normalized = normalize_column_names(organisms_df, target_cols)

    # Add missing columns
    for col in taxa_ext_df.columns:
        if col not in organisms_normalized.columns:
            organisms_normalized[col] = ''

    organisms_normalized = organisms_normalized[taxa_ext_df.columns]

    # Merge
    if backup and taxa_ext.exists():
        backup_path = taxa_ext.with_suffix('.tsv.backup')
        taxa_ext.rename(backup_path)
        print(f"   Backed up to: {backup_path}")

    merged_taxa = pd.concat([taxa_ext_df, organisms_normalized], ignore_index=True)
    merged_taxa.to_csv(taxa_ext, sep='\t', index=False)
    print(f"   ✓ Merged: {len(merged_taxa)} rows")

    print("\n✓ Organisms merge complete!")
    return organisms_ext


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Merge duplicate sheets into consolidated tables"
    )
    parser.add_argument(
        '--data-dir',
        type=Path,
        default=Path('data/txt/sheet'),
        help='Directory containing TSV files'
    )
    parser.add_argument(
        '--no-backup',
        action='store_true',
        help='Do not backup existing files'
    )

    args = parser.parse_args()

    # Merge genes
    genes_files = merge_genes(args.data_dir, backup=not args.no_backup)

    # Merge organisms
    organisms_file = merge_organisms(args.data_dir, backup=not args.no_backup)

    print("\n" + "="*60)
    print("✓ All merges complete!")
    print("="*60)
    print("\nFiles ready for deletion:")
    for f in genes_files:
        print(f"  - {f}")
    print(f"  - {organisms_file}")
    print("\nRun the cleanup script to delete these files.")


if __name__ == "__main__":
    main()
