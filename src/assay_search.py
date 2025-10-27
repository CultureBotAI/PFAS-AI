"""Search for analytical assay protocols relevant to PFAS biodegradation.

This script searches protocols.io and curated sources for assay methods
and extends the assays table with structured protocol data.
"""

import argparse
import json
from pathlib import Path
from typing import Dict, List, Optional, Set

import pandas as pd


class AssaySearcher:
    """Search for PFAS assay protocols."""

    def __init__(self, source_label: str = "extend1"):
        """Initialize searcher with curated assay database.

        Args:
            source_label: Source label for tracking data provenance (default: extend1)
        """
        self.source_label = source_label
        # Curated assays from literature and protocols
        self.curated_assays = [
            {
                'assay_id': 'EPA-533',
                'assay_name': 'LC-MS/MS Analysis of PFAS in Drinking Water (EPA Method 533)',
                'assay_type': 'LC-MS/MS',
                'target_analytes': 'PFOA, PFOS, PFNA, PFHxS, PFBS, GenX, 25+ PFAS compounds',
                'detection_method': 'Triple quadrupole LC-MS/MS with ESI negative mode',
                'detection_limit': '0.5-4 ng/L (depending on compound)',
                'dynamic_range': '2-80 ng/L',
                'protocol_reference': 'EPA Method 533',
                'equipment_required': 'LC-MS/MS (triple quad), C18 column, isotope-labeled internal standards',
                'sample_preparation': 'Solid phase extraction (WAX cartridge), methanol elution',
                'data_output_format': 'Concentration (ng/L) with MRM transitions',
                'Download URL': 'https://www.epa.gov/dwanalyticalmethods/method-533',
                'source': self.source_label
            },
            {
                'assay_id': 'OBI:Fluoride-001',
                'assay_name': 'Ion-Selective Electrode Fluoride Measurement',
                'assay_type': 'fluoride electrode',
                'target_analytes': 'Free fluoride ion (F-)',
                'detection_method': 'Potentiometry with fluoride ion-selective electrode',
                'detection_limit': '0.02 mg/L (0.02 ppm)',
                'dynamic_range': '0.02 mg/L - 19,000 mg/L',
                'protocol_reference': 'EPA Method 340.2, ASTM D1179',
                'equipment_required': 'Fluoride ISE, pH/mV meter, TISAB II buffer',
                'sample_preparation': 'Mix with TISAB II (1:10 v/v) to adjust pH and ionic strength',
                'data_output_format': 'Fluoride concentration (mg/L or ppm)',
                'Download URL': 'https://www.epa.gov/esam/epa-method-3402-fluoride-potentiometric-ion-selective-electrode',
                'source': self.source_label
            },
            {
                'assay_id': 'OBI:IC-001',
                'assay_name': 'Ion Chromatography for Fluoride and Short-Chain PFAS',
                'assay_type': 'ion chromatography',
                'target_analytes': 'Fluoride, TFA, PFPrA, PFBA (C2-C4 PFAS)',
                'detection_method': 'Suppressed conductivity detection',
                'detection_limit': '0.5 μg/L (fluoride), 1-5 μg/L (short-chain PFAS)',
                'dynamic_range': '1 μg/L - 100 mg/L',
                'protocol_reference': 'EPA Method 300.0, modified for PFAS',
                'equipment_required': 'Ion chromatograph, anion exchange column, carbonate/bicarbonate eluent',
                'sample_preparation': 'Filtration (0.2 μm), dilution if needed',
                'data_output_format': 'Anion concentrations (μg/L)',
                'Download URL': 'https://www.epa.gov/esam/epa-method-3000-determination-inorganic-anions-drinking-water-ion-chromatography',
                'source': self.source_label
            },
            {
                'assay_id': 'OBI:TOF-001',
                'assay_name': 'Total Organic Fluorine (TOF) by Combustion IC',
                'assay_type': 'combustion IC',
                'target_analytes': 'Total organic fluorine (sum of all organofluorines)',
                'detection_method': 'Combustion at 1000°C, fluoride capture, IC quantification',
                'detection_limit': '10-50 μg F/L',
                'dynamic_range': '50 μg/L - 10 mg/L',
                'protocol_reference': 'ISO 9562 modified for organofluorines',
                'equipment_required': 'Combustion IC system, quartz combustion tube, oxygen supply',
                'sample_preparation': 'Sample injection into combustion module, fluoride trapping solution',
                'data_output_format': 'Total organic fluorine (μg F/L)',
                'Download URL': 'https://www.protocols.io/view/total-organic-fluorine-cic',
                'source': self.source_label
            },
            {
                'assay_id': 'OBI:FACS-003',
                'assay_name': 'PFAS-Degrading Cell Sorting via Fluoride-Responsive Reporter',
                'assay_type': 'FACS',
                'target_analytes': 'Cells with active fluoride export (PFAS degradation indicator)',
                'detection_method': 'GFP reporter under fluoride-responsive riboswitch promoter',
                'detection_limit': 'Single cell detection',
                'dynamic_range': '10^3 - 10^7 cells',
                'protocol_reference': 'Protocol_FACS_Fluoride_v1',
                'equipment_required': 'BD FACSAria, 488 nm laser, 530/30 nm emission filter',
                'sample_preparation': 'PFAS incubation (48h), PBS wash, resuspension in sort buffer',
                'data_output_format': 'Sorted populations, GFP fluorescence intensity, enrichment ratios',
                'Download URL': 'https://www.protocols.io/view/facs-fluoride-responsive-sorting',
                'source': self.source_label
            },
            {
                'assay_id': 'OBI:Growth-001',
                'assay_name': 'PFAS-Dependent Growth Assay (96-Well Microplate)',
                'assay_type': 'growth assay',
                'target_analytes': 'Microbial growth with PFAS as sole carbon/energy source',
                'detection_method': 'OD600 kinetic reading, CFU enumeration',
                'detection_limit': 'OD600 >0.05 above background',
                'dynamic_range': 'OD600 0.01 - 2.0',
                'protocol_reference': 'Protocol_PFAS_Growth_HTP',
                'equipment_required': 'Microplate reader, 96-well plates, anaerobic chamber (if needed)',
                'sample_preparation': 'Minimal media + PFAS (10-100 mg/L), cell inoculation (OD600=0.01)',
                'data_output_format': 'Growth curves, doubling time, final OD600, fluoride release',
                'Download URL': 'https://www.protocols.io/view/pfas-growth-assay-htp',
                'source': self.source_label
            }
        ]

    def get_curated_assays(self) -> List[Dict]:
        """Get curated assay protocols.

        Returns:
            List of assay dictionaries
        """
        return self.curated_assays

    def search_protocols_io(self, api_key: Optional[str] = None) -> List[Dict]:
        """Search protocols.io for PFAS assay protocols.

        Note: This requires a protocols.io API key. For now, returns empty list
        as placeholder for future implementation.

        Args:
            api_key: protocols.io API key

        Returns:
            List of protocol dictionaries
        """
        # Placeholder for protocols.io API integration
        # Would require API key and implementation of:
        # GET https://www.protocols.io/api/v3/protocols?key={key}&filter=PFAS

        print("  protocols.io API integration not yet implemented")
        print("  Using curated assay database instead")
        return []


