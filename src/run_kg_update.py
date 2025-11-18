#!/usr/bin/env python3
"""
Master workflow for kg-update: Knowledge Graph mining for data table updates

This script orchestrates repeatable KG-based table updates:
1. KG mining for core tables (genes, pathways, chemicals, taxa)
2. Cross-table enrichment (proteins → pathways → chemicals) [future]
3. Literature mining for publications [future]

All new records are labeled with source='kg_update' (repeatable operation).

This is designed to be run periodically as Knowledge Graph databases are updated.
"""

import argparse
import sys
from pathlib import Path
from typing import List, Dict
import pandas as pd

# Import all kg-update modules
from src.kg_update_genes import extend_genes_from_kg
from src.kg_update_pathways import extend_pathways_from_kg
from src.kg_update_chemicals import extend_chemicals_from_kg
from src.kg_update_genomes import extend_genomes_from_kg


class KGUpdateWorkflow:
    """
    Orchestrates repeatable KG-based table updates.
    """

    def __init__(
        self,
        output_dir: str = "data/txt/sheet/extended",
        dry_run: bool = False
    ):
        """
        Initialize workflow.

        Args:
            output_dir: Output directory for extended TSV files
            dry_run: If True, show what would be done without executing
        """
        self.output_dir = Path(output_dir)
        self.dry_run = dry_run
        self.results: Dict[str, pd.DataFrame] = {}

    def run_phase1_kg_mining(self) -> None:
        """
        Phase 1: Knowledge Graph Mining

        Mine core tables from kg-microbe and kg-microbe-function:
        - Genes/proteins (highest priority - 7-9x expected growth)
        - Pathways (6-8x expected growth)
        - Chemicals (4-5x expected growth)
        - Taxa/genomes (2-3x expected growth)
        """
        print("\n" + "=" * 80)
        print("PHASE 1: KNOWLEDGE GRAPH MINING")
        print("=" * 80)

        if self.dry_run:
            print("DRY RUN: Would execute KG mining scripts")
            return

        # 1. Extend genes/proteins (highest priority)
        print("\n[1/4] Extending genes/proteins from function KG...")
        try:
            genes_df = extend_genes_from_kg(
                output_file=str(self.output_dir / "BER_CMM_Data_for_AI_genes_and_proteins_extended.tsv"),
                source_label="kg_update",
                limit_per_taxon=2000,
                append=True
            )
            self.results['genes'] = genes_df
            print(f"✓ Added {len(genes_df)} new gene/protein records")
        except Exception as e:
            print(f"❌ Error extending genes: {e}")
            self.results['genes'] = pd.DataFrame()

        # 2. Extend pathways
        print("\n[2/4] Extending pathways from function KG...")
        try:
            pathways_df = extend_pathways_from_kg(
                output_file=str(self.output_dir / "BER_CMM_Data_for_AI_pathways_extended.tsv"),
                source_label="kg_update",
                append=True
            )
            self.results['pathways'] = pathways_df
            print(f"✓ Added {len(pathways_df)} new pathway records")
        except Exception as e:
            print(f"❌ Error extending pathways: {e}")
            self.results['pathways'] = pd.DataFrame()

        # 3. Extend chemicals
        print("\n[3/4] Extending chemicals from function KG...")
        try:
            chemicals_df = extend_chemicals_from_kg(
                output_file=str(self.output_dir / "BER_CMM_Data_for_AI_chemicals_extended.tsv"),
                source_label="kg_update",
                append=True
            )
            self.results['chemicals'] = chemicals_df
            print(f"✓ Added {len(chemicals_df)} new chemical records")
        except Exception as e:
            print(f"❌ Error extending chemicals: {e}")
            self.results['chemicals'] = pd.DataFrame()

        # 4. Extend taxa/genomes
        print("\n[4/4] Extending taxa/genomes from both KGs...")
        try:
            taxa_df = extend_genomes_from_kg(
                output_file=str(self.output_dir / "BER_CMM_Data_for_AI_taxa_and_genomes_extended.tsv"),
                append=True
            )
            self.results['taxa'] = taxa_df
            print(f"✓ Added {len(taxa_df)} new taxa records")
        except Exception as e:
            print(f"❌ Error extending taxa: {e}")
            self.results['taxa'] = pd.DataFrame()

    def run_phase2_cross_table_mining(self) -> None:
        """
        Phase 2: Cross-Table Enrichment

        Mine relationships between existing tables:
        - Proteins → Pathways (find pathways containing known proteins)
        - Pathways → Chemicals (find metabolites in known pathways)
        - Genes → Structures (find PDB entries for known proteins)
        """
        print("\n" + "=" * 80)
        print("PHASE 2: CROSS-TABLE ENRICHMENT")
        print("=" * 80)

        if self.dry_run:
            print("DRY RUN: Would execute cross-table mining")
            return

        print("⚠️  Phase 2 (cross-table mining) - To be implemented")
        print("    - This will mine existing tables to find relationships")
        print("    - Examples: proteins in pathways, metabolites in pathways")

    def run_phase3_external_apis(self) -> None:
        """
        Phase 3: External API Mining

        Query external databases for additional data:
        - Publications (PubMed, bioRxiv)
        - Structures (PDB, AlphaFold)
        - Datasets (GEO, SRA, MetaboLights)
        """
        print("\n" + "=" * 80)
        print("PHASE 3: EXTERNAL API MINING")
        print("=" * 80)

        if self.dry_run:
            print("DRY RUN: Would execute external API queries")
            return

        print("⚠️  Phase 3 (external APIs) - Using existing extend scripts")
        print("    - Run existing extend_publications.py, extend_structures.py, etc.")
        print("    - These can be run separately via Makefile")

    def print_summary(self) -> None:
        """Print final summary of kg-update workflow."""
        print("\n" + "=" * 80)
        print("KG-UPDATE WORKFLOW SUMMARY")
        print("=" * 80)

        total_new_records = 0

        for table_name, df in self.results.items():
            if not df.empty:
                print(f"✓ {table_name}: +{len(df)} records")
                total_new_records += len(df)
            else:
                print(f"  {table_name}: 0 records (skipped or failed)")

        print(f"\nTotal new records added: {total_new_records}")
        print("=" * 80)

    def run(self, phases: List[int] = None) -> None:
        """
        Run the complete kg-update workflow.

        Args:
            phases: List of phase numbers to run (default: Phase 1 only)
        """
        if phases is None:
            phases = [1]  # Default to Phase 1 only (KG mining)

        print("=" * 80)
        print("KG-UPDATE WORKFLOW")
        print("=" * 80)
        print(f"Output directory: {self.output_dir}")
        print(f"Dry run: {self.dry_run}")
        print(f"Phases to run: {phases}")
        print("=" * 80)

        if 1 in phases:
            self.run_phase1_kg_mining()

        if 2 in phases:
            self.run_phase2_cross_table_mining()

        if 3 in phases:
            self.run_phase3_external_apis()

        self.print_summary()


