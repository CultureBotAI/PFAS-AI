# Makefile for CMM-AI data pipeline operations
# 
# This Makefile provides commands to update CMM data tables with lanthanide-relevant
# bacteria and archaea from NCBI databases.

.PHONY: help update-genomes update-biosamples update-pathways update-datasets update-genes update-structures update-publications update-chemicals update-assays update-bioprocesses update-screening update-protocols update-all clean install test validate-schema validate-consistency gen-linkml-models convert-pdfs-to-markdown extract-from-documents update-experimental-data download-pdfs extend2

# Default target
help:
	@echo "CMM-AI Data Pipeline Commands:"
	@echo "=============================="
	@echo ""
	@echo "Data Updates:"
	@echo "  update-genomes      - Update taxa and genomes table with NCBI data"
	@echo "  update-biosamples   - Update biosamples table with NCBI data"
	@echo "  update-pathways     - Update pathways table with KEGG/MetaCyc data"
	@echo "  update-datasets     - Update datasets table with database searches"
	@echo "  update-genes        - Update genes and proteins table with UniProt/KEGG"
	@echo "  update-structures   - Update macromolecular structures with PDB data"
	@echo "  update-publications - Update publications table with PubMed/arXiv"
	@echo ""
	@echo "Experimental Data Updates:"
	@echo "  update-chemicals    - Update chemicals table with PubChem/CHEBI"
	@echo "  update-assays       - Update assays table with curated protocols"
	@echo "  update-bioprocesses - (Manual) Update bioprocesses table"
	@echo "  update-screening    - (Manual) Update screening results table"
	@echo "  update-protocols    - (Manual) Update protocols table"
	@echo ""
	@echo "  update-all          - Update all tables (full pipeline)"
	@echo ""
	@echo "Utilities:"
	@echo "  install             - Install/sync dependencies with uv"
	@echo "  test                - Run tests and validation"
	@echo "  validate-schema     - Validate extended TSV data against LinkML schema"
	@echo "  validate-consistency - Validate cross-sheet referential integrity"
	@echo "  gen-linkml-models   - Generate Python dataclasses from LinkML schema"
	@echo "  download-pdfs       - Download PDFs from publications table URLs"
	@echo "  convert-pdfs-to-markdown - Convert PDFs to markdown format"
	@echo "  extract-from-documents - Extract experimental data from markdown files"
	@echo "  update-experimental-data - Full pipeline: PDF→markdown→extract→validate"
	@echo "  extend2             - Run full extend pipeline with source=extend2 label"
	@echo "  clean               - Remove temporary and output files"
	@echo "  convert-excel       - Convert Excel sheets to TSV files"
	@echo "  add-annotations     - Add annotation URLs to existing genomes table"
	@echo ""
	@echo "Files:"
	@echo "  Input:  data/txt/sheet/BER_CMM_Data_for_AI_taxa_and_genomes.tsv"
	@echo "  Input:  data/txt/sheet/BER_CMM_Data_for_AI_biosamples.tsv"
	@echo "  Input:  data/txt/sheet/BER_CMM_Data_for_AI_pathways.tsv"
	@echo "  Input:  data/txt/sheet/BER_CMM_Data_for_AI_datasets.tsv"
	@echo "  Input:  data/txt/sheet/BER_CMM_Data_for_AI_genes_and_proteins.tsv"
	@echo "  Input:  data/txt/sheet/BER_CMM_Data_for_AI_macromolecular_structures.tsv"
	@echo "  Input:  data/txt/sheet/BER_CMM_Data_for_AI_publications.tsv"
	@echo "  Output: data/txt/sheet/BER_CMM_Data_for_AI_*_extended.tsv"

# Install dependencies
install:
	@echo "Installing dependencies..."
	uv sync
	@echo "Dependencies installed successfully."

# Update taxa and genomes table with lanthanide-relevant organisms
update-genomes: install data/txt/sheet/BER_CMM_Data_for_AI_taxa_and_genomes.tsv
	@echo "Updating taxa and genomes table..."
	@echo "Searching NCBI for lanthanide-relevant bacteria and archaea..."
	uv run python extend_lanthanide_data.py
	@echo "Adding annotation download URLs..."
	uv run python add_annotation_urls.py
	@echo "Taxa and genomes table updated successfully."
	@echo "Output: data/txt/sheet/BER_CMM_Data_for_AI_taxa_and_genomes_extended.tsv"

