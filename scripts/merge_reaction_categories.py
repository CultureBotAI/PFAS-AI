#!/usr/bin/env python3
"""Merge category-specific extended reaction files into unified reactions table.

This script combines all category-specific reaction extended files
(with gene linking) into a single comprehensive PFAS_Data_for_AI_reactions_extended.tsv.
"""

import argparse
from pathlib import Path
from typing import List

import pandas as pd


# Category files to merge (in order)
CATEGORY_FILES = [
    'PFAS_Reactions_dehalogenase_extended.tsv',
    'PFAS_Reactions_fluoride_resistance_extended.tsv',
    'PFAS_Reactions_hydrocarbon_degradation_extended.tsv',
    'PFAS_Reactions_known_pfas_degraders_extended.tsv',
    'PFAS_Reactions_oxygenase_cometabolism_extended.tsv',
    'PFAS_Reactions_important_genes_extended.tsv',
]


def merge_reaction_categories(
    data_dir: Path,
    output_file: Path,
    backup: bool = True
) -> None:
    """Merge category-specific reaction files into unified table.

    Args:
        data_dir: Directory containing category TSV files
        output_file: Output path for merged file
        backup: If True, backup existing output file
    """
    print("="*60)
    print("Merging Reaction Category Files")
    print("="*60)
    print("")

    # Backup existing file if requested
    if backup and output_file.exists():
        backup_path = output_file.with_suffix('.tsv.backup')
        output_file.rename(backup_path)
        print(f"Backed up existing file to: {backup_path}")
        print("")

    # Load and merge category files
    all_dfs = []
    total_reactions = 0

    for category_file in CATEGORY_FILES:
        file_path = data_dir / category_file

        if not file_path.exists():
            print(f"⚠️  Warning: {category_file} not found, skipping...")
            continue

        # Load category data
        df = pd.read_csv(file_path, sep='\t')

        # Get category name from filename
        category = category_file.replace('PFAS_Reactions_', '').replace('_extended.tsv', '')

        print(f"📂 {category}:")
        print(f"   File: {category_file}")
        print(f"   Rows: {len(df)}")
        print(f"   Columns: {', '.join(df.columns[:5])}...")

        # Track statistics
        if 'linked_genes' in df.columns:
            linked_count = (df['linked_genes'].notna() & (df['linked_genes'] != '')).sum()
            print(f"   Gene-linked: {linked_count}/{len(df)}")

        all_dfs.append(df)
        total_reactions += len(df)
        print("")

    if not all_dfs:
        print("❌ Error: No category files found to merge!")
        return

    # Merge all dataframes
    print("Merging dataframes...")
    merged_df = pd.concat(all_dfs, ignore_index=True)

    # Get all unique columns
    all_columns = []
    for df in all_dfs:
        all_columns.extend(df.columns)
    unique_columns = list(dict.fromkeys(all_columns))

    # Reorder columns for consistency
    priority_cols = [
        'Reaction identifier', 'reaction_id',
        'Equation', 'equation',
        'Enzyme class', 'enzyme_class',
        'ec_number',
        'rhea_id',
        'kegg_reaction_id',
        'linked_genes',
        'pfas_degrader_context',
        'url',
        'reaction_category',
        'source',
        'Note', 'note'
    ]

    # Build final column order
    final_cols = []
    for col in priority_cols:
        if col in merged_df.columns and col not in final_cols:
            final_cols.append(col)

    # Add any remaining columns not in priority list
    for col in merged_df.columns:
        if col not in final_cols:
            final_cols.append(col)

    merged_df = merged_df[final_cols]

    # Remove duplicate reactions (same Reaction identifier)
    reaction_id_col = 'Reaction identifier' if 'Reaction identifier' in merged_df.columns else 'reaction_id'
    if reaction_id_col in merged_df.columns:
        initial_count = len(merged_df)
        merged_df = merged_df.drop_duplicates(subset=[reaction_id_col], keep='first')
        deduped_count = len(merged_df)
        if initial_count > deduped_count:
            print(f"Removed {initial_count - deduped_count} duplicate reactions")

    # Save merged file
    merged_df.to_csv(output_file, sep='\t', index=False)

    print("")
    print("="*60)
    print("✓ Merge Complete!")
    print("="*60)
    print(f"Output file: {output_file}")
    print(f"Total reactions: {len(merged_df)}")
    print(f"Total columns: {len(merged_df.columns)}")
    print("")

    # Summary statistics
    print("Summary by category:")
    if 'reaction_category' in merged_df.columns:
        category_counts = merged_df['reaction_category'].value_counts()
        for cat, count in category_counts.items():
            print(f"  {cat}: {count}")

    if 'linked_genes' in merged_df.columns:
        linked_total = (merged_df['linked_genes'].notna() & (merged_df['linked_genes'] != '')).sum()
        print(f"\nTotal gene-linked reactions: {linked_total}/{len(merged_df)}")

    print("")


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Merge category-specific reaction files into unified table"
    )
    parser.add_argument(
        '--data-dir',
        type=Path,
        default=Path('data/txt/sheet'),
        help='Directory containing category TSV files'
    )
    parser.add_argument(
        '--output',
        type=Path,
        default=Path('data/txt/sheet/PFAS_Data_for_AI_reactions_extended.tsv'),
        help='Output path for merged file'
    )
    parser.add_argument(
        '--no-backup',
        action='store_true',
        help='Do not backup existing output file'
    )

    args = parser.parse_args()

    merge_reaction_categories(
        args.data_dir,
        args.output,
        backup=not args.no_backup
    )


if __name__ == "__main__":
    main()
