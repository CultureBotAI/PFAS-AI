#!/usr/bin/env python3
"""
Fix validation issues automatically.

Categories of fixes:
1. CHEBI IDs with duplicate prefix (CHEBI:CHEBI:12345 → CHEBI:12345)
2. PubChem IDs stored as floats (165668.0 → 165668)
3. Publication DOIs without URL prefix (10.1111/... → https://doi.org/10.1111/...)
4. Truncated FTP URLs (wildcard patterns → proper URLs)
"""

import argparse
import pandas as pd
from pathlib import Path
import re


def fix_chebi_ids(df: pd.DataFrame, column: str) -> int:
    """Fix CHEBI IDs with duplicate prefix."""
    if column not in df.columns:
        return 0
    
    fixed_count = 0
    for idx, value in df[column].items():
        if pd.isna(value):
            continue
        
        value_str = str(value)
        # Fix duplicate CHEBI: prefix
        if value_str.startswith("CHEBI:CHEBI:"):
            fixed = value_str.replace("CHEBI:CHEBI:", "CHEBI:", 1)
            df.at[idx, column] = fixed
            fixed_count += 1
    
    return fixed_count


def fix_pubchem_ids(df: pd.DataFrame, column: str) -> int:
    """Fix PubChem IDs stored as floats."""
    if column not in df.columns:
        return 0

    fixed_count = 0
    for idx, value in df[column].items():
        if pd.isna(value):
            continue

        # Convert float to integer string
        if isinstance(value, float):
            df.at[idx, column] = str(int(value))
            fixed_count += 1
        elif isinstance(value, str) and value.endswith('.0'):
            df.at[idx, column] = value.replace('.0', '')
            fixed_count += 1

    # Explicitly convert column to string dtype to prevent pandas from auto-converting
    if fixed_count > 0:
        df[column] = df[column].astype(str).replace('nan', '')

    return fixed_count


def fix_publication_urls(df: pd.DataFrame, url_column: str) -> int:
    """Fix publication DOIs without URL prefix."""
    if url_column not in df.columns:
        return 0
    
    fixed_count = 0
    for idx, value in df[url_column].items():
        if pd.isna(value):
            continue
        
        value_str = str(value).strip()
        
        # Check if it's a DOI without URL prefix
        if re.match(r'^10\.\d{4,}/', value_str) and not value_str.startswith('http'):
            df.at[idx, url_column] = f"https://doi.org/{value_str}"
            fixed_count += 1
    
    return fixed_count


def fix_ftp_urls(df: pd.DataFrame, url_column: str) -> int:
    """Fix truncated FTP URLs with wildcard patterns."""
    if url_column not in df.columns:
        return 0
    
    fixed_count = 0
    for idx, value in df[url_column].items():
        if pd.isna(value):
            continue
        
        value_str = str(value)
        
        # Check if URL is truncated (ends with .g instead of .gff.gz or .gbff.gz)
        if 'ftp://ftp.ncbi.nlm.nih.gov' in value_str and value_str.endswith('.g'):
            # Likely truncated, mark for review but don't auto-fix
            # These need assembly accession to reconstruct properly
            continue
    
    return fixed_count


def fix_chemicals_table(input_file: str, output_file: str) -> dict:
    """Fix validation issues in chemicals table."""
    print("\n" + "=" * 80)
    print("Fixing Chemicals Table")
    print("=" * 80)
    
    df = pd.read_csv(input_file, sep='\t')
    print(f"Loaded {len(df)} chemical records")
    
    fixes = {
        'chebi_ids': 0,
        'pubchem_ids': 0
    }
    
    # Fix CHEBI IDs
    fixes['chebi_ids'] = fix_chebi_ids(df, 'chebi_id')
    
    # Fix PubChem IDs
    fixes['pubchem_ids'] = fix_pubchem_ids(df, 'pubchem_id')
    
    # Save
    df.to_csv(output_file, sep='\t', index=False)
    
    print(f"✓ Fixed {fixes['chebi_ids']} CHEBI IDs")
    print(f"✓ Fixed {fixes['pubchem_ids']} PubChem IDs")
    print(f"✓ Saved to {output_file}")
    
    return fixes


