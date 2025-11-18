#!/usr/bin/env python3
"""
Compare Excel file with existing TSV files to identify differences.

This helps determine if Excel sheets have been updated relative to the TSV files,
and whether you need to run merge-excel to sync the changes.

Usage:
    python src/compare_excel_tsv.py  # Compare with default files
    python src/compare_excel_tsv.py --excel-file path/to/file.xlsx --tsv-dir path/to/tsv/
    python src/compare_excel_tsv.py --summary  # Brief summary only
"""

import argparse
import sys
from pathlib import Path
from typing import Dict, List, Tuple, Set, Optional
import pandas as pd


class ExcelTSVComparator:
    """Compare Excel file with TSV files."""

    def __init__(self, verbose: bool = True):
        self.verbose = verbose
        self.differences_found = False
        self.sheets_compared = 0
        self.sheets_identical = 0
        self.sheets_different = 0
        self.sheets_missing_tsv = 0

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

    def find_tsv_file(self, sheet_name: str, tsv_dir: Path) -> Optional[Tuple[Path, str]]:
        """
        Find corresponding TSV file for an Excel sheet.

        Prefers *_extended.tsv, falls back to base .tsv file.

        Args:
            sheet_name: Name of the Excel sheet
            tsv_dir: Directory containing TSV files

        Returns:
            Tuple of (path, type) where type is "extended" or "base", or None if not found
        """
        # Sanitize sheet name (spaces to underscores)
        sanitized_name = sheet_name.replace(' ', '_')

        # Try extended file first
        extended_path = tsv_dir / f"BER_CMM_Data_for_AI_{sanitized_name}_extended.tsv"
        if extended_path.exists():
            return (extended_path, "extended")

        # Fallback to base file
        base_path = tsv_dir / f"BER_CMM_Data_for_AI_{sanitized_name}.tsv"
        if base_path.exists():
            return (base_path, "base")

        return None

    def compare_dataframes(self, df_excel: pd.DataFrame, df_tsv: pd.DataFrame,
                          sheet_name: str) -> Dict[str, any]:
        """
        Compare Excel sheet DataFrame with TSV DataFrame.

        Returns:
            Dictionary with comparison results
        """
        diff = {
            'identical': False,
            'shape_same': df_excel.shape == df_tsv.shape,
            'excel_shape': df_excel.shape,
            'tsv_shape': df_tsv.shape,
            'columns_same': set(df_excel.columns) == set(df_tsv.columns),
            'excel_columns': list(df_excel.columns),
            'tsv_columns': list(df_tsv.columns),
            'added_columns': set(df_excel.columns) - set(df_tsv.columns),
            'removed_columns': set(df_tsv.columns) - set(df_excel.columns),
            'data_differences': {}
        }

        # Report shape differences
        if not diff['shape_same']:
            self.log(f"    Shape differs: Excel {df_excel.shape} vs TSV {df_tsv.shape}", "WARNING")
            self.differences_found = True
        else:
            self.log(f"    Shape: {df_excel.shape} ✓", "SUCCESS")

        # Report column differences
        if not diff['columns_same']:
            self.log(f"    Columns differ", "WARNING")
            self.differences_found = True

            if diff['added_columns']:
                self.log(f"      Excel has new: {diff['added_columns']}", "WARNING")

            if diff['removed_columns']:
                self.log(f"      TSV has extra: {diff['removed_columns']}", "WARNING")
        else:
            self.log(f"    Columns: {len(df_excel.columns)} ✓", "SUCCESS")

        # Compare data for common columns
        common_cols = set(df_excel.columns) & set(df_tsv.columns)

        if common_cols and df_excel.shape[0] > 0 and df_tsv.shape[0] > 0:
            # Compare values for common columns
            data_same = True
            for col in common_cols:
                try:
                    # Handle NaN values
                    col_equal = df_excel[col].fillna('').equals(df_tsv[col].fillna(''))

                    if not col_equal:
                        # Count differences
                        if df_excel.shape[0] == df_tsv.shape[0]:
                            diff_mask = df_excel[col].fillna('') != df_tsv[col].fillna('')
                            diff_count = diff_mask.sum()
                            if diff_count > 0:
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
        else:
            # Can't compare data if no common columns or empty DataFrames
            diff['identical'] = False

        return diff

    def compare(self, excel_file: Path, tsv_dir: Path) -> Dict[str, any]:
        """
        Compare Excel file with TSV files.

        Args:
            excel_file: Path to Excel file
            tsv_dir: Directory containing TSV files

        Returns:
            Dictionary with comparison results
        """
        print("=" * 80)
        print("EXCEL vs TSV COMPARISON")
        print("=" * 80)
        print(f"Excel file: {excel_file}")
        print(f"TSV directory: {tsv_dir}")
        print()

        # Check files exist
        if not excel_file.exists():
            self.log(f"Excel file not found: {excel_file}", "ERROR")
            return {"error": "Excel file not found"}

        if not tsv_dir.exists():
            self.log(f"TSV directory not found: {tsv_dir}", "ERROR")
            return {"error": "TSV directory not found"}

        # Load Excel file
        self.log("Loading Excel file...", "INFO")
        try:
            excel = pd.ExcelFile(excel_file)
            sheet_names = excel.sheet_names
            self.log(f"Found {len(sheet_names)} sheets in Excel file", "INFO")
        except Exception as e:
            self.log(f"Error loading Excel file: {e}", "ERROR")
            return {"error": str(e)}

        results = {
            'sheets_with_tsv': [],
            'sheets_without_tsv': [],
            'identical_sheets': [],
            'different_sheets': [],
            'sheet_details': {}
        }

        # Compare each sheet
        print()
        self.log("Comparing sheets...", "INFO")
        print()

        for sheet_name in sorted(sheet_names):
            self.sheets_compared += 1

            # Find corresponding TSV file
            tsv_result = self.find_tsv_file(sheet_name, tsv_dir)

            if tsv_result is None:
                self.log(f"Sheet '{sheet_name}': NO TSV FILE FOUND", "ERROR")
                results['sheets_without_tsv'].append(sheet_name)
                self.sheets_missing_tsv += 1
                self.differences_found = True
                continue

            tsv_path, tsv_type = tsv_result
            self.log(f"Sheet '{sheet_name}':", "INFO")
            self.log(f"  → {tsv_path.name} ({tsv_type})", "INFO")
            results['sheets_with_tsv'].append(sheet_name)

            # Load and compare
            try:
                df_excel = pd.read_excel(excel_file, sheet_name=sheet_name)
                df_tsv = pd.read_csv(tsv_path, sep='\t')

                diff = self.compare_dataframes(df_excel, df_tsv, sheet_name)

                results['sheet_details'][sheet_name] = {
                    'tsv_file': tsv_path.name,
                    'tsv_type': tsv_type,
                    'diff': diff
                }

                if diff['identical']:
                    results['identical_sheets'].append(sheet_name)
                    self.sheets_identical += 1
                else:
                    results['different_sheets'].append(sheet_name)
                    self.sheets_different += 1

            except Exception as e:
                self.log(f"  Error comparing: {e}", "ERROR")
                results['sheet_details'][sheet_name] = {
                    'tsv_file': tsv_path.name if tsv_path else None,
                    'tsv_type': tsv_type if tsv_result else None,
                    'error': str(e)
                }
                self.differences_found = True

            print()

        # Summary
        self.print_summary(results)

        return results

    def print_summary(self, results: Dict):
        """Print comparison summary."""
        print("=" * 80)
        print("SUMMARY")
        print("=" * 80)
        print()

        print(f"Total sheets compared: {self.sheets_compared}")
        print(f"  ✓ Identical: {self.sheets_identical}")
        print(f"  ✗ Different: {self.sheets_different}")
        print(f"  ✗ Missing TSV: {self.sheets_missing_tsv}")
        print()

        if results['identical_sheets']:
            print(f"IDENTICAL SHEETS ({len(results['identical_sheets'])}):")
            for sheet in sorted(results['identical_sheets']):
                detail = results['sheet_details'][sheet]
                diff = detail['diff']
                print(f"  ✓ {sheet} ({diff['excel_shape'][0]} rows, {diff['excel_shape'][1]} cols)")
            print()

        if results['different_sheets']:
            print(f"DIFFERENT SHEETS ({len(results['different_sheets'])}):")
            for sheet in sorted(results['different_sheets']):
                detail = results['sheet_details'][sheet]
                diff = detail['diff']
                print(f"  ✗ {sheet}")
                print(f"      Excel: {diff['excel_shape'][0]} rows, {diff['excel_shape'][1]} cols")
                print(f"      TSV:   {diff['tsv_shape'][0]} rows, {diff['tsv_shape'][1]} cols")
                if diff.get('added_columns'):
                    print(f"      New columns in Excel: {', '.join(diff['added_columns'])}")
                if diff.get('removed_columns'):
                    print(f"      Extra columns in TSV: {', '.join(diff['removed_columns'])}")
            print()

        if results['sheets_without_tsv']:
            print(f"SHEETS WITHOUT TSV FILES ({len(results['sheets_without_tsv'])}):")
            for sheet in sorted(results['sheets_without_tsv']):
                print(f"  ✗ {sheet}")
            print()

        # Recommendations
        print("=" * 80)
        if self.differences_found:
            print("RECOMMENDATION:")
            print("  Differences detected. To merge Excel changes into TSV files:")
            print()
            print("  1. Preview merge:")
            print("     make merge-excel-dry-run")
            print()
            print("  2. Apply merge (backs up existing TSV files):")
            print("     make merge-excel")
            print()
            print("  3. Validate after merge:")
            print("     make validate-consistency")
            print("     make validate-schema")
        else:
            print("RESULT: All sheets are identical - no merge needed!")
        print("=" * 80)
        print()


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Compare Excel file with TSV files to identify differences",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Compare with default files
  python src/compare_excel_tsv.py

  # Compare specific files
  python src/compare_excel_tsv.py --excel-file data/sheet/file.xlsx --tsv-dir data/txt/sheet

  # Brief summary only
  python src/compare_excel_tsv.py --summary

Exit codes:
  0 - All sheets are identical
  1 - Differences found
  2 - Error occurred
        """
    )

    parser.add_argument(
        '--excel-file',
        type=Path,
        default=Path('data/sheet/BER CMM Data for AI.xlsx'),
        help='Excel file to compare (default: data/sheet/BER CMM Data for AI.xlsx)'
    )

    parser.add_argument(
        '--tsv-dir',
        type=Path,
        default=Path('data/txt/sheet'),
        help='Directory containing TSV files (default: data/txt/sheet)'
    )

    parser.add_argument(
        '--summary',
        action='store_true',
        help='Show brief summary only (less verbose)'
    )

    args = parser.parse_args()

    try:
        comparator = ExcelTSVComparator(verbose=not args.summary)
        results = comparator.compare(args.excel_file, args.tsv_dir)

        if 'error' in results:
            sys.exit(2)

        sys.exit(0 if not comparator.differences_found else 1)

    except Exception as e:
        print(f"\n✗ Fatal error: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        sys.exit(2)


if __name__ == "__main__":
    main()