# Update biosamples table with lanthanide-relevant samples
update-biosamples: install data/txt/sheet/BER_CMM_Data_for_AI_biosamples.tsv
	@echo "Updating biosamples table..."
	@echo "Searching NCBI for lanthanide-relevant biosamples..."
	uv run python extend_lanthanide_data.py
	@echo "Biosamples table updated successfully."
	@echo "Output: data/txt/sheet/BER_CMM_Data_for_AI_biosamples_extended.tsv"

# Update pathways table with lanthanide-relevant pathways
update-pathways: install data/txt/sheet/BER_CMM_Data_for_AI_pathways.tsv
	@echo "Updating pathways table..."
	@echo "Searching KEGG and MetaCyc for lanthanide-relevant pathways..."
	uv run python extend_pathways.py
	@echo "Pathways table updated successfully."
	@echo "Output: data/txt/sheet/BER_CMM_Data_for_AI_pathways_extended.tsv"

# Update datasets table with database searches  
update-datasets: install data/txt/sheet/BER_CMM_Data_for_AI_datasets.tsv
	@echo "Updating datasets table..."
	@echo "Searching multiple databases for lanthanide-relevant datasets..."
	uv run python extend_datasets.py
	@echo "Datasets table updated successfully."
	@echo "Output: data/txt/sheet/BER_CMM_Data_for_AI_datasets_extended.tsv"

# Update genes and proteins table with UniProt/KEGG data
update-genes: install data/txt/sheet/BER_CMM_Data_for_AI_genes_and_proteins.tsv
	@echo "Updating genes and proteins table..."
	@echo "Searching UniProt, KEGG and curated databases..."
	uv run python extend_genes.py
	@echo "Genes and proteins table updated successfully."
	@echo "Output: data/txt/sheet/BER_CMM_Data_for_AI_genes_and_proteins_extended.tsv"

# Update macromolecular structures table with PDB data
update-structures: install data/txt/sheet/BER_CMM_Data_for_AI_macromolecular_structures.tsv
	@echo "Updating macromolecular structures table..."
	@echo "Searching PDB and structural databases..."
	uv run python extend_structures.py
	@echo "Structures table updated successfully."
	@echo "Output: data/txt/sheet/BER_CMM_Data_for_AI_macromolecular_structures_extended.tsv"

# Update publications table with literature searches
update-publications: install data/txt/sheet/BER_CMM_Data_for_AI_publications.tsv
	@echo "Updating publications table..."
	@echo "Searching PubMed, arXiv, bioRxiv and curated literature..."
	uv run python extend_publications.py
	@echo "Publications table updated successfully."
	@echo "Output: data/txt/sheet/BER_CMM_Data_for_AI_publications_extended.tsv"

# Update chemicals table with PubChem/CHEBI data
update-chemicals: install data/txt/sheet/BER_CMM_Data_for_AI_chemicals.tsv
	@echo "Updating chemicals table with PubChem/CHEBI data..."
	uv run python src/chemical_search.py --source-label extend1
	@echo "Chemicals table updated successfully."
	@echo "Output: data/txt/sheet/BER_CMM_Data_for_AI_chemicals_extended.tsv"

# Update assays table with curated protocols
update-assays: install data/txt/sheet/BER_CMM_Data_for_AI_assays.tsv
	@echo "Updating assays table with curated assay protocols..."
	uv run python src/assay_search.py --source-label extend1
	@echo "Assays table updated successfully."
	@echo "Output: data/txt/sheet/BER_CMM_Data_for_AI_assays_extended.tsv"

# Download PDFs from publications table
download-pdfs: install
	@echo "Downloading PDFs from publications table..."
	@echo ""
	uv run python src/download_pdfs_from_publications.py
	@echo ""
	@echo "✓ PDF download completed!"
	@echo "  PDFs saved to: data/publications/"

# Update bioprocesses table (placeholder - manual data entry for now)
update-bioprocesses: install
	@echo "Bioprocesses table: Manual data entry"
	@echo "Template available at: data/txt/sheet/BER_CMM_Data_for_AI_bioprocesses.tsv"
	@echo "Note: Automated bioprocess data extraction not yet implemented"

