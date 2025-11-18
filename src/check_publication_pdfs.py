#!/usr/bin/env python3
"""
Check which PDFs from the publications TSV are available in data/publications/.

This script:
1. Reads the publications TSV file
2. Checks which PDFs exist in data/publications/
3. Reports which publications have PDFs available
4. Reports which publications are missing PDFs
5. Shows conversion status (PDF → markdown)

Usage:
    python src/check_publication_pdfs.py
    python src/check_publication_pdfs.py --publications-file data/txt/sheet/BER_CMM_Data_for_AI_publications.tsv
"""

import argparse
import sys
from pathlib import Path
from typing import Dict, List, Tuple, Set
import pandas as pd
import re


def extract_pdf_identifier(url: str) -> str:
    """
    Extract a potential PDF identifier from a URL.

    Args:
        url: Publication URL

    Returns:
        Potential PDF filename (without extension)
    """
    if not url or pd.isna(url):
        return ""

    # Extract PMID
    pmid_match = re.search(r'pubmed\.ncbi\.nlm\.nih\.gov/(\d+)', url)
    if pmid_match:
        return f"PMID_{pmid_match.group(1)}"

    # Extract PMC ID
    pmc_match = re.search(r'PMC(\d+)', url)
    if pmc_match:
        return f"PMC{pmc_match.group(1)}"

    # Extract DOI
    doi_match = re.search(r'doi\.org/(.+?)(?:\?|$)', url)
    if doi_match:
        doi = doi_match.group(1)
        # Sanitize DOI for filename
        doi_clean = doi.replace('/', '-').replace('.', '_')
        return f"doi_{doi_clean}"

    return ""


def check_publication_pdfs(publications_file: Path, pdf_dir: Path) -> Dict:
    """
    Check PDF availability for publications.

    Args:
        publications_file: Path to publications TSV
        pdf_dir: Directory containing PDFs

    Returns:
        Dictionary with analysis results
    """
    print("=" * 80)
    print("PUBLICATION PDF AVAILABILITY REPORT")
    print("=" * 80)
    print()

    # Read publications TSV
    print(f"Reading publications from: {publications_file}")
    df = pd.read_csv(publications_file, sep='\t')
    print(f"Total publications in TSV: {len(df)}")
    print()

    # Get all PDFs and markdowns in directory
    pdfs_on_disk = {p.stem: p for p in pdf_dir.glob("*.pdf")}
    mds_on_disk = {p.stem: p for p in pdf_dir.glob("*.md")}

    print(f"PDFs in {pdf_dir.name}/: {len(pdfs_on_disk)}")
    print(f"Markdown files in {pdf_dir.name}/: {len(mds_on_disk)}")
    print()

    # Analyze each publication
    results = {
        'total_pubs': len(df),
        'pdfs_found': 0,
        'pdfs_missing': 0,
        'pdfs_with_md': 0,
        'pdfs_without_md': 0,
        'found_list': [],
        'missing_list': [],
        'md_missing_list': []
    }

    for idx, row in df.iterrows():
        url = row.get('URL', '')
        title = row.get('Title', '')[:80]  # Truncate for display

        # Try to find PDF identifier
        identifier = extract_pdf_identifier(url)

        if identifier and identifier in pdfs_on_disk:
            results['pdfs_found'] += 1
            results['found_list'].append({
                'identifier': identifier,
                'title': title,
                'url': url,
                'pdf_path': pdfs_on_disk[identifier]
            })

            # Check if markdown exists
            if identifier in mds_on_disk:
                results['pdfs_with_md'] += 1
            else:
                results['pdfs_without_md'] += 1
                results['md_missing_list'].append(identifier)
        else:
            results['pdfs_missing'] += 1
            results['missing_list'].append({
                'identifier': identifier if identifier else 'unknown',
                'title': title,
                'url': url
            })

    return results


def print_report(results: Dict):
    """Print formatted report."""

    print("=" * 80)
    print("SUMMARY")
    print("=" * 80)
    print()
    print(f"Total publications in TSV:  {results['total_pubs']}")
    print(f"  ✓ PDFs available:         {results['pdfs_found']} ({results['pdfs_found']/results['total_pubs']*100:.1f}%)")
    print(f"  ✗ PDFs missing:           {results['pdfs_missing']} ({results['pdfs_missing']/results['total_pubs']*100:.1f}%)")
    print()
    print(f"PDF → Markdown conversion:")
    print(f"  ✓ Converted to markdown:  {results['pdfs_with_md']} ({results['pdfs_with_md']/results['pdfs_found']*100:.1f}% of available)" if results['pdfs_found'] > 0 else "  No PDFs to convert")
    print(f"  ✗ Not yet converted:      {results['pdfs_without_md']}")
    print()

    if results['pdfs_without_md'] > 0:
        print("=" * 80)
        print(f"PDFs WITHOUT MARKDOWN ({len(results['md_missing_list'])})")
        print("=" * 80)
        for identifier in results['md_missing_list']:
            print(f"  - {identifier}.pdf")
        print()
        print("Run 'make convert-pdfs-to-markdown' to convert these PDFs")
        print()

    if results['missing_list']:
        print("=" * 80)
        print(f"PUBLICATIONS MISSING PDFs ({len(results['missing_list'])})")
        print("=" * 80)
        print()
        for pub in results['missing_list']:
            print(f"Expected identifier: {pub['identifier']}")
            print(f"  Title: {pub['title']}")
            print(f"  URL: {pub['url']}")
            print()

        print("These publications may need to be downloaded manually.")
        print("Check if the PDFs are behind paywalls or use alternative sources.")
        print()

    print("=" * 80)


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Check PDF availability for publications in TSV file",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )

    parser.add_argument(
        '--publications-file',
        type=Path,
        default=Path('data/txt/sheet/BER_CMM_Data_for_AI_publications.tsv'),
        help='Path to publications TSV file (default: data/txt/sheet/BER_CMM_Data_for_AI_publications.tsv)'
    )

    parser.add_argument(
        '--pdf-dir',
        type=Path,
        default=Path('data/publications'),
        help='Directory containing PDFs (default: data/publications)'
    )

    args = parser.parse_args()

    # Check files exist
    if not args.publications_file.exists():
        print(f"✗ Publications file not found: {args.publications_file}", file=sys.stderr)
        sys.exit(1)

    if not args.pdf_dir.exists():
        print(f"✗ PDF directory not found: {args.pdf_dir}", file=sys.stderr)
        sys.exit(1)

    # Run analysis
    try:
        results = check_publication_pdfs(args.publications_file, args.pdf_dir)
        print_report(results)

        # Exit code: 0 if all PDFs available, 1 if some missing
        sys.exit(0 if results['pdfs_missing'] == 0 else 1)

    except Exception as e:
        print(f"\n✗ Error: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        sys.exit(2)


if __name__ == "__main__":
    main()
