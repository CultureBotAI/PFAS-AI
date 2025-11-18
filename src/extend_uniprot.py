"""Orchestrate UniProt API integration across all data tables.

This script coordinates the extension of multiple data tables using UniProt API:
- Genes/proteins: Comprehensive protein data with GO, EC, CHEBI
- Functions: Biological functions (enzymes, GO processes, reactions, pathways, chemicals)
- Chemicals: CHEBI compounds from protein cofactors
- Pathways: Pathway annotations (KEGG, Reactome, UniPathway)
- Publications: Literature citations from protein entries
"""

import argparse
import sys
from pathlib import Path
from typing import List, Optional

try:
    from src.gene_search import create_extended_genes_table
    from src.uniprot_functions import create_functions_table
    from src.chemical_search import extend_chemicals_table
    from src.pathway_search import create_extended_pathways_table
    from src.publication_search import create_extended_publications_table
except ImportError:
    from gene_search import create_extended_genes_table
    from uniprot_functions import create_functions_table
    from chemical_search import extend_chemicals_table
    from pathway_search import create_extended_pathways_table
    from publication_search import create_extended_publications_table


def extend_all_with_uniprot(
    data_dir: str = "data/txt/sheet",
    tables: Optional[List[str]] = None,
    source_label: str = "uniprot_api"
) -> None:
    """Extend all data tables with UniProt API data.

    Args:
        data_dir: Directory containing TSV data files
        tables: List of table names to extend (default: all tables)
        source_label: Source label for data provenance

    Tables available:
        - genes: Genes and proteins with comprehensive annotations
        - functions: Biological functions (EC, GO, Rhea, pathways, CHEBI)
        - chemicals: Chemical compounds from CHEBI
        - pathways: Metabolic pathways from KEGG/Reactome/UniPathway
        - publications: Literature citations
    """
    data_path = Path(data_dir)

    # Default to all tables
    if tables is None:
        tables = ["genes", "functions", "chemicals", "pathways", "publications"]

    print("=" * 80)
    print("UniProt API Integration - Extending Data Tables")
    print("=" * 80)
    print(f"Data directory: {data_path}")
    print(f"Source label: {source_label}")
    print(f"Tables to extend: {', '.join(tables)}")
    print("")

    # Extend genes and proteins table
    if "genes" in tables:
        print("\n" + "=" * 80)
        print("1. EXTENDING GENES AND PROTEINS TABLE")
        print("=" * 80)

        genes_input = data_path / "BER_CMM_Data_for_AI_genes_and_proteins.tsv"

        if genes_input.exists():
            try:
                create_extended_genes_table(
                    input_file=str(genes_input),
                    output_dir=str(data_path),
                    use_comprehensive=True,
                    fetch_details=False  # Set to True for maximum detail (slower)
                )
                print("✓ Genes and proteins table extended successfully")
            except Exception as e:
                print(f"✗ Error extending genes table: {e}")
        else:
            print(f"⚠ Genes input file not found: {genes_input}")

    # Create biological functions table
    if "functions" in tables:
        print("\n" + "=" * 80)
        print("2. CREATING BIOLOGICAL FUNCTIONS TABLE")
        print("=" * 80)

        try:
            create_functions_table(
                output_dir=str(data_path),
                source_label=source_label
            )
            print("✓ Biological functions table created successfully")
        except Exception as e:
            print(f"✗ Error creating functions table: {e}")

    # Extend chemicals table
    if "chemicals" in tables:
        print("\n" + "=" * 80)
        print("3. EXTENDING CHEMICALS TABLE")
        print("=" * 80)

        chemicals_input = data_path / "BER_CMM_Data_for_AI_chemicals.tsv"
        chemicals_output = data_path / "BER_CMM_Data_for_AI_chemicals_extended.tsv"

        if chemicals_input.exists():
            try:
                extend_chemicals_table(
                    input_tsv=chemicals_input,
                    output_tsv=chemicals_output,
                    source_label=source_label,
                    include_uniprot=True
                )
                print("✓ Chemicals table extended successfully")
            except Exception as e:
                print(f"✗ Error extending chemicals table: {e}")
        else:
            print(f"⚠ Chemicals input file not found: {chemicals_input}")

    # Extend pathways table
    if "pathways" in tables:
        print("\n" + "=" * 80)
        print("4. EXTENDING PATHWAYS TABLE")
        print("=" * 80)

        pathways_input = data_path / "BER_CMM_Data_for_AI_pathways.tsv"

        if pathways_input.exists():
            try:
                create_extended_pathways_table(
                    input_file=str(pathways_input),
                    output_dir=str(data_path),
                    include_uniprot=True
                )
                print("✓ Pathways table extended successfully")
            except Exception as e:
                print(f"✗ Error extending pathways table: {e}")
        else:
            print(f"⚠ Pathways input file not found: {pathways_input}")

    # Extend publications table
    if "publications" in tables:
        print("\n" + "=" * 80)
        print("5. EXTENDING PUBLICATIONS TABLE")
        print("=" * 80)

        publications_input = data_path / "BER_CMM_Data_for_AI_publications.tsv"

        if publications_input.exists():
            try:
                create_extended_publications_table(
                    input_file=str(publications_input),
                    output_dir=str(data_path),
                    include_uniprot=True
                )
                print("✓ Publications table extended successfully")
            except Exception as e:
                print(f"✗ Error extending publications table: {e}")
        else:
            print(f"⚠ Publications input file not found: {publications_input}")

    # Summary
    print("\n" + "=" * 80)
    print("SUMMARY")
    print("=" * 80)
    print(f"Extended {len(tables)} tables with UniProt API data")
    print(f"Output directory: {data_path}")
    print("")
    print("Output files:")
    for table in tables:
        if table == "genes":
            print(f"  - {data_path / 'BER_CMM_Data_for_AI_genes_and_proteins_extended.tsv'}")
        elif table == "functions":
            print(f"  - {data_path / 'BER_CMM_Data_for_AI_biological_functions.tsv'}")
        elif table == "chemicals":
            print(f"  - {data_path / 'BER_CMM_Data_for_AI_chemicals_extended.tsv'}")
        elif table == "pathways":
            print(f"  - {data_path / 'BER_CMM_Data_for_AI_pathways_extended.tsv'}")
        elif table == "publications":
            print(f"  - {data_path / 'BER_CMM_Data_for_AI_publications_extended.tsv'}")
    print("=" * 80)


