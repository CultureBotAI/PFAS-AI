# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository Overview

PFAS-AI - ML-enabled automated data pipeline for PFAS biodegradation research. Extends small seed datasets (6 organisms, 23 publications) into comprehensive research databases by integrating NCBI, KEGG, UniProt, PDB, and other biological databases.

**Scientific Focus**: Per- and polyfluoroalkyl substances (PFAS) biodegradation using machine learning-guided microbial consortia design.

**Key Research Targets**:
- C-F bond cleavage enzymes (dehalogenases, defluorinases)
- Fluoride resistance mechanisms (CrcB, FEX transporters)
- Hydrocarbon-degrading microbes for PFAS backbone metabolism
- Dechlorinating microbes with potential C-F bond cleavage activity

## Commands

### Dependency Management
**Always use `uv`** for managing dependencies. Never use `pip`.
- `uv sync` or `make install` - Install dependencies
- `uv run <command>` - Run commands in project environment

### Pipeline Commands (via Makefile)

**Basic Workflow**:
```bash
make convert-excel       # Excel → TSV (prerequisite)
make update-all          # Extend all tables (extend1)
make extend2             # Advanced: PDF download → data extraction
make extendbypub         # Cross-reference publications
make status              # Check pipeline status
```

**Individual Table Extensions** (extend1):
- `make update-genomes` - NCBI Assembly/BioSample for PFAS microbes
- `make update-pathways` - KEGG/MetaCyc dehalogenation pathways
- `make update-genes` - UniProt/KEGG dehalogenases and fluoride exporters
- `make update-structures` - PDB structures for dehalogenases
- `make update-publications` - PubMed/arXiv PFAS literature
- `make update-datasets` - Multi-repository dataset search
- `make update-chemicals` - PubChem/CHEBI PFAS compounds
- `make update-assays` - Fluoride/PFAS detection protocols
- `make update-reactions` - RHEA/KEGG biochemical reactions
- `make update-transcriptomics` - SRA/GEO RNA-seq datasets
- `make update-strains` - Culture collection IDs and procurement
- `make update-media` - Growth media formulations

**Reaction Data Management**:
- `make merge-reactions` - Merge PFAS_Reactions category files (static reference data, 113 reactions)
- Note: PFAS_Reactions_* files in `data/txt/sheet/PFAS_Reactions/` are static reference data
- New reactions extend main `reactions_extended.tsv` only (no category-specific extensions)

**KG-Microbe Integration**:
- `make create-kg-db` - Create DuckDB knowledge graph from TSV files
- `make query-kg-db` - Query knowledge graph (see data/kgm/README.md for API)

**Data Management**:
- `make merge-excel` - Merge Excel updates while preserving generated data
- `make merge-excel-dry-run` - Preview merge without applying

### Testing and Validation
```bash
make test                   # Run doctests and validation
make validate-schema        # Validate against LinkML schema
make validate-consistency   # Cross-sheet referential integrity
uv run ruff check src/      # Linting
uv run ruff format src/     # Code formatting
```

## Architecture

### Directory Structure
```
src/                      # Flat Python module structure (NO src/pfas_ai/ subdirectory)
  parsers.py             # Excel/Word/PDF converters with filename sanitization
  ncbi_search.py         # NCBI Assembly/BioSample search + annotation URL generation
  *_search.py            # Database-specific search modules (pathway, gene, structure, etc.)
  extend_*.py            # Pipeline automation scripts
  validate_consistency.py # Cross-sheet validation with fuzzy organism matching
  tsv_to_linkml.py       # TSV → LinkML YAML converter
  merge_excel_updates.py # Intelligent Excel merge preserving generated data
  extend_by_publication.py # Publication cross-reference with keyword matching
  kg_analysis/           # KG-Microbe DuckDB integration
    kg_database.py       # Knowledge graph database operations
schema/
  pfas_biodegradation.yaml # LinkML schema (13 classes: genomes, genes, reactions, etc.)
data/
  sheet/                 # Original Excel: "PFAS Data for AI.xlsx"
  txt/sheet/             # Converted TSV + *_extended.tsv files
    PFAS_Reactions/      # Static reference: category-specific reaction files (not extended)
  publications/          # Downloaded PDFs
  kgm/                   # KG-Microbe TSV files and kg-microbe.duckdb
Makefile                 # Pipeline automation (NO justfile)
```

### Data Pipeline Architecture

**Two-Phase Extension Model**:

