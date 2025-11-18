#!/usr/bin/env python3
"""Download PDFs from publication URLs in the publications TSV file.

This script reads the publications table and downloads PDFs from URLs,
handling different sources like PMC, direct PDFs, and DOI links.
"""

import argparse
import re
import time
from pathlib import Path
from typing import Optional
from urllib.parse import urlparse

import pandas as pd
import requests


def sanitize_filename(url: str, title: Optional[str] = None) -> str:
    """Generate safe filename from URL or title.

    Args:
        url: Publication URL
        title: Optional title to use for filename

    Returns:
        Sanitized filename (without .pdf extension)
    """
    # Try to extract identifier from URL
    # PMC format: https://pmc.ncbi.nlm.nih.gov/articles/PMC9301485/
    pmc_match = re.search(r'PMC(\d+)', url)
    if pmc_match:
        return f"PMC{pmc_match.group(1)}"

    # DOI format: https://doi.org/10.1038/nature16174
    doi_match = re.search(r'10\.\d+/[\w\-\.]+', url)
    if doi_match:
        doi = doi_match.group(0).replace('/', '-').replace('.', '_')
        return f"doi_{doi}"

    # PubMed format: https://pubmed.ncbi.nlm.nih.gov/12345678/
    pubmed_match = re.search(r'pubmed\.ncbi\.nlm\.nih\.gov/(\d+)', url)
    if pubmed_match:
        return f"PMID_{pubmed_match.group(1)}"

    # Fallback to title-based filename
    if title:
        # Sanitize title for filename
        safe_title = re.sub(r'[^\w\s\-]', '', title)
        safe_title = re.sub(r'\s+', '_', safe_title)
        return safe_title[:50]  # Limit length

    # Last resort: use domain and hash
    parsed = urlparse(url)
    return f"{parsed.netloc}_{hash(url) % 10000}"


def convert_pmc_to_pdf_url(pmc_url: str) -> Optional[str]:
    """Convert PMC article URL to PDF download URL.

    Args:
        pmc_url: PMC article URL

    Returns:
        PDF download URL or None if not PMC
    """
    # PMC URL format: https://pmc.ncbi.nlm.nih.gov/articles/PMC9301485/
    pmc_match = re.search(r'PMC(\d+)', pmc_url)
    if pmc_match:
        pmc_id = pmc_match.group(1)
        return f"https://www.ncbi.nlm.nih.gov/pmc/articles/PMC{pmc_id}/pdf/"
    return None


def download_pdf(url: str, output_path: Path, timeout: int = 30) -> bool:
    """Download PDF from URL.

    Args:
        url: URL to download from
        output_path: Path to save PDF
        timeout: Request timeout in seconds

    Returns:
        True if successful, False otherwise
    """
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
        }

        response = requests.get(url, headers=headers, timeout=timeout, stream=True)
        response.raise_for_status()

        # Check if response is actually a PDF
        content_type = response.headers.get('content-type', '').lower()
        if 'pdf' not in content_type and not url.endswith('.pdf'):
            print(f"  ⚠️  Warning: Content type is '{content_type}', may not be PDF")

        # Write to file
        with open(output_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)

        # Verify file was created and has content
        if output_path.exists() and output_path.stat().st_size > 0:
            size_kb = output_path.stat().st_size / 1024
            print(f"  ✓ Downloaded: {output_path.name} ({size_kb:.1f} KB)")
            return True
        else:
            print(f"  ✗ Failed: File is empty")
            if output_path.exists():
                output_path.unlink()
            return False

    except requests.exceptions.RequestException as e:
        print(f"  ✗ Error downloading: {e}")
        return False
    except Exception as e:
        print(f"  ✗ Unexpected error: {e}")
        return False