def main():
    """Main entry point for command-line usage."""
    parser = argparse.ArgumentParser(
        description="Extend data tables with UniProt API integration",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Extend all tables
  python -m src.extend_uniprot

  # Extend specific tables only
  python -m src.extend_uniprot --tables genes functions

  # Use custom data directory and source label
  python -m src.extend_uniprot --data-dir data/txt/sheet --source-label uniprot_2024

Available tables:
  - genes: Genes and proteins with comprehensive annotations
  - functions: Biological functions (EC, GO, Rhea, pathways, CHEBI)
  - chemicals: Chemical compounds from CHEBI
  - pathways: Metabolic pathways from KEGG/Reactome/UniPathway
  - publications: Literature citations
        """
    )

    parser.add_argument(
        '--data-dir',
        type=str,
        default='data/txt/sheet',
        help='Directory containing TSV data files (default: data/txt/sheet)'
    )

    parser.add_argument(
        '--tables',
        nargs='+',
        choices=['genes', 'functions', 'chemicals', 'pathways', 'publications'],
        default=None,
        help='Tables to extend (default: all tables)'
    )

    parser.add_argument(
        '--source-label',
        type=str,
        default='uniprot_api',
        help='Source label for data provenance tracking (default: uniprot_api)'
    )

    args = parser.parse_args()

    try:
        extend_all_with_uniprot(
            data_dir=args.data_dir,
            tables=args.tables,
            source_label=args.source_label
        )
        sys.exit(0)
    except Exception as e:
        print(f"\n✗ Fatal error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
