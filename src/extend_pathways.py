#!/usr/bin/env python3
"""Script to extend CMM pathways data with additional lanthanide-relevant pathways."""

import sys
from pathlib import Path


def main():
    """Main function to extend the pathways data table."""
    
    # Path to existing data
    pathways_path = "data/txt/sheet/BER_CMM_Data_for_AI_pathways.tsv"
    
    # Check if file exists
    if not Path(pathways_path).exists():
        print(f"Error: Pathways file not found: {pathways_path}")
        print("Please run 'make convert-excel' first to convert Excel files to TSV.")
        return 1
    
    print("Starting pathway extension for lanthanide bioprocessing...")
    print("Searching KEGG and MetaCyc databases for relevant pathways...")
    print("=" * 60)
    
    try:
        create_extended_pathways_table(pathways_path)
        print("=" * 60)
        print("Successfully extended the pathways table!")
        return 0
        
    except Exception as e:
        print(f"Error extending pathways table: {e}")
        print("This might be due to:")
        print("- Network connectivity issues") 
        print("- KEGG API rate limits")
        print("- File permission issues")
        return 1


if __name__ == "__main__":
    sys.exit(main())