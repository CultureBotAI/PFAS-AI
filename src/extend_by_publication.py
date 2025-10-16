#!/usr/bin/env python3
"""
Extend data sheets by cross-referencing with publication content.

This script reads markdown files converted from PDFs and checks if each publication
is relevant to any row in the data sheets. If relevant, it appends the publication
identifier (DOI or other standard ID) to the source column with a '|' delimiter.

Usage:
    python src/extend_by_publication.py --publications-file data/txt/sheet/BER_CMM_Data_for_AI_publications.tsv \
                                        --markdown-dir data/publications \
                                        --data-dir data/txt/sheet
"""

import argparse
import re
from pathlib import Path
from typing import Dict, List, Optional, Set, Tuple
import pandas as pd


def extract_publication_id(url: str) -> Optional[str]:
    """
    Extract a standard publication identifier from a URL.

    Prioritizes DOI > PMC ID > PMID > filename

    Args:
        url: Publication URL

    Returns:
        Standard identifier (e.g., '10.1038/nature16174', 'PMC6764073', 'PMID:38269599')
    """
    # DOI pattern
    doi_match = re.search(r'10\.\d+/[\w\-\.]+', url)
    if doi_match:
        return doi_match.group(0)

    # PMC pattern
    pmc_match = re.search(r'PMC(\d+)', url)
    if pmc_match:
        return f"PMC{pmc_match.group(1)}"

    # PMID pattern
    pmid_match = re.search(r'pubmed\.ncbi\.nlm\.nih\.gov/(\d+)', url)
    if pmid_match:
        return f"PMID:{pmid_match.group(1)}"

    # ArXiv pattern
    arxiv_match = re.search(r'arxiv\.org/abs/([\d\.]+)', url)
    if arxiv_match:
        return f"arXiv:{arxiv_match.group(1)}"

    # BioRxiv DOI
    biorxiv_match = re.search(r'biorxiv\.org/content/(10\.\d+/[\d\.v]+)', url)
    if biorxiv_match:
        return biorxiv_match.group(1)

    return None


def get_markdown_path(pub_id: str, markdown_dir: Path) -> Optional[Path]:
    """
    Get the markdown file path for a publication ID.

    Args:
        pub_id: Publication identifier (DOI, PMC, PMID, etc.)
        markdown_dir: Directory containing markdown files

    Returns:
        Path to markdown file or None if not found
    """
    # Convert pub_id to expected filename
    if pub_id.startswith('10.'):
        # DOI: convert to doi_XX_XXXX format
        filename = f"doi_{pub_id.replace('/', '-').replace('.', '_')}.md"
    elif pub_id.startswith('PMC'):
        filename = f"{pub_id}.md"
    elif pub_id.startswith('PMID:'):
        filename = f"{pub_id.replace(':', '_')}.md"
    elif pub_id.startswith('arXiv:'):
        # ArXiv files might be saved with title
        # Search for any file containing the arxiv ID
        arxiv_id = pub_id.replace('arXiv:', '')
        for md_file in markdown_dir.glob('*.md'):
            if arxiv_id.replace('.', '_') in md_file.stem:
                return md_file
        return None
    else:
        return None

    md_path = markdown_dir / filename
    return md_path if md_path.exists() else None


def read_markdown_content(md_path: Path) -> str:
    """
    Read markdown file content.

    Args:
        md_path: Path to markdown file

    Returns:
        Markdown content as string
    """
    try:
        with open(md_path, 'r', encoding='utf-8') as f:
            return f.read()
    except Exception as e:
        print(f"  ⚠️  Error reading {md_path}: {e}")
        return ""


def extract_keywords_from_row(row: pd.Series, sheet_name: str) -> Set[str]:
    """
    Extract searchable keywords from a data row.

    Args:
        row: Pandas Series representing a row
        sheet_name: Name of the sheet (for context-specific extraction)

    Returns:
        Set of keywords to search for in publications
    """
    keywords = set()

    # Convert all string values to lowercase for searching
    for value in row.values:
        if pd.notna(value) and isinstance(value, str):
            # Skip URLs and very short strings
            if len(value) < 3 or value.startswith('http'):
                continue

            # Add the full value
            keywords.add(value.lower())

            # Extract scientific names (e.g., "Methylobacterium extorquens")
            scientific_name_match = re.search(r'\b([A-Z][a-z]+\s+[a-z]+)\b', value)
            if scientific_name_match:
                keywords.add(scientific_name_match.group(1).lower())

            # Extract gene names (e.g., "xoxF", "mxaF")
            gene_matches = re.findall(r'\b([a-z]{3,}[A-Z])\b', value)
            keywords.update([g.lower() for g in gene_matches])

            # Extract chemical formulas (e.g., "Eu3+", "La3+")
            chem_matches = re.findall(r'\b([A-Z][a-z]?\d?\+?)\b', value)
            keywords.update([c.lower() for c in chem_matches])

    return keywords


