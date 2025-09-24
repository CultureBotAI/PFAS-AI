#!/usr/bin/env python3
"""Script to extend CMM datasets data with additional lanthanide-relevant datasets."""

import sys
from pathlib import Path

# Add current directory to path for imports
sys.path.insert(0, '.')
from dataset_search import create_extended_datasets_table


def main():
    """Main function to extend the datasets data table."""
    
    # Path to existing data
    datasets_path = "data/txt/sheet/BER_CMM_Data_for_AI_datasets.tsv"
    
    # Check if file exists
    if not Path(datasets_path).exists():
        print(f"Error: Datasets file not found: {datasets_path}")
        print("Please run 'make convert-excel' first to convert Excel files to TSV.")
        return 1
    
    print("Starting dataset extension for lanthanide bioprocessing...")
    print("Searching multiple databases for relevant datasets...")
    print("=" * 60)
    
    try:
        create_extended_datasets_table(datasets_path)
        print("=" * 60)
        print("Successfully extended the datasets table!")
        return 0
        
    except Exception as e:
        print(f"Error extending datasets table: {e}")
        print("This might be due to:")
        print("- Network connectivity issues")
        print("- Database API changes")
        print("- File permission issues")
        return 1


if __name__ == "__main__":
    sys.exit(main())