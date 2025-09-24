#!/usr/bin/env python3
"""Script to extend CMM genes and proteins data with additional lanthanide-relevant genes."""

import sys
from pathlib import Path
from cmm_ai.gene_search import create_extended_genes_table


def main():
    """Main function to extend the genes and proteins data table."""
    
    # Path to existing data
    genes_path = "data/txt/sheet/BER_CMM_Data_for_AI_genes_and_proteins.tsv"
    
    # Check if file exists
    if not Path(genes_path).exists():
        print(f"Error: Genes file not found: {genes_path}")
        print("Please run 'make convert-excel' first to convert Excel files to TSV.")
        return 1
    
    print("Starting genes and proteins extension for lanthanide bioprocessing...")
    print("Searching UniProt, KEGG, and curated databases...")
    print("=" * 60)
    
    try:
        create_extended_genes_table(genes_path)
        print("=" * 60)
        print("Successfully extended the genes and proteins table!")
        return 0
        
    except Exception as e:
        print(f"Error extending genes table: {e}")
        print("This might be due to:")
        print("- Network connectivity issues")
        print("- UniProt API rate limits")
        print("- File permission issues")
        return 1


if __name__ == "__main__":
    sys.exit(main())