# Update screening results table (placeholder - manual data entry for now)
update-screening: install
	@echo "Screening results table: Manual data entry"
	@echo "Template available at: data/txt/sheet/BER_CMM_Data_for_AI_screening_results.tsv"
	@echo "Note: Automated screening data import not yet implemented"

# Update protocols table (placeholder - manual data entry for now)
update-protocols: install
	@echo "Protocols table: Manual data entry"
	@echo "Template available at: data/txt/sheet/BER_CMM_Data_for_AI_protocols.tsv"
	@echo "Note: Automated protocols.io search not yet implemented"

# Update all tables (full pipeline)
update-all: update-genomes update-biosamples update-pathways update-datasets update-genes update-structures update-publications update-chemicals update-assays update-bioprocesses update-screening update-protocols
	@echo ""
	@echo "Full data pipeline completed successfully!"
	@echo "Updated files:"
	@echo "  - data/txt/sheet/BER_CMM_Data_for_AI_taxa_and_genomes_extended.tsv"
	@echo "  - data/txt/sheet/BER_CMM_Data_for_AI_biosamples_extended.tsv"
	@echo "  - data/txt/sheet/BER_CMM_Data_for_AI_pathways_extended.tsv"
	@echo "  - data/txt/sheet/BER_CMM_Data_for_AI_datasets_extended.tsv"
	@echo "  - data/txt/sheet/BER_CMM_Data_for_AI_genes_and_proteins_extended.tsv"
	@echo "  - data/txt/sheet/BER_CMM_Data_for_AI_macromolecular_structures_extended.tsv"
	@echo "  - data/txt/sheet/BER_CMM_Data_for_AI_publications_extended.tsv"
	@wc -l data/txt/sheet/BER_CMM_Data_for_AI_*_extended.tsv

# Convert Excel files to TSV (prerequisite step)
convert-excel: install
	@echo "Converting Excel files to TSV format..."
	@mkdir -p data/txt/plan data/txt/sheet data/txt/proposal data/txt/publications
	uv run python convert_sheets.py
	@echo "Excel files converted successfully."

# Add annotation URLs to existing genomes table
add-annotations: install data/txt/sheet/BER_CMM_Data_for_AI_taxa_and_genomes_extended.tsv
	@echo "Adding annotation download URLs to genomes table..."
	uv run python add_annotation_urls.py
	@echo "Annotation URLs added successfully."

# Run tests and validation
test: install
	@echo "Running tests and validation..."
	uv run python test_annotation_urls.py
	@echo "Running doctests..."
	uv run python -m doctest src/parsers.py -v
	uv run python -m doctest src/ncbi_search.py -v
	@echo "Tests completed."

# Generate LinkML Python dataclasses from schema
gen-linkml-models: install
	@echo "Generating Python dataclasses from LinkML schema..."
	uv run gen-python schema/lanthanide_bioprocessing.yaml > src/linkml_models.py
	@echo "Generated src/linkml_models.py successfully."

# Validate extended TSV data against LinkML schema
validate-schema: install gen-linkml-models
	@echo "Validating extended TSV data against LinkML schema..."
	@echo "Converting TSV files to LinkML YAML format..."
	uv run python src/tsv_to_linkml.py --data-dir data/txt/sheet --output data/linkml_database.yaml
	@echo ""
	@echo "Validating YAML data against schema..."
	uv run linkml-validate -s schema/lanthanide_bioprocessing.yaml data/linkml_database.yaml
	@echo ""
	@echo "✓ Validation completed successfully!"
	@echo "  Data file: data/linkml_database.yaml"
	@echo "  Schema: schema/lanthanide_bioprocessing.yaml"

# Validate cross-sheet consistency and referential integrity
validate-consistency: install
	@echo "Validating cross-sheet consistency and referential integrity..."
	@echo ""
	uv run python src/validate_consistency.py --data-dir data/txt/sheet
	@echo ""
	@echo "✓ Consistency validation completed!"