def is_publication_relevant(
    markdown_content: str,
    keywords: Set[str],
    min_matches: int = 3
) -> Tuple[bool, int]:
    """
    Determine if a publication is relevant based on keyword matching.

    Args:
        markdown_content: Publication content as markdown string
        keywords: Set of keywords to search for
        min_matches: Minimum number of keyword matches required

    Returns:
        Tuple of (is_relevant, match_count)
    """
    content_lower = markdown_content.lower()

    match_count = 0
    for keyword in keywords:
        if keyword in content_lower:
            match_count += 1

    return match_count >= min_matches, match_count


def update_source_column(
    current_source: str,
    pub_id: str
) -> str:
    """
    Update the source column by appending publication ID with '|' delimiter.

    Args:
        current_source: Current source column value
        pub_id: Publication identifier to add

    Returns:
        Updated source string
    """
    if pd.isna(current_source) or current_source == '':
        return pub_id

    # Split by '|' and check if pub_id already exists
    sources = [s.strip() for s in str(current_source).split('|')]
    if pub_id in sources:
        return current_source  # Already exists

    # Append new publication ID
    sources.append(pub_id)
    return '|'.join(sources)


def process_sheet(
    sheet_path: Path,
    publications: pd.DataFrame,
    markdown_dir: Path,
    min_keyword_matches: int = 3,
    dry_run: bool = False
) -> Dict[str, int]:
    """
    Process a single data sheet and update source columns.

    Args:
        sheet_path: Path to TSV sheet
        publications: DataFrame of publications
        markdown_dir: Directory containing markdown files
        min_keyword_matches: Minimum keyword matches for relevance
        dry_run: If True, don't write changes

    Returns:
        Dictionary with statistics
    """
    sheet_name = sheet_path.stem
    print(f"\n{'='*70}")
    print(f"Processing: {sheet_name}")
    print(f"{'='*70}")

    # Read sheet
    try:
        df = pd.read_csv(sheet_path, sep='\t', dtype=str)
    except Exception as e:
        print(f"  ✗ Error reading sheet: {e}")
        return {'rows': 0, 'updated': 0, 'publications_added': 0}

    # Check if sheet has source column
    if 'source' not in df.columns:
        print(f"  ⊙ Skipped: No 'source' column found")
        return {'rows': len(df), 'updated': 0, 'publications_added': 0}

    stats = {
        'rows': len(df),
        'updated': 0,
        'publications_added': 0
    }

    # Process each publication
    for _, pub_row in publications.iterrows():
        pub_url = pub_row['URL']
        pub_title = pub_row.get('Title', 'Unknown')
        pub_id = extract_publication_id(pub_url)

        if not pub_id:
            continue

        # Get markdown file
        md_path = get_markdown_path(pub_id, markdown_dir)
        if not md_path:
            continue

        # Read markdown content
        markdown_content = read_markdown_content(md_path)
        if not markdown_content or len(markdown_content) < 200:
            # Skip placeholder/empty files
            continue

        print(f"\n  Checking publication: {pub_id}")
        print(f"  Title: {pub_title[:80]}...")

        # Check each row in the sheet
        rows_matched = 0
        for idx, row in df.iterrows():
            # Extract keywords from row
            keywords = extract_keywords_from_row(row, sheet_name)

            if not keywords:
                continue

            # Check relevance
            is_relevant, match_count = is_publication_relevant(
                markdown_content,
                keywords,
                min_matches=min_keyword_matches
            )

            if is_relevant:
                rows_matched += 1
                current_source = row['source']
                updated_source = update_source_column(current_source, pub_id)

                if updated_source != current_source:
                    df.at[idx, 'source'] = updated_source
                    stats['updated'] += 1
                    stats['publications_added'] += 1

        if rows_matched > 0:
            print(f"  ✓ Matched {rows_matched} rows (added to {rows_matched} rows)")

    # Write updated sheet
    if stats['updated'] > 0 and not dry_run:
        try:
            df.to_csv(sheet_path, sep='\t', index=False)
            print(f"\n  ✓ Updated {sheet_path.name}")
            print(f"    - {stats['updated']} rows updated")
            print(f"    - {stats['publications_added']} publication references added")
        except Exception as e:
            print(f"  ✗ Error writing sheet: {e}")
    elif stats['updated'] > 0:
        print(f"\n  ⊙ DRY RUN: Would update {stats['updated']} rows")
    else:
        print(f"\n  ⊙ No updates needed")

    return stats


