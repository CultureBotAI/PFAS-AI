#!/usr/bin/env python3
"""Script to add annotation download URLs to the existing extended genomes table."""

import pandas as pd
from pathlib import Path

from ncbi_search import get_annotation_download_url


def add_annotation_urls_to_table(input_file: str, output_file: str = None) -> None:
    """Add annotation download URLs to genomes table.
    
    Args:
        input_file: Path to input TSV file
        output_file: Path to output TSV file. If None, updates input file.
    """
    if output_file is None:
        output_file = input_file
    
    print(f"Reading {input_file}...")
    df = pd.read_csv(input_file, sep='\t')
    
    # Add annotation URL column if it doesn't exist
    if "Annotation download URL" not in df.columns:
        df["Annotation download URL"] = ""
        print("Added 'Annotation download URL' column")
    
    # Fill annotation URLs for existing genome identifiers
    updated_count = 0
    for idx, row in df.iterrows():
        genome_id = row.get("Genome identifier (GenBank, IMG etc)", "")
        current_url = row.get("Annotation download URL", "")
        
        # Add URL if genome ID exists but URL is missing
        if genome_id and pd.notna(genome_id) and (pd.isna(current_url) or current_url == ""):
            url = get_annotation_download_url(str(genome_id))
            if url:
                df.at[idx, "Annotation download URL"] = url
                updated_count += 1
                print(f"  Added URL for {row.get('Scientific name', genome_id)}")
    
    # Save updated table
    df.to_csv(output_file, sep='\t', index=False)
    
    print(f"Updated {updated_count} entries with annotation URLs")
    print(f"Saved to: {output_file}")


def main():
    """Main function to update the extended genomes table."""
    
    input_file = "data/txt/sheet/PFAS_Data_for_AI_taxa_and_genomes_extended.tsv"

    if not Path(input_file).exists():
        print(f"Error: File not found: {input_file}")
        print("Please run the extend_pfas_data.py script first.")
        return 1
    
    print("Adding annotation download URLs to extended genomes table...")
    print("=" * 60)
    
    try:
        add_annotation_urls_to_table(input_file)
        print("=" * 60)
        print("Successfully added annotation URLs!")
        return 0
        
    except Exception as e:
        print(f"Error adding annotation URLs: {e}")
        return 1


if __name__ == "__main__":
    import sys
    sys.exit(main())