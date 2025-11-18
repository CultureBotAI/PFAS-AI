#!/usr/bin/env python3
"""
Mine extended proteins table to extract pathways, chemicals, publications, etc.

This script:
1. Reads the extended genes/proteins table
2. Fetches detailed UniProt data for each protein
3. Extracts and aggregates:
   - Pathways (KEGG, Reactome, UniPathway, BioCyc)
   - Chemicals (CHEBI cofactors and substrates)
   - Publications (PubMed IDs, DOIs)
4. Extends corresponding tables with discovered data

Usage:
    python src/mine_extended_proteins.py
    python src/mine_extended_proteins.py --tables pathways chemicals
    python src/mine_extended_proteins.py --max-proteins 50
"""

import argparse
import sys
from pathlib import Path
from typing import List, Dict, Set, Tuple, Optional
from collections import defaultdict
import pandas as pd
import time

try:
    from src.apis.uniprot_client import UniProtClient
except ImportError:
    from apis.uniprot_client import UniProtClient


class ProteinDataMiner:
    """Mine extended proteins table for additional data."""

    def __init__(self, data_dir: str = "data/txt/sheet"):
        self.data_dir = Path(data_dir)
        self.client = UniProtClient()

        # Track discovered data
        self.pathways = defaultdict(lambda: {
            'pathway_id': '',
            'pathway_name': '',
            'database': '',
            'organisms': set(),
            'proteins': set()
        })

        self.chemicals = defaultdict(lambda: {
            'chemical_id': '',
            'chemical_name': '',
            'role': '',
            'organisms': set(),
            'proteins': set()
        })

        self.publications = {}  # doi/pmid -> pub_data

    def load_proteins(self, max_proteins: Optional[int] = None) -> List[Dict]:
        """Load proteins from extended table."""
        proteins_file = self.data_dir / "BER_CMM_Data_for_AI_genes_and_proteins_extended.tsv"

        if not proteins_file.exists():
            print(f"⚠ Proteins file not found: {proteins_file}")
            return []

        df = pd.read_csv(proteins_file, sep='\t')
        print(f"Loaded {len(df)} proteins from extended table")

        # Filter to only proteins from UniProt/lanM (have accession IDs)
        # UniProt accessions are typically 6-10 characters, alphanumeric
        # Exclude KEGG K numbers (K##### format) and custom identifiers
        def is_uniprot_accession(id_str):
            if pd.isna(id_str):
                return False
            id_str = str(id_str).strip()
            # Exclude KEGG K numbers
            if id_str.startswith('K') and len(id_str) == 6 and id_str[1:].isdigit():
                return False
            # Exclude custom identifiers
            if id_str.startswith('custom_'):
                return False
            # Accept UniProt-style accessions (6-10 alphanumeric characters)
            if 6 <= len(id_str) <= 10 and id_str.replace('_', '').isalnum():
                return True
            return False

        df_filtered = df[df['gene or protein id'].apply(is_uniprot_accession)]
        print(f"  {len(df_filtered)} have UniProt-style accession IDs")

        if max_proteins:
            df_filtered = df_filtered.head(max_proteins)
            print(f"  Limited to first {max_proteins} proteins")

        proteins = []
        for _, row in df_filtered.iterrows():
            proteins.append({
                'accession': row['gene or protein id'],
                'organism': row.get('organism (from taxa and genomes tab)', ''),
                'annotation': row.get('annotation', '')
            })

        return proteins

    def mine_protein_data(self, proteins: List[Dict]) -> None:
        """Fetch detailed UniProt data and extract information."""
        print()
        print("=" * 80)
        print("MINING PROTEIN DATA FROM UNIPROT")
        print("=" * 80)
        print()
        print(f"Fetching details for {len(proteins)} proteins...")
        print("(This may take several minutes due to rate limiting)")
        print()

        for i, protein in enumerate(proteins, 1):
            accession = protein['accession']
            organism = protein['organism']

            print(f"[{i}/{len(proteins)}] {accession}...", end=" ", flush=True)

            try:
                entry = self.client.get_protein_entry(accession, format='json')

                if not entry:
                    print("❌ No data")
                    continue

                # Extract pathways
                pathway_data = self.client.extract_pathways(entry)
                for db, pathway_ids in pathway_data.items():
                    for pathway_id in pathway_ids:
                        key = f"{db}:{pathway_id}"
                        self.pathways[key]['pathway_id'] = pathway_id
                        self.pathways[key]['pathway_name'] = f"{db} pathway {pathway_id}"
                        self.pathways[key]['database'] = db
                        self.pathways[key]['organisms'].add(organism)
                        self.pathways[key]['proteins'].add(accession)

                # Extract chemicals
                chebi_data = self.client.extract_chebi_terms(entry)
                for chebi_id, chebi_name, role in chebi_data:
                    self.chemicals[chebi_id]['chemical_id'] = chebi_id
                    self.chemicals[chebi_id]['chemical_name'] = chebi_name
                    self.chemicals[chebi_id]['role'] = role
                    self.chemicals[chebi_id]['organisms'].add(organism)
                    self.chemicals[chebi_id]['proteins'].add(accession)

                # Extract publications
                pub_data = self.client.extract_publications(entry)
                for pmid, doi, title in pub_data:
                    key = doi if doi else f"PMID:{pmid}"
                    if key and key not in self.publications:
                        url = f"https://doi.org/{doi}" if doi else f"https://pubmed.ncbi.nlm.nih.gov/{pmid}/"
                        self.publications[key] = {
                            'url': url,
                            'title': title if title else key,
                            'doi': doi,
                            'pmid': pmid,
                            'proteins': set([accession])
                        }
                    elif key:
                        self.publications[key]['proteins'].add(accession)

                print(f"✓ P:{len(pathway_data.get('KEGG', []))} C:{len(chebi_data)} Pub:{len(pub_data)}")

                time.sleep(0.5)  # Rate limiting

            except Exception as e:
                print(f"❌ Error: {e}")
                continue

        print()
        print(f"✓ Discovered:")
        print(f"    Pathways: {len(self.pathways)}")
        print(f"    Chemicals: {len(self.chemicals)}")
        print(f"    Publications: {len(self.publications)}")
        print()

    def extend_pathways_table(self) -> None:
        """Extend pathways table with discovered pathway data."""
        print("=" * 80)
        print("EXTENDING PATHWAYS TABLE")
        print("=" * 80)
        print()

        pathways_file = self.data_dir / "BER_CMM_Data_for_AI_pathways.tsv"
        output_file = self.data_dir / "BER_CMM_Data_for_AI_pathways_extended.tsv"

        # Load existing pathways
        if pathways_file.exists():
            pathways_df = pd.read_csv(pathways_file, sep='\t')
            print(f"Loaded existing pathways table: {len(pathways_df)} rows")
        else:
            pathways_df = pd.DataFrame(columns=[
                'pathway id', 'pathway name', 'organism',
                'genes (from genes and proteins tab)',
                'genes (from genes & proteins tab)',
                'Source'
            ])

        # Add Source column if missing
        if 'Source' not in pathways_df.columns:
            pathways_df['Source'] = ''

        # Get existing pathway IDs
        existing_ids = set(pathways_df['pathway id'].dropna())

        # Add new pathways
        new_rows = []
        for key, pathway_data in self.pathways.items():
            pathway_id = pathway_data['pathway_id']

            if pathway_id not in existing_ids:
                organisms = '; '.join(sorted(pathway_data['organisms']))[:200]  # Limit length
                proteins = '; '.join(sorted(list(pathway_data['proteins']))[:10])  # First 10 proteins

                new_rows.append({
                    'pathway id': pathway_id,
                    'pathway name': pathway_data['pathway_name'],
                    'organism': organisms if organisms else 'Multiple organisms',
                    'genes (from genes and proteins tab)': proteins,
                    'genes (from genes & proteins tab)': f"{pathway_data['database']} pathway with {len(pathway_data['proteins'])} proteins",
                    'Source': 'UniProt API mining from extended proteins'
                })

        if new_rows:
            new_df = pd.DataFrame(new_rows)
            pathways_df = pd.concat([pathways_df, new_df], ignore_index=True)
            print(f"✓ Added {len(new_rows)} new pathways")
        else:
            print("No new pathways to add")

        # Save extended table
        pathways_df.to_csv(output_file, sep='\t', index=False)
        print(f"✓ Saved: {output_file}")
        print(f"  Total rows: {len(pathways_df)}")
        print()

    def extend_chemicals_table(self) -> None:
        """Extend chemicals table with discovered CHEBI compounds."""
        print("=" * 80)
        print("EXTENDING CHEMICALS TABLE")
        print("=" * 80)
        print()

        chemicals_file = self.data_dir / "BER_CMM_Data_for_AI_chemicals.tsv"
        output_file = self.data_dir / "BER_CMM_Data_for_AI_chemicals_extended.tsv"

        # Load existing chemicals
        if chemicals_file.exists():
            chemicals_df = pd.read_csv(chemicals_file, sep='\t')
            print(f"Loaded existing chemicals table: {len(chemicals_df)} rows")
        else:
            chemicals_df = pd.DataFrame(columns=[
                'chemical_id', 'chemical_name', 'compound_type',
                'molecular_formula', 'molecular_weight', 'role_in_bioprocess',
                'chebi_id', 'pubchem_id', 'chembl_id', 'properties',
                'Download URL', 'source'
            ])

        # Add source column if missing
        if 'source' not in chemicals_df.columns:
            chemicals_df['source'] = ''

        # Get existing chemical IDs
        existing_ids = set(chemicals_df['chemical_id'].dropna())

        # Add new chemicals
        new_rows = []
        for chebi_id, chem_data in self.chemicals.items():
            if chebi_id not in existing_ids:
                # Determine compound type from role
                compound_type = 'cofactor'
                role = chem_data['role']
                if 'substrate' in role.lower():
                    compound_type = 'substrate'
                elif 'product' in role.lower():
                    compound_type = 'product'

                new_rows.append({
                    'chemical_id': chebi_id,
                    'chemical_name': chem_data['chemical_name'],
                    'compound_type': compound_type,
                    'molecular_formula': '',
                    'molecular_weight': '',
                    'role_in_bioprocess': role,
                    'chebi_id': chebi_id,
                    'pubchem_id': '',
                    'chembl_id': '',
                    'properties': f"Found in {len(chem_data['proteins'])} proteins",
                    'Download URL': f"https://www.ebi.ac.uk/chebi/searchId.do?chebiId={chebi_id}",
                    'source': 'UniProt API mining from extended proteins'
                })

        if new_rows:
            new_df = pd.DataFrame(new_rows)
            chemicals_df = pd.concat([chemicals_df, new_df], ignore_index=True)
            print(f"✓ Added {len(new_rows)} new chemicals")
        else:
            print("No new chemicals to add")

        # Save extended table
        chemicals_df.to_csv(output_file, sep='\t', index=False)
        print(f"✓ Saved: {output_file}")
        print(f"  Total rows: {len(chemicals_df)}")
        print()

    def extend_publications_table(self) -> None:
        """Extend publications table with discovered literature."""
        print("=" * 80)
        print("EXTENDING PUBLICATIONS TABLE")
        print("=" * 80)
        print()

        publications_file = self.data_dir / "BER_CMM_Data_for_AI_publications.tsv"
        output_file = self.data_dir / "BER_CMM_Data_for_AI_publications_extended.tsv"

        # Load existing publications
        if publications_file.exists():
            publications_df = pd.read_csv(publications_file, sep='\t')
            print(f"Loaded existing publications table: {len(publications_df)} rows")
        else:
            publications_df = pd.DataFrame(columns=[
                'URL', 'Title', 'Journal', 'Year', 'Authors', 'Download', 'Source'
            ])

        # Add Source column if missing
        if 'Source' not in publications_df.columns:
            publications_df['Source'] = ''

        # Get existing publication URLs
        existing_urls = set(publications_df['URL'].dropna())

        # Add new publications
        new_rows = []
        for key, pub_data in self.publications.items():
            url = pub_data['url']

            if url not in existing_urls:
                new_rows.append({
                    'URL': url,
                    'Title': pub_data['title'],
                    'Journal': '',
                    'Year': '',
                    'Authors': '',
                    'Download': url,
                    'Source': 'UniProt API mining from extended proteins'
                })

        if new_rows:
            new_df = pd.DataFrame(new_rows)
            publications_df = pd.concat([publications_df, new_df], ignore_index=True)
            print(f"✓ Added {len(new_rows)} new publications")
        else:
            print("No new publications to add")

        # Save extended table
        publications_df.to_csv(output_file, sep='\t', index=False)
        print(f"✓ Saved: {output_file}")
        print(f"  Total rows: {len(publications_df)}")
        print()


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Mine extended proteins table to extract pathways, chemicals, publications",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Extend all tables
  python src/mine_extended_proteins.py

  # Extend specific tables
  python src/mine_extended_proteins.py --tables pathways chemicals

  # Limit number of proteins to process
  python src/mine_extended_proteins.py --max-proteins 50

