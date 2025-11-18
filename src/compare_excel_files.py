#!/usr/bin/env python3
"""
Compare two Excel files to check if they're identical or show differences.

This is useful before running merge-excel to verify if the spreadsheet has actually
been updated since the last version.

Usage:
    python src/compare_excel_files.py  # Compare default files
    python src/compare_excel_files.py --file1 path/to/file1.xlsx --file2 path/to/file2.xlsx
    python src/compare_excel_files.py --summary  # Brief summary only
"""

import argparse
import sys
from pathlib import Path
from typing import Dict, List, Tuple, Set
import pandas as pd
import hashlib


class ExcelComparator:
    """Compare two Excel files for differences."""

    def __init__(self, verbose: bool = True):
        self.verbose = verbose
        self.differences_found = False

    def log(self, message: str, level: str = "INFO"):
        """Log a message."""
        if self.verbose:
            if level == "ERROR":
                print(f"✗ {message}", file=sys.stderr)
            elif level == "WARNING":
                print(f"⚠ {message}")
            elif level == "SUCCESS":
                print(f"✓ {message}")
            else:
                print(f"  {message}")

    def compute_file_hash(self, file_path: Path) -> str:
        """Compute SHA256 hash of file."""
        sha256 = hashlib.sha256()
        with open(file_path, 'rb') as f:
            for chunk in iter(lambda: f.read(8192), b''):
                sha256.update(chunk)
        return sha256.hexdigest()

    def compare_binary(self, file1: Path, file2: Path) -> bool:
        """
        Compare files at binary level.

        Returns:
            True if files are identical, False otherwise
        """
        self.log("Computing file hashes...", "INFO")

        hash1 = self.compute_file_hash(file1)
        hash2 = self.compute_file_hash(file2)

        if hash1 == hash2:
            self.log(f"Files are IDENTICAL (hash: {hash1[:16]}...)", "SUCCESS")
            return True
        else:
            self.log("Files are DIFFERENT (binary comparison)", "WARNING")
            self.log(f"  File 1 hash: {hash1[:16]}...", "INFO")
            self.log(f"  File 2 hash: {hash2[:16]}...", "INFO")
            return False

    def compare_sheets(self, file1: Path, file2: Path) -> Dict[str, any]:
        """
        Compare Excel files sheet by sheet.

        Returns:
            Dictionary with comparison results
        """
        self.log("\nLoading Excel files...", "INFO")

        try:
            excel1 = pd.ExcelFile(file1)
            excel2 = pd.ExcelFile(file2)
        except Exception as e:
            self.log(f"Error loading Excel files: {e}", "ERROR")
            return {"error": str(e)}

        sheets1 = set(excel1.sheet_names)
        sheets2 = set(excel2.sheet_names)

        results = {
            'sheets_only_in_file1': sheets1 - sheets2,
            'sheets_only_in_file2': sheets2 - sheets1,
            'common_sheets': sheets1 & sheets2,
            'sheet_differences': {}
        }

        # Report sheet-level differences
        if results['sheets_only_in_file1']:
            self.log(f"\nSheets only in file 1: {results['sheets_only_in_file1']}", "WARNING")
            self.differences_found = True

        if results['sheets_only_in_file2']:
            self.log(f"Sheets only in file 2: {results['sheets_only_in_file2']}", "WARNING")
            self.differences_found = True

        # Compare common sheets
        self.log(f"\nComparing {len(results['common_sheets'])} common sheets...", "INFO")

        for sheet_name in sorted(results['common_sheets']):
            self.log(f"\n  Sheet: '{sheet_name}'", "INFO")

            try:
                df1 = pd.read_excel(file1, sheet_name=sheet_name)
                df2 = pd.read_excel(file2, sheet_name=sheet_name)

                sheet_diff = self.compare_dataframes(df1, df2, sheet_name)
                results['sheet_differences'][sheet_name] = sheet_diff

            except Exception as e:
                self.log(f"    Error comparing sheet: {e}", "ERROR")
                results['sheet_differences'][sheet_name] = {'error': str(e)}
                self.differences_found = True

        return results

    def compare_dataframes(self, df1: pd.DataFrame, df2: pd.DataFrame,
                          sheet_name: str) -> Dict[str, any]:
        """
        Compare two dataframes in detail.

        Returns:
            Dictionary with comparison results
        """
        diff = {
            'identical': False,
            'shape_same': df1.shape == df2.shape,
            'shape1': df1.shape,
            'shape2': df2.shape,
            'columns_same': set(df1.columns) == set(df2.columns),
            'columns1': list(df1.columns),
            'columns2': list(df2.columns),
            'added_columns': set(df2.columns) - set(df1.columns),
            'removed_columns': set(df1.columns) - set(df2.columns),
            'renamed_columns': {},
            'data_differences': {}
        }

        # Report shape differences
        if not diff['shape_same']:
            self.log(f"    Shape differs: {df1.shape} vs {df2.shape}", "WARNING")
            self.differences_found = True
        else:
            self.log(f"    Shape: {df1.shape} ✓", "INFO")

        # Report column differences
        if not diff['columns_same']:
            self.log(f"    Columns differ", "WARNING")
            self.differences_found = True

            if diff['added_columns']:
                self.log(f"      Added: {diff['added_columns']}", "WARNING")

            if diff['removed_columns']:
                self.log(f"      Removed: {diff['removed_columns']}", "WARNING")

            # Detect potential renames (columns in same position but different names)
            if diff['removed_columns'] and diff['added_columns']:
                for i, (col1, col2) in enumerate(zip(df1.columns, df2.columns)):
                    if col1 != col2 and col1 in diff['removed_columns'] and col2 in diff['added_columns']:
                        diff['renamed_columns'][col1] = col2
                        self.log(f"      Possible rename: '{col1}' → '{col2}'", "WARNING")
        else:
            self.log(f"    Columns: {len(df1.columns)} ✓", "INFO")

        # Compare data for common columns
        common_cols = set(df1.columns) & set(df2.columns)

        if common_cols and df1.shape[0] > 0 and df2.shape[0] > 0:
            # Compare values for common columns
            data_same = True
            for col in common_cols:
                try:
                    # Handle NaN values
                    col_equal = df1[col].fillna('').equals(df2[col].fillna(''))

                    if not col_equal:
                        # Count differences
                        if df1.shape[0] == df2.shape[0]:
                            diff_mask = df1[col].fillna('') != df2[col].fillna('')
                            diff_count = diff_mask.sum()
                            diff['data_differences'][col] = diff_count
                            data_same = False
                        else:
                            diff['data_differences'][col] = 'row count differs'
                            data_same = False

                except Exception as e:
                    diff['data_differences'][col] = f'error: {e}'
                    data_same = False

            if diff['data_differences']:
                self.log(f"    Data differences in {len(diff['data_differences'])} columns:", "WARNING")
                self.differences_found = True
                for col, count in sorted(diff['data_differences'].items()):
                    if isinstance(count, int):
                        self.log(f"      '{col}': {count} row(s) differ", "WARNING")
                    else:
                        self.log(f"      '{col}': {count}", "WARNING")
            else:
                self.log(f"    Data: identical ✓", "SUCCESS")

            diff['identical'] = diff['shape_same'] and diff['columns_same'] and data_same

        return diff

    def compare(self, file1: Path, file2: Path, binary_first: bool = True) -> bool:
        """
        Compare two Excel files.

        Args:
            file1: Path to first Excel file
            file2: Path to second Excel file
            binary_first: If True, do binary comparison first (fast)

        Returns:
            True if files are identical, False otherwise
        """
        print("=" * 80)
        print("EXCEL FILE COMPARISON")
        print("=" * 80)
        print(f"File 1: {file1}")
        print(f"File 2: {file2}")
        print()

        # Check files exist
        if not file1.exists():
            self.log(f"File 1 not found: {file1}", "ERROR")
            return False

        if not file2.exists():
            self.log(f"File 2 not found: {file2}", "ERROR")
            return False

        # Binary comparison (fast check)
        if binary_first:
            if self.compare_binary(file1, file2):
                print("\n" + "=" * 80)
                print("RESULT: Files are IDENTICAL (binary match)")
                print("=" * 80)
                return True

        # Detailed sheet-by-sheet comparison
        results = self.compare_sheets(file1, file2)

        # Summary
        print("\n" + "=" * 80)
        if self.differences_found:
            print("RESULT: Files are DIFFERENT")
            print("=" * 80)
            print("\nSummary of differences:")
            if results.get('sheets_only_in_file1'):
                print(f"  - Sheets removed: {len(results['sheets_only_in_file1'])}")
            if results.get('sheets_only_in_file2'):
                print(f"  - Sheets added: {len(results['sheets_only_in_file2'])}")

            if results.get('sheet_differences'):
                sheets_with_diffs = sum(1 for diff in results['sheet_differences'].values()
                                       if not diff.get('identical', False))
                print(f"  - Sheets with differences: {sheets_with_diffs}/{len(results['common_sheets'])}")
        else:
            print("RESULT: Files are IDENTICAL (content match)")
            print("=" * 80)

        print()
        return not self.differences_found


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Compare two Excel files to check if they're identical",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Compare default files (current vs last)
  python src/compare_excel_files.py

  # Compare specific files
  python src/compare_excel_files.py --file1 data/v1.xlsx --file2 data/v2.xlsx

  # Brief summary only
  python src/compare_excel_files.py --summary

Exit codes:
  0 - Files are identical
  1 - Files are different
  2 - Error occurred
        """
    )

    parser.add_argument(
        '--file1',
        type=Path,
        default=Path('data/sheet/BER CMM Data for AI.xlsx'),
        help='First Excel file (default: current version)'
    )

    parser.add_argument(
        '--file2',
        type=Path,
        default=Path('data/sheet/BER CMM Data for AI_last.xlsx'),
        help='Second Excel file (default: last version)'
    )

    parser.add_argument(
        '--summary',
        action='store_true',
        help='Show brief summary only (less verbose)'
    )

    parser.add_argument(
        '--no-binary-check',
        action='store_true',
        help='Skip binary comparison (always do full sheet comparison)'
    )

    args = parser.parse_args()

    try:
        comparator = ExcelComparator(verbose=not args.summary)
        identical = comparator.compare(
            args.file1,
            args.file2,
            binary_first=not args.no_binary_check
        )

        sys.exit(0 if identical else 1)

    except Exception as e:
        print(f"\n✗ Fatal error: {e}", file=sys.stderr)
        sys.exit(2)


if __name__ == "__main__":
    main()
