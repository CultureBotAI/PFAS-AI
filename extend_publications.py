#!/usr/bin/env python3
"""Script to extend CMM publications data with additional lanthanide-relevant publications."""

import sys
from pathlib import Path
from cmm_ai.publication_search import create_extended_publications_table


def main():
    """Main function to extend the publications data table."""
    
    # Path to existing data
    publications_path = "data/txt/sheet/BER_CMM_Data_for_AI_publications.tsv"
    
    # Check if file exists
    if not Path(publications_path).exists():
        print(f"Error: Publications file not found: {publications_path}")
        print("Please run 'make convert-excel' first to convert Excel files to TSV.")
        return 1
    
    print("Starting publications extension for lanthanide bioprocessing...")
    print("Searching PubMed, arXiv, bioRxiv and curated literature...")
    print("=" * 60)
    
    try:
        create_extended_publications_table(publications_path)
        print("=" * 60)
        print("Successfully extended the publications table!")
        return 0
        
    except Exception as e:
        print(f"Error extending publications table: {e}")
        print("This might be due to:")
        print("- Network connectivity issues")
        print("- PubMed API rate limits") 
        print("- NCBI Entrez configuration")
        print("- File permission issues")
        return 1


if __name__ == "__main__":
    sys.exit(main())