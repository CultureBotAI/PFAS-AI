#!/usr/bin/env python3
"""
Generate a comprehensive markdown report of missing publication PDFs.

This script analyzes the publications TSV and creates a detailed markdown report
of which PDFs are missing, organized by publisher.

Usage:
    python src/generate_missing_pdfs_report.py
    python src/generate_missing_pdfs_report.py --output MISSING_PUBLICATION_PDFS.md
"""

import argparse
import sys
from pathlib import Path
from datetime import datetime
import pandas as pd
import re
from typing import Dict, List, Tuple
from collections import defaultdict


def extract_pdf_identifier(url: str) -> str:
    """Extract a potential PDF identifier from a URL."""
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
        doi_clean = doi.replace('/', '-').replace('.', '_')
        return f"doi_{doi_clean}"

    return "unknown"


def categorize_publisher(url: str) -> str:
    """Categorize publication by publisher based on URL."""
    if not url or pd.isna(url):
        return "Invalid/Missing URL"

    url_lower = url.lower()

    # Nature Publishing Group
    if 'nature.com' in url_lower or 'doi.org/10.1038' in url_lower:
        return "Nature Publishing Group"

    # American Chemical Society
    if 'acs.org' in url_lower or 'doi.org/10.1021' in url_lower:
        return "American Chemical Society (ACS)"

    # American Society for Microbiology
    if 'doi.org/10.1128' in url_lower:
        return "American Society for Microbiology (ASM)"

    # Wiley
    if 'wiley.com' in url_lower or 'doi.org/10.1111' in url_lower or 'doi.org/10.1002' in url_lower:
        return "Wiley Publishers"

    # PLOS
    if 'plos' in url_lower or 'doi.org/10.1371/journal' in url_lower:
        return "PLOS (Public Library of Science)"

    # Microbiology Society
    if 'doi.org/10.1099' in url_lower:
        return "Microbiology Society (IJSEM)"

    # Elsevier
    if 'elsevier' in url_lower or 'doi.org/10.1016' in url_lower:
        return "Elsevier Journals"

    # Oxford
    if 'oxford' in url_lower or 'doi.org/10.1093' in url_lower:
        return "Oxford Academic"

    # Springer
    if 'springer' in url_lower or 'doi.org/10.1007' in url_lower:
        return "Springer Journals"

    # Royal Society of Chemistry
    if 'rsc.org' in url_lower or 'doi.org/10.1039' in url_lower:
        return "Royal Society of Chemistry"

    # JBC
    if 'doi.org/10.1074' in url_lower:
        return "Journal of Biological Chemistry"

    # Portland Press
    if 'doi.org/10.1042' in url_lower:
        return "Portland Press / Biochemical Journal"

    # Mary Ann Liebert
    if 'doi.org/10.1089' in url_lower:
        return "Mary Ann Liebert Publishers"

    # JSME
    if 'doi.org/10.1264' in url_lower:
        return "Japanese Society of Microbial Ecology"

    # Wiley other
    if 'doi.org/10.1046' in url_lower:
        return "Wiley Publishers"

    # Research Square
    if 'researchsquare' in url_lower or 'doi.org/10.21203' in url_lower:
        return "Research Square Preprints"

    # arXiv
    if 'arxiv.org' in url_lower:
        return "arXiv Preprints"

    # bioRxiv
    if 'biorxiv.org' in url_lower:
        return "bioRxiv Preprints"

    # PubMed
    if 'pubmed.ncbi.nlm.nih.gov' in url_lower:
        return "PubMed/NCBI (Abstract Links)"

    return "Other Publishers"


