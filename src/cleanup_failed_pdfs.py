#!/usr/bin/env python3
"""Identify and clean up failed PDF downloads (HTML error pages, paywalls, etc.)."""

import os
from pathlib import Path


def identify_failed_pdfs(pdf_dir: str = "data/publications", size_threshold: int = 5000) -> None:
    """Identify PDFs that are likely HTML error pages or paywalls.

    Args:
        pdf_dir: Directory containing PDFs
        size_threshold: Files smaller than this (in bytes) are likely failed downloads
    """
    pdf_dir = Path(pdf_dir)

    if not pdf_dir.exists():
        print(f"Error: Directory not found: {pdf_dir}")
        return

    print("Scanning for failed PDF downloads...")
    print(f"Directory: {pdf_dir}")
    print(f"Size threshold: {size_threshold} bytes")
    print()

    failed_pdfs = []
    html_errors = []
    successful = []

    for pdf_path in sorted(pdf_dir.glob("*.pdf")):
        size = pdf_path.stat().st_size

        # Check if it's HTML (common for error pages)
        with open(pdf_path, 'rb') as f:
            header = f.read(min(100, size))

        is_html = b'<html' in header.lower() or b'<!doctype' in header.lower()

        if is_html:
            html_errors.append((pdf_path, size))
            failed_pdfs.append(pdf_path)
        elif size < size_threshold:
            failed_pdfs.append((pdf_path, size))
        else:
            successful.append((pdf_path, size))

    print("=" * 80)
    print("SCAN RESULTS")
    print("=" * 80)
    print()

    if html_errors:
        print(f"HTML ERROR PAGES ({len(html_errors)} files):")
        for pdf_path, size in html_errors:
            print(f"  {pdf_path.name} ({size} bytes)")
        print()

    if failed_pdfs:
        print(f"FAILED/INCOMPLETE DOWNLOADS ({len(failed_pdfs)} files < {size_threshold} bytes):")
        for item in failed_pdfs:
            if isinstance(item, tuple):
                pdf_path, size = item
                print(f"  {pdf_path.name} ({size} bytes)")
            else:
                print(f"  {item.name} (HTML error)")
        print()

    if successful:
        print(f"SUCCESSFUL DOWNLOADS ({len(successful)} files >= {size_threshold} bytes):")
        for pdf_path, size in successful[:10]:  # Show first 10
            print(f"  {pdf_path.name} ({size:,} bytes)")
        if len(successful) > 10:
            print(f"  ... and {len(successful) - 10} more")
        print()

    print("=" * 80)
    print("SUMMARY")
    print("=" * 80)
    print(f"Total PDF files: {len(list(pdf_dir.glob('*.pdf')))}")
    print(f"  ✓ Successful: {len(successful)}")
    print(f"  ✗ Failed: {len(failed_pdfs)}")
    print(f"    - HTML errors: {len(html_errors)}")
    print(f"    - Too small: {len([f for f in failed_pdfs if isinstance(f, tuple)])}")
    print()

    # Suggestions
    print("=" * 80)
    print("RECOMMENDATIONS")
    print("=" * 80)
    print()
    print("Failed PDFs are likely due to:")
    print("  1. PMC/PubMed returning HTML login/error pages instead of PDFs")
    print("  2. Publisher paywalls (Elsevier, ACS, etc.)")
    print("  3. Invalid or moved URLs")
    print()
    print("To improve PDF availability:")
    print("  1. Use institutional access/VPN for paywalled content")
    print("  2. Try alternative sources (arXiv, bioRxiv, author copies)")
    print("  3. Extract data from available open-access PDFs only")
    print("  4. Consider using PubMed Central Open Access subset")
    print()


if __name__ == "__main__":
    identify_failed_pdfs()