Available tables:
  - pathways: Metabolic pathways from KEGG, Reactome, UniPathway, BioCyc
  - chemicals: CHEBI compounds (cofactors, substrates)
  - publications: Literature citations (PubMed, DOIs)
        """
    )

    parser.add_argument(
        '--data-dir',
        type=str,
        default='data/txt/sheet',
        help='Directory containing TSV data files'
    )

    parser.add_argument(
        '--tables',
        nargs='+',
        choices=['pathways', 'chemicals', 'publications'],
        default=['pathways', 'chemicals', 'publications'],
        help='Tables to extend (default: all)'
    )

    parser.add_argument(
        '--max-proteins',
        type=int,
        default=None,
        help='Maximum proteins to process (default: all)'
    )

    args = parser.parse_args()

    try:
        miner = ProteinDataMiner(data_dir=args.data_dir)

        # Step 1: Load proteins
        proteins = miner.load_proteins(max_proteins=args.max_proteins)

        if not proteins:
            print("No proteins to process. Exiting.")
            sys.exit(0)

        # Step 2: Mine protein data
        miner.mine_protein_data(proteins)

        # Step 3: Extend selected tables
        if 'pathways' in args.tables:
            miner.extend_pathways_table()

        if 'chemicals' in args.tables:
            miner.extend_chemicals_table()

        if 'publications' in args.tables:
            miner.extend_publications_table()

        print("=" * 80)
        print("✓ MINING COMPLETE!")
        print("=" * 80)
        print()

        sys.exit(0)

    except Exception as e:
        print(f"\n✗ Fatal error: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