def generate_markdown_report(publications_file: Path, pdf_dir: Path, output_file: Path):
    """Generate comprehensive markdown report of missing PDFs."""

    # Read publications
    df = pd.read_csv(publications_file, sep='\t')

    # Get available PDFs
    pdfs_on_disk = {p.stem for p in pdf_dir.glob("*.pdf")}

    # Analyze missing PDFs
    missing_pubs = []
    available_count = 0

    for idx, row in df.iterrows():
        url = row.get('URL', '')
        title = row.get('Title', '')

        identifier = extract_pdf_identifier(url)

        if identifier and identifier in pdfs_on_disk:
            available_count += 1
        else:
            publisher = categorize_publisher(url)
            missing_pubs.append({
                'identifier': identifier,
                'title': title,
                'url': url,
                'publisher': publisher
            })

    # Group by publisher
    by_publisher = defaultdict(list)
    for pub in missing_pubs:
        by_publisher[pub['publisher']].append(pub)

    # Sort publishers by count
    sorted_publishers = sorted(by_publisher.items(), key=lambda x: len(x[1]), reverse=True)

    # Generate markdown
    lines = []
    lines.append("# Missing Publication PDFs - Complete List\n")
    lines.append(f"**Total Publications in TSV:** {len(df)}")
    lines.append(f"**PDFs Available:** {available_count} ({available_count/len(df)*100:.1f}%)")
    lines.append(f"**PDFs Missing:** {len(missing_pubs)} ({len(missing_pubs)/len(df)*100:.1f}%)\n")
    lines.append(f"Generated: {datetime.now().strftime('%Y-%m-%d')}\n")
    lines.append("---\n")

    # Add publications by publisher
    pub_num = 1
    for publisher, pubs in sorted_publishers:
        lines.append(f"## {publisher} ({len(pubs)} publications)\n")

        for pub in pubs:
            lines.append(f"{pub_num}. {pub['url']}")
            if pub['title']:
                # Truncate long titles
                title_display = pub['title'][:100] + "..." if len(pub['title']) > 100 else pub['title']
                lines.append(f"   - *{title_display}*")
            lines.append("")
            pub_num += 1

        lines.append("---\n")

    # Add summary table
    lines.append("## Summary by Publisher\n")
    lines.append("| Publisher | Count | Percentage |")
    lines.append("|-----------|-------|------------|")
    for publisher, pubs in sorted_publishers:
        pct = len(pubs) / len(missing_pubs) * 100
        lines.append(f"| {publisher} | {len(pubs)} | {pct:.1f}% |")
    lines.append("")

    # Add recommendations
    lines.append("---\n")
    lines.append("## Recommended Actions\n")
    lines.append("### For Institutional Access:")
    lines.append("- Use university library VPN/proxy to download from paywalled sources")
    lines.append("- Check if institution has subscriptions to major publishers\n")
    lines.append("### For Open Access Alternatives:")
    lines.append("1. **Check PubMed Central (PMC)** for open access versions")
    lines.append("2. **Use Unpaywall** browser extension to find legal free versions")
    lines.append("3. **Search Google Scholar** for author preprints")
    lines.append("4. **Check ResearchGate/Academia.edu** for author-uploaded copies")
    lines.append("5. **Contact authors directly** via email (most will share PDFs)\n")
    lines.append("### For Preprints:")
    lines.append("- arXiv and bioRxiv links need special download scripts")
    lines.append("- Current URLs point to abstract pages, not PDF downloads\n")
    lines.append("### For PubMed Links:")
    lines.append("- These link to abstracts only")
    lines.append("- Full text PDFs are usually on publisher sites")
    lines.append("- Some may be available in PMC (free access)\n")
    lines.append("---\n")
    lines.append(f"*Generated by: src/generate_missing_pdfs_report.py*  ")
    lines.append(f"*Repository: CMM-AI*  ")
    lines.append(f"*Last Updated: {datetime.now().strftime('%Y-%m-%d')}*\n")

    # Write to file
    output_file.write_text('\n'.join(lines))

    print(f"✓ Report generated: {output_file}")
    print(f"  Total publications: {len(df)}")
    print(f"  PDFs available: {available_count} ({available_count/len(df)*100:.1f}%)")
    print(f"  PDFs missing: {len(missing_pubs)} ({len(missing_pubs)/len(df)*100:.1f}%)")
    print(f"  Publishers identified: {len(sorted_publishers)}")


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Generate markdown report of missing publication PDFs",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )

    parser.add_argument(
        '--publications-file',
        type=Path,
        default=Path('data/txt/sheet/BER_CMM_Data_for_AI_publications.tsv'),
        help='Path to publications TSV file'
    )

    parser.add_argument(
        '--pdf-dir',
        type=Path,
        default=Path('data/publications'),
        help='Directory containing PDFs'
    )

    parser.add_argument(
        '--output',
        type=Path,
        default=Path('MISSING_PUBLICATION_PDFS.md'),
        help='Output markdown file (default: MISSING_PUBLICATION_PDFS.md)'
    )

    args = parser.parse_args()

    # Check files exist
    if not args.publications_file.exists():
        print(f"✗ Publications file not found: {args.publications_file}", file=sys.stderr)
        sys.exit(1)

    if not args.pdf_dir.exists():
        print(f"✗ PDF directory not found: {args.pdf_dir}", file=sys.stderr)
        sys.exit(1)

    try:
        generate_markdown_report(args.publications_file, args.pdf_dir, args.output)
        sys.exit(0)

    except Exception as e:
        print(f"\n✗ Error: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        sys.exit(2)


if __name__ == "__main__":
    main()
