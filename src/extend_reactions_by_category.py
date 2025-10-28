#!/usr/bin/env python3
"""Extend individual reaction category sheets with category-specific enrichment.

This script extends each reaction category with targeted enrichment:
- Dehalogenase: Link to dehalogenase genes via EC numbers
- Fluoride resistance: Link to fluoride transporters
- Hydrocarbon degradation: Link to alkane metabolism genes
- Known PFAS degraders: Add organism strain information
- Oxygenase: Link to monooxygenase/dioxygenase genes
"""

import argparse
import re
from pathlib import Path
from typing import Dict, List, Optional, Set

import pandas as pd

from reaction_search import parse_ec_numbers, parse_rhea_id, get_rhea_url


# Category-specific enrichment strategies
CATEGORY_ENRICHMENT = {
    'dehalogenase': {
        'description': 'C-F and C-X bond cleavage enzymes',
        'target_ec_classes': ['3.8.1', '1.21', '4.5.1'],  # Haloacid/haloalkane dehalogenases, reductive dehalogenases
        'target_genes': ['rdhA', 'pceA', 'tceA', 'dhaA', 'dehH', 'fda'],
        'focus': 'Enzymes that cleave carbon-halogen bonds'
    },
    'fluoride_resistance': {
        'description': 'Fluoride transport and homeostasis',
        'target_genes': ['crcB', 'fex', 'fluc', 'crcA'],
        'target_go': ['GO:0015698'],  # inorganic anion transport
        'focus': 'Fluoride exporters and resistance mechanisms'
    },
    'hydrocarbon_degradation': {
        'description': 'Alkane and hydrocarbon metabolism',
        'target_ec_classes': ['1.14.15', '1.14.12', '1.14.13'],  # Monooxygenases, dioxygenases
        'target_genes': ['alkB', 'alkM', 'alkG', 'ladA'],
        'focus': 'Enzymes for hydrocarbon backbone degradation'
    },
    'known_pfas_degraders': {
        'description': 'Reactions from validated PFAS-degrading organisms',
        'target_organisms': ['Pseudomonas sp. Strain 273', 'Acidimicrobium', 'Hyphomicrobium'],
        'focus': 'Experimentally validated PFAS degradation pathways'
    },
    'oxygenase_cometabolism': {
        'description': 'Oxygenase-mediated co-metabolism',
        'target_ec_classes': ['1.14', '1.13'],  # Monooxygenases, dioxygenases
        'target_genes': ['almA', 'pmoA', 'mmoX', 'tmoA'],
        'focus': 'Co-metabolic oxidation pathways'
    },
    'important_genes': {
        'description': 'Non-enzymatic genes (transporters, regulators)',
        'focus': 'Regulatory and transport genes without enzymatic activity'
    }
}


def load_genes_table(genes_tsv: Path) -> pd.DataFrame:
    """Load genes and proteins table.

    Args:
        genes_tsv: Path to genes table

    Returns:
        DataFrame with genes data
    """
    if not genes_tsv.exists():
        print(f"Warning: Genes table not found: {genes_tsv}")
        return pd.DataFrame()

    return pd.read_csv(genes_tsv, sep='\t')


def match_genes_by_ec(reaction_row: pd.Series, genes_df: pd.DataFrame) -> List[str]:
    """Match genes to reaction based on EC numbers.

    Args:
        reaction_row: Reaction data row
        genes_df: Genes dataframe

    Returns:
        List of matching gene IDs
    """
    if genes_df.empty:
        return []

    # Get EC numbers from reaction
    enzyme_class = reaction_row.get('Enzyme class', '')
    ec_numbers = parse_ec_numbers(str(enzyme_class))

    if not ec_numbers:
        return []

    # Match against genes table
    matching_genes = []
    for ec in ec_numbers:
        ec_clean = ec.replace('EC:', '')

        # Try exact match first
        exact_matches = genes_df[
            (genes_df['EC'].astype(str) == ec_clean) |
            (genes_df['EC Number'].astype(str) == ec_clean)
        ]

        # If no exact match, try EC class match (e.g., 3.8.1.* matches 3.8.1.6)
        if exact_matches.empty:
            # Extract EC class (first 3 numbers)
            ec_parts = ec_clean.split('.')
            if len(ec_parts) >= 3:
                ec_class = '.'.join(ec_parts[:3])
                exact_matches = genes_df[
                    (genes_df['EC'].astype(str).str.startswith(ec_class, na=False)) |
                    (genes_df['EC Number'].astype(str).str.startswith(ec_class, na=False))
                ]

        for _, gene in exact_matches.iterrows():
            gene_id = gene.get('Gene/Protein Identifier') or gene.get('gene or protein id')
            if pd.notna(gene_id) and gene_id not in matching_genes:
                matching_genes.append(str(gene_id))

    return matching_genes


