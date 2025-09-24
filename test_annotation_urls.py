#!/usr/bin/env python3
"""Test script to verify annotation download URLs are correctly formatted."""

import pandas as pd
import requests
from urllib.parse import urlparse
from cmm_ai.ncbi_search import get_annotation_download_url


def test_url_format():
    """Test URL generation for different assembly accession formats."""
    
    test_cases = [
        ("GCF_000333655.1", "ftp://ftp.ncbi.nlm.nih.gov/genomes/all/GCF/000/333/655"),
        ("GCA_052039795.1", "ftp://ftp.ncbi.nlm.nih.gov/genomes/all/GCA/052/039/795"),
        ("GCF_051554815.1", "ftp://ftp.ncbi.nlm.nih.gov/genomes/all/GCF/051/554/815"),
    ]
    
    print("Testing URL generation...")
    for accession, expected_base in test_cases:
        url = get_annotation_download_url(accession)
        print(f"  {accession} -> {url}")
        
        if expected_base in url:
            print(f"    ✓ Correct base path")
        else:
            print(f"    ✗ Incorrect base path")
        
        if "_genomic.gff.gz" in url:
            print(f"    ✓ Correct file extension")
        else:
            print(f"    ✗ Missing genomic.gff.gz")
        print()


def check_sample_urls():
    """Check a few sample URLs from the extended table."""
    
    print("Checking sample URLs from extended table...")
    
    df = pd.read_csv("data/txt/sheet/BER_CMM_Data_for_AI_taxa_and_genomes_extended.tsv", sep='\t')
    
    # Get first 3 entries with URLs
    sample_entries = df[df["Annotation download URL"].notna() & (df["Annotation download URL"] != "")].head(3)
    
    for idx, row in sample_entries.iterrows():
        organism = row["Scientific name"]
        genome_id = row["Genome identifier (GenBank, IMG etc)"]
        url = row["Annotation download URL"]
        
        print(f"Organism: {organism}")
        print(f"Genome ID: {genome_id}")
        print(f"URL: {url}")
        
        # Parse URL to check format
        parsed = urlparse(url)
        if parsed.scheme == "ftp" and "ftp.ncbi.nlm.nih.gov" in parsed.netloc:
            print("    ✓ Valid NCBI FTP URL")
        else:
            print("    ✗ Invalid URL format")
            
        if genome_id in url:
            print("    ✓ Genome ID present in URL")
        else:
            print("    ✗ Genome ID missing from URL")
            
        print()


def create_usage_examples():
    """Create example commands for downloading annotations."""
    
    print("Example usage for downloading genome annotations:")
    print("=" * 60)
    
    df = pd.read_csv("data/txt/sheet/BER_CMM_Data_for_AI_taxa_and_genomes_extended.tsv", sep='\t')
    
    # Get first entry with URL
    sample = df[df["Annotation download URL"].notna() & (df["Annotation download URL"] != "")].iloc[0]
    
    organism = sample["Scientific name"]
    genome_id = sample["Genome identifier (GenBank, IMG etc)"]
    url = sample["Annotation download URL"]
    
    # Convert wildcard URL to specific directory for browsing
    base_url = url.split("*")[0].rstrip("/")
    
    print(f"Example for: {organism}")
    print(f"Genome ID: {genome_id}")
    print()
    print("1. Browse the FTP directory:")
    print(f"   {base_url}/")
    print()
    print("2. Look for files ending in '_genomic.gff.gz'")
    print()
    print("3. Download using wget or curl:")
    print(f"   wget {base_url}/{genome_id}_*_genomic.gff.gz")
    print(f"   # or")
    print(f"   curl -O {base_url}/{genome_id}_*_genomic.gff.gz")
    print()
    print("4. The GFF3 file contains genome annotations including:")
    print("   - Gene locations and features")
    print("   - Protein coding sequences")
    print("   - Functional annotations")
    print("   - Regulatory elements")
    

def main():
    """Main test function."""
    print("Testing genome annotation URL functionality")
    print("=" * 60)
    
    test_url_format()
    print()
    
    check_sample_urls()
    print()
    
    create_usage_examples()


if __name__ == "__main__":
    main()