1. **extend1 (Database Enrichment)**: Query external APIs to find related data
   - Input: Seed TSV files (6 organisms, 23 publications)
   - Process: Search NCBI, KEGG, UniProt, PDB with PFAS-specific terms
   - Output: Extended TSV files with `source=extend1`
   - URL Generation: Direct download links for all resources

2. **extend2 (Document Extraction)**: Extract experimental data from publications
   - Input: Publication URLs from publications table
   - Process: Download PDFs → convert to markdown → extract data
   - Output: Additional rows in chemicals, assays, bioprocesses with `source=extend2` or DOI
   - Cross-Reference: `extendbypub` appends publication IDs to source column with `|` delimiter

**Source Provenance System**:
All extended rows include a `source` column:
- `extend1` - Initial database search extension
- `extend2` - Second round PDF extraction
- DOI (e.g., `10.1016/j.jhazmat.2021.126361`) - Extracted from specific papers
- Combined (e.g., `extend2|10.1016/j.jhazmat.2021.126361`) - After cross-referencing

### Key Architectural Patterns

**Filename Sanitization**: All output files use `sanitize_filename()` (spaces → underscores)

**Rate Limiting**: 0.5-1.0 sec delays between API calls throughout codebase

**Deduplication**: Each search module removes duplicates based on unique IDs

**URL Generation**:
- NCBI: FTP URLs for genome annotations via `get_annotation_download_url()`
- BioSample: Direct links to SRA data via `get_biosample_download_url()`
- All databases: Construct valid download URLs, not just landing pages

**Reaction Categories**: Reactions table includes `reaction_category` column (from PFAS_Reactions reference data):
- `dehalogenase` - C-F bond cleavage (16 reactions)
- `fluoride_resistance` - Fluoride transport (38 reactions)
- `hydrocarbon_degradation` - Alkane metabolism (19 reactions)
- `known_pfas_degraders` - Validated PFAS degraders (11 reactions)
- `oxygenase_cometabolism` - Oxygenase pathways (29 reactions)
- `important_genes` - Non-enzymatic genes (3 entries)
- Category files are in `data/txt/sheet/PFAS_Reactions/` as static reference (not extended)

**Data Validation** (two independent levels):
1. **Schema Validation**: TSV → YAML → LinkML schema validation (types, patterns, ontology terms)
2. **Cross-Sheet Consistency**: Referential integrity with fuzzy genus-level matching for organism names

### Module Organization

**Core Utilities** (`parsers.py`):
- `xlsx_to_tsv()`, `docx_to_text()`, `pdf_to_text()`
- All functions sanitize filenames and use pandas for TSV I/O

**Search Modules** (`*_search.py`):
Each database integration follows the same pattern:
- Query API with PFAS-specific search terms
- Extract structured data
- Generate download URLs
- Return pandas DataFrame

**Extension Scripts** (`extend_*.py`):
Pipeline automation that:
1. Reads seed TSV file
2. Calls appropriate search module
3. Deduplicates and merges results
4. Writes `*_extended.tsv` with source column

**Advanced Workflows**:
- `merge_excel_updates.py`: 3-way merge (Excel + base TSV + extended TSV) with backup
- `extend_by_publication.py`: Keyword-based publication matching across sheets
- `validate_consistency.py`: Cross-table validation with warnings (⚠️) and errors (❌)

### PFAS-Specific Search Terms

**Chemical Terms**: PFAS, perfluorinated, polyfluorinated, PFOA, PFOS, AFFF, C-F bond, defluorination, fluoride

**Functional Terms**: Dehalogenase, defluorinase, fluoroacetate dehalogenase, reductive dehalogenase (RdhA), haloalkane dehalogenase, fluoride exporter (CrcB, FEX)

**Organisms**: Pseudomonas, Hyphomicrobium, Acidimicrobium, Dehalococcoides, Desulfitobacterium, Rhodococcus, Mycobacterium

**Environments**: PFAS-contaminated sites, AFFF-impacted groundwater, wastewater treatment

## LinkML Schema

**Schema Location**: `schema/pfas_biodegradation.yaml`

**13 Main Classes**:
- **Core (7)**: GenomeRecord, BiosampleRecord, PathwayRecord, GeneProteinRecord, MacromolecularStructureRecord, PublicationRecord, DatasetRecord
- **Experimental (6)**: ReactionRecord, ChemicalCompoundRecord, AssayMeasurementRecord, BioprocessConditionsRecord, ScreeningResultRecord, ProtocolRecord
- **New (3)**: TranscriptomicsRecord, StrainRecord, GrowthMediaRecord, MediaIngredientRecord

