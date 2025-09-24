#!/usr/bin/env python3
"""Script to extend CMM macromolecular structures data with additional lanthanide-relevant structures."""

import sys
from pathlib import Path


def main():
    """Main function to extend the macromolecular structures data table."""
    
    # Path to existing data
    structures_path = "data/txt/sheet/BER_CMM_Data_for_AI_macromolecular_structures.tsv"
    
    # Check if file exists
    if not Path(structures_path).exists():
        print(f"Error: Structures file not found: {structures_path}")
        print("Please run 'make convert-excel' first to convert Excel files to TSV.")
        return 1
    
    print("Starting macromolecular structures extension for lanthanide bioprocessing...")
    print("Searching PDB and curated structural databases...")
    print("=" * 60)
    
    try:
        create_extended_structures_table(structures_path)
        print("=" * 60)
        print("Successfully extended the macromolecular structures table!")
        return 0
        
    except Exception as e:
        print(f"Error extending structures table: {e}")
        print("This might be due to:")
        print("- Network connectivity issues")
        print("- PDB API changes")
        print("- File permission issues")
        return 1


if __name__ == "__main__":
    sys.exit(main())