"""Search and enrich PFAS-relevant biochemical reactions.

This module provides functions to search for and enrich reaction data from
RHEA, KEGG Reaction, and other databases.
"""

import re
import time
from pathlib import Path
from typing import Dict, List, Optional
from urllib.parse import urlencode

import pandas as pd


def parse_ec_numbers(enzyme_class_str: str) -> List[str]:
    """Extract EC numbers from enzyme class string.

    Args:
        enzyme_class_str: String containing EC numbers and enzyme names

    Returns:
        List of EC numbers in format "EC:1.2.3.4"

    Examples:
        >>> parse_ec_numbers("EC:3.8.1.6 4-chlorobenzoate dehalogenase")
        ['EC:3.8.1.6']
        >>> parse_ec_numbers("EC:1.14.13.2 4-hydroxybenzoate 3-monooxygenase;EC:1.14.13.33 4-hydroxybenzoate 3-monooxygenase [NAD(P)H]")
        ['EC:1.14.13.2', 'EC:1.14.13.33']
        >>> parse_ec_numbers("")
        []
    """
    if pd.isna(enzyme_class_str) or not enzyme_class_str:
        return []

    # Find all EC numbers in format EC:X.X.X.X or EC:X.X.X.-
    ec_pattern = r'EC:(\d+\.\d+\.\d+\.(?:\d+|-))'
    matches = re.findall(ec_pattern, str(enzyme_class_str))

    return [f"EC:{ec}" for ec in matches]


def parse_rhea_id(reaction_id_str: str) -> Optional[str]:
    """Extract RHEA ID from reaction identifier string.

    Args:
        reaction_id_str: Reaction identifier (may be RHEA:12345 or other format)

    Returns:
        RHEA ID in format "RHEA:12345" or None

    Examples:
        >>> parse_rhea_id("RHEA:23440")
        'RHEA:23440'
        >>> parse_rhea_id("R12345")

        >>> parse_rhea_id("")

    """
    if pd.isna(reaction_id_str) or not reaction_id_str:
        return None

    if str(reaction_id_str).startswith("RHEA:"):
        return str(reaction_id_str)

    return None


def parse_kegg_reaction_id(reaction_id_str: str) -> Optional[str]:
    """Extract KEGG Reaction ID from reaction identifier string.

    Args:
        reaction_id_str: Reaction identifier (may be R12345 or other format)

    Returns:
        KEGG Reaction ID in format "R12345" or None

    Examples:
        >>> parse_kegg_reaction_id("R12345")
        'R12345'
        >>> parse_kegg_reaction_id("RHEA:23440")

    """
    if pd.isna(reaction_id_str) or not reaction_id_str:
        return None

    if re.match(r'^R\d{5}$', str(reaction_id_str)):
        return str(reaction_id_str)

    return None


def get_rhea_url(rhea_id: str) -> str:
    """Get URL for RHEA reaction page.

    Args:
        rhea_id: RHEA identifier (with or without prefix)

    Returns:
        URL to RHEA reaction page

    Examples:
        >>> get_rhea_url("RHEA:23440")
        'https://www.rhea-db.org/rhea/23440'
        >>> get_rhea_url("23440")
        'https://www.rhea-db.org/rhea/23440'
    """
    rhea_id_clean = rhea_id.replace("RHEA:", "")
    return f"https://www.rhea-db.org/rhea/{rhea_id_clean}"


def get_kegg_reaction_url(kegg_id: str) -> str:
    """Get URL for KEGG Reaction page.

    Args:
        kegg_id: KEGG Reaction identifier

    Returns:
        URL to KEGG Reaction page

    Examples:
        >>> get_kegg_reaction_url("R00001")
        'https://www.kegg.jp/entry/R00001'
    """
    return f"https://www.kegg.jp/entry/{kegg_id}"


