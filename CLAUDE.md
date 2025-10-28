# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository Overview

PFAS-AI - ML-enabled automated data pipeline for PFAS biodegradation research. Extends small seed datasets into comprehensive research databases by integrating NCBI, KEGG, UniProt, PDB, and other biological databases to identify and characterize PFAS-degrading microorganisms.

**Scientific Focus**: Per- and polyfluoroalkyl substances (PFAS) biodegradation using machine learning-guided microbial consortia design.

**Key Research Areas**:
- C-F bond cleavage enzymes (dehalogenases, defluorinases)
- Fluoride resistance mechanisms and transport systems
- Hydrocarbon-degrading microbes for PFAS backbone metabolism
- Dechlorinating microbes with potential C-F bond cleavage activity
- Environmental microbes from PFAS-contaminated sites
- Microbial consortia design for polyfluorinated and perfluorinated compound degradation

**Current Status**: Initial development - transitioning from CMM-AI (lanthanides) to PFAS-AI with new seed data and ML integration focus.

## Project Objectives

1. **ML-Powered Database**: Build a semantically-aware database using KG-Microbe platform to identify putative PFAS biodegradation genes, pathways, taxa, environments, and microbial communities
2. **Consortia Design**: Use ML to design optimized microbial consortia (3-5 members each) for efficient PFAS degradation
3. **Experimental Validation**: Test 10-15 consortia, down-select to 5 most effective for detailed PFAS degradation analysis

## Commands

### Dependency Management
- **Always use `uv`** for managing dependencies. Never use `pip`.
- `uv run <command>` - Run commands in the project environment
- `uv sync` or `make install` - Install dependencies

### Pipeline Commands (via Makefile)

**Basic Data Extension**:
- `make` or `make help` - Show all available commands
- `make update-all` - Run full pipeline (all tables)
- `make update-genomes` - Extend taxa and genomes with NCBI Assembly data
- `make update-biosamples` - Extend biosamples with NCBI BioSample data
- `make update-pathways` - Extend pathways with KEGG/MetaCyc
- `make update-genes` - Extend genes/proteins with UniProt/KEGG
- `make update-structures` - Extend structures with PDB/AlphaFold
- `make update-publications` - Extend publications with PubMed/arXiv
- `make update-datasets` - Extend datasets with repository searches
- `make convert-excel` - Convert Excel sheets to TSV (prerequisite)

**Experimental Data Tables**:
- `make update-chemicals` - Extend chemicals with PubChem/CHEBI (PFAS compounds)
- `make update-assays` - Extend assays with curated protocols (fluoride, PFAS detection)
- `make update-reactions` - Extend reactions with RHEA/KEGG data (dehalogenation, fluoride resistance)
- `make update-bioprocesses` - (Manual) Update bioprocesses table
- `make update-screening` - (Manual) Update screening results table
- `make update-protocols` - (Manual) Update protocols table

**Advanced Workflows**:
- `make extend2` - Full extend2 workflow: download PDFs → extend chemicals/assays → extract experimental data
- `make extendbypub` - Cross-reference publications with data sheets and append publication IDs to source columns
- `make merge-excel` - Merge Excel updates while preserving generated data and publication references
- `make merge-excel-dry-run` - Preview merge without applying changes

**Utilities**:
- `make status` - Check pipeline status (file existence and line counts)
- `make test` - Run doctests and validation

### Testing Commands
- `make test` - Run doctests and test_annotation_urls.py
- `make validate-schema` - Validate extended TSV data against LinkML schema
- `make validate-consistency` - Validate cross-sheet referential integrity and data quality
- `uv run python -m doctest src/parsers.py -v` - Run parsers doctests
- `uv run python -m doctest src/ncbi_search.py -v` - Run NCBI doctests
- `uv run ruff check src/` - Check code formatting
- `uv run ruff format src/` - Format code

## Architecture

