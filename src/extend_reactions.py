#!/usr/bin/env python3
"""Extend reactions data by converting Excel and enriching with database information."""

import argparse
from pathlib import Path

from convert_reactions_excel import convert_reactions_excel
from reaction_search import extend_reactions_table


def main():
    """Main entry point for reactions extension pipeline."""
    parser = argparse.ArgumentParser(
        description="Extend PFAS reactions data pipeline"
    )
    parser.add_argument(
        '--excel-input',
        type=Path,
        default=Path('data/sheet/Reactions related to PFAS degradation.xlsx'),
        help='Input reactions Excel file'
    )
    parser.add_argument(
        '--output-dir',
        type=Path,
        default=Path('data/txt/sheet'),
        help='Output directory for TSV files'
    )
    parser.add_argument(
        '--source-label',
        type=str,
        default='extend1',
        help='Source label for data provenance'
    )
    parser.add_argument(
        '--skip-conversion',
        action='store_true',
        help='Skip Excel to TSV conversion (use existing TSV)'
    )

    args = parser.parse_args()

    print("="*60)
    print("PFAS Reactions Extension Pipeline")
    print("="*60)
    print("")

    # Step 1: Convert Excel to TSV
    if not args.skip_conversion:
        print("Step 1: Converting Excel to TSV...")
        print("-"*60)
        convert_reactions_excel(
            args.excel_input,
            args.output_dir,
            create_unified=True
        )
        print("")
    else:
        print("Step 1: Skipped (using existing TSV)")
        print("")

    # Step 2: Enrich reactions data
    print("Step 2: Enriching reactions data...")
    print("-"*60)
    reactions_tsv = args.output_dir / "PFAS_Data_for_AI_reactions.tsv"
    reactions_extended_tsv = args.output_dir / "PFAS_Data_for_AI_reactions_extended.tsv"

    extend_reactions_table(
        reactions_tsv,
        reactions_extended_tsv,
        source_label=args.source_label
    )
    print("")

    print("="*60)
    print("Reactions extension complete!")
    print("="*60)
    print(f"Output files:")
    print(f"  - {reactions_tsv}")
    print(f"  - {reactions_extended_tsv}")

    return 0


if __name__ == "__main__":
    import sys
    sys.exit(main())
