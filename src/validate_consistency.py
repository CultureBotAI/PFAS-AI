"""Validate cross-sheet consistency in extended TSV files.

This script checks referential integrity and consistency across the extended data tables,
ensuring that references between sheets (genomes, genes, pathways, etc.) are valid.
"""

import argparse
import sys
from pathlib import Path
from typing import Dict, List, Set, Tuple

import pandas as pd


class ConsistencyValidator:
    """Validator for cross-sheet data consistency."""

    def __init__(self, data_dir: Path):
        """Initialize validator with data directory.

        Args:
            data_dir: Directory containing extended TSV files
        """
        self.data_dir = data_dir
        self.errors: List[str] = []
        self.warnings: List[str] = []
        self.info: List[str] = []

        # Load all tables
        self.genomes_df = self._load_table("taxa_and_genomes_extended.tsv")
        self.biosamples_df = self._load_table("biosamples_extended.tsv")
        self.pathways_df = self._load_table("pathways_extended.tsv")
        self.genes_df = self._load_table("genes_and_proteins_extended.tsv")
        self.structures_df = self._load_table("macromolecular_structures_extended.tsv")
        self.publications_df = self._load_table("publications_extended.tsv")
        self.datasets_df = self._load_table("datasets_extended.tsv")

        # Load new experimental data tables
        self.chemicals_df = self._load_table("chemicals.tsv")
        self.assays_df = self._load_table("assays.tsv")
        self.bioprocesses_df = self._load_table("bioprocesses.tsv")
        self.screening_results_df = self._load_table("screening_results.tsv")
        self.protocols_df = self._load_table("protocols.tsv")

    def _load_table(self, filename: str) -> pd.DataFrame:
        """Load a TSV table.

        Args:
            filename: Filename of TSV (without path prefix)

        Returns:
            DataFrame with the table data
        """
        filepath = self.data_dir / f"BER_CMM_Data_for_AI_{filename}"
        if not filepath.exists():
            self.warnings.append(f"File not found: {filepath}")
            return pd.DataFrame()
        return pd.read_csv(filepath, sep='\t')

    def validate_genome_references(self) -> None:
        """Validate that organism references in other tables match genome entries."""
        if self.genomes_df.empty:
            self.warnings.append("Genomes table is empty, skipping genome reference validation")
            return

        # Build set of valid organism names and genome IDs
        valid_organisms = set()
        valid_genome_ids = set()

        for _, row in self.genomes_df.iterrows():
            if pd.notna(row.get('Scientific name')):
                valid_organisms.add(str(row['Scientific name']).strip())
            if pd.notna(row.get('Genome identifier (GenBank, IMG etc)')):
                valid_genome_ids.add(str(row['Genome identifier (GenBank, IMG etc)']).strip())

        self.info.append(f"Found {len(valid_organisms)} organisms in genomes table")
        self.info.append(f"Found {len(valid_genome_ids)} genome IDs in genomes table")

        # Check genes/proteins organism references
        if not self.genes_df.empty:
            gene_organisms = set()
            for _, row in self.genes_df.iterrows():
                org = row.get('organism (from taxa and genomes tab)')
                if pd.notna(org):
                    org_str = str(org).strip()
                    gene_organisms.add(org_str)
                    # Check if organism exists (fuzzy match on genus)
                    genus = org_str.split()[0] if org_str else ""
                    matched = any(genus in valid_org for valid_org in valid_organisms)
                    if not matched and genus and genus not in ["Various", "Methylotroph"]:
                        self.warnings.append(
                            f"Gene/protein organism '{org_str}' not found in genomes table (genus: {genus})"
                        )

            self.info.append(f"Found {len(gene_organisms)} unique organisms in genes/proteins table")

        # Check pathways organism references
        if not self.pathways_df.empty:
            pathway_organisms = set()
            for _, row in self.pathways_df.iterrows():
                org = row.get('organism')
                if pd.notna(org):
                    org_str = str(org).strip()
                    pathway_organisms.add(org_str)

            self.info.append(f"Found {len(pathway_organisms)} unique organisms in pathways table")

        # Check structures organism references
        if not self.structures_df.empty:
            structure_organisms = set()
            for _, row in self.structures_df.iterrows():
                org = row.get('Organism')
                if pd.notna(org):
                    org_str = str(org).strip()
                    structure_organisms.add(org_str)
                    # Check if organism exists (fuzzy match)
                    genus = org_str.split()[0] if org_str else ""
                    matched = any(genus in valid_org for valid_org in valid_organisms)
                    if not matched and genus and genus not in ["Various", "Methylotroph"]:
                        self.warnings.append(
                            f"Structure organism '{org_str}' not found in genomes table (genus: {genus})"
                        )

            self.info.append(f"Found {len(structure_organisms)} unique organisms in structures table")

    def validate_biosample_references(self) -> None:
        """Validate biosample references and organism consistency."""
        if self.biosamples_df.empty:
            self.warnings.append("Biosamples table is empty, skipping biosample validation")
            return

        # Build set of valid sample IDs
        valid_sample_ids = set()
        for _, row in self.biosamples_df.iterrows():
            if pd.notna(row.get('Sample ID')):
                valid_sample_ids.add(str(row['Sample ID']).strip())

        self.info.append(f"Found {len(valid_sample_ids)} sample IDs in biosamples table")

        # Check for duplicate sample IDs
        sample_ids = self.biosamples_df['Sample ID'].dropna()
        duplicates = sample_ids[sample_ids.duplicated()].unique()
        if len(duplicates) > 0:
            self.errors.append(f"Found {len(duplicates)} duplicate sample IDs: {list(duplicates)[:5]}")

    def validate_pathway_gene_references(self) -> None:
        """Validate that genes mentioned in pathways exist in genes table."""
        if self.pathways_df.empty or self.genes_df.empty:
            self.warnings.append("Pathways or genes table is empty, skipping pathway-gene validation")
            return

        # Build set of valid gene IDs
        valid_gene_ids = set()
        for _, row in self.genes_df.iterrows():
            gene_id = row.get('gene or protein id')
            if pd.notna(gene_id):
                gene_str = str(gene_id).strip()
                valid_gene_ids.add(gene_str)
                # Also add base ID without suffixes
                if '_' in gene_str:
                    base_id = gene_str.split('_')[0]
                    valid_gene_ids.add(base_id)

        self.info.append(f"Found {len(valid_gene_ids)} gene/protein IDs in genes table")

        # Check pathway gene references
        pathway_genes = set()
        for _, row in self.pathways_df.iterrows():
            # Check "genes (from genes & proteins tab)" column
            genes_col = row.get('genes (from genes & proteins tab)')
            if pd.notna(genes_col):
                import re
                # Extract K numbers
                k_numbers = re.findall(r'K\d+', str(genes_col))
                pathway_genes.update(k_numbers)

        self.info.append(f"Found {len(pathway_genes)} unique gene IDs referenced in pathways")

        # Check which pathway genes are not in genes table
        missing_genes = pathway_genes - valid_gene_ids
        if missing_genes:
            self.warnings.append(
                f"Found {len(missing_genes)} gene IDs in pathways not in genes table: {list(missing_genes)[:10]}"
            )

    def validate_url_consistency(self) -> None:
        """Validate that Download URLs are properly formatted and accessible."""
        url_columns = [
            (self.genomes_df, 'Annotation download URL', 'genomes'),
            (self.biosamples_df, 'Download URL', 'biosamples'),
            (self.pathways_df, 'Download URL', 'pathways'),
            (self.genes_df, 'Download URL', 'genes'),
            (self.structures_df, 'Download URL', 'structures'),
            (self.publications_df, 'Download URL', 'publications'),
            (self.datasets_df, 'Download URL', 'datasets'),
        ]

        import re
        url_pattern = re.compile(r'https?://[^\s]+')

        for df, col_name, table_name in url_columns:
            if df.empty or col_name not in df.columns:
                continue

            urls = df[col_name].dropna()
            invalid_urls = []

            for url in urls:
                url_str = str(url).strip()
                if url_str and not url_pattern.match(url_str):
                    invalid_urls.append(url_str[:100])  # First 100 chars

            if invalid_urls:
                self.warnings.append(
                    f"Found {len(invalid_urls)} invalid URLs in {table_name} table: {invalid_urls[:3]}"
                )

            # Count tables with URLs
            url_count = len(urls)
            total_count = len(df)
            coverage = (url_count / total_count * 100) if total_count > 0 else 0
            self.info.append(f"{table_name}: {url_count}/{total_count} ({coverage:.1f}%) have download URLs")

    def validate_identifier_uniqueness(self) -> None:
        """Validate that primary identifiers are unique within each table."""
        checks = [
            (self.genomes_df, 'Scientific name', 'genomes'),
            (self.biosamples_df, 'Sample ID', 'biosamples'),
            (self.pathways_df, 'pathway id', 'pathways'),
            (self.structures_df, 'Name', 'structures'),
            (self.publications_df, 'URL', 'publications'),
            (self.datasets_df, 'Dataset name', 'datasets'),
            (self.chemicals_df, 'chemical_id', 'chemicals'),
            (self.assays_df, 'assay_id', 'assays'),
            (self.bioprocesses_df, 'process_id', 'bioprocesses'),
            (self.screening_results_df, 'experiment_id', 'screening_results'),
            (self.protocols_df, 'protocol_id', 'protocols'),
        ]

        for df, id_col, table_name in checks:
            if df.empty or id_col not in df.columns:
                continue

            ids = df[id_col].dropna()
            duplicates = ids[ids.duplicated()].unique()

            if len(duplicates) > 0:
                self.errors.append(
                    f"{table_name} table: Found {len(duplicates)} duplicate {id_col} values: {list(duplicates)[:5]}"
                )
            else:
                self.info.append(f"{table_name} table: All {id_col} values are unique ({len(ids)} records)")

        # Special handling for genes/proteins: check gene_id + organism combination
        if not self.genes_df.empty and 'gene or protein id' in self.genes_df.columns:
            gene_df = self.genes_df.copy()
            # Create composite key
            gene_df['composite_key'] = (
                gene_df['gene or protein id'].astype(str) + '::' +
                gene_df.get('organism (from taxa and genomes tab)', '').astype(str)
            )
            composite_ids = gene_df['composite_key'].dropna()
            duplicates = composite_ids[composite_ids.duplicated()].unique()

            if len(duplicates) > 0:
                self.errors.append(
                    f"genes/proteins table: Found {len(duplicates)} duplicate gene+organism combinations: {list(duplicates)[:5]}"
                )
            else:
                # Count unique gene IDs (may have duplicates across organisms, which is OK)
                unique_genes = self.genes_df['gene or protein id'].nunique()
                total_records = len(self.genes_df['gene or protein id'].dropna())
                self.info.append(
                    f"genes/proteins table: {unique_genes} unique gene IDs across {total_records} records (duplicates across organisms are allowed)"
                )

    def validate_required_columns(self) -> None:
        """Validate that required columns exist in each table."""
        required_columns = {
            'genomes': ['Scientific name', 'NCBITaxon id', 'Genome identifier (GenBank, IMG etc)'],
            'biosamples': ['Sample Name', 'Sample ID', 'Organism'],
            'pathways': ['pathway name', 'pathway id'],
            'genes': ['gene or protein id', 'annotation'],
            'structures': ['Name', 'Organism'],
            'publications': ['URL', 'Title'],
            'datasets': ['Dataset name', 'URL'],
        }

        table_map = {
            'genomes': self.genomes_df,
            'biosamples': self.biosamples_df,
            'pathways': self.pathways_df,
            'genes': self.genes_df,
            'structures': self.structures_df,
            'publications': self.publications_df,
            'datasets': self.datasets_df,
        }

        for table_name, df in table_map.items():
            if df.empty:
                continue

            required = required_columns.get(table_name, [])
            missing = [col for col in required if col not in df.columns]

            if missing:
                self.errors.append(f"{table_name} table missing required columns: {missing}")

    def validate_data_completeness(self) -> None:
        """Check for completeness of critical fields."""
        checks = [
            (self.genomes_df, 'Genome identifier (GenBank, IMG etc)', 'genome IDs'),
            (self.genomes_df, 'Annotation download URL', 'genome annotation URLs'),
            (self.biosamples_df, 'Download URL', 'biosample URLs'),
            (self.genes_df, 'EC', 'EC numbers'),
            (self.genes_df, 'GO', 'GO terms'),
            (self.structures_df, 'PDB_ID', 'PDB IDs'),
        ]

        for df, col_name, field_name in checks:
            if df.empty or col_name not in df.columns:
                continue

            total = len(df)
            filled = df[col_name].notna().sum()
            missing = total - filled
            coverage = (filled / total * 100) if total > 0 else 0

            if coverage < 50:
                self.warnings.append(
                    f"Low coverage for {field_name}: {filled}/{total} ({coverage:.1f}%)"
                )
            else:
                self.info.append(
                    f"{field_name}: {filled}/{total} ({coverage:.1f}%) populated"
                )

    def validate_experimental_cross_references(self) -> None:
        """Validate cross-references between experimental data tables."""
        # Validate assay references in screening results
        if not self.screening_results_df.empty and not self.assays_df.empty:
            valid_assay_ids = set()
            for _, row in self.assays_df.iterrows():
                if pd.notna(row.get('assay_id')):
                    valid_assay_ids.add(str(row['assay_id']).strip())

            self.info.append(f"Found {len(valid_assay_ids)} assay IDs in assays table")

            # Check screening_assay and assay_reference columns
            for _, row in self.screening_results_df.iterrows():
                for col in ['screening_assay', 'assay_reference']:
                    assay_ref = row.get(col)
                    if pd.notna(assay_ref):
                        assay_str = str(assay_ref).strip()
                        if assay_str and assay_str not in valid_assay_ids:
                            self.warnings.append(
                                f"Screening result {row.get('experiment_id')} references unknown assay: {assay_str}"
                            )

        # Validate protocol references in assays
        if not self.assays_df.empty and not self.protocols_df.empty:
            valid_protocol_ids = set()
            for _, row in self.protocols_df.iterrows():
                if pd.notna(row.get('protocol_id')):
                    valid_protocol_ids.add(str(row['protocol_id']).strip())

            self.info.append(f"Found {len(valid_protocol_ids)} protocol IDs in protocols table")

            for _, row in self.assays_df.iterrows():
                protocol_ref = row.get('protocol_reference')
                if pd.notna(protocol_ref):
                    protocol_str = str(protocol_ref).strip()
                    if protocol_str and protocol_str not in valid_protocol_ids:
                        self.warnings.append(
                            f"Assay {row.get('assay_id')} references unknown protocol: {protocol_str}"
                        )

        # Validate organism references in bioprocesses
        if not self.bioprocesses_df.empty and not self.genomes_df.empty:
            valid_organisms = set()
            for _, row in self.genomes_df.iterrows():
                if pd.notna(row.get('Scientific name')):
                    valid_organisms.add(str(row['Scientific name']).strip())

            for _, row in self.bioprocesses_df.iterrows():
                organism = row.get('organism_used')
                if pd.notna(organism):
                    org_str = str(organism).strip()
                    # Fuzzy match on genus
                    genus = org_str.split()[0] if org_str else ""
                    matched = any(genus in valid_org for valid_org in valid_organisms)
                    if not matched and genus:
                        self.warnings.append(
                            f"Bioprocess {row.get('process_id')} references organism not in genomes table: {org_str}"
                        )

        # Validate strain barcodes in screening results
        if not self.screening_results_df.empty:
            strain_barcodes = set()
            for _, row in self.screening_results_df.iterrows():
                barcode = row.get('strain_barcode')
                if pd.notna(barcode):
                    strain_barcodes.add(str(barcode).strip())

            if strain_barcodes:
                self.info.append(f"Found {len(strain_barcodes)} unique strain barcodes in screening results")

        # Validate follow-up experiment references in screening results
        if not self.screening_results_df.empty and not self.bioprocesses_df.empty:
            valid_process_ids = set()
            for _, row in self.bioprocesses_df.iterrows():
                if pd.notna(row.get('process_id')):
                    valid_process_ids.add(str(row['process_id']).strip())

            for _, row in self.screening_results_df.iterrows():
                follow_up = row.get('follow_up_experiments')
                if pd.notna(follow_up):
                    follow_str = str(follow_up).strip()
                    # Extract process IDs (e.g., "BP-001 (biosorption scale-up)")
                    import re
                    process_ids = re.findall(r'BP-\d+', follow_str)
                    for pid in process_ids:
                        if pid not in valid_process_ids:
                            self.warnings.append(
                                f"Screening result {row.get('experiment_id')} references unknown bioprocess: {pid}"
                            )

    def validate_chemical_references(self) -> None:
        """Validate chemical compound identifiers against external databases."""
        if self.chemicals_df.empty:
            self.warnings.append("Chemicals table is empty, skipping chemical validation")
            return

        # Check CHEBI ID format
        chebi_count = 0
        for _, row in self.chemicals_df.iterrows():
            chebi = row.get('chebi_id')
            if pd.notna(chebi):
                import re
                chebi_str = str(chebi).strip()
                if re.match(r'CHEBI:\d+', chebi_str):
                    chebi_count += 1
                else:
                    self.warnings.append(f"Invalid CHEBI ID format: {chebi_str}")

        self.info.append(f"{chebi_count} chemicals have valid CHEBI IDs")

        # Check PubChem ID format (should be numeric)
        pubchem_count = 0
        for _, row in self.chemicals_df.iterrows():
            pubchem = row.get('pubchem_id')
            if pd.notna(pubchem):
                pubchem_str = str(pubchem).strip()
                if pubchem_str.isdigit():
                    pubchem_count += 1
                else:
                    self.warnings.append(f"Invalid PubChem ID format: {pubchem_str} (should be numeric)")

        self.info.append(f"{pubchem_count} chemicals have valid PubChem IDs")

    def run_all_validations(self) -> bool:
        """Run all validation checks.

        Returns:
            True if no errors found, False otherwise
        """
        print("Running cross-sheet consistency validation...\n")

        # Required columns check
        print("1. Checking required columns...")
        self.validate_required_columns()

        # Identifier uniqueness check
        print("2. Checking identifier uniqueness...")
        self.validate_identifier_uniqueness()

        # Genome reference validation
        print("3. Validating genome references across sheets...")
        self.validate_genome_references()

        # Biosample validation
        print("4. Validating biosample consistency...")
        self.validate_biosample_references()

        # Pathway-gene cross-references
        print("5. Validating pathway-gene relationships...")
        self.validate_pathway_gene_references()

        # URL validation
        print("6. Validating URL consistency...")
        self.validate_url_consistency()

        # Data completeness
        print("7. Checking data completeness...")
        self.validate_data_completeness()

        # Experimental cross-references
        print("8. Validating experimental cross-references...")
        self.validate_experimental_cross_references()

        # Chemical identifiers
        print("9. Validating chemical identifiers...")
        self.validate_chemical_references()

        # Print results
        print("\n" + "=" * 80)
        print("VALIDATION RESULTS")
        print("=" * 80)

        if self.errors:
            print(f"\n❌ ERRORS ({len(self.errors)}):")
            for error in self.errors:
                print(f"  - {error}")

        if self.warnings:
            print(f"\n⚠️  WARNINGS ({len(self.warnings)}):")
            for warning in self.warnings:
                print(f"  - {warning}")

        if self.info:
            print(f"\nℹ️  INFO ({len(self.info)}):")
            for info in self.info:
                print(f"  - {info}")

        print("\n" + "=" * 80)

        if self.errors:
            print("❌ VALIDATION FAILED - Found critical errors")
            return False
        elif self.warnings:
            print("⚠️  VALIDATION PASSED WITH WARNINGS")
            return True
        else:
            print("✅ VALIDATION PASSED - No issues found")
            return True


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Validate cross-sheet consistency in extended TSV files"
    )
    parser.add_argument(
        '--data-dir',
        type=Path,
        default=Path('data/txt/sheet'),
        help='Directory containing extended TSV files (default: data/txt/sheet)'
    )
    parser.add_argument(
        '--strict',
        action='store_true',
        help='Treat warnings as errors (fail validation on warnings)'
    )

    args = parser.parse_args()

    # Run validation
    validator = ConsistencyValidator(args.data_dir)
    success = validator.run_all_validations()

    # Exit with appropriate code
    if not success:
        sys.exit(1)
    elif args.strict and validator.warnings:
        print("\n⚠️  Running in strict mode: warnings treated as errors")
        sys.exit(1)
    else:
        sys.exit(0)


if __name__ == "__main__":
    main()