### Directory Structure
```
src/                   # Main Python source code (flat structure)
  parsers.py          # Excel/Word/PDF to TSV/text converters
  ncbi_search.py      # NCBI Assembly/BioSample search (PFAS microbes)
  pathway_search.py   # KEGG/MetaCyc pathway search (dehalogenation, fluoride)
  gene_search.py      # UniProt/KEGG gene/protein search (dehalogenase, defluorinase)
  structure_search.py # PDB/AlphaFold structure search
  publication_search.py # PubMed/arXiv literature search (PFAS biodegradation)
  dataset_search.py   # Multi-repository dataset search
  extend_*.py         # Pipeline automation scripts
  tsv_to_linkml.py    # TSV to LinkML YAML converter
  validate_consistency.py # Cross-sheet consistency validator
  linkml_models.py    # Generated Python models (auto-generated)
  cli.py             # Command-line interface
schema/               # LinkML schema definitions
  pfas_biodegradation.yaml # Main schema file (to be created)
data/                 # Research data
  sheet/             # Original Excel files (PFAS Data for AI.xlsx)
  txt/sheet/         # Converted TSV + extended tables
  linkml_database.yaml # LinkML YAML format (generated)
  publications/      # PDF research papers
  proposal/          # Project documentation (proposal.txt)
Makefile             # Pipeline automation
pyproject.toml       # Package configuration (uses uv/hatchling)
```

### Data Pipeline Flow

**Basic Extension (extend1)**:
1. **Input**: Small seed datasets (6 organisms, 23 publications) in Excel format
2. **Conversion**: Excel → TSV via `parsers.py`
3. **Extension**: Query APIs (NCBI, KEGG, UniProt, PDB) to find PFAS-related data
4. **URL Generation**: Create direct download links for all resources
5. **Output**: Extended TSV tables with download URLs

**Advanced Extension (extend2)**:
1. **PDF Download**: Download publications from URLs in publications table
2. **Chemical/Assay Extension**: Extend chemicals (PFAS compounds) and assays (fluoride detection, PFAS analysis) with source=extend2 label
3. **PDF Conversion**: Convert PDFs to markdown format for text extraction
4. **Data Extraction**: Extract experimental data from PDFs (DOI-based provenance)
5. **Validation**: Run consistency checks and LinkML schema validation
6. **Cross-Reference (extendbypub)**: Link publications to data rows by keyword matching

**Source Tracking**:
- All extended rows include a `source` column for data provenance
- Source labels: `extend1` (initial extension), `extend2` (second round), DOI (extracted from specific papers)
- Publication cross-references appended to source column with `|` delimiter (e.g., `extend2|10.1016/j.jhazmat.2021.126361`)

### Key Modules

**parsers.py**: File format converters
- `xlsx_to_tsv()` - Excel to TSV with filename sanitization
- `docx_to_text()` - Word to plain text
- `pdf_to_text()` - PDF to plain text
- All functions sanitize filenames (spaces → underscores)

**ncbi_search.py**: NCBI database integration
- `search_ncbi_assembly()` - Query Assembly database
- `search_ncbi_biosample()` - Query BioSample database
- `search_pfas_organisms()` - Main search logic for PFAS-relevant microbes (to be created)
- `get_annotation_download_url()` - Generate FTP URLs for genome annotations
- `create_extended_tables()` - Orchestrate genome/biosample extension

**pathway_search.py**: Metabolic pathway search (KEGG/MetaCyc for dehalogenation, fluoride metabolism)
**gene_search.py**: Gene/protein search (UniProt/KEGG with focus on dehalogenases, defluorinases, fluoride exporters)
**structure_search.py**: 3D structure search (PDB/AlphaFold for dehalogenase structures)
**publication_search.py**: Literature search (PubMed/arXiv/bioRxiv for PFAS biodegradation)
**dataset_search.py**: Dataset search (GEO, SRA, MetaboLights, PFAS metagenomes)
**chemical_search.py**: Chemical compound search (PubChem/CHEBI for PFAS compounds) with source labeling
**assay_search.py**: Assay protocol search with curated methods (fluoride detection, PFAS quantification)
**reaction_search.py**: Biochemical reaction enrichment from RHEA/KEGG databases
**convert_reactions_excel.py**: Convert reactions Excel with reaction_category column tracking
**extend_reactions.py**: Main reactions extension pipeline script
**pdf_to_markdown.py**: Convert PDFs to markdown for text extraction
**extract_from_documents.py**: Extract experimental data from markdown files with DOI tracking
**download_pdfs_from_publications.py**: Download PDFs from publications table URLs
**extend_by_publication.py**: Cross-reference publications with data sheets
**merge_excel_updates.py**: Intelligently merge Excel updates while preserving generated data
**validate_consistency.py**: Cross-sheet consistency and referential integrity validation
**tsv_to_linkml.py**: Convert TSV data to LinkML YAML format

