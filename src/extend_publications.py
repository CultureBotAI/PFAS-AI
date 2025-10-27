#!/usr/bin/env python3
"""Script to extend PFAS publications data with additional PFAS-relevant publications."""

import sys
from pathlib import Path
import pandas as pd

# Add current directory to path for imports
sys.path.insert(0, '.')

from publication_search import search_pubmed_publications


def main():
    """Main function to extend the publications data table."""

    # Path to existing data
    publications_path = "data/txt/sheet/PFAS_Data_for_AI_publications.tsv"

    # Check if file exists
    if not Path(publications_path).exists():
        print(f"Error: Publications file not found: {publications_path}")
        print("Please run 'make convert-excel' first to convert Excel files to TSV.")
        return 1

    print("Starting publications extension for PFAS biodegradation...")
    print("Searching PubMed, arXiv, bioRxiv and curated literature...")
    print("=" * 60)

    try:
        # Read existing data
        existing_df = pd.read_csv(publications_path, sep='\t')
        print(f"Existing publications: {len(existing_df)} records")

        # Search for new publications
        print("\nSearching PubMed for PFAS biodegradation publications...")
        new_pubs = search_pubmed_publications()
        print(f"Found {len(new_pubs)} new publications")

        if new_pubs:
            # Convert to DataFrame
            new_pubs_df = pd.DataFrame(new_pubs)

            # Add source column
            new_pubs_df['source'] = 'extend1'

            # Combine with existing data
            combined_df = pd.concat([existing_df, new_pubs_df], ignore_index=True)

            # Remove duplicates based on URL
            combined_df = combined_df.drop_duplicates(subset=['url'], keep='first')

            # Save extended table
            output_path = publications_path.replace('.tsv', '_extended.tsv')
            combined_df.to_csv(output_path, sep='\t', index=False)

            print(f"\nTotal publications in extended table: {len(combined_df)}")
            print(f"Output saved to: {output_path}")
        else:
            print("\nNo new publications found. Keeping existing data.")

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
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())