#!/usr/bin/env python3
"""Script to extend PFAS transcriptomics data with PFAS-relevant RNA-seq datasets.

This script searches NCBI SRA, GEO, and ArrayExpress for transcriptomics experiments
from organisms in the taxa_and_genomes table.
"""

import sys
from pathlib import Path

# Import the search module
from transcriptomics_search import create_extended_transcriptomics_table


def main():
    """Main function to extend the transcriptomics data table."""

    # Path to existing data
    transcriptomics_path = "data/txt/sheet/PFAS_Data_for_AI_transcriptomics.tsv"

    # Check if file exists
    if not Path(transcriptomics_path).exists():
        print(f"Error: Transcriptomics file not found: {transcriptomics_path}")
        print("Please run 'make convert-excel' first to convert Excel files to TSV.")
        return 1

    print("Starting transcriptomics extension for PFAS bioprocessing...")
    print("Searching NCBI SRA, GEO, and ArrayExpress for RNA-seq datasets...")
    print()

    try:
        create_extended_transcriptomics_table(transcriptomics_path)
        print()
        print("Successfully extended the transcriptomics table!")
        return 0

    except Exception as e:
        print()
        print(f"Error extending transcriptomics table: {e}")
        print()
        print("This might be due to:")
        print("- Network connectivity issues")
        print("- NCBI API rate limits")
        print("- ArrayExpress API availability")
        print("- File permission issues")
        print()
        return 1


if __name__ == "__main__":
    sys.exit(main())