### Search Strategy

**PFAS-specific terms**:
- PFAS, perfluorinated, polyfluorinated, PFOA, PFOS, AFFF
- C-F bond, defluorination, dehalogenation, fluoride
- Per- and polyfluoroalkyl substances, forever chemicals

**Functional terms**:
- Dehalogenase, defluorinase, fluoroacetate dehalogenase
- Fluoride exporter, fluoride resistance, CrcB, FEX
- Reductive dehalogenase (RdhA), haloalkane dehalogenase
- Hydrocarbon degradation, aromatic degradation

**Organism groups**:
- Pseudomonas (known PFAS degraders)
- Hyphomicrobium (C1 metabolism, potential PFAS degradation)
- Acidimicrobium (extremophile, acid-tolerant)
- Dechlorinating bacteria (Dehalococcoides, Desulfitobacterium)
- Hydrocarbon degraders (Rhodococcus, Mycobacterium)
- PFAS-contaminated site isolates

**Environmental context**:
- PFAS-contaminated sites, AFFF-impacted groundwater
- Wastewater treatment, activated sludge
- Biofilm, anaerobic digestion
- Fluoride-rich environments

**Rate limiting**: 0.5-1.0 second delays between API calls
**Deduplication**: Remove duplicates based on unique IDs (assembly_id, sample_id, etc.)

### Data Table Schema

All extended tables follow TSV format with consistent column naming:
- **Genomes**: Scientific name, NCBITaxon id, Genome identifier, Annotation download URL, source
- **Biosamples**: Sample Name, Sample ID, Organism, Download URL
- **Pathways**: Pathway name, Database (KEGG/MetaCyc), Pathway ID, URL, genes (focus on dehalogenation)
- **Genes/Proteins**: Gene name, Protein ID, Database, Sequence URL, functional annotations (dehalogenase, fluoride exporter)
- **Structures**: Protein name, PDB ID, Method, Resolution, Structure URL (dehalogenase structures)
- **Publications**: Title, Authors, Journal, PMID, DOI, URL (PFAS biodegradation focus)
- **Chemicals**: PFAS compounds (PFOA, PFOS, precursors), CHEBI/PubChem IDs, molecular formula, compound_type
- **Assays**: Fluoride detection, PFAS quantification, LC-MS/MS protocols
- **Reactions**: Biochemical reactions (RHEA IDs, equations, EC numbers, reaction_category for dehalogenation/fluoride resistance/hydrocarbon degradation)

## Development Principles

### Testing
- Use doctests liberally as both examples and tests
- Write pytest functional style (not unittest OO)
- Use `@pytest.mark.parametrize` for testing input combinations
- Mark external API tests with `@pytest.mark.integration`
- Never write mock tests unless explicitly requested
- Don't weaken test conditions to make them pass - fix the underlying issue

### Code Style
- Always use type hints for all functions
- Document all methods and classes with docstrings
- Pydantic or LinkML for data objects, dataclasses for engine-style OO state
- Fail fast - avoid try/except blocks that mask bugs
- Follow DRY principle, but avoid premature over-abstraction
- Declarative principles favored

### API Integration
- All API calls must respect rate limits (0.5-1.0 sec delays)
- Handle missing/malformed data gracefully
- Generate valid URLs for all database resources
- Use Bio.Entrez for NCBI (email must be configured)

### File Handling
- Sanitize all output filenames (spaces → underscores via `sanitize_filename()`)
- Use pandas for TSV reading/writing (sep='\t')
- Output files go to `data/txt/sheet/` with `_extended.tsv` suffix
- Input Excel file: `data/sheet/PFAS Data for AI.xlsx`

## LinkML Schema

This repository will include a comprehensive LinkML schema for modeling PFAS biodegradation data.

**Schema Location**: `schema/pfas_biodegradation.yaml` (to be created)

### Schema Overview

The schema models thirteen main classes for comprehensive PFAS biodegradation research:

#### Core Data Tables (7)

1. **GenomeRecord**: Bacterial/archaeal genomes with taxonomy and annotations
   - Maps to: NCBITaxon (taxonomy), NCBI Assembly (genome accessions)
   - Key fields: scientific_name, ncbi_taxon_id, genome_identifier, annotation_download_url
   - Focus: PFAS-degrading microbes, dehalogenase-containing genomes

