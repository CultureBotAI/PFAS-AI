"""Search PubChem and CHEBI for PFAS-relevant chemical compounds.

This script searches chemical databases for compounds relevant to PFAS
biodegradation and extends the chemicals table with structured data.
"""

import argparse
import json
import time
from pathlib import Path
from typing import Dict, List, Optional, Set

import pandas as pd
import requests


class ChemicalSearcher:
    """Search chemical databases for PFAS-relevant compounds."""

    def __init__(self, source_label: str = "extend1"):
        """Initialize searcher with API endpoints.

        Args:
            source_label: Source label for tracking data provenance (default: extend1)
        """
        self.pubchem_base = "https://pubchem.ncbi.nlm.nih.gov/rest/pug"
        self.chebi_base = "https://www.ebi.ac.uk/chebi"
        self.rate_limit_delay = 0.5  # seconds between API calls
        self.source_label = source_label

        # Major PFAS compounds
        self.pfas_compounds = [
            "PFOA", "PFOS", "PFNA", "PFDA", "PFHxS", "PFBS",
            "GenX", "PFBA", "PFHxA", "PFDoA", "PFOSA",
            "6:2 FTOH", "8:2 FTOH"
        ]

        # PFAS-relevant search terms
        self.search_terms = [
            "perfluorooctanoic acid",
            "perfluorooctane sulfonic acid",
            "perfluorinated compound",
            "polyfluorinated compound",
            "fluorinated surfactant",
            "fluorotelomer alcohol",
            "perfluoroalkyl acid",
            "AFFF compound"
        ]

    def search_pubchem_pfas(self) -> List[Dict]:
        """Search PubChem for PFAS compounds.

        Returns:
            List of compound dictionaries
        """
        compounds = []

        for compound_name in self.pfas_compounds:
            print(f"  Searching PubChem for: {compound_name}")

            try:
                # Search by name
                url = f"{self.pubchem_base}/compound/name/{compound_name}/JSON"
                response = requests.get(url, timeout=30)

                if response.status_code == 200:
                    data = response.json()
                    if 'PC_Compounds' in data:
                        pc_compound = data['PC_Compounds'][0]
                        compound = self._parse_pubchem_compound(pc_compound, compound_name)
                        if compound:
                            compounds.append(compound)

                time.sleep(self.rate_limit_delay)

            except Exception as e:
                print(f"    Error searching {compound_name}: {e}")
                continue

        return compounds

    def search_pubchem_pfas_precursors(self) -> List[Dict]:
        """Search PubChem for PFAS precursors and metabolites.

        Returns:
            List of compound dictionaries
        """
        compounds = []

        for term in self.search_terms:
            print(f"  Searching PubChem for: {term}")

            try:
                # Search by name
                url = f"{self.pubchem_base}/compound/name/{term}/JSON"
                response = requests.get(url, timeout=30)

                if response.status_code == 200:
                    data = response.json()
                    if 'PC_Compounds' in data:
                        # Take first result only
                        pc_compound = data['PC_Compounds'][0]
                        compound = self._parse_pubchem_compound(pc_compound, None)
                        if compound:
                            compounds.append(compound)

                time.sleep(self.rate_limit_delay)

            except Exception as e:
                print(f"    Error searching {term}: {e}")
                continue

        return compounds

    def _parse_pubchem_compound(self, pc_compound: Dict, element_name: Optional[str]) -> Optional[Dict]:
        """Parse PubChem compound data.

        Args:
            pc_compound: PubChem compound JSON
            element_name: Element name for lanthanide cations

        Returns:
            Compound dictionary or None
        """
        try:
            cid = pc_compound['id']['id']['cid']

            # Extract properties
            props = pc_compound.get('props', [])
            molecular_formula = None
            molecular_weight = None
            iupac_name = None

            for prop in props:
                label = prop.get('urn', {}).get('label', '')
                value = prop.get('value', {})

                if label == 'Molecular Formula':
                    molecular_formula = value.get('sval')
                elif label == 'Molecular Weight':
                    molecular_weight = value.get('fval')
                elif label == 'IUPAC Name':
                    iupac_name = value.get('sval')

            # Determine compound type
            compound_type = "lanthanide" if element_name else "chelator"
            if "lanthanophore" in str(iupac_name).lower():
                compound_type = "lanthanophore"
            elif "siderophore" in str(iupac_name).lower():
                compound_type = "lanthanophore"

            # Generate chemical name
            chemical_name = iupac_name or (f"{element_name}(III) cation" if element_name else f"PubChem_{cid}")

            # Role in bioprocess
            role = "TRL assay probe for REE detection" if element_name else "Lanthanide chelation and transport"

            compound = {
                'chemical_id': f"PubChem:{cid}",
                'chemical_name': chemical_name,
                'compound_type': compound_type,
                'molecular_formula': molecular_formula,
                'molecular_weight': molecular_weight,
                'role_in_bioprocess': role,
                'chebi_id': None,
                'pubchem_id': str(cid),
                'chembl_id': None,
                'properties': json.dumps({
                    'source': 'PubChem',
                    'iupac_name': iupac_name
                }),
                'Download URL': f"https://pubchem.ncbi.nlm.nih.gov/compound/{cid}",
                'source': self.source_label
            }

            return compound

        except Exception as e:
            print(f"    Error parsing PubChem compound: {e}")
            return None

    def search_chebi_lanthanophores(self) -> List[Dict]:
        """Search CHEBI for lanthanophores and related compounds.

        Note: CHEBI doesn't have a simple REST API, so this is a placeholder
        for manual curation or future web scraping implementation.

        Returns:
            List of compound dictionaries
        """
        # Manual curated CHEBI entries for lanthanide-relevant compounds
        curated_compounds = [
            {
                'chemical_id': 'CHEBI:138675',
                'chemical_name': 'Methylolanthanin',
                'compound_type': 'lanthanophore',
                'molecular_formula': 'C30H42N6O15',
                'molecular_weight': 730.69,
                'role_in_bioprocess': 'Lanthanide chelation and transport',
                'chebi_id': 'CHEBI:138675',
                'pubchem_id': '136161579',
                'chembl_id': None,
                'properties': json.dumps({
                    'source': 'CHEBI',
                    'metal_binding': 'high affinity for La/Ce/Nd',
                    'producer': 'Methylobacterium extorquens',
                    'structure': 'hydroxamate-type siderophore'
                }),
                'Download URL': 'https://www.ebi.ac.uk/chebi/searchId.do?chebiId=CHEBI:138675',
                'source': self.source_label
            }
        ]

        print("  Using curated CHEBI lanthanophore entries")
        return curated_compounds


