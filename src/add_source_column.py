"""Add 'source' column to all TSV files and label existing data as 'extend1'.

This script adds a 'source' column to all experimental data TSV files
and sets the value to 'extend1' for all existing records.
"""

import argparse
from pathlib import Path

import pandas as pd


def add_source_column(tsv_path: Path, source_value: str = "extend1", dry_run: bool = False):
    """Add source column to TSV file.

    Args:
        tsv_path: Path to TSV file
        source_value: Default source value for existing records
        dry_run: If True, print changes without modifying files
    """
    if not tsv_path.exists():
        print(f"  Skipping {tsv_path.name} (file not found)")
        return

    # Read TSV with string dtype to preserve integer formats
    # (pandas converts int columns to float when there are NaN values)
    df = pd.read_csv(tsv_path, sep='\t', dtype=str, keep_default_na=False)

    # Replace empty strings with pd.NA for proper handling
    df = df.replace('', pd.NA)

    # Check if source column already exists
    if 'source' in df.columns:
        print(f"  {tsv_path.name}: source column already exists")
        # Fill any NA values with the source_value
        df['source'] = df['source'].fillna(source_value)
    else:
        print(f"  {tsv_path.name}: adding source column")
        # Add source column
        df['source'] = source_value

    if dry_run:
        print(f"    Would update {len(df)} records with source='{source_value}'")
    else:
        # Save updated TSV (replace pd.NA with empty string for TSV format)
        df = df.fillna('')
        df.to_csv(tsv_path, sep='\t', index=False)
        print(f"    Updated {len(df)} records with source='{source_value}'")


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Add source column to experimental data TSV files"
    )
    parser.add_argument(
        '--data-dir',
        type=Path,
        default=Path('data/txt/sheet'),
        help='Directory containing TSV files'
    )
    parser.add_argument(
        '--source-value',
        type=str,
        default='extend1',
        help='Default source value for existing records (default: extend1)'
    )
    parser.add_argument(
        '--dry-run',
        action='store_true',
        help='Print changes without modifying files'
    )

    args = parser.parse_args()

    # List of experimental data files to update
    experimental_files = [
        'PFAS_Data_for_AI_chemicals.tsv',
        'PFAS_Data_for_AI_assays.tsv',
        'PFAS_Data_for_AI_bioprocesses.tsv',
        'PFAS_Data_for_AI_screening_results.tsv',
        'PFAS_Data_for_AI_protocols.tsv',
    ]

    # Also update extended files if they exist
    extended_files = [
        'PFAS_Data_for_AI_chemicals_extended.tsv',
        'PFAS_Data_for_AI_assays_extended.tsv',
    ]

    all_files = experimental_files + extended_files

    print(f"Adding 'source' column to experimental data files...")
    print(f"Data directory: {args.data_dir}")
    print(f"Source value: {args.source_value}")
    if args.dry_run:
        print("DRY RUN - No files will be modified")
    print("")

    for filename in all_files:
        file_path = args.data_dir / filename
        add_source_column(file_path, args.source_value, args.dry_run)

    print("")
    print("Done!")


if __name__ == "__main__":
    main()