def match_genes_by_annotation(category: str, genes_df: pd.DataFrame) -> Dict[str, List[str]]:
    """Get gene mappings for a category based on annotations.

    Args:
        category: Reaction category
        genes_df: Genes dataframe

    Returns:
        Dictionary mapping reaction types to gene IDs
    """
    if genes_df.empty:
        return {}

    enrichment = CATEGORY_ENRICHMENT.get(category, {})
    target_genes = enrichment.get('target_genes', [])

    if not target_genes:
        return {}

    gene_mapping = {}
    for target in target_genes:
        # Search in annotation columns
        matches = genes_df[
            (genes_df['Annotation'].astype(str).str.contains(target, case=False, na=False)) |
            (genes_df['annotation'].astype(str).str.contains(target, case=False, na=False))
        ]

        gene_ids = []
        for _, gene in matches.iterrows():
            gene_id = gene.get('Gene/Protein Identifier') or gene.get('gene or protein id')
            if pd.notna(gene_id):
                gene_ids.append(str(gene_id))

        if gene_ids:
            gene_mapping[target] = gene_ids

    return gene_mapping


def enrich_category_sheet(
    input_tsv: Path,
    output_tsv: Path,
    genes_tsv: Path,
    category: str
) -> None:
    """Enrich a category-specific reaction sheet.

    Args:
        input_tsv: Input category TSV file
        output_tsv: Output enriched TSV file
        genes_tsv: Path to genes table
        category: Reaction category name
    """
    print(f"\nEnriching {category} reactions...")
    print(f"Input: {input_tsv}")
    print(f"Output: {output_tsv}")

    # Load data
    df = pd.read_csv(input_tsv, sep='\t')
    genes_df = load_genes_table(genes_tsv)

    print(f"Loaded {len(df)} entries")

    # Special handling for important_genes (not reactions, just gene list)
    if category == 'important_genes':
        print("Note: This is a gene list, not reactions data")
        print("No enrichment needed - copying to extended file")
        df.to_csv(output_tsv, sep='\t', index=False)
        print(f"Saved to: {output_tsv}")
        return

    # Get category enrichment strategy
    enrichment = CATEGORY_ENRICHMENT.get(category, {})
    print(f"Strategy: {enrichment.get('focus', 'General enrichment')}")

    # Parse EC numbers and RHEA IDs
    df['ec_number'] = df['Enzyme class'].apply(
        lambda x: ';'.join(parse_ec_numbers(str(x))) if pd.notna(x) else ''
    )
    df['rhea_id'] = df['Reaction identifier'].apply(lambda x: parse_rhea_id(str(x)))

    # Generate URLs
    df['url'] = df['rhea_id'].apply(lambda x: get_rhea_url(x) if pd.notna(x) else '')

    # Category-specific enrichment
    if category in ['dehalogenase', 'hydrocarbon_degradation', 'oxygenase_cometabolism']:
        # Link reactions to genes via EC numbers
        df['linked_genes'] = df.apply(
            lambda row: ';'.join(match_genes_by_ec(row, genes_df)),
            axis=1
        )
        linked_count = (df['linked_genes'] != '').sum()
        print(f"  Linked {linked_count} reactions to genes via EC numbers")

    elif category == 'fluoride_resistance':
        # Get fluoride transporter genes
        gene_mapping = match_genes_by_annotation(category, genes_df)
        if gene_mapping:
            all_transporter_genes = []
            for genes_list in gene_mapping.values():
                all_transporter_genes.extend(genes_list)
            df['linked_genes'] = ';'.join(set(all_transporter_genes))
            print(f"  Linked to fluoride transporters: {', '.join(gene_mapping.keys())}")

    elif category == 'known_pfas_degraders':
        # Add organism context
        df['pfas_degrader_context'] = 'Validated PFAS degradation pathway'

    # Reorder columns
    base_cols = ['Reaction identifier', 'Equation', 'Enzyme class', 'ec_number', 'rhea_id']
    extra_cols = [c for c in df.columns if c not in base_cols and c not in ['Enzymes', 'reaction_category', 'source', 'Note', 'url']]
    final_cols = base_cols + extra_cols + ['url', 'reaction_category', 'source']
    if 'Note' in df.columns:
        final_cols.insert(-2, 'Note')

    # Only include columns that exist
    final_cols = [c for c in final_cols if c in df.columns]
    df = df[final_cols]

    # Save enriched data
    df.to_csv(output_tsv, sep='\t', index=False)
    print(f"Saved enriched reactions to: {output_tsv}")
    print(f"Total reactions: {len(df)}")


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Extend individual reaction category sheets"
    )
    parser.add_argument(
        '--category',
        type=str,
        required=True,
        choices=list(CATEGORY_ENRICHMENT.keys()),
        help='Reaction category to extend'
    )
    parser.add_argument(
        '--input-dir',
        type=Path,
        default=Path('data/txt/sheet'),
        help='Directory containing category TSV files'
    )
    parser.add_argument(
        '--genes-table',
        type=Path,
        default=Path('data/txt/sheet/PFAS_Data_for_AI_genes_and_proteins_extended.tsv'),
        help='Path to genes table'
    )

    args = parser.parse_args()

    # Determine input/output paths
    input_tsv = args.input_dir / f"PFAS_Reactions_{args.category}.tsv"
    output_tsv = args.input_dir / f"PFAS_Reactions_{args.category}_extended.tsv"

    if not input_tsv.exists():
        print(f"Error: Input file not found: {input_tsv}")
        return 1

    enrich_category_sheet(
        input_tsv,
        output_tsv,
        args.genes_table,
        args.category
    )

    return 0


if __name__ == "__main__":
    import sys
    sys.exit(main())
