"""Search for analytical assay protocols relevant to lanthanide bioprocessing.

This script searches protocols.io and curated sources for assay methods
and extends the assays table with structured protocol data.
"""

import argparse
import json
from pathlib import Path
from typing import Dict, List, Optional, Set

import pandas as pd


class AssaySearcher:
    """Search for lanthanide assay protocols."""

    def __init__(self, source_label: str = "extend1"):
        """Initialize searcher with curated assay database.

        Args:
            source_label: Source label for tracking data provenance (default: extend1)
        """
        self.source_label = source_label
        # Curated assays from literature and protocols
        self.curated_assays = [
            {
                'assay_id': 'OBI:TRL-002',
                'assay_name': 'Microplate-based TRL Assay for Lanthanide Screening',
                'assay_type': 'time-resolved luminescence (TRL)',
                'target_analytes': 'Eu3+, Tb3+, Sm3+, Dy3+',
                'detection_method': 'Time-gated luminescence with 100 μs delay',
                'detection_limit': '0.05 nM',
                'dynamic_range': '0.05 nM - 50 μM',
                'protocol_reference': 'Protocol_TRL_HTP_v1',
                'equipment_required': 'Tecan Spark multimode plate reader, black 384-well plates',
                'sample_preparation': 'Cell lysis with Triton X-100, 1:10 dilution in TRL buffer (pH 7.4)',
                'data_output_format': 'Luminescence counts (CPS) and calculated concentrations',
                'Download URL': 'https://www.protocols.io/view/lanthanide-trl-htp-screening',
                'source': self.source_label
            },
            {
                'assay_id': 'OBI:ICP-002',
                'assay_name': 'Multi-element REE Analysis by ICP-MS',
                'assay_type': 'ICP-MS',
                'target_analytes': 'La, Ce, Pr, Nd, Sm, Eu, Gd, Tb, Dy, Ho, Er, Tm, Yb, Lu',
                'detection_method': 'Quadrupole ICP-MS with collision/reaction cell',
                'detection_limit': '0.01 ppb',
                'dynamic_range': '0.01 ppb - 1 ppm',
                'protocol_reference': 'EPA Method 200.8',
                'equipment_required': 'Agilent 7900 ICP-MS, microwave digestion system',
                'sample_preparation': 'Microwave-assisted acid digestion (HNO3 + H2O2), dilution to 2% HNO3',
                'data_output_format': 'Elemental concentrations (μg/L) with isotope ratios',
                'Download URL': 'https://www.epa.gov/esam/method-2008-determination-trace-elements-waters-and-wastes-inductively-coupled-plasma-mass',
                'source': self.source_label
            },
            {
                'assay_id': 'OBI:FACS-002',
                'assay_name': 'Lanthanide Binding Cell Enrichment via FACS',
                'assay_type': 'FACS',
                'target_analytes': 'Lanthanide-binding cells (Eu3+ fluorescence)',
                'detection_method': '355 nm excitation, 615 nm emission (Eu3+ 5D0→7F2 transition)',
                'detection_limit': 'Single cell with >10^4 Eu3+ ions bound',
                'dynamic_range': '10^3 - 10^7 cells',
                'protocol_reference': 'Protocol_FACS_REE_v2',
                'equipment_required': 'BD FACSAria Fusion, 355 nm UV laser, custom 610/20 nm filter',
                'sample_preparation': 'Eu3+ incubation (100 μM, 1h), PBS wash (3x), resuspension in sort buffer',
                'data_output_format': 'Sorted cell populations, FCS files, enrichment fold-change',
                'Download URL': 'https://www.protocols.io/view/facs-ree-enrichment-v2',
                'source': self.source_label
            },
            {
                'assay_id': 'OBI:Fluor-001',
                'assay_name': 'Steady-State Fluorescence Spectroscopy for Lanthanide Complexation',
                'assay_type': 'fluorescence spectroscopy',
                'target_analytes': 'Eu3+, Tb3+ complexes with organic ligands',
                'detection_method': 'Excitation at ligand absorption wavelength, emission at lanthanide f-f transitions',
                'detection_limit': '1 nM',
                'dynamic_range': '1 nM - 100 μM',
                'protocol_reference': None,
                'equipment_required': 'Fluorescence spectrometer (Horiba FluoroMax-4), quartz cuvettes',
                'sample_preparation': 'Mix lanthanide (10 μM) with ligand (0-100 μM) in buffered solution',
                'data_output_format': 'Emission spectra (300-700 nm), binding constants from titration',
                'Download URL': None,
                'source': self.source_label
            },
            {
                'assay_id': 'OBI:UV-001',
                'assay_name': 'UV-Vis Absorption Spectroscopy for Lanthanide Complex Formation',
                'assay_type': 'UV-visible spectroscopy',
                'target_analytes': 'Lanthanide-ligand complexes',
                'detection_method': 'Absorbance at ligand peak wavelength (250-400 nm)',
                'detection_limit': '100 nM',
                'dynamic_range': '100 nM - 1 mM',
                'protocol_reference': None,
                'equipment_required': 'UV-Vis spectrophotometer, quartz cuvettes (1 cm path length)',
                'sample_preparation': 'Prepare lanthanide-ligand mixtures in transparent buffer (pH 7.0)',
                'data_output_format': 'Absorption spectra (200-800 nm), Job plots for stoichiometry',
                'Download URL': None,
                'source': self.source_label
            },
            {
                'assay_id': 'OBI:XRF-001',
                'assay_name': 'X-ray Fluorescence for Solid-Phase REE Quantification',
                'assay_type': 'X-ray fluorescence (XRF)',
                'target_analytes': 'All lanthanides in solid matrices',
                'detection_method': 'Energy-dispersive X-ray fluorescence (ED-XRF)',
                'detection_limit': '10 ppm',
                'dynamic_range': '10 ppm - 100%',
                'protocol_reference': None,
                'equipment_required': 'Handheld XRF analyzer or benchtop ED-XRF',
                'sample_preparation': 'Dry biomass, pressed pellets, or direct solid sampling',
                'data_output_format': 'Elemental composition (wt%), REE oxide concentrations',
                'Download URL': None,
                'source': self.source_label
            },
            {
                'assay_id': 'OBI:AA-001',
                'assay_name': 'Atomic Absorption Spectroscopy for Lanthanide Quantification',
                'assay_type': 'atomic absorption spectroscopy (AAS)',
                'target_analytes': 'Individual lanthanides (one element at a time)',
                'detection_method': 'Flame or graphite furnace atomic absorption',
                'detection_limit': '1 ppb (GFAAS) or 10 ppb (FAAS)',
                'dynamic_range': '1 ppb - 100 ppm',
                'protocol_reference': 'EPA Method 7000B',
                'equipment_required': 'AA spectrometer with lanthanide hollow cathode lamps',
                'sample_preparation': 'Acid digestion, dilution to working range, matrix matching',
                'data_output_format': 'Absorbance values, calculated concentrations (mg/L)',
                'Download URL': 'https://www.epa.gov/hw-sw846/sw-846-test-method-7000b-flame-atomic-absorption-spectrophotometry',
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
        """Search protocols.io for lanthanide assay protocols.

        Note: This requires a protocols.io API key. For now, returns empty list
        as placeholder for future implementation.

        Args:
            api_key: protocols.io API key

        Returns:
            List of protocol dictionaries
        """
        # Placeholder for protocols.io API integration
        # Would require API key and implementation of:
        # GET https://www.protocols.io/api/v3/protocols?key={key}&filter=lanthanide

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

    print("Searching for lanthanide assay protocols...")
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
        description="Search for lanthanide assay protocols"
    )
    parser.add_argument(
        '--input',
        type=Path,
        default=Path('data/txt/sheet/BER_CMM_Data_for_AI_assays.tsv'),
        help='Input assays TSV file'
    )
    parser.add_argument(
        '--output',
        type=Path,
        default=Path('data/txt/sheet/BER_CMM_Data_for_AI_assays_extended.tsv'),
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
