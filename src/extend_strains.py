#!/usr/bin/env python3
"""Script to extend PFAS strains data with culture collection and procurement information.

This script queries KG-Microbe (DuckDB), NCBI Taxonomy, and BacDive to extract
standardized strain information including culture collection IDs, type strain
designation, and procurement URLs.
"""

import sys
from pathlib import Path

# Import the search module
from strain_search import create_extended_strains_table


def main():
    """Main function to extend the strains data table."""

    # Path to existing data
    taxa_path = "data/txt/sheet/PFAS_Data_for_AI_taxa_and_genomes_extended.tsv"

    # Check if file exists
    if not Path(taxa_path).exists():
        print(f"Error: Taxa and genomes file not found: {taxa_path}")
        print("Please run 'make update-genomes' first to create taxa table.")
        return 1

    print("Starting strains extension for PFAS-degrading microbial culture collections...")
    print("Data sources: KG-Microbe (DuckDB), NCBI Taxonomy, BacDive")
    print()

    try:
        create_extended_strains_table(
            input_file=taxa_path,
            max_rows=100  # Process up to 100 PFAS-relevant organisms
        )
        print()
        print("Successfully extended the strains table!")
        return 0

    except Exception as e:
        print()
        print(f"Error extending strains table: {e}")
        print()
        print("This might be due to:")
        print("- Network connectivity issues")
        print("- NCBI API rate limits")
        print("- KG-Microbe database not found (run 'make create-kg-db' first)")
        print("- File permission issues")
        print()
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