2. **BiosampleRecord**: Environmental and cultured samples
   - Maps to: NCBI BioSample, SRA
   - Key fields: sample_id, sample_name, organism, download_url
   - Focus: PFAS-contaminated sites, AFFF-impacted environments

3. **PathwayRecord**: Metabolic pathways for PFAS degradation
   - Maps to: KEGG, MetaCyc, EC, GO
   - Key fields: pathway_id, pathway_name, genes, genes_kegg
   - Focus: Dehalogenation, fluoride metabolism, hydrocarbon degradation

4. **GeneProteinRecord**: Genes and proteins with functional annotations
   - Maps to: UniProt, KEGG, GO, EC, CHEBI
   - Key fields: gene_protein_id, annotation, ec_number, go_terms, chebi_terms
   - Focus: Dehalogenases, defluorinases, fluoride exporters, reductive dehalogenases

5. **MacromolecularStructureRecord**: Protein and complex 3D structures
   - Maps to: PDB, AlphaFold
   - Key fields: pdb_id, structure_name, components, method, resolution
   - Focus: Dehalogenase structures, fluoride exporter structures

6. **PublicationRecord**: Scientific literature
   - Maps to: DOI, PMID, arXiv, bioRxiv
   - Key fields: url, title, journal, year, authors
   - Focus: PFAS biodegradation, C-F bond cleavage, microbial consortia

7. **DatasetRecord**: Research datasets from repositories
   - Maps to: SRA, GEO, MetaboLights, etc.
   - Key fields: dataset_name, data_type, url, license
   - Focus: PFAS metagenomes, contaminated site microbiomes

#### Experimental Data Tables (6)

8. **ReactionRecord**: Biochemical reactions for PFAS biodegradation
   - Maps to: RHEA (reaction database), KEGG Reaction, EC (Enzyme Commission)
   - Key fields: reaction_id, equation, reaction_category, ec_number, rhea_id, kegg_reaction_id
   - Reaction categories: dehalogenase (C-F bond cleavage), fluoride_resistance (transport), hydrocarbon_degradation, oxygenase_cometabolism, known_pfas_degraders

9. **ChemicalCompoundRecord**: PFAS compounds and related chemicals
   - Maps to: CHEBI, PubChem, ChEMBL
   - Key fields: chemical_id, chemical_name, compound_type, molecular_formula, role_in_bioprocess
   - Compound types: perfluorinated (PFOA, PFOS), polyfluorinated (precursors), fluoride, metabolites, degradation products

10. **AssayMeasurementRecord**: Analytical assays for PFAS and fluoride
    - Maps to: OBI (Ontology for Biomedical Investigations), BAO (BioAssay Ontology)
    - Key fields: assay_id, assay_name, assay_type, target_analytes, detection_method, detection_limit
    - Assay types: LC-MS/MS (PFAS quantification), fluoride electrode, ion chromatography, total organic fluorine

11. **BioprocessConditionsRecord**: Experimental conditions for PFAS biodegradation
    - Maps to: ENVO, MIXS, OBI
    - Key fields: process_id, process_name, process_type, strain_used, pH, temperature, pfas_concentration
    - Process types: aerobic degradation, anaerobic degradation, sequential anaerobic-aerobic, bioaugmentation, consortia-based

12. **ScreeningResultRecord**: High-throughput screening data
    - Maps to: OBI, BAO
    - Key fields: experiment_id, plate_coordinates, strain_barcode, screening_assay, measurement_values, hit_classification
    - Focus: Fluoride production, PFAS degradation, growth on PFAS

13. **ProtocolRecord**: Experimental protocols and SOPs
    - Maps to: OBI
    - Key fields: protocol_id, protocol_name, protocol_type, protocol_version, protocol_doi, dbtl_iteration
    - Protocol types: PFAS extraction, fluoride measurement, consortia assembly, LC-MS/MS analysis

### Ontology Mappings

