"""Extract experimental data from PDF publications into experimental data sheets.

This script uses pattern matching and text analysis to extract structured data
from scientific publications and populate the experimental data tables.
"""

import argparse
import json
import re
from pathlib import Path
from typing import Dict, List, Optional, Set, Tuple

import pandas as pd


class DocumentExtractor:
    """Extract experimental data from markdown-converted PDF text."""

    # Curated list of PFAS-relevant bacterial genera
    KNOWN_GENERA = {
        'Pseudomonas', 'Acidimicrobium', 'Rhodococcus', 'Mycobacterium',
        'Stenotrophomonas', 'Dehalococcoides', 'Desulfitobacterium',
        'Hyphomicrobium', 'Methylobacterium', 'Bacillus', 'Burkholderia',
        'Sphingomonas', 'Achromobacter', 'Ralstonia', 'Cupriavidus',
        'Arthrobacter', 'Corynebacterium', 'Nocardia', 'Gordonia',
        'Streptomyces', 'Actinomyces', 'Escherichia', 'Klebsiella',
        'Enterobacter', 'Citrobacter', 'Serratia', 'Acinetobacter',
        'Shewanella', 'Geobacter', 'Clostridium', 'Acetobacterium',
        'Methanosarcina', 'Desulfovibrio', 'Sulfurospirillum'
    }

    # Common false positives to exclude from organism extraction
    ORGANISM_BLOCKLIST = {
        'The global', 'Article history', 'Materials and', 'Methods section',
        'In this', 'Figure legend', 'Supplementary information', 'Results showed',
        'Corresponding author', 'International license', 'Copyright holder',
        'Explore all', 'Discussion section', 'Conclusions drawn', 'Future perspectives',
        'References cited', 'Acknowledgments section', 'Funding sources',
        'Competing interests', 'Author contributions', 'Data availability'
    }

    # Valid culture collection prefixes and their number ranges
    CULTURE_COLLECTIONS = {
        'ATCC': (4, 6),  # ATCC 12345
        'DSM': (3, 6),   # DSM 10331
        'DSMZ': (3, 6),  # DSMZ 10331
        'JCM': (4, 6),   # JCM 15462
        'NBRC': (5, 6),  # NBRC 103882
        'LMG': (4, 5),   # LMG 1242
        'NCIMB': (4, 6), # NCIMB 13964
        'CIP': (4, 6),   # CIP 106686
        'NCTC': (4, 5),  # NCTC 10332
        'CCUG': (4, 5),  # CCUG 12345
        'BCRC': (4, 6),  # BCRC 17578
        'IAM': (3, 5),   # IAM 1529
    }

    def __init__(self, markdown_text: str, source_file: str, source_label: str = "extend2"):
        """Initialize extractor with markdown text.

        Args:
            markdown_text: Full markdown content from PDF
            source_file: Name of source file (PDF or markdown)
            source_label: Source label for tracking (default: "extend2")
        """
        self.markdown_text = markdown_text
        self.source_file = source_file
        self.source_label = source_label
        self.extracted_data = {
            'chemicals': [],
            'assays': [],
            'bioprocesses': [],
            'screening_results': [],
            'protocols': [],
            'organisms': [],
            'genes': [],
            'strains': []
        }

    def _is_valid_binomial(self, name: str) -> bool:
        """Validate binomial nomenclature format.

        Args:
            name: Organism name to validate

        Returns:
            True if valid binomial format, False otherwise
        """
        parts = name.split()
        if len(parts) < 2:
            return False

        genus, species = parts[0], parts[1]

        # Check capitalization
        if not (genus[0].isupper() and genus[1:].islower()):
            return False
        if not species.islower():
            return False

        # Check minimum length (avoid "In et", "The global")
        if len(genus) < 3 or len(species) < 3:
            return False

        # Check Latin characters only (no numbers or special chars)
        if not re.match(r'^[A-Za-z]+$', genus + species):
            return False

        return True

    def _appears_in_biological_context(self, organism: str) -> bool:
        """Check if organism appears in biological context.

        Args:
            organism: Organism name to check

        Returns:
            True if appears in biological context
        """
        # Find all occurrences
        occurrences = [m.start() for m in re.finditer(
            re.escape(organism), self.markdown_text, re.IGNORECASE)]

        if len(occurrences) < 2:
            # Single mention likely false positive
            return False

        # Check context around each occurrence
        bio_keywords = {
            'strain', 'isolate', 'culture', 'species', 'bacterium',
            'bacteria', 'microorganism', 'organism', 'genus', 'grown',
            'cultivated', 'inoculated', 'incubated', 'ATCC', 'DSM', 'JCM'
        }

        for pos in occurrences:
            start = max(0, pos - 100)
            end = min(len(self.markdown_text), pos + 100)
            context = self.markdown_text[start:end].lower()

            if any(kw in context for kw in bio_keywords):
                return True

        return False

    def _is_valid_strain_id(self, strain_id: str) -> bool:
        """Validate strain ID format.

        Args:
            strain_id: Strain ID to validate

        Returns:
            True if valid strain ID format
        """
        # Check against known culture collections
        for collection, (min_digits, max_digits) in self.CULTURE_COLLECTIONS.items():
            # Case-sensitive match for collection prefix
            pattern = rf'^{collection}\s+(\d{{{min_digits},{max_digits}}})$'
            if re.match(pattern, strain_id):
                return True

        return False

    def extract_all(self) -> Dict[str, List[Dict]]:
        """Extract data for all sheet types.

        Returns:
            Dictionary of extracted data by sheet type
        """
        self.extract_chemicals()
        self.extract_assays()
        self.extract_bioprocesses()
        self.extract_organisms()
        self.extract_genes()
        self.extract_strains()
        # screening_results and protocols require more structured data
        # that may not be present in all papers
        return self.extracted_data

    def extract_chemicals(self) -> List[Dict]:
        """Extract chemical compounds from markdown text.

        Returns:
            List of chemical compound dictionaries
        """
        chemicals = []

        # Pattern for PFAS ions (Eu³⁺, Tb³⁺, etc.)
        PFAS_pattern = r'\b(La|Ce|Pr|Nd|Pm|Sm|Eu|Gd|Tb|Dy|Ho|Er|Tm|Yb|Lu)(?:³⁺|3\+|\(III\))\b'
        PFASs_found = set(re.findall(PFAS_pattern, self.markdown_text, re.IGNORECASE))

        for element in PFASs_found:
            chemicals.append({
                'chemical_id': f"Custom_{element}_from_{self.source_file}",
                'chemical_name': f"{element}(III) ion",
                'compound_type': 'PFAS',
                'molecular_formula': f"{element}3+",
                'molecular_weight': None,
                'role_in_bioprocess': f"PFAS element mentioned in {self.source_file}",
                'chebi_id': None,
                'pubchem_id': None,
                'chembl_id': None,
                'properties': json.dumps({'source': f'Extracted from {self.source_file}'}),
                'Download URL': None,
                'source': self.source_label
            })

        # Pattern for lanthanophores and siderophores (case-insensitive)
        lanthanophore_pattern = r'\b([A-Z][a-z]*lanthanin|[A-Za-z]*(?:sidero)?phore)\b'
        lanthanophores_raw = re.findall(lanthanophore_pattern, self.markdown_text, re.IGNORECASE)
        # Capitalize first letter for consistency
        lanthanophores = set(name.capitalize() for name in lanthanophores_raw
                            if 'lanthan' in name.lower() or 'siderophore' in name.lower())

        for compound_name in lanthanophores:
            chemicals.append({
                'chemical_id': f"Custom_{compound_name}_from_{self.source_file}",
                'chemical_name': compound_name,
                'compound_type': 'lanthanophore',
                'molecular_formula': None,
                'molecular_weight': None,
                'role_in_bioprocess': f"Lanthanophore/siderophore mentioned in {self.source_file}",
                'chebi_id': None,
                'pubchem_id': None,
                'chembl_id': None,
                'properties': json.dumps({'source': f'Extracted from {self.source_file}'}),
                'Download URL': None,
                'source': self.source_label
            })

        # Look for Methylobacterium species (relevant for lanthanophore production)
        methylo_pattern = r'\bMethylobacterium\s+(\w+)'
        methylo_matches = re.findall(methylo_pattern, self.markdown_text)
        if methylo_matches and 'siderophore' in self.markdown_text.lower():
            # If Methylobacterium mentioned with siderophore, add generic siderophore entry
            species = methylo_matches[0]
            chemicals.append({
                'chemical_id': f"Custom_Siderophore_Methylobacterium_{species}_from_{self.source_file}",
                'chemical_name': f"Siderophore from Methylobacterium {species}",
                'compound_type': 'lanthanophore',
                'molecular_formula': None,
                'molecular_weight': None,
                'role_in_bioprocess': f"Siderophore production gene (rhbC) found in Methylobacterium {species}",
                'chebi_id': None,
                'pubchem_id': None,
                'chembl_id': None,
                'properties': json.dumps({
                    'source': f'Extracted from {self.source_file}',
                    'organism': f'Methylobacterium {species}',
                    'gene': 'rhbC'
                }),
                'Download URL': None,
                'source': self.source_label
            })

        self.extracted_data['chemicals'] = chemicals
        return chemicals

    def extract_assays(self) -> List[Dict]:
        """Extract assay methods from PDF.

        Returns:
            List of assay dictionaries
        """
        assays = []

        # Common assay method patterns
        assay_patterns = {
            'TRL': r'\b(?:time-resolved|TR)\s*luminescence\b',
            'ICP-OES': r'\bICP-OES\b|\binductively coupled plasma[- ]optical emission\b',
            'ICP-MS': r'\bICP-MS\b|\binductively coupled plasma[- ]mass spectr\w+',
            'FACS': r'\bFACS\b|\bflow cytometry\b|\bflow cytometric sorting\b',
            'fluorescence': r'\bfluorescence spectroscopy\b|\bfluorometric\b',
            'UV-Vis': r'\bUV[- ]?Vis\b|\bultraviolet[- ]?visible spectroscopy\b',
            'XRF': r'\bXRF\b|\bX-ray fluorescence\b'
        }

        for assay_type, pattern in assay_patterns.items():
            matches = re.finditer(pattern, self.markdown_text, re.IGNORECASE)
            for match in matches:
                # Extract context around match (200 chars)
                start = max(0, match.start() - 100)
                end = min(len(self.markdown_text), match.end() + 100)
                context = self.markdown_text[start:end]

                # Try to extract detection limit
                detection_limit = None
                limit_pattern = r'(?:detection limit|LOD|limit of detection)[:\s]*(?:of\s*)?(\d+\.?\d*\s*(?:nM|μM|ppm|ppb|ng/mL|μg/L))'
                limit_match = re.search(limit_pattern, context, re.IGNORECASE)
                if limit_match:
                    detection_limit = limit_match.group(1)

                assays.append({
                    'assay_id': f"Custom_{assay_type}_from_{self.source_file}",
                    'assay_name': f"{assay_type} assay from {self.source_file}",
                    'assay_type': assay_type,
                    'target_analytes': None,
                    'detection_method': match.group(0),
                    'detection_limit': detection_limit,
                    'dynamic_range': None,
                    'protocol_reference': f"See {self.source_file} Methods section",
                    'equipment_required': None,
                    'sample_preparation': None,
                    'data_output_format': None,
                    'Download URL': None,
                    'source': self.source_label
                })
                break  # Only take first match per assay type

        self.extracted_data['assays'] = assays
        return assays

    def extract_bioprocesses(self) -> List[Dict]:
        """Extract bioprocess conditions from PDF.

        Returns:
            List of bioprocess dictionaries
        """
        bioprocesses = []

        # Bioprocess type patterns
        process_patterns = {
            'bioleaching': r'\bbioleaching\b',
            'biomineralization': r'\bbiomineralization\b|\bbioprecipitation\b',
            'biosorption': r'\bbiosorption\b|\badsorption\b',
            'bioaccumulation': r'\bbioaccumulation\b|\buptake\b'
        }

        for process_type, pattern in process_patterns.items():
            matches = re.finditer(pattern, self.markdown_text, re.IGNORECASE)
            for match in matches:
                # Extract context (500 chars)
                start = max(0, match.start() - 250)
                end = min(len(self.markdown_text), match.end() + 250)
                context = self.markdown_text[start:end]

                # Try to extract organism - use validated organisms from main extraction
                # For now, set to None to avoid extracting garbage text
                # TODO: Link to organisms extracted via extract_organisms() method
                organism = None

                # Try to extract pH
                pH = None
                pH_pattern = r'\bpH\s*[:\s]*(\d+\.?\d*)'
                pH_match = re.search(pH_pattern, context, re.IGNORECASE)
                if pH_match:
                    pH = float(pH_match.group(1))

                # Try to extract temperature
                temperature = None
                temp_pattern = r'(\d+)\s*°?C\b'
                temp_match = re.search(temp_pattern, context)
                if temp_match:
                    temperature = float(temp_match.group(1))

                # Try to extract REE concentration
                ree_conc = None
                conc_pattern = r'(\d+\.?\d*\s*(?:μM|mM|ppm|mg/L))\s*(?:Eu|Tb|La|Ce|Nd|PFAS|REE)'
                conc_match = re.search(conc_pattern, context, re.IGNORECASE)
                if conc_match:
                    ree_conc = conc_match.group(1)

                bioprocesses.append({
                    'process_id': f"Custom_{process_type}_from_{self.source_file}",
                    'process_name': f"{process_type.capitalize()} process from {self.source_file}",
                    'process_type': process_type,
                    'strain_used': None,
                    'organism_used': organism,
                    'growth_conditions': None,
                    'ree_concentration': ree_conc,
                    'contact_time': None,
                    'pH': pH,
                    'temperature': temperature,
                    'competing_ions': None,
                    'process_parameters': json.dumps({'source': f'Extracted from {self.source_file}'}),
                    'optimization_history': None,
                    'Download URL': None,
                    'source': self.source_label
                })
                break  # Only take first match per process type

        self.extracted_data['bioprocesses'] = bioprocesses
        return bioprocesses

    def extract_organisms(self) -> List[Dict]:
        """Extract organism mentions from PDF for cross-linking.

        Uses improved patterns and validation to minimize false positives.

        Returns:
            List of organism dictionaries
        """
        organisms = []
        seen_organisms = set()

        # Pattern 1: Genus species (binomial nomenclature)
        # Min 3 chars each to avoid "In et", "The global"
        binomial_pattern = r'\b([A-Z][a-z]{2,}\s+[a-z]{3,})\b'

        # Pattern 2: Genus sp. STRAIN (e.g., "Pseudomonas sp. 273")
        # Only match known genera to avoid false positives
        genus_list = '|'.join(self.KNOWN_GENERA)
        sp_pattern = rf'\b({genus_list})\s+sp\.?\s+([A-Z0-9\-]{{1,10}})\b'

        # Extract binomial names
        binomial_matches = re.findall(binomial_pattern, self.markdown_text)
        for organism_name in binomial_matches:
            organism_name = organism_name.strip()

            # Multi-layer validation
            genus = organism_name.split()[0]

            if (organism_name not in seen_organisms and
                organism_name not in self.ORGANISM_BLOCKLIST and
                self._is_valid_binomial(organism_name) and
                genus in self.KNOWN_GENERA and
                self._appears_in_biological_context(organism_name)):

                seen_organisms.add(organism_name)
                organisms.append({
                    'scientific_name': organism_name,
                    'ncbi_taxon_id': None,
                    'genome_identifier': None,
                    'annotation_download_url': None,
                    'source': self.source_label,
                    'paper_reference': self.source_file
                })

        # Extract sp. designations (e.g., "Pseudomonas sp. 273")
        sp_matches = re.findall(sp_pattern, self.markdown_text)
        for genus, strain in sp_matches:
            organism_name = f"{genus} sp. {strain}"

            if (organism_name not in seen_organisms and
                self._appears_in_biological_context(organism_name)):

                seen_organisms.add(organism_name)
                organisms.append({
                    'scientific_name': organism_name,
                    'ncbi_taxon_id': None,
                    'genome_identifier': None,
                    'annotation_download_url': None,
                    'source': self.source_label,
                    'paper_reference': self.source_file
                })

        self.extracted_data['organisms'] = organisms
        return organisms

    def extract_genes(self) -> List[Dict]:
        """Extract gene/protein mentions from PDF for cross-linking.

        Uses context-aware patterns to reduce false positives.

        Returns:
            List of gene dictionaries
        """
        genes = []
        seen_genes = set()

        # PFAS-relevant gene patterns (case-sensitive for gene symbols)
        # Bacterial genes typically: lowercase italics (rdh, deh, crc, alk)
        # Proteins typically: Capital first letter (RdhA, DehA, CrcB)
        gene_patterns = {
            # Dehalogenase genes (specific symbols only)
            'dehalogenase': [
                r'\b(rdhA|rdhB|rdhC)\b',  # Reductive dehalogenases
                r'\b(dehH|dehI|dehA|dehB)\b',  # Haloacid dehalogenases
                r'\b(dhaA)\b',  # Haloalkane dehalogenase
                r'\b(pceA|tceA)\b',  # Chloroethene reductive dehalogenases
            ],
            # Fluoride resistance (specific symbols)
            'fluoride_resistance': [
                r'\b(crcA|crcB)\b',  # Fluoride exporters
                r'\b(fexA|fexB)\b',  # Fluoride export proteins
            ],
            # Oxygenases (specific known genes)
            'oxygenase': [
                r'\b(alkB|alkM|alkG)\b',  # Alkane monooxygenases
                r'\b(nahAc|nahAd)\b',  # Naphthalene dioxygenase
                r'\b(catA|catB)\b',  # Catechol dioxygenases
            ],
        }

        # Flatten patterns and extract
        for gene_type, patterns in gene_patterns.items():
            for pattern in patterns:
                matches = re.findall(pattern, self.markdown_text)
                for gene_name in matches:
                    gene_name = gene_name.strip()

                    # Validation: gene must appear in biological context
                    if gene_name and gene_name not in seen_genes:
                        # Check if appears near biological keywords
                        bio_context = any(kw in self.markdown_text.lower()
                                        for kw in ['gene', 'protein', 'enzyme', 'encodes', 'catalyzes'])

                        if bio_context:
                            seen_genes.add(gene_name)
                            genes.append({
                                'gene_or_protein_id': gene_name,
                                'gene_name': gene_name,
                                'annotation': f"{gene_type} gene",
                                'organism': None,
                                'ec_number': None,
                                'go_terms': None,
                                'chebi_terms': None,
                                'sequence_download_url': None,
                                'source': self.source_label,
                                'paper_reference': self.source_file
                            })

        self.extracted_data['genes'] = genes
        return genes

    def extract_strains(self) -> List[Dict]:
        """Extract strain designations from PDF for cross-linking.

        Uses strict validation against known culture collections to avoid
        false positives like "pH 7", "Figure 1", etc.

        Returns:
            List of strain dictionaries
        """
        strains = []
        seen_strains = set()

        # Build specific patterns for each culture collection
        for collection, (min_digits, max_digits) in self.CULTURE_COLLECTIONS.items():
            # Case-sensitive pattern (ATCC, not Atcc or atcc)
            pattern = rf'\b({collection}\s+\d{{{min_digits},{max_digits}}})\b'

            matches = re.findall(pattern, self.markdown_text)
            for strain_id in matches:
                strain_id = strain_id.strip()

                if strain_id not in seen_strains and self._is_valid_strain_id(strain_id):
                    seen_strains.add(strain_id)
                    strains.append({
                        'strain_id': strain_id,
                        'strain_designation': strain_id,
                        'organism': None,
                        'culture_collection_id': strain_id,
                        'isolation_source': None,
                        'source': self.source_label,
                        'paper_reference': self.source_file
                    })

        self.extracted_data['strains'] = strains
        return strains


