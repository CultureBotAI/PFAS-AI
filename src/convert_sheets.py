#!/usr/bin/env python3
"""Convert Excel files with multiple sheets to separate TSV files."""

import pandas as pd
from pathlib import Path
import re


def sanitize_filename(name: str) -> str:
    """Sanitize filename to replace spaces and special characters with underscores.
    
    Args:
        name: Original filename or sheet name
        
    Returns:
        Sanitized filename safe for filesystem
    """
    # Replace spaces and consecutive whitespace with single underscores
    sanitized = re.sub(r'\s+', '_', name)
    # Replace other problematic characters with underscores
    sanitized = re.sub(r'[^\w\-_.]', '_', sanitized)
    # Remove multiple consecutive underscores
    sanitized = re.sub(r'_+', '_', sanitized)
    # Remove leading/trailing underscores
    sanitized = sanitized.strip('_')
    return sanitized


def convert_excel_sheets(input_path: str, output_dir: str) -> None:
    """Convert each sheet in Excel file to separate TSV.
    
    Args:
        input_path: Path to Excel file
        output_dir: Directory to save TSV files
    """
    input_path = Path(input_path)
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Read all sheets
    sheets = pd.read_excel(input_path, sheet_name=None)
    
    print(f"Converting {input_path.name} with {len(sheets)} sheets:")
    
    for sheet_name, df in sheets.items():
        # Create safe filename for both filename base and sheet name
        safe_base = sanitize_filename(input_path.stem)
        safe_sheet = sanitize_filename(sheet_name)
        output_file = output_dir / f"{safe_base}_{safe_sheet}.tsv"
        
        # Convert to TSV
        df.to_csv(output_file, sep='\t', index=False)
        
        print(f"  - {sheet_name} → {output_file.name} ({len(df)} rows)")


def main():
    """Convert Excel files to separate TSV per sheet."""

    # Convert PFAS Excel file
    files_to_convert = [
        ("data/sheet/PFAS Data for AI.xlsx", "data/txt/sheet")
    ]
    
    for excel_file, output_dir in files_to_convert:
        if Path(excel_file).exists():
            convert_excel_sheets(excel_file, output_dir)
        else:
            print(f"File not found: {excel_file}")


if __name__ == "__main__":
    main()