The schema integrates the following ontologies and vocabularies:
- **NCBITaxon**: Organism taxonomy
- **SRA**: Sequence Read Archive identifiers
- **CHEBI**: Chemical entities (PFAS, fluoride, metabolites)
- **ENVO**: Environmental ontology (contaminated sites, groundwater)
- **MIXS**: Minimum Information about any Sequence
- **UniProtKB**: Protein sequences and annotations
- **GO**: Gene Ontology (molecular function, biological process)
- **EC**: Enzyme Commission numbers (dehalogenases: EC 3.8.1.-)
- **RHEA**: Reaction database
- **KEGG/MetaCyc**: Metabolic pathways (dehalogenation, fluoride metabolism)
- **PDB**: Protein Data Bank structures
- **OBI**: Ontology for Biomedical Investigations (assays, protocols)
- **BAO**: BioAssay Ontology
- **PubChem**: Chemical compound database (PFAS structures)
- **ChEMBL**: Bioactive molecule database

### Using LinkML Tools

```bash
# Install LinkML dependencies
uv sync

# Validate extended TSV data against schema (complete workflow)
make validate-schema

# Individual LinkML commands:
# Generate Python dataclasses from schema
make gen-linkml-models
# OR manually:
uv run gen-python schema/pfas_biodegradation.yaml > src/linkml_models.py

# Generate JSON Schema
uv run gen-json-schema schema/pfas_biodegradation.yaml > schema/schema.json

# Convert TSV to LinkML YAML format
uv run python src/tsv_to_linkml.py --data-dir data/txt/sheet --output data/linkml_database.yaml

# Validate YAML data against schema
uv run linkml-validate -s schema/pfas_biodegradation.yaml data/linkml_database.yaml
```

### Schema Design Principles

- **Ontology-aligned**: All slots map to standard ontologies where possible
- **Flexible IDs**: Support for KEGG K numbers, UniProt IDs, custom IDs, GenBank accessions
- **Validation patterns**: Regex patterns for accession numbers (GCF_*, SAMN*, GO:*, EC:3.8.1.*, CHEBI:*, etc.)
- **Enumerations**: Controlled vocabularies for PFAS compound types, assay methods, degradation processes
- **Multivalued slots**: Support for multiple GO terms, CHEBI terms, genes per record
- **URL handling**: Proper URIs with schema.org mappings

## Data Validation

The project includes two levels of validation:

### 1. Schema Validation (`make validate-schema`)

Validates that TSV data conforms to the LinkML schema structure:
- Converts TSV files to LinkML YAML format
- Checks required fields, data types, and patterns
- Validates ontology term formats (GO:*, CHEBI:*, EC numbers for dehalogenases)
- Verifies URL formatting and identifier patterns

**Validation workflow**:
```bash
make validate-schema
# 1. Generates Python models from schema
# 2. Converts TSV → YAML with deduplication
# 3. Validates YAML against schema
# 4. Reports validation errors and statistics
```

### 2. Cross-Sheet Consistency Validation (`make validate-consistency`)

Validates referential integrity and data quality across tables:

**Validation checks**:
1. **Required columns**: Ensures all tables have expected column names
2. **Identifier uniqueness**: Checks for duplicate IDs within tables
   - Genomes: Scientific name must be unique
   - Biosamples: Sample ID must be unique
   - Genes/proteins: Gene ID + organism combination must be unique
3. **Genome references**: Validates organism names across tables
   - Checks genes/proteins organism references match genomes table
   - Checks structures organism references match genomes table
   - Uses fuzzy genus-level matching for organism name variants
4. **Biosample consistency**: Validates sample IDs and checks for duplicates
5. **Pathway-gene relationships**: Validates gene IDs referenced in pathways exist in genes table
6. **URL consistency**: Checks download URL formatting (http/https/ftp patterns)
7. **Data completeness**: Reports coverage statistics for critical fields
   - Genome IDs and annotation URLs
   - EC numbers (focus on dehalogenases), GO terms, PDB IDs
   - Download URLs across all tables

**Output format**:
- ❌ **ERRORS**: Critical issues that fail validation (exit code 1)
- ⚠️ **WARNINGS**: Data quality issues that pass validation but need attention
- ℹ️ **INFO**: Statistics and coverage metrics

**Example usage**:
```bash
# Standard validation (warnings don't fail)
make validate-consistency

# Strict mode (warnings treated as errors)
uv run python src/validate_consistency.py --data-dir data/txt/sheet --strict
```

## ML Integration (KG-Microbe)

This project integrates with the KG-Microbe platform for ML-enabled PFAS biodegradation research:

### Training Data Categories

1. **Known PFAS degraders**: Microbes with demonstrated PFAS biodegradation
2. **Dechlorinating microbes**: Organisms with dehalogenases (potential C-F bond cleavage)
3. **Fluoride-resistant microbes**: Organisms with fluoride exporters and resistance genes
4. **Hydrocarbon degraders**: Microbes for cleaving C-C bonds in PFAS backbones
5. **PFAS-contaminated site isolates**: Environmental microbes from AFFF sites
6. **Co-occurrence patterns**: Microbial associations in PFAS-contaminated environments
7. **Similar organisms**: High similarity to categories 1-6

### Negative Controls
- Pristine environment microbes (no PFAS exposure)
- Human pathogens (filter housekeeping genes)

### Feature Extraction
- Dehalogenase genes (RdhA, DehH, DhaA, etc.)
- Fluoride exporters (CrcB, FEX)
- Hydrocarbon degradation pathways
- Reactive oxygen species production
- Metabolic co-dependencies
- Environmental metadata (pH, temperature, salinity, PFAS concentration)

### Model Outputs
- PFAS biodegradation potential scores
- Community design recommendations (3-5 members per consortium)
- Stability predictions (microbe-microbe interactions)
- Pathway completeness assessment

## Workflow Examples

### Complete Extension Workflow
```bash
# 1. Convert Excel to TSV (PFAS Data for AI.xlsx)
make convert-excel

# 2. Run basic extension (extend1) - search for PFAS-related data
make update-all

# 3. Run advanced extension (extend2)
make extend2
# This includes: PDF download → chemical/assay extension → PDF extraction → validation

# 4. Cross-reference publications with data
make extendbypub

# 5. Validate everything
make validate-consistency
make validate-schema

# 6. Check status
make status
```

### Merging Excel Updates
```bash
# Preview changes without applying
make merge-excel-dry-run

# Apply merge (backs up existing TSV files)
make merge-excel

# Validate after merge
make validate-consistency
```

### Individual Table Updates
```bash
# Update specific tables with custom source labels
uv run python src/chemical_search.py --source-label extend2  # PFAS compounds
uv run python src/assay_search.py --source-label extend2     # Fluoride/PFAS assays

# Extract data from a specific PDF directory
uv run python src/extract_from_documents.py --pdf-dir data/publications --output-dir data/txt/sheet
```

## Important Notes

- This repo uses Makefile for main commands (no justfile)
- No tests/ directory - tests are embedded as doctests or in src/ files
- No docs/ directory or mkdocs - documentation is in README.md and CLAUDE.md
- Python files are in src/ directly, not src/pfas_ai/ subdirectory
- NCBI Entrez.email should be set (currently "your.email@example.com")
- Data is initial seed data (6 organisms, 23 publications) - to be extended
- LinkML schema needs to be created for PFAS biodegradation domain
- **Source Provenance**: All extended data includes source column tracking data origin (extend1, extend2, DOI)
- **Publication Tracking**: Source columns can contain multiple references separated by `|` (e.g., `extend2|10.1016/j.jhazmat.2021.126361`)
- **Merge Strategy**: `merge-excel` backs up TSV files and intelligently merges schema changes while preserving extended rows
- **PFAS Focus**: Search terms and curated genes should prioritize PFAS biodegradation (dehalogenase, fluoride resistance, hydrocarbon degradation)

## Refactoring Checklist

Items to update from CMM-AI (lanthanides) to PFAS-AI:

- [x] CLAUDE.md - Updated with PFAS focus
- [ ] README.md - Update project description, tables, examples
- [ ] pyproject.toml - Update name from cmm-ai to pfas-ai
- [ ] Makefile - Update table names if needed (currently compatible)
- [ ] ncbi_search.py - Replace lanthanide search terms with PFAS terms
- [ ] gene_search.py - Update curated gene lists (dehalogenases, fluoride exporters)
- [ ] pathway_search.py - Focus on dehalogenation, fluoride pathways
- [ ] publication_search.py - Update search terms to PFAS-specific
- [ ] chemical_search.py - PFAS compound types and roles
- [ ] assay_search.py - Fluoride detection, PFAS quantification assays
- [ ] LinkML schema - Create schema/pfas_biodegradation.yaml
- [ ] Documentation strings - Update scientific context in all modules