# Convert PDFs to markdown format
convert-pdfs-to-markdown: install
	@echo "Converting PDF publications to markdown..."
	@echo ""
	uv run python src/pdf_to_markdown.py --batch data/publications --output-dir data/publications
	@echo ""
	@echo "✓ PDF to markdown conversion completed!"

# Extract experimental data from markdown (converted from PDFs)
extract-from-documents: install convert-pdfs-to-markdown
	@echo ""
	@echo "Extracting experimental data from markdown files..."
	@echo ""
	uv run python src/extract_from_documents.py --pdf-dir data/publications --output-dir data/txt/sheet
	@echo ""
	@echo "✓ Extraction completed! Review extracted data in TSV files."
	@echo "  All extracted data labeled with source='extend2'"

# Combined workflow: extract data + validate + convert to LinkML
update-experimental-data: extract-from-documents validate-consistency validate-schema
	@echo ""
	@echo "============================================================"
	@echo "✓ Experimental data pipeline completed successfully!"
	@echo "============================================================"
	@echo ""
	@echo "Summary:"
	@echo "  1. Extracted data from PDFs in data/publications/"
	@echo "  2. Validated cross-sheet consistency"
	@echo "  3. Validated against LinkML schema"
	@echo ""
	@echo "Next steps:"
	@echo "  - Review extracted data for accuracy"
	@echo "  - Manually curate any uncertain entries"
	@echo "  - Run 'make status' to see updated file counts"

# extend2 workflow: Run full extend pipeline with source=extend2 label
extend2: install convert-excel
	@echo ""
	@echo "============================================================"
	@echo "EXTEND2 WORKFLOW - Second Round Data Extension"
	@echo "============================================================"
	@echo ""
	@echo "Step 1: Download PDFs from publications table..."
	@$(MAKE) download-pdfs
	@echo ""
	@echo "Step 2: Update chemicals with source=extend2..."
	@uv run python src/chemical_search.py --source-label extend2
	@echo ""
	@echo "Step 3: Update assays with source=extend2..."
	@uv run python src/assay_search.py --source-label extend2
	@echo ""
	@echo "Step 4: Process PDFs and extract data..."
	@$(MAKE) update-experimental-data
	@echo ""
	@echo "============================================================"
	@echo "✓ EXTEND2 WORKFLOW COMPLETED!"
	@echo "============================================================"
	@echo ""
	@echo "Summary:"
	@echo "  - Downloaded PDFs from publications"
	@echo "  - Extended chemicals with source=extend2"
	@echo "  - Extended assays with source=extend2"
	@echo "  - Extracted experimental data from PDFs with DOI sources"
	@echo "  - Validated all data"
	@echo ""
	@echo "Data provenance:"
	@echo "  - extend1 = Initial round (manual + database searches)"
	@echo "  - extend2 = Second round (this workflow)"
	@echo "  - DOI = Extracted from specific publications"

# Clean up temporary and output files
clean:
	@echo "Cleaning up temporary files..."
	rm -f *.log
	rm -f extend_lanthanide_data.py
	rm -f add_annotation_urls.py 
	rm -f test_annotation_urls.py
	rm -f convert_sheets.py
	@echo "Cleanup completed."

# Clean extended output files (use with caution)
clean-extended:
	@echo "WARNING: This will delete extended data files!"
	@echo "Press Ctrl+C within 5 seconds to cancel..."
	@sleep 5
	rm -f data/txt/sheet/BER_CMM_Data_for_AI_*_extended.tsv
	@echo "Extended files removed."

# Check that input files exist
data/txt/sheet/BER_CMM_Data_for_AI_taxa_and_genomes.tsv:
	@echo "Error: Input file not found: $@"
	@echo "Please run 'make convert-excel' first to convert Excel files to TSV."
	@exit 1

data/txt/sheet/BER_CMM_Data_for_AI_biosamples.tsv:
	@echo "Error: Input file not found: $@"
	@echo "Please run 'make convert-excel' first to convert Excel files to TSV."
	@exit 1

data/txt/sheet/BER_CMM_Data_for_AI_pathways.tsv:
	@echo "Error: Input file not found: $@"
	@echo "Please run 'make convert-excel' first to convert Excel files to TSV."
	@exit 1