def download_pdfs_from_publications(
    publications_file: str,
    output_dir: str = "data/publications",
    skip_existing: bool = True,
    delay: float = 1.0
) -> None:
    """Download PDFs from publications table.

    Args:
        publications_file: Path to publications TSV file
        output_dir: Directory to save PDFs
        skip_existing: Skip files that already exist
        delay: Delay between downloads (seconds)
    """
    publications_file = Path(publications_file)
    output_dir = Path(output_dir)

    if not publications_file.exists():
        print(f"Error: Publications file not found: {publications_file}")
        return

    output_dir.mkdir(parents=True, exist_ok=True)

    # Read publications table
    print(f"Reading publications from: {publications_file}")
    df = pd.read_csv(publications_file, sep='\t', dtype=str, keep_default_na=False)

    # Find URL column (case-insensitive)
    url_col = None
    title_col = None
    for col in df.columns:
        if col.lower() == 'url':
            url_col = col
        elif col.lower() == 'title':
            title_col = col

    if url_col is None:
        print(f"Error: No 'URL' column found in publications table")
        print(f"Available columns: {list(df.columns)}")
        return

    print(f"Found {len(df)} publications")
    print(f"Output directory: {output_dir}")
    print(f"Skip existing: {skip_existing}")
    print()

    downloaded = 0
    skipped = 0
    failed = 0

    for idx, row in df.iterrows():
        url = row[url_col]
        title = row.get(title_col, '') if title_col else ''

        if not url or pd.isna(url) or url.strip() == '':
            print(f"[{idx+1}/{len(df)}] Skipping: No URL")
            skipped += 1
            continue

        print(f"[{idx+1}/{len(df)}] Processing: {url}")

        # Generate filename
        filename = sanitize_filename(url, title)
        output_path = output_dir / f"{filename}.pdf"

        # Check if already exists
        if skip_existing and output_path.exists():
            size_kb = output_path.stat().st_size / 1024
            print(f"  ⊙ Exists: {output_path.name} ({size_kb:.1f} KB)")
            skipped += 1
            continue

        # Try to convert PMC URL to PDF
        pdf_url = convert_pmc_to_pdf_url(url)
        if pdf_url:
            print(f"  → Converted to PDF URL: {pdf_url}")
            url = pdf_url

        # Download PDF
        if download_pdf(url, output_path):
            downloaded += 1
        else:
            failed += 1
            # Try alternative: append /pdf to URL if it's PMC
            if 'pmc.ncbi.nlm.nih.gov' in url and not url.endswith('/pdf/'):
                alt_url = url.rstrip('/') + '/pdf/'
                print(f"  → Trying alternative URL: {alt_url}")
                if download_pdf(alt_url, output_path):
                    downloaded += 1
                    failed -= 1

        # Rate limiting
        if idx < len(df) - 1:
            time.sleep(delay)

    print()
    print("=" * 60)
    print("DOWNLOAD SUMMARY")
    print("=" * 60)
    print(f"Total publications: {len(df)}")
    print(f"  ✓ Downloaded: {downloaded}")
    print(f"  ⊙ Skipped (existing): {skipped}")
    print(f"  ✗ Failed: {failed}")
    print()

    if failed > 0:
        print("Note: Some downloads failed. This may be due to:")
        print("  - Paywalled content (subscription required)")
        print("  - Non-PDF URLs (HTML articles)")
        print("  - Broken or moved links")
        print("  - Network connectivity issues")
        print()
        print("You may need to manually download failed PDFs.")


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Download PDFs from publications table"
    )
    parser.add_argument(
        '--publications-file',
        type=str,
        default='data/txt/sheet/PFAS_Data_for_AI_publications.tsv',
        help='Path to publications TSV file'
    )
    parser.add_argument(
        '--output-dir',
        type=str,
        default='data/publications',
        help='Directory to save PDFs'
    )
    parser.add_argument(
        '--no-skip-existing',
        action='store_true',
        help='Re-download existing files'
    )
    parser.add_argument(
        '--delay',
        type=float,
        default=1.0,
        help='Delay between downloads in seconds (default: 1.0)'
    )

    args = parser.parse_args()

    download_pdfs_from_publications(
        publications_file=args.publications_file,
        output_dir=args.output_dir,
        skip_existing=not args.no_skip_existing,
        delay=args.delay
    )


if __name__ == "__main__":
    main()