def main():
    parser = argparse.ArgumentParser(
        description='Cross-reference publications with data sheets'
    )
    parser.add_argument(
        '--publications-file',
        type=Path,
        default=Path('data/txt/sheet/BER_CMM_Data_for_AI_publications.tsv'),
        help='Path to publications TSV file'
    )
    parser.add_argument(
        '--markdown-dir',
        type=Path,
        default=Path('data/publications'),
        help='Directory containing markdown files'
    )
    parser.add_argument(
        '--data-dir',
        type=Path,
        default=Path('data/txt/sheet'),
        help='Directory containing data TSV files'
    )
    parser.add_argument(
        '--min-keyword-matches',
        type=int,
        default=3,
        help='Minimum keyword matches for relevance (default: 3)'
    )
    parser.add_argument(
        '--sheets',
        nargs='+',
        help='Specific sheets to process (default: all sheets with source column)'
    )
    parser.add_argument(
        '--dry-run',
        action='store_true',
        help='Show what would be updated without writing changes'
    )

    args = parser.parse_args()

    print("="*70)
    print("PUBLICATION CROSS-REFERENCE EXTENSION")
    print("="*70)
    print(f"Publications file: {args.publications_file}")
    print(f"Markdown directory: {args.markdown_dir}")
    print(f"Data directory: {args.data_dir}")
    print(f"Min keyword matches: {args.min_keyword_matches}")
    if args.dry_run:
        print("MODE: DRY RUN (no changes will be written)")
    print()

    # Read publications
    try:
        publications = pd.read_csv(args.publications_file, sep='\t', dtype=str)
        print(f"Loaded {len(publications)} publications")
    except Exception as e:
        print(f"Error reading publications file: {e}")
        return 1

    # Find sheets to process
    if args.sheets:
        sheet_paths = [args.data_dir / f"BER_CMM_Data_for_AI_{sheet}.tsv"
                      for sheet in args.sheets]
    else:
        # Process all sheets with source column
        sheet_paths = []
        for tsv_file in sorted(args.data_dir.glob('BER_CMM_Data_for_AI_*.tsv')):
            # Skip publications sheet itself
            if 'publications' in tsv_file.stem:
                continue
            sheet_paths.append(tsv_file)

    # Process each sheet
    total_stats = {
        'rows': 0,
        'updated': 0,
        'publications_added': 0,
        'sheets_processed': 0
    }

    for sheet_path in sheet_paths:
        if not sheet_path.exists():
            print(f"⚠️  Sheet not found: {sheet_path}")
            continue

        stats = process_sheet(
            sheet_path,
            publications,
            args.markdown_dir,
            min_keyword_matches=args.min_keyword_matches,
            dry_run=args.dry_run
        )

        total_stats['rows'] += stats['rows']
        total_stats['updated'] += stats['updated']
        total_stats['publications_added'] += stats['publications_added']
        if stats['updated'] > 0:
            total_stats['sheets_processed'] += 1

    # Print summary
    print("\n" + "="*70)
    print("SUMMARY")
    print("="*70)
    print(f"Total rows processed: {total_stats['rows']}")
    print(f"Sheets with updates: {total_stats['sheets_processed']}")
    print(f"Rows updated: {total_stats['updated']}")
    print(f"Publication references added: {total_stats['publications_added']}")

    if args.dry_run:
        print("\n⚠️  DRY RUN: No changes were written")
    else:
        print("\n✓ All updates complete")

    return 0


if __name__ == '__main__':
    exit(main())