def enrich_reaction_data(reactions_df: pd.DataFrame) -> pd.DataFrame:
    """Enrich reactions dataframe with parsed fields.

    Adds the following columns:
    - rhea_id: Parsed RHEA identifier
    - kegg_reaction_id: Parsed KEGG Reaction identifier
    - ec_number: Parsed EC numbers (semicolon-separated)
    - url: URL to reaction database page

    Args:
        reactions_df: DataFrame with reactions data

    Returns:
        Enriched DataFrame
    """
    df = reactions_df.copy()

    # Parse RHEA IDs
    if 'Reaction identifier' in df.columns:
        df['rhea_id'] = df['Reaction identifier'].apply(parse_rhea_id)
        df['kegg_reaction_id'] = df['Reaction identifier'].apply(parse_kegg_reaction_id)

    # Parse EC numbers
    if 'Enzyme class' in df.columns:
        df['ec_number'] = df['Enzyme class'].apply(
            lambda x: ';'.join(parse_ec_numbers(x)) if parse_ec_numbers(x) else ''
        )

    # Generate URLs
    df['url'] = df.apply(
        lambda row: get_rhea_url(row['rhea_id']) if pd.notna(row.get('rhea_id'))
        else get_kegg_reaction_url(row['kegg_reaction_id']) if pd.notna(row.get('kegg_reaction_id'))
        else '',
        axis=1
    )

    # Rename columns to match schema
    column_mapping = {
        'Reaction identifier': 'reaction_id',
        'Equation': 'equation',
        'Enzyme class': 'enzyme_class',
        'Note': 'note',
        'reaction_category': 'reaction_category',
        'source': 'source'
    }

    df = df.rename(columns=column_mapping)

    # Select relevant columns in proper order
    output_cols = [
        'reaction_id', 'equation', 'reaction_category', 'enzyme_class',
        'ec_number', 'rhea_id', 'kegg_reaction_id', 'note', 'url', 'source'
    ]

    # Only include columns that exist
    output_cols = [col for col in output_cols if col in df.columns]

    return df[output_cols]


def search_rhea_reactions(query: str, max_results: int = 10) -> List[Dict]:
    """Search RHEA database for reactions.

    Note: This is a placeholder for future implementation. The RHEA API
    requires web scraping or TSV parsing which is not yet implemented.

    Args:
        query: Search query string
        max_results: Maximum number of results to return

    Returns:
        List of reaction dictionaries
    """
    print("  RHEA API search not yet implemented")
    print("  Future: Use RHEA TSV export or web scraping")
    return []


def search_kegg_reactions(query: str, max_results: int = 10) -> List[Dict]:
    """Search KEGG Reaction database.

    Note: This is a placeholder for future implementation. The KEGG API
    has usage restrictions and requires careful rate limiting.

    Args:
        query: Search query string
        max_results: Maximum number of results to return

    Returns:
        List of reaction dictionaries
    """
    print("  KEGG Reaction API search not yet implemented")
    print("  Future: Use KEGG REST API with rate limiting")
    return []


def extend_reactions_table(
    input_tsv: Path,
    output_tsv: Path,
    source_label: str = "extend1"
) -> None:
    """Extend reactions table with enriched data.

    Args:
        input_tsv: Input reactions TSV file
        output_tsv: Output enriched TSV file
        source_label: Source label for tracking data provenance
    """
    if not input_tsv.exists():
        print(f"Input file not found: {input_tsv}")
        return

    print(f"Enriching reactions data...")
    print(f"Input: {input_tsv}")
    print(f"Output: {output_tsv}")
    print("")

    # Load reactions data
    df = pd.read_csv(input_tsv, sep='\t')
    print(f"Loaded {len(df)} reactions")

    # Enrich data
    enriched_df = enrich_reaction_data(df)
    print(f"Enriched with parsed EC numbers and database IDs")

    # Save enriched data
    enriched_df.to_csv(output_tsv, sep='\t', index=False)
    print(f"\nSaved enriched reactions to: {output_tsv}")
    print(f"Total reactions: {len(enriched_df)}")

    # Print summary
    print("\nEnrichment summary:")
    print(f"  RHEA IDs: {enriched_df['rhea_id'].notna().sum()}")
    print(f"  EC numbers: {(enriched_df['ec_number'] != '').sum()}")
    print(f"  URLs: {(enriched_df['url'] != '').sum()}")


def main():
    """Main entry point."""
    import argparse

    parser = argparse.ArgumentParser(
        description="Enrich PFAS reactions data"
    )
    parser.add_argument(
        '--input',
        type=Path,
        default=Path('data/txt/sheet/PFAS_Data_for_AI_reactions.tsv'),
        help='Input reactions TSV file'
    )
    parser.add_argument(
        '--output',
        type=Path,
        default=Path('data/txt/sheet/PFAS_Data_for_AI_reactions_extended.tsv'),
        help='Output enriched TSV file'
    )
    parser.add_argument(
        '--source-label',
        type=str,
        default='extend1',
        help='Source label for data provenance'
    )

    args = parser.parse_args()

    extend_reactions_table(args.input, args.output, source_label=args.source_label)


if __name__ == "__main__":
    main()
