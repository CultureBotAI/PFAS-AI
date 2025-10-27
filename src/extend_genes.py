#!/usr/bin/env python3
"""Script to extend PFAS genes and proteins data with additional PFAS-relevant genes."""

import sys
from pathlib import Path
import pandas as pd

# Add current directory to path for imports
sys.path.insert(0, '.')

from gene_search import get_pfas_genes_database


def main():
    """Main function to extend the genes and proteins data table."""

    # Path to existing data
    genes_path = "data/txt/sheet/PFAS_Data_for_AI_genes_and_proteins.tsv"

    # Check if file exists
    if not Path(genes_path).exists():
        print(f"Error: Genes file not found: {genes_path}")
        print("Please run 'make convert-excel' first to convert Excel files to TSV.")
        return 1

    print("Starting genes and proteins extension for PFAS biodegradation...")
    print("Searching UniProt, KEGG, and curated databases...")
    print("=" * 60)

    try:
        # Read existing data
        existing_df = pd.read_csv(genes_path, sep='\t')
        print(f"Existing genes: {len(existing_df)} records")

        # Get PFAS genes from curated database
        print("\nRetrieving curated PFAS biodegradation genes...")
        pfas_genes = get_pfas_genes_database()
        print(f"Found {len(pfas_genes)} curated PFAS genes")

        # Convert to DataFrame
        new_genes_df = pd.DataFrame(pfas_genes)

        # Rename columns to match expected format
        new_genes_df = new_genes_df.rename(columns={
            'gene_id': 'Gene/Protein Identifier',
            'organism': 'Organism',
            'annotation': 'Annotation',
            'ec': 'EC Number',
            'go': 'GO Terms',
            'chebi': 'CHEBI Terms'
        })

        # Add source column
        new_genes_df['source'] = 'extend1'

        # Combine with existing data
        combined_df = pd.concat([existing_df, new_genes_df], ignore_index=True)

        # Remove duplicates based on gene_id
        combined_df = combined_df.drop_duplicates(subset=['Gene/Protein Identifier'], keep='first')

        # Save extended table
        output_path = genes_path.replace('.tsv', '_extended.tsv')
        combined_df.to_csv(output_path, sep='\t', index=False)

        print(f"\nTotal genes in extended table: {len(combined_df)}")
        print(f"Output saved to: {output_path}")
        print("=" * 60)
        print("Successfully extended the genes and proteins table!")
        return 0

    except Exception as e:
        print(f"Error extending genes table: {e}")
        print("This might be due to:")
        print("- Network connectivity issues")
        print("- UniProt API rate limits")
        print("- File permission issues")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())