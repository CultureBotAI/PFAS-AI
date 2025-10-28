#!/usr/bin/env python3
"""Convert 'Reactions related to PFAS degradation.xlsx' to TSV format.

This script converts the reactions Excel file to TSV, adding a reaction_category
column to track the source sheet for each reaction.
"""

import argparse
from pathlib import Path
from typing import List

import pandas as pd


# Mapping of sheet names to reaction category values
SHEET_CATEGORY_MAP = {
    'Dehalogenase': 'dehalogenase',
    'Known PFAS degraders': 'known_pfas_degraders',
    'Fluoride resistance': 'fluoride_resistance',
    'Hydrocarbon degradation': 'hydrocarbon_degradation',
    'Important genes without enzymat': 'important_genes',
    '(Mono)Oxygenase (co-metabolism)': 'oxygenase_cometabolism'
}


def convert_reactions_excel(
    excel_path: Path,
    output_dir: Path,
    create_unified: bool = True
) -> None:
    """Convert reactions Excel to TSV files.

    Args:
        excel_path: Path to input Excel file
        output_dir: Directory for output TSV files
        create_unified: If True, create unified reactions table
    """
    output_dir.mkdir(parents=True, exist_ok=True)

    print(f"Converting reactions Excel: {excel_path}")
    print(f"Output directory: {output_dir}")
    print("")

    xl = pd.ExcelFile(excel_path)
    all_reactions = []

    for sheet_name in xl.sheet_names:
        print(f"Processing sheet: {sheet_name}")
        df = pd.read_excel(xl, sheet_name)

        # Get reaction category
        category = SHEET_CATEGORY_MAP.get(sheet_name, sheet_name.lower().replace(' ', '_'))

        # Special handling for 'Important genes without enzymat' sheet
        if sheet_name == 'Important genes without enzymat':
            # This sheet has different structure - just convert as-is
            output_path = output_dir / f"PFAS_Reactions_{category}.tsv"
            df.to_csv(output_path, sep='\t', index=False)
            print(f"  Saved: {output_path} ({len(df)} rows)")
            print("")
            continue

        # Add reaction_category column
        df['reaction_category'] = category

        # Add source column for provenance
        df['source'] = 'reactions_excel'

        # Reorder columns: put category and source at the end
        cols = [c for c in df.columns if c not in ['reaction_category', 'source']]
        cols.extend(['reaction_category', 'source'])
        df = df[cols]

        # Save individual sheet
        output_path = output_dir / f"PFAS_Reactions_{category}.tsv"
        df.to_csv(output_path, sep='\t', index=False)
        print(f"  Saved: {output_path} ({len(df)} rows)")

        # Add to unified list
        all_reactions.append(df)
        print("")

    # Create unified reactions table
    if create_unified and all_reactions:
        unified_df = pd.concat(all_reactions, ignore_index=True)
        unified_path = output_dir / "PFAS_Data_for_AI_reactions.tsv"
        unified_df.to_csv(unified_path, sep='\t', index=False)
        print(f"Created unified reactions table: {unified_path}")
        print(f"Total reactions: {len(unified_df)}")
        print("")

        # Print summary by category
        print("Reactions by category:")
        category_counts = unified_df['reaction_category'].value_counts()
        for cat, count in category_counts.items():
            print(f"  {cat}: {count}")


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Convert reactions Excel to TSV format"
    )
    parser.add_argument(
        '--input',
        type=Path,
        default=Path('data/sheet/Reactions related to PFAS degradation.xlsx'),
        help='Input Excel file path'
    )
    parser.add_argument(
        '--output-dir',
        type=Path,
        default=Path('data/txt/sheet'),
        help='Output directory for TSV files'
    )
    parser.add_argument(
        '--no-unified',
        action='store_true',
        help='Do not create unified reactions table'
    )

    args = parser.parse_args()

    if not args.input.exists():
        print(f"Error: Input file not found: {args.input}")
        return 1

    convert_reactions_excel(
        args.input,
        args.output_dir,
        create_unified=not args.no_unified
    )

    return 0


if __name__ == "__main__":
    import sys
    sys.exit(main())