def fix_publications_table(input_file: str, output_file: str) -> dict:
    """Fix validation issues in publications table."""
    print("\n" + "=" * 80)
    print("Fixing Publications Table")
    print("=" * 80)

    df = pd.read_csv(input_file, sep='\t')
    print(f"Loaded {len(df)} publication records")

    fixes = {
        'urls': 0
    }

    # Fix DOI URLs in all URL columns
    fixes['urls'] = fix_publication_urls(df, 'url')
    fixes['urls'] += fix_publication_urls(df, 'URL')
    fixes['urls'] += fix_publication_urls(df, 'Download URL')

    # Save
    df.to_csv(output_file, sep='\t', index=False)

    print(f"✓ Fixed {fixes['urls']} publication URLs")
    print(f"✓ Saved to {output_file}")

    return fixes


def fix_genomes_table(input_file: str, output_file: str) -> dict:
    """Fix validation issues in genomes table."""
    print("\n" + "=" * 80)
    print("Fixing Genomes Table")
    print("=" * 80)
    
    df = pd.read_csv(input_file, sep='\t')
    print(f"Loaded {len(df)} genome records")
    
    fixes = {
        'ftp_urls': 0
    }
    
    # Note: FTP URL fixes require assembly accessions - marking for manual review
    truncated_count = 0
    for idx, row in df.iterrows():
        url = row.get('Annotation download URL', '')
        if pd.notna(url) and str(url).endswith('.g'):
            truncated_count += 1
    
    if truncated_count > 0:
        print(f"⚠️  Found {truncated_count} truncated FTP URLs")
        print(f"   These need assembly accessions to reconstruct properly")
        print(f"   Consider running: make update-genomes")
    
    # Save (no automatic fixes for now)
    df.to_csv(output_file, sep='\t', index=False)
    
    print(f"✓ Analyzed genome URLs")
    print(f"✓ Saved to {output_file}")
    
    return fixes


def add_missing_organisms(data_dir: Path) -> int:
    """Add missing organism references to genomes table.

    Args:
        data_dir: Directory containing TSV files

    Returns:
        Number of organisms added
    """
    print("\n" + "=" * 80)
    print("Adding Missing Organisms")
    print("=" * 80)

    # Import the function from add_missing_organisms module
    try:
        from add_missing_organisms import add_missing_organisms_to_genomes

        genes_file = data_dir / "BER_CMM_Data_for_AI_genes_and_proteins_extended.tsv"
        genomes_file = data_dir / "BER_CMM_Data_for_AI_taxa_and_genomes_extended.tsv"

        if not genes_file.exists() or not genomes_file.exists():
            print("⚠️  Extended files not found, skipping organism additions")
            return 0

        added_count = add_missing_organisms_to_genomes(
            str(genes_file),
            str(genomes_file)
        )

        return added_count

    except Exception as e:
        print(f"❌ Error adding organisms: {e}")
        return 0