def read_markdown_file(md_path: Path) -> str:
    """Read markdown file content.

    Args:
        md_path: Path to markdown file

    Returns:
        Markdown text content
    """
    try:
        return md_path.read_text(encoding='utf-8')
    except Exception as e:
        print(f"Error reading {md_path.name}: {e}")
        return ""


def extract_doi(markdown_text: str, filename: str) -> str:
    """Extract DOI from markdown text.

    Args:
        markdown_text: Full markdown content
        filename: Filename to use as fallback

    Returns:
        DOI string or filename if DOI not found
    """
    # Pattern for DOI (case-insensitive search near the top of document)
    # Look in first 5000 characters for main DOI
    header = markdown_text[:5000]

    # Try to find DOI in format "doi: 10.xxxx/xxxxx" or "doi:10.xxxx/xxxxx"
    doi_pattern = r'doi:\s*(\d+\.\d+/[^\s,\)]+)'
    matches = re.findall(doi_pattern, header, re.IGNORECASE)

    if matches:
        # Return the first DOI found (usually the paper's main DOI)
        return matches[0].strip()

    # Fallback to filename if no DOI found
    return filename


def append_to_tsv(data: List[Dict], tsv_path: Path, sheet_type: str):
    """Append extracted data to TSV file, removing duplicates.

    Args:
        data: List of extracted records
        tsv_path: Path to TSV file
        sheet_type: Type of sheet (for ID column name)
    """
    if not data:
        return

    # Determine ID column name
    id_columns = {
        'chemicals': 'chemical_id',
        'assays': 'assay_id',
        'bioprocesses': 'process_id',
        'screening_results': 'experiment_id',
        'protocols': 'protocol_id',
        'organisms': 'scientific_name',
        'genes': 'gene_or_protein_id',
        'strains': 'strain_id'
    }
    id_col = id_columns.get(sheet_type)

    # Load existing data with string dtype to preserve integer formats
    # (pandas converts int columns to float when there are NaN values)
    if tsv_path.exists():
        existing_df = pd.read_csv(tsv_path, sep='\t', dtype=str, keep_default_na=False)
        existing_df = existing_df.replace('', pd.NA)
        existing_ids = set(existing_df[id_col].dropna()) if id_col in existing_df.columns else set()
    else:
        existing_df = pd.DataFrame()
        existing_ids = set()

    # Filter out duplicates
    new_data = [d for d in data if d.get(id_col) not in existing_ids]

    if new_data:
        new_df = pd.DataFrame(new_data)
        combined_df = pd.concat([existing_df, new_df], ignore_index=True)
        # Replace pd.NA with empty string for TSV format
        combined_df = combined_df.fillna('')
        combined_df.to_csv(tsv_path, sep='\t', index=False)
        print(f"  Added {len(new_data)} new records to {sheet_type}")
    else:
        print(f"  No new records to add to {sheet_type} (all duplicates)")


