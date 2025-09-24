#!/usr/bin/env python3
"""Script to extend CMM data with lanthanide-relevant bacteria and archaea from NCBI."""

import sys
from pathlib import Path
from cmm_ai.ncbi_search import create_extended_tables


def main():
    """Main function to extend the lanthanide data tables."""
    
    # Paths to existing data
    genomes_path = "data/txt/sheet/BER_CMM_Data_for_AI_taxa_and_genomes.tsv"
    biosamples_path = "data/txt/sheet/BER_CMM_Data_for_AI_biosamples.tsv"
    
    # Check if files exist
    if not Path(genomes_path).exists():
        print(f"Error: Genomes file not found: {genomes_path}")
        return 1
        
    if not Path(biosamples_path).exists():
        print(f"Error: Biosamples file not found: {biosamples_path}")
        return 1
    
    print("Starting NCBI search for lanthanide-relevant organisms...")
    print("This may take several minutes due to NCBI API rate limits...")
    print("=" * 60)
    
    try:
        create_extended_tables(genomes_path, biosamples_path)
        print("=" * 60)
        print("Successfully extended the data tables!")
        return 0
        
    except Exception as e:
        print(f"Error extending tables: {e}")
        print("This might be due to:")
        print("- NCBI API rate limits")
        print("- Network connectivity issues") 
        print("- Missing email configuration in ncbi_search.py")
        return 1


if __name__ == "__main__":
    sys.exit(main())