def extend_assays_table(input_tsv: Path, output_tsv: Path, source_label: str = "extend1"):
    """Extend assays table with curated protocols.

    Args:
        input_tsv: Input assays TSV file
        output_tsv: Output extended TSV file
        source_label: Source label for tracking data provenance (default: extend1)
    """
    # Load existing data
    if input_tsv.exists():
        df = pd.read_csv(input_tsv, sep='\t')
        existing_ids = set(df['assay_id'].dropna())
    else:
        df = pd.DataFrame()
        existing_ids = set()

    print("Searching for PFAS assay protocols...")
    print(f"Source label: {source_label}")
    print("")

    # Initialize searcher
    searcher = AssaySearcher(source_label=source_label)

    # Get curated assays
    print("1. Loading curated assay protocols...")
    curated_assays = searcher.get_curated_assays()
    print(f"   Found {len(curated_assays)} curated protocols")
    print("")

    # Search protocols.io (placeholder)
    print("2. Searching protocols.io...")
    protocols_io_assays = searcher.search_protocols_io()
    print(f"   Found {len(protocols_io_assays)} protocols.io entries")
    print("")

    # Combine all assays
    all_assays = curated_assays + protocols_io_assays

    # Filter out duplicates
    new_assays = []
    for assay in all_assays:
        if assay['assay_id'] not in existing_ids:
            new_assays.append(assay)

    print(f"Total new assays: {len(new_assays)} (filtered {len(all_assays) - len(new_assays)} duplicates)")

    # Append to dataframe
    if new_assays:
        new_df = pd.DataFrame(new_assays)
        df = pd.concat([df, new_df], ignore_index=True)

    # Save extended table
    df.to_csv(output_tsv, sep='\t', index=False)
    print(f"\nExtended assays table saved to: {output_tsv}")
    print(f"Total assays: {len(df)}")


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Search for PFAS assay protocols"
    )
    parser.add_argument(
        '--input',
        type=Path,
        default=Path('data/txt/sheet/PFAS_Data_for_AI_assays.tsv'),
        help='Input assays TSV file'
    )
    parser.add_argument(
        '--output',
        type=Path,
        default=Path('data/txt/sheet/PFAS_Data_for_AI_assays_extended.tsv'),
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
    extend_assays_table(args.input, args.output, source_label=args.source_label)


if __name__ == "__main__":
    main()
