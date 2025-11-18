#!/usr/bin/env python3
"""Fix PubChem ID format in chemicals table (convert floats to integers)."""

import pandas as pd
from pathlib import Path


def fix_pubchem_ids(file_path: str) -> None:
    """Fix PubChem IDs stored as floats (e.g., 69619.0 -> 69619).

    Args:
        file_path: Path to chemicals TSV file
    """
    file_path = Path(file_path)

    if not file_path.exists():
        print(f"Error: File not found: {file_path}")
        return

    print(f"Reading {file_path}...")
    df = pd.read_csv(file_path, sep='\t')

    # Fix pubchem_id column
    if 'pubchem_id' in df.columns:
        original_count = df['pubchem_id'].notna().sum()

        # Convert float strings to integers
        def fix_id(val):
            if pd.isna(val) or val == '':
                return ''
            try:
                # Convert to float first, then to int, then to string
                float_val = float(val)
                int_val = int(float_val)
                return str(int_val)
            except (ValueError, TypeError):
                return str(val)

        df['pubchem_id'] = df['pubchem_id'].apply(fix_id)

        fixed_count = df['pubchem_id'].apply(lambda x: x != '' and x != 'nan').sum()

        print(f"  Fixed {original_count} PubChem IDs")
        print(f"  Valid IDs after fix: {fixed_count}")

    # Save back to file
    df.to_csv(file_path, sep='\t', index=False)
    print(f"✓ Saved fixed file: {file_path}")


if __name__ == "__main__":
    import sys

    # Default path
    file_path = "data/txt/sheet/PFAS_Data_for_AI_chemicals_extended.tsv"

    # Allow override from command line
    if len(sys.argv) > 1:
        file_path = sys.argv[1]

    fix_pubchem_ids(file_path)