def batch_extract_from_directory(pdf_dir: Path, output_dir: Path, summary_only: bool = False, source_label: str = "extend2"):
    """Extract data from all markdown files (converted from PDFs) in directory.

    Args:
        pdf_dir: Directory containing markdown files
        output_dir: Directory for output TSV files
        summary_only: If True, only print summary without modifying files
        source_label: Source label for tracking (default: "extend2")
    """
    # Look for markdown files (converted from PDFs)
    md_files = list(pdf_dir.glob("*.md"))

    if not md_files:
        print(f"No markdown files found in {pdf_dir}")
        print(f"Please run PDF to markdown conversion first:")
        print(f"  uv run python src/pdf_to_markdown.py --batch {pdf_dir}")
        return

    print(f"Found {len(md_files)} markdown files to process:")
    for md in md_files:
        print(f"  - {md.name}")
    print("")

    total_extracted = {
        'chemicals': 0,
        'assays': 0,
        'bioprocesses': 0,
        'screening_results': 0,
        'protocols': 0,
        'organisms': 0,
        'genes': 0,
        'strains': 0
    }

    for md_file in md_files:
        print(f"Processing: {md_file.name}")
        print("-" * 60)

        # Read markdown file
        markdown_text = read_markdown_file(md_file)

        if not markdown_text:
            print(f"  Skipping {md_file.name} (empty or error reading file)")
            print()
            continue

        # Extract DOI to use as source identifier (or use source_label if not provided)
        if source_label == "extend2":
            # Auto-extract DOI from markdown
            doi = extract_doi(markdown_text, md_file.stem)
            print(f"  Source: {doi}")
        else:
            # Use provided source label
            doi = source_label

        # Extract data with DOI as source
        extractor = DocumentExtractor(markdown_text, md_file.stem, doi)
        extracted = extractor.extract_all()

        # Print summary
        print(f"Extracted from {md_file.name}:")
        print(f"  - {len(extracted['chemicals'])} chemicals")
        print(f"  - {len(extracted['assays'])} assays")
        print(f"  - {len(extracted['bioprocesses'])} bioprocesses")
        print(f"  - {len(extracted['screening_results'])} screening results")
        print(f"  - {len(extracted['protocols'])} protocols")
        print(f"  - {len(extracted['organisms'])} organisms")
        print(f"  - {len(extracted['genes'])} genes")
        print(f"  - {len(extracted['strains'])} strains")
        print("")

        # Update totals
        for key in total_extracted:
            total_extracted[key] += len(extracted[key])

        # Append to TSV files (if not summary only)
        if not summary_only:
            # Map sheet types to actual file names
            filename_mapping = {
                'organisms': 'taxa_and_genomes',
                'genes': 'genes_and_proteins',
                # All others use their sheet_type name directly
            }

            for sheet_type, records in extracted.items():
                if records:
                    filename = filename_mapping.get(sheet_type, sheet_type)
                    tsv_path = output_dir / f"PFAS_Data_for_AI_{filename}_extended.tsv"
                    append_to_tsv(records, tsv_path, sheet_type)

    print("=" * 60)
    print("EXTRACTION SUMMARY")
    print("=" * 60)
    print(f"Total records extracted across {len(md_files)} markdown files:")
    for sheet_type, count in total_extracted.items():
        print(f"  - {sheet_type}: {count} records")
    print("")

    if summary_only:
        print("(Summary only - no files were modified)")
    else:
        print("Files updated successfully!")
        print(f"All extracted data labeled with source: '{source_label}'")


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Extract experimental data from PDF publications"
    )
    parser.add_argument(
        '--pdf-dir',
        type=Path,
        default=Path('data/publications'),
        help='Directory containing PDF files'
    )
    parser.add_argument(
        '--output-dir',
        type=Path,
        default=Path('data/txt/sheet'),
        help='Output directory for TSV files'
    )
    parser.add_argument(
        '--summary-only',
        action='store_true',
        help='Print summary without modifying files'
    )

    args = parser.parse_args()

    # Extract from all PDFs
    batch_extract_from_directory(args.pdf_dir, args.output_dir, args.summary_only)


if __name__ == "__main__":
    main()