**Ontology Mappings**: NCBITaxon, SRA, CHEBI, ENVO, MIXS, UniProtKB, GO, EC, RHEA, KEGG, PDB, OBI, BAO, PubChem

**Using LinkML Tools**:
```bash
make validate-schema     # Complete workflow: TSV→YAML→validate
make gen-linkml-models   # Generate src/linkml_models.py from schema

# Manual commands:
uv run gen-python schema/pfas_biodegradation.yaml > src/linkml_models.py
uv run gen-json-schema schema/pfas_biodegradation.yaml > schema/schema.json
uv run python src/tsv_to_linkml.py --data-dir data/txt/sheet --output data/linkml_database.yaml
uv run linkml-validate -s schema/pfas_biodegradation.yaml data/linkml_database.yaml
```

## Development Principles

### Testing
- Use doctests liberally (see `parsers.py`, `ncbi_search.py` for examples)
- pytest functional style (NOT unittest OO)
- Mark external API tests with `@pytest.mark.integration`
- **Never write mock tests** unless explicitly requested
- Don't weaken test conditions - fix the underlying issue

### Code Style
- Always use type hints
- Document with docstrings (Google style)
- Pydantic/LinkML for data objects, dataclasses for OO state
- **Fail fast** - avoid try/except that masks bugs
- DRY principle, but avoid premature abstraction

### API Integration
- Respect rate limits (0.5-1.0 sec delays via `time.sleep()`)
- Handle missing/malformed data gracefully
- Generate **valid download URLs**, not just landing pages
- Use `Bio.Entrez` for NCBI (requires `Entrez.email` configuration)

### File Handling
- Sanitize all output filenames via `sanitize_filename()`
- Use pandas for TSV: `pd.read_csv(sep='\t')`, `df.to_csv(sep='\t')`
- Output files: `data/txt/sheet/PFAS_Data_for_AI_*_extended.tsv`
- Input Excel: `data/sheet/PFAS Data for AI.xlsx`

## KG-Microbe Integration

This project integrates with KG-Microbe platform for ML-enabled discovery:

**Database Location**: `data/kgm/kg-microbe.duckdb` (created from TSV files)

**Training Categories**:
1. Known PFAS degraders
2. Dechlorinating microbes (dehalogenases)
3. Fluoride-resistant microbes (CrcB, FEX)
4. Hydrocarbon degraders
5. PFAS-contaminated site isolates

**Feature Extraction**:
- Dehalogenase genes (RdhA, DehH, DhaA)
- Fluoride exporters (CrcB, FEX)
- Hydrocarbon degradation pathways
- Environmental metadata (pH, temperature, PFAS concentration)

**Usage**: See `data/kgm/README.md` for Python API examples

## Important Notes

- **Repo uses Makefile**, not justfile
- **No tests/ directory** - tests are embedded as doctests or in src/
- **No docs/ directory** - documentation in README.md and CLAUDE.md
- **Flat src/ structure** - Python files in src/ directly, NOT src/pfas_ai/
- **NCBI Entrez.email** should be configured (currently "your.email@example.com")
- **Source Provenance**: All extended data tracked via source column (extend1, extend2, DOI)
- **Publication Tracking**: Source columns support `|` delimiter for multiple references
- **Merge Strategy**: `merge-excel` backs up TSV files before intelligent merge
- **Data is extensible**: Started with 6 organisms, designed to grow to 100+

## Common Workflows

### Complete Extension Pipeline
```bash
make convert-excel        # 1. Excel → TSV
make update-all           # 2. Extend all tables (extend1)
make extend2              # 3. PDF download → extraction (extend2)
make extendbypub          # 4. Cross-reference publications
make validate-consistency # 5. Validate data
make validate-schema      # 6. Validate against LinkML
make status               # 7. Check results
```

### Update Specific Tables
```bash
# With custom source labels:
uv run python src/chemical_search.py --source-label extend2
uv run python src/assay_search.py --source-label extend2

# Extract from specific PDF directory:
uv run python src/extract_from_documents.py --pdf-dir data/publications --output-dir data/txt/sheet
```

### Merge Excel Updates
```bash
make merge-excel-dry-run  # Preview changes
make merge-excel          # Apply merge (creates backups)
make validate-consistency # Validate after merge
```

### Knowledge Graph Operations
```bash
# Create DuckDB database from TSV files
make create-kg-db

# Query via Python API (see data/kgm/README.md):
from src.kg_analysis.kg_database import KGDatabase
kg = KGDatabase('data/kgm/kg-microbe.duckdb')
results = kg.query("SELECT * FROM nodes WHERE category='Genome'")
```
