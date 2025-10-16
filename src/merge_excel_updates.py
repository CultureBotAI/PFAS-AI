#!/usr/bin/env python3
"""
Merge Excel updates with existing TSV files while preserving generated data.

This script handles the case where the Excel source file has been updated
(e.g., column headers changed) but doesn't contain programmatically generated
data like publication references, extended rows, etc.

Usage:
    python src/merge_excel_updates.py --dry-run  # Preview changes
    python src/merge_excel_updates.py            # Apply merge
"""

import argparse
import pandas as pd
from pathlib import Path
import shutil
from typing import Dict, List, Tuple, Optional, Set
from datetime import datetime
import json


class ExcelMerger:
    """Handles intelligent merging of Excel updates with existing TSV data."""

    def __init__(self, dry_run: bool = False, verbose: bool = True):
        self.dry_run = dry_run
        self.verbose = verbose
        self.changes_report = []

    def log(self, message: str, level: str = "INFO"):
        """Log a message."""
        prefix = "  " if level == "DETAIL" else ""
        if self.verbose or level != "DETAIL":
            print(f"{prefix}{message}")
        self.changes_report.append(f"[{level}] {message}")

    def detect_id_column(self, df: pd.DataFrame) -> Optional[str]:
        """
        Detect the primary ID column for a dataframe.

        Args:
            df: Input dataframe

        Returns:
            Column name to use as ID, or None if not found
        """
        # Common ID column patterns
        id_patterns = ['_id', 'id', 'name', 'identifier']

        for col in df.columns:
            col_lower = col.lower()
            if any(pattern in col_lower for pattern in id_patterns):
                # Check if values are unique
                if df[col].notna().all() and df[col].is_unique:
                    return col

        # Fallback to first column if it's unique
        first_col = df.columns[0]
        if df[first_col].is_unique:
            return first_col

        return None

    def compare_schemas(self, old_df: pd.DataFrame, new_df: pd.DataFrame,
                       sheet_name: str) -> Dict[str, any]:
        """
        Compare schemas between old and new dataframes.

        Args:
            old_df: Existing dataframe
            new_df: New dataframe from Excel
            sheet_name: Name of the sheet

        Returns:
            Dictionary with schema differences
        """
        old_cols = set(old_df.columns)
        new_cols = set(new_df.columns)

        added_cols = new_cols - old_cols
        removed_cols = old_cols - new_cols
        common_cols = old_cols & new_cols

        # Try to detect renames by comparing column positions
        renames = {}
        if removed_cols and added_cols:
            old_list = list(old_df.columns)
            new_list = list(new_df.columns)

            for i, (old_col, new_col) in enumerate(zip(old_list, new_list)):
                if old_col != new_col and old_col in removed_cols and new_col in added_cols:
                    # Likely a rename at the same position
                    renames[old_col] = new_col

        # Identify generated columns (those with extend/publication data)
        generated_cols = set()
        for col in old_cols:
            if col in old_df.columns:
                # Check if column has extend1/extend2/DOI/PMID patterns
                sample_values = old_df[col].dropna().head(10).astype(str)
                if any('extend' in str(v) or '10.' in str(v) or 'PMID:' in str(v) or 'PMC' in str(v)
                       for v in sample_values):
                    generated_cols.add(col)

        return {
            'added_columns': added_cols,
            'removed_columns': removed_cols,
            'common_columns': common_cols,
            'renamed_columns': renames,
            'generated_columns': generated_cols,
            'old_row_count': len(old_df),
            'new_row_count': len(new_df)
        }

    def merge_dataframes(self, old_df: pd.DataFrame, new_df: pd.DataFrame,
                        schema_diff: Dict, id_col: str) -> pd.DataFrame:
        """
        Merge old and new dataframes intelligently.

        Strategy:
        1. Use new Excel schema (columns) as base
        2. Preserve generated columns from old TSV
        3. Merge rows by ID, preferring new Excel data for non-generated columns
        4. Keep extended rows that don't exist in Excel

        Args:
            old_df: Existing dataframe with generated data
            new_df: New dataframe from Excel
            schema_diff: Schema differences from compare_schemas
            id_col: Column to use as primary key

        Returns:
            Merged dataframe
        """
        # Start with new Excel schema
        result_cols = list(new_df.columns)

        # Apply any detected renames to old dataframe
        old_df_renamed = old_df.copy()
        for old_name, new_name in schema_diff['renamed_columns'].items():
            if old_name in old_df_renamed.columns:
                old_df_renamed = old_df_renamed.rename(columns={old_name: new_name})
                self.log(f"    Renamed column: {old_name} → {new_name}", "DETAIL")

        # Add generated columns to result schema if not already present
        for gen_col in schema_diff['generated_columns']:
            # Apply renames
            actual_col = schema_diff['renamed_columns'].get(gen_col, gen_col)
            if actual_col not in result_cols:
                result_cols.append(actual_col)
                self.log(f"    Preserving generated column: {actual_col}", "DETAIL")

        # Ensure ID column exists in result
        if id_col not in result_cols:
            result_cols.insert(0, id_col)

        # Merge data row by row
        merged_rows = []
        new_ids = set(new_df[id_col].values)
        old_ids = set(old_df_renamed[id_col].values) if id_col in old_df_renamed.columns else set()

        # Process rows from new Excel
        for _, new_row in new_df.iterrows():
            row_id = new_row[id_col]
            merged_row = {}

            # Start with new Excel data
            for col in new_row.index:
                merged_row[col] = new_row[col]

            # Overlay generated columns from old data if this ID existed before
            if row_id in old_ids and id_col in old_df_renamed.columns:
                old_row = old_df_renamed[old_df_renamed[id_col] == row_id].iloc[0]
                for gen_col in schema_diff['generated_columns']:
                    actual_col = schema_diff['renamed_columns'].get(gen_col, gen_col)
                    if actual_col in old_row.index and pd.notna(old_row[actual_col]):
                        merged_row[actual_col] = old_row[actual_col]

            merged_rows.append(merged_row)

        # Add extended rows that don't exist in new Excel
        extended_ids = old_ids - new_ids
        if extended_ids and id_col in old_df_renamed.columns:
            self.log(f"    Preserving {len(extended_ids)} extended rows not in Excel", "DETAIL")
            for ext_id in extended_ids:
                old_row = old_df_renamed[old_df_renamed[id_col] == ext_id].iloc[0]
                merged_row = {}

                # Copy all available data from old row
                for col in result_cols:
                    if col in old_row.index:
                        merged_row[col] = old_row[col]
                    else:
                        merged_row[col] = None

                merged_rows.append(merged_row)

        # Create result dataframe with correct column order
        result_df = pd.DataFrame(merged_rows, columns=result_cols)

        return result_df

    def backup_tsv(self, tsv_path: Path, backup_dir: Path):
        """Backup a TSV file."""
        backup_dir.mkdir(parents=True, exist_ok=True)
        backup_path = backup_dir / tsv_path.name
        shutil.copy2(tsv_path, backup_path)
        self.log(f"  Backed up: {tsv_path.name}", "DETAIL")

    def merge_sheet(self, sheet_name: str, new_excel_df: pd.DataFrame,
                   old_tsv_path: Path, backup_dir: Path) -> bool:
        """
        Merge a single sheet.

        Args:
            sheet_name: Name of the sheet
            new_excel_df: New data from Excel
            old_tsv_path: Path to existing TSV file
            backup_dir: Directory for backups

        Returns:
            True if changes were made, False otherwise
        """
        self.log(f"\nProcessing: {old_tsv_path.name}")

        # Read old TSV
        if not old_tsv_path.exists():
            self.log(f"  ⊙ No existing TSV found, will create new", "DETAIL")
            if not self.dry_run:
                new_excel_df.to_csv(old_tsv_path, sep='\t', index=False)
            return True

        old_df = pd.read_csv(old_tsv_path, sep='\t', dtype=str)

        # Detect ID column
        id_col = self.detect_id_column(new_excel_df)
        if not id_col:
            self.log(f"  ⚠️  No unique ID column found, using positional merge")
            id_col = new_excel_df.columns[0]
        else:
            self.log(f"  Using ID column: {id_col}", "DETAIL")

        # Compare schemas
        schema_diff = self.compare_schemas(old_df, new_excel_df, sheet_name)

        # Report differences
        changes_detected = False

        if schema_diff['added_columns']:
            changes_detected = True
            self.log(f"  ✓ Added columns: {', '.join(schema_diff['added_columns'])}")

        if schema_diff['removed_columns'] - schema_diff['generated_columns']:
            non_generated_removed = schema_diff['removed_columns'] - schema_diff['generated_columns']
            if non_generated_removed:
                changes_detected = True
                self.log(f"  ✓ Removed columns: {', '.join(non_generated_removed)}")

        if schema_diff['renamed_columns']:
            changes_detected = True
            for old, new in schema_diff['renamed_columns'].items():
                self.log(f"  ✓ Renamed: {old} → {new}")

        if schema_diff['generated_columns']:
            self.log(f"  ℹ️  Preserving {len(schema_diff['generated_columns'])} generated column(s)")

        row_diff = schema_diff['new_row_count'] - schema_diff['old_row_count']
        if row_diff != 0:
            changes_detected = True
            symbol = "+" if row_diff > 0 else ""
            self.log(f"  ✓ Row count change: {symbol}{row_diff} ({schema_diff['old_row_count']} → {schema_diff['new_row_count']})")

        if not changes_detected:
            self.log(f"  ⊙ No changes detected")
            return False

        # Merge dataframes
        merged_df = self.merge_dataframes(old_df, new_excel_df, schema_diff, id_col)

        self.log(f"  ✓ Merged result: {len(merged_df)} rows, {len(merged_df.columns)} columns")

        # Apply changes
        if not self.dry_run:
            # Backup original
            self.backup_tsv(old_tsv_path, backup_dir)

            # Write merged result
            merged_df.to_csv(old_tsv_path, sep='\t', index=False)
            self.log(f"  ✓ Updated: {old_tsv_path.name}")

        return True

    def process_excel(self, excel_path: Path, tsv_dir: Path):
        """
        Process Excel file and merge with existing TSVs.

        Args:
            excel_path: Path to Excel file
            tsv_dir: Directory containing TSV files
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_dir = tsv_dir.parent / f"sheet.backup_{timestamp}"

        self.log("="*70)
        if self.dry_run:
            self.log("EXCEL MERGE (DRY RUN - NO CHANGES WILL BE MADE)")
        else:
            self.log("EXCEL MERGE")
        self.log("="*70)
        self.log(f"Excel source: {excel_path}")
        self.log(f"TSV directory: {tsv_dir}")
        if not self.dry_run:
            self.log(f"Backup directory: {backup_dir}")

        # Read Excel sheets
        self.log("\nReading Excel file...")
        sheets = pd.read_excel(excel_path, sheet_name=None, dtype=str)
        self.log(f"Found {len(sheets)} sheets in Excel")

        # Process each sheet
        total_changes = 0
        for sheet_name, new_df in sheets.items():
            # Determine TSV filename
            excel_base = excel_path.stem.replace(' ', '_')
            sheet_safe = sheet_name.replace(' ', '_').replace('/', '_')
            tsv_name = f"{excel_base}_{sheet_safe}.tsv"
            tsv_path = tsv_dir / tsv_name

            # Also check for _extended version
            tsv_extended_path = tsv_dir / tsv_name.replace('.tsv', '_extended.tsv')

            # Merge base TSV
            if self.merge_sheet(sheet_name, new_df, tsv_path, backup_dir):
                total_changes += 1

            # Merge extended TSV if it exists
            if tsv_extended_path.exists():
                old_extended = pd.read_csv(tsv_extended_path, sep='\t', dtype=str)
                if len(old_extended) > len(new_df):
                    # Extended has additional rows, merge them too
                    self.log(f"\n  Processing extended version: {tsv_extended_path.name}")
                    if self.merge_sheet(f"{sheet_name} (extended)", new_df,
                                      tsv_extended_path, backup_dir):
                        total_changes += 1

        # Summary
        self.log("\n" + "="*70)
        self.log("SUMMARY")
        self.log("="*70)
        self.log(f"Sheets processed: {len(sheets)}")
        self.log(f"Files with changes: {total_changes}")

        if self.dry_run:
            self.log("\n⚠️  DRY RUN: No changes were written")
            self.log("Remove --dry-run flag to apply changes")
        else:
            self.log(f"\n✓ Changes applied successfully")
            self.log(f"Backups saved to: {backup_dir}")

        return total_changes > 0


def main():
    parser = argparse.ArgumentParser(
        description='Merge Excel updates with existing TSV files while preserving generated data'
    )
    parser.add_argument(
        '--excel-file',
        type=Path,
        default=Path('data/sheet/BER CMM Data for AI.xlsx'),
        help='Path to Excel file (default: data/sheet/BER CMM Data for AI.xlsx)'
    )
    parser.add_argument(
        '--tsv-dir',
        type=Path,
        default=Path('data/txt/sheet'),
        help='Directory containing TSV files (default: data/txt/sheet)'
    )
    parser.add_argument(
        '--dry-run',
        action='store_true',
        help='Preview changes without applying them'
    )
    parser.add_argument(
        '--quiet',
        action='store_true',
        help='Reduce output verbosity'
    )

    args = parser.parse_args()

    # Validate inputs
    if not args.excel_file.exists():
        print(f"Error: Excel file not found: {args.excel_file}")
        return 1

    if not args.tsv_dir.exists():
        print(f"Error: TSV directory not found: {args.tsv_dir}")
        return 1

    # Run merge
    merger = ExcelMerger(dry_run=args.dry_run, verbose=not args.quiet)
    has_changes = merger.process_excel(args.excel_file, args.tsv_dir)

    return 0 if has_changes or args.dry_run else 1


if __name__ == '__main__':
    exit(main())