def main():
    """Command-line interface."""
    parser = argparse.ArgumentParser(
        description="Run kg-update workflow for repeatable Knowledge Graph-based table updates",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Run KG mining (default - Phase 1 only)
  python src/run_kg_update.py

  # Dry run (show what would be done)
  python src/run_kg_update.py --dry-run

  # Run via Makefile
  make kg-update

Phases:
  1. Knowledge Graph Mining (genes, pathways, chemicals, taxa) - ACTIVE
  2. Cross-Table Enrichment (future)
  3. External API Mining (future)

Source Labels:
  All records added: source='kg_update'

Repeatability:
  This workflow is designed to be run periodically as KG databases are updated.
  Deduplication ensures no duplicate records are created on repeated runs.
        """
    )

    parser.add_argument(
        "--output-dir",
        default="data/txt/sheet/extended",
        help="Output directory for extended TSV files"
    )
    parser.add_argument(
        "--phases",
        type=int,
        nargs="+",
        choices=[1, 2, 3],
        help="Phases to run (default: all)"
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show what would be done without executing"
    )

    args = parser.parse_args()

    # Create and run workflow
    workflow = KGUpdateWorkflow(
        output_dir=args.output_dir,
        dry_run=args.dry_run
    )

    workflow.run(phases=args.phases)


if __name__ == "__main__":
    main()