def extend_chemicals_table(input_tsv: Path, output_tsv: Path, source_label: str = "extend1"):
    """Extend chemicals table with PubChem and CHEBI data.

    Args:
        input_tsv: Input chemicals TSV file
        output_tsv: Output extended TSV file
        source_label: Source label for tracking data provenance (default: extend1)
    """
    # Load existing data
    if input_tsv.exists():
        df = pd.read_csv(input_tsv, sep='\t')
        existing_ids = set(df['chemical_id'].dropna())
    else:
        df = pd.DataFrame()
        existing_ids = set()

    print("Searching chemical databases for lanthanide compounds...")
    print(f"Source label: {source_label}")
    print("")

    # Initialize searcher
    searcher = ChemicalSearcher(source_label=source_label)

    # Search PubChem
    print("1. Searching PubChem for lanthanide cations...")
    lanthanide_compounds = searcher.search_pubchem_lanthanides()
    print(f"   Found {len(lanthanide_compounds)} lanthanide cations")
    print("")

    print("2. Searching PubChem for lanthanide complexes...")
    complex_compounds = searcher.search_pubchem_complexes()
    print(f"   Found {len(complex_compounds)} complexes")
    print("")

    print("3. Adding curated CHEBI lanthanophores...")
    chebi_compounds = searcher.search_chebi_lanthanophores()
    print(f"   Found {len(chebi_compounds)} CHEBI compounds")
    print("")

    # Combine all compounds
    all_compounds = lanthanide_compounds + complex_compounds + chebi_compounds

    # Filter out duplicates
    new_compounds = []
    for compound in all_compounds:
        if compound['chemical_id'] not in existing_ids:
            new_compounds.append(compound)

    print(f"Total new compounds: {len(new_compounds)} (filtered {len(all_compounds) - len(new_compounds)} duplicates)")

    # Append to dataframe
    if new_compounds:
        new_df = pd.DataFrame(new_compounds)
        df = pd.concat([df, new_df], ignore_index=True)

    # Save extended table
    df.to_csv(output_tsv, sep='\t', index=False)
    print(f"\nExtended chemicals table saved to: {output_tsv}")
    print(f"Total compounds: {len(df)}")


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Search PubChem and CHEBI for lanthanide-relevant compounds"
    )
    parser.add_argument(
        '--input',
        type=Path,
        default=Path('data/txt/sheet/BER_CMM_Data_for_AI_chemicals.tsv'),
        help='Input chemicals TSV file'
    )
    parser.add_argument(
        '--output',
        type=Path,
        default=Path('data/txt/sheet/BER_CMM_Data_for_AI_chemicals_extended.tsv'),
        help='Output extended TSV file'
    )
    parser.add_argument(
        '--source-label',
        type=str,
        default='extend1',
        help='Source label for data provenance tracking (default: extend1, use extend2 for round 2)'
    )

    args = parser.parse_args()

    # Extend table
    extend_chemicals_table(args.input, args.output, source_label=args.source_label)


if __name__ == "__main__":
    main()