def main():
    """Command-line interface."""
    parser = argparse.ArgumentParser(
        description="Automatically fix validation issues",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Fix all tables
  python src/fix_validation_issues.py --all

  # Fix specific table
  python src/fix_validation_issues.py --table chemicals

Fixes applied:
  - CHEBI IDs: CHEBI:CHEBI:12345 → CHEBI:12345
  - PubChem IDs: 165668.0 → 165668
  - Publication URLs: 10.1111/... → https://doi.org/10.1111/...
  - Missing organisms: Queries NCBI to add organisms from genes table
"""
    )

    parser.add_argument(
        "--add-organisms",
        action="store_true",
        help="Add missing organism references from genes table"
    )

    parser.add_argument(
        "--table",
        choices=["chemicals", "publications", "genomes"],
        help="Specific table to fix"
    )
    parser.add_argument(
        "--all",
        action="store_true",
        help="Fix all tables"
    )
    parser.add_argument(
        "--data-dir",
        default="data/txt/sheet",
        help="Data directory (default: data/txt/sheet)"
    )

    args = parser.parse_args()

    data_dir = Path(args.data_dir)

    if not args.all and not args.table:
        parser.error("Must specify either --table or --all")

    # Define table operations
    # Process both original and extended files
    tables = {
        "chemicals": {
            "input": data_dir / "BER_CMM_Data_for_AI_chemicals.tsv",
            "output": data_dir / "BER_CMM_Data_for_AI_chemicals.tsv",
            "func": fix_chemicals_table
        },
        "chemicals_extended": {
            "input": data_dir / "BER_CMM_Data_for_AI_chemicals_extended.tsv",
            "output": data_dir / "BER_CMM_Data_for_AI_chemicals_extended.tsv",
            "func": fix_chemicals_table
        },
        "publications": {
            "input": data_dir / "BER_CMM_Data_for_AI_publications.tsv",
            "output": data_dir / "BER_CMM_Data_for_AI_publications.tsv",
            "func": fix_publications_table
        },
        "publications_extended": {
            "input": data_dir / "BER_CMM_Data_for_AI_publications_extended.tsv",
            "output": data_dir / "BER_CMM_Data_for_AI_publications_extended.tsv",
            "func": fix_publications_table
        },
        "genomes": {
            "input": data_dir / "BER_CMM_Data_for_AI_taxa_and_genomes.tsv",
            "output": data_dir / "BER_CMM_Data_for_AI_taxa_and_genomes.tsv",
            "func": fix_genomes_table
        },
        "genomes_extended": {
            "input": data_dir / "BER_CMM_Data_for_AI_taxa_and_genomes_extended.tsv",
            "output": data_dir / "BER_CMM_Data_for_AI_taxa_and_genomes_extended.tsv",
            "func": fix_genomes_table
        }
    }

    # Determine which tables to process
    if args.all:
        tables_to_process = tables.keys()
    else:
        tables_to_process = [args.table]

    print("=" * 80)
    print("AUTOMATED VALIDATION FIXES")
    print("=" * 80)
    print(f"Data directory: {data_dir}")
    print(f"Tables to fix: {', '.join(tables_to_process)}")
    print("=" * 80)

    # Track total fixes
    total_fixes = {}

    # Process tables
    for table_name in tables_to_process:
        table_info = tables[table_name]
        
        # Check if input file exists
        if not table_info["input"].exists():
            print(f"\n⚠️  Skipping {table_name}: file not found")
            continue
        
        # Run fix function
        try:
            fixes = table_info["func"](
                str(table_info["input"]),
                str(table_info["output"])
            )
            
            # Accumulate fixes
            for fix_type, count in fixes.items():
                total_fixes[fix_type] = total_fixes.get(fix_type, 0) + count
                
        except Exception as e:
            print(f"\n❌ Error fixing {table_name}: {e}")
            import traceback
            traceback.print_exc()

    # Add missing organisms if requested
    organisms_added = 0
    if args.add_organisms:
        organisms_added = add_missing_organisms(data_dir)
        if organisms_added > 0:
            total_fixes["organisms_added"] = organisms_added

    print("\n" + "=" * 80)
    print("✓ VALIDATION FIXES COMPLETE")
    print("=" * 80)

    if total_fixes:
        print("\nTotal fixes applied:")
        for fix_type, count in total_fixes.items():
            print(f"  • {fix_type}: {count}")
    else:
        print("\n✓ No fixes needed")

    print("\nRecommended next steps:")
    print("  1. Run validation again: make validate-consistency")
    print("  2. Review any remaining warnings")
    if organisms_added > 0:
        print("  3. Run crosslink to update gene-genome references: make crosslink")
    print("  3. Manual fixes may be needed for:")
    print("     - Truncated FTP URLs (run: make update-genomes)")
    if not args.add_organisms:
        print("     - Missing organism references (run: python src/fix_validation_issues.py --all --add-organisms)")
    print("     - Missing protocol references")


if __name__ == "__main__":
    main()