data/txt/sheet/BER_CMM_Data_for_AI_datasets.tsv:
	@echo "Error: Input file not found: $@"
	@echo "Please run 'make convert-excel' first to convert Excel files to TSV."
	@exit 1

data/txt/sheet/BER_CMM_Data_for_AI_genes_and_proteins.tsv:
	@echo "Error: Input file not found: $@"
	@echo "Please run 'make convert-excel' first to convert Excel files to TSV."
	@exit 1

data/txt/sheet/BER_CMM_Data_for_AI_macromolecular_structures.tsv:
	@echo "Error: Input file not found: $@"
	@echo "Please run 'make convert-excel' first to convert Excel files to TSV."
	@exit 1

data/txt/sheet/BER_CMM_Data_for_AI_publications.tsv:
	@echo "Error: Input file not found: $@"
	@echo "Please run 'make convert-excel' first to convert Excel files to TSV."
	@exit 1

data/txt/sheet/BER_CMM_Data_for_AI_taxa_and_genomes_extended.tsv:
	@echo "Error: Extended genomes file not found: $@"
	@echo "Please run 'make update-genomes' first to create extended table."
	@exit 1

# Show current data status
status:
	@echo "CMM-AI Data Pipeline Status:"
	@echo "============================"
	@echo ""
	@echo "Input files:"
	@if [ -f "data/txt/sheet/BER_CMM_Data_for_AI_taxa_and_genomes.tsv" ]; then \
		echo "  ✓ Taxa and genomes TSV exists ($$(wc -l < data/txt/sheet/BER_CMM_Data_for_AI_taxa_and_genomes.tsv) lines)"; \
	else \
		echo "  ✗ Taxa and genomes TSV missing"; \
	fi
	@if [ -f "data/txt/sheet/BER_CMM_Data_for_AI_biosamples.tsv" ]; then \
		echo "  ✓ Biosamples TSV exists ($$(wc -l < data/txt/sheet/BER_CMM_Data_for_AI_biosamples.tsv) lines)"; \
	else \
		echo "  ✗ Biosamples TSV missing"; \
	fi
	@if [ -f "data/txt/sheet/BER_CMM_Data_for_AI_pathways.tsv" ]; then \
		echo "  ✓ Pathways TSV exists ($$(wc -l < data/txt/sheet/BER_CMM_Data_for_AI_pathways.tsv) lines)"; \
	else \
		echo "  ✗ Pathways TSV missing"; \
	fi
	@if [ -f "data/txt/sheet/BER_CMM_Data_for_AI_datasets.tsv" ]; then \
		echo "  ✓ Datasets TSV exists ($$(wc -l < data/txt/sheet/BER_CMM_Data_for_AI_datasets.tsv) lines)"; \
	else \
		echo "  ✗ Datasets TSV missing"; \
	fi
	@if [ -f "data/txt/sheet/BER_CMM_Data_for_AI_genes_and_proteins.tsv" ]; then \
		echo "  ✓ Genes and proteins TSV exists ($$(wc -l < data/txt/sheet/BER_CMM_Data_for_AI_genes_and_proteins.tsv) lines)"; \
	else \
		echo "  ✗ Genes and proteins TSV missing"; \
	fi
	@if [ -f "data/txt/sheet/BER_CMM_Data_for_AI_macromolecular_structures.tsv" ]; then \
		echo "  ✓ Structures TSV exists ($$(wc -l < data/txt/sheet/BER_CMM_Data_for_AI_macromolecular_structures.tsv) lines)"; \
	else \
		echo "  ✗ Structures TSV missing"; \
	fi
	@if [ -f "data/txt/sheet/BER_CMM_Data_for_AI_publications.tsv" ]; then \
		echo "  ✓ Publications TSV exists ($$(wc -l < data/txt/sheet/BER_CMM_Data_for_AI_publications.tsv) lines)"; \
	else \
		echo "  ✗ Publications TSV missing"; \
	fi
	@echo ""
	@echo "Extended files:"
	@if [ -f "data/txt/sheet/BER_CMM_Data_for_AI_taxa_and_genomes_extended.tsv" ]; then \
		echo "  ✓ Extended taxa and genomes exists ($$(wc -l < data/txt/sheet/BER_CMM_Data_for_AI_taxa_and_genomes_extended.tsv) lines)"; \
	else \
		echo "  ✗ Extended taxa and genomes missing"; \
	fi
	@if [ -f "data/txt/sheet/BER_CMM_Data_for_AI_biosamples_extended.tsv" ]; then \
		echo "  ✓ Extended biosamples exists ($$(wc -l < data/txt/sheet/BER_CMM_Data_for_AI_biosamples_extended.tsv) lines)"; \
	else \
		echo "  ✗ Extended biosamples missing"; \
	fi
	@if [ -f "data/txt/sheet/BER_CMM_Data_for_AI_pathways_extended.tsv" ]; then \
		echo "  ✓ Extended pathways exists ($$(wc -l < data/txt/sheet/BER_CMM_Data_for_AI_pathways_extended.tsv) lines)"; \
	else \
		echo "  ✗ Extended pathways missing"; \
	fi
	@if [ -f "data/txt/sheet/BER_CMM_Data_for_AI_datasets_extended.tsv" ]; then \
		echo "  ✓ Extended datasets exists ($$(wc -l < data/txt/sheet/BER_CMM_Data_for_AI_datasets_extended.tsv) lines)"; \
	else \
		echo "  ✗ Extended datasets missing"; \
	fi
	@if [ -f "data/txt/sheet/BER_CMM_Data_for_AI_genes_and_proteins_extended.tsv" ]; then \
		echo "  ✓ Extended genes and proteins exists ($$(wc -l < data/txt/sheet/BER_CMM_Data_for_AI_genes_and_proteins_extended.tsv) lines)"; \
	else \
		echo "  ✗ Extended genes and proteins missing"; \
	fi
	@if [ -f "data/txt/sheet/BER_CMM_Data_for_AI_macromolecular_structures_extended.tsv" ]; then \
		echo "  ✓ Extended structures exists ($$(wc -l < data/txt/sheet/BER_CMM_Data_for_AI_macromolecular_structures_extended.tsv) lines)"; \
	else \
		echo "  ✗ Extended structures missing"; \
	fi
	@if [ -f "data/txt/sheet/BER_CMM_Data_for_AI_publications_extended.tsv" ]; then \
		echo "  ✓ Extended publications exists ($$(wc -l < data/txt/sheet/BER_CMM_Data_for_AI_publications_extended.tsv) lines)"; \
	else \
		echo "  ✗ Extended publications missing"; \
	fi
	@echo ""
	@echo "Experimental data files:"
	@if [ -f "data/txt/sheet/BER_CMM_Data_for_AI_chemicals.tsv" ]; then \
		echo "  ✓ Chemicals TSV exists ($$(wc -l < data/txt/sheet/BER_CMM_Data_for_AI_chemicals.tsv) lines)"; \
	else \
		echo "  ✗ Chemicals TSV missing"; \
	fi
	@if [ -f "data/txt/sheet/BER_CMM_Data_for_AI_assays.tsv" ]; then \
		echo "  ✓ Assays TSV exists ($$(wc -l < data/txt/sheet/BER_CMM_Data_for_AI_assays.tsv) lines)"; \
	else \
		echo "  ✗ Assays TSV missing"; \
	fi
	@if [ -f "data/txt/sheet/BER_CMM_Data_for_AI_bioprocesses.tsv" ]; then \
		echo "  ✓ Bioprocesses TSV exists ($$(wc -l < data/txt/sheet/BER_CMM_Data_for_AI_bioprocesses.tsv) lines)"; \
	else \
		echo "  ✗ Bioprocesses TSV missing"; \
	fi
	@if [ -f "data/txt/sheet/BER_CMM_Data_for_AI_screening_results.tsv" ]; then \
		echo "  ✓ Screening results TSV exists ($$(wc -l < data/txt/sheet/BER_CMM_Data_for_AI_screening_results.tsv) lines)"; \
	else \
		echo "  ✗ Screening results TSV missing"; \
	fi
	@if [ -f "data/txt/sheet/BER_CMM_Data_for_AI_protocols.tsv" ]; then \
		echo "  ✓ Protocols TSV exists ($$(wc -l < data/txt/sheet/BER_CMM_Data_for_AI_protocols.tsv) lines)"; \
	else \
		echo "  ✗ Protocols TSV missing"; \
	fi