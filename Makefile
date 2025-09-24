# Makefile for CMM-AI data pipeline operations
# 
# This Makefile provides commands to update CMM data tables with lanthanide-relevant
# bacteria and archaea from NCBI databases.

.PHONY: help update-genomes update-biosamples update-pathways update-datasets update-genes update-structures update-publications update-all clean install test

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
	@echo "  update-all          - Update all tables (full pipeline)"
	@echo ""
	@echo "Utilities:"
	@echo "  install           - Install/sync dependencies with uv"
	@echo "  test              - Run tests and validation"
	@echo "  clean             - Remove temporary and output files"
	@echo "  convert-excel     - Convert Excel sheets to TSV files"
	@echo "  add-annotations   - Add annotation URLs to existing genomes table"
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

# Update all tables (full pipeline)
update-all: update-genomes update-biosamples update-pathways update-datasets update-genes update-structures update-publications
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
	uv run python -m doctest src/cmm_ai/parsers.py -v
	uv run python -m doctest src/cmm_ai/ncbi_search.py -v
	@echo "Tests completed."

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