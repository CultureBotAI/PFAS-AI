# Makefile for PFAS-AI data pipeline operations
#
# This Makefile provides commands to update PFAS data tables with PFAS-degrading
# bacteria and archaea from NCBI databases.

.PHONY: help update-genomes update-biosamples update-pathways update-datasets update-genes update-structures update-publications update-uniprot extend-from-pfas-degraders mine-proteins update-chemicals update-assays update-reactions merge-reactions update-bioprocesses update-screening update-protocols update-transcriptomics update-strains update-media update-all clean install test validate-schema validate-consistency fix-validation gen-linkml-models convert-pdfs-to-markdown extract-from-documents update-experimental-data download-pdfs extend2 extend-api kg-update kg-update-genes kg-update-pathways kg-update-chemicals kg-update-genomes kg-update-all crosslink annotate-kg extendbypub merge-excel merge-excel-dry-run compare-excel compare-excel-tsv report-missing-pdfs create-kg-db query-kg-db status

# Default target
help:
	@echo "PFAS-AI Data Pipeline Commands:"
	@echo "=============================="
	@echo ""
	@echo "Data Updates:"
	@echo "  update-genomes      - Update taxa and genomes table with NCBI data"
	@echo "  update-biosamples   - Update biosamples table with NCBI data"
	@echo "  update-pathways     - Update pathways table with KEGG/MetaCyc data"
	@echo "  update-datasets     - Update datasets table with database searches"
	@echo "  update-transcriptomics - Update transcriptomics table with SRA/GEO/ArrayExpress data"
	@echo "  update-strains      - Update strains table with culture collection IDs"
	@echo "  update-media        - Update growth media and media ingredients tables"
	@echo "  update-genes        - Update genes and proteins table with UniProt/KEGG"
	@echo "  update-structures   - Update macromolecular structures with PDB data"
	@echo "  update-publications - Update publications table with PubMed/arXiv"
	@echo "  update-uniprot      - Comprehensive UniProt integration (all tables)"
	@echo "  extend-from-pfas-degraders - Extend tables using PFAS-degrading proteins as seeds"
	@echo "  mine-proteins       - Mine extended proteins for pathways/chemicals/pubs"
	@echo ""
	@echo "Experimental Data Updates:"
	@echo "  update-chemicals    - Update chemicals table with PubChem/CHEBI"
	@echo "  update-assays       - Update assays table with curated protocols"
	@echo "  update-reactions    - Update reactions table with RHEA/KEGG data"
	@echo "  merge-reactions     - Merge PFAS_Reactions category files (static reference data)"
	@echo ""
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
	@echo "  fix-validation      - Automatically fix validation issues (IDs, URLs)"
	@echo "  gen-linkml-models   - Generate Python dataclasses from LinkML schema"
	@echo "  download-pdfs       - Download PDFs from publications table URLs"
	@echo "  convert-pdfs-to-markdown - Convert PDFs to markdown format"
	@echo "  extract-from-documents - Extract experimental data from markdown files"
	@echo "  update-experimental-data - Full pipeline: PDF→markdown→extract→validate"
	@echo "  extend2             - Run full extend pipeline with source=extend2 label"
	@echo "  extend-api          - Run API-based extensions (ROUND=3 default, repeatable)"
	@echo ""
	@echo "Knowledge Graph Updates (repeatable):"
	@echo "  kg-update           - Update all tables from Knowledge Graph databases"
	@echo "  kg-update-all       - Same as kg-update (comprehensive KG mining)"
	@echo "  kg-update-genes     - Update genes/proteins from function KG"
	@echo "  kg-update-pathways  - Update pathways from function KG"
	@echo "  kg-update-chemicals - Update chemicals from function KG"
	@echo "  kg-update-genomes   - Update taxa/genomes from both KGs"
	@echo "  annotate-kg         - Annotate existing rows with KG node identifiers"
	@echo ""
	@echo "Cross-Linking & References:"
	@echo "  crosslink           - Cross-link related data across sheets (genes→genomes, etc.)"
	@echo "  extendbypub         - Cross-reference publications with data sheets"
	@echo "  compare-excel       - Compare current and last Excel files for differences"
	@echo "  compare-excel-tsv   - Compare Excel file with existing TSV files"
	@echo "  report-missing-pdfs - Generate report of missing publication PDFs"
	@echo "  merge-excel         - Merge Excel updates while preserving generated data"
	@echo "  merge-excel-dry-run - Preview Excel merge without applying changes"
	@echo "  create-kg-db        - Create DuckDB knowledge graph database"
	@echo "  query-kg-db         - Run example knowledge graph queries"
	@echo "  clean               - Remove temporary and output files"
	@echo "  convert-excel       - Convert Excel sheets to TSV files"
	@echo "  add-annotations     - Add annotation URLs to existing genomes table"
	@echo ""
	@echo "Files:"
	@echo "  Input:  data/txt/sheet/PFAS_Data_for_AI_taxa_and_genomes.tsv"
	@echo "  Input:  data/txt/sheet/PFAS_Data_for_AI_biosamples.tsv"
	@echo "  Input:  data/txt/sheet/PFAS_Data_for_AI_pathways.tsv"
	@echo "  Input:  data/txt/sheet/PFAS_Data_for_AI_datasets.tsv"
	@echo "  Input:  data/txt/sheet/PFAS_Data_for_AI_genes_and_proteins.tsv"
	@echo "  Input:  data/txt/sheet/PFAS_Data_for_AI_macromolecular_structures.tsv"
	@echo "  Input:  data/txt/sheet/PFAS_Data_for_AI_publications.tsv"
	@echo "  Output: data/txt/sheet/PFAS_Data_for_AI_*_extended.tsv"

# Install dependencies
install:
	@echo "Installing dependencies..."
	uv sync
	@echo "Dependencies installed successfully."

# Update taxa and genomes table with PFAS-relevant organisms
update-genomes: install data/txt/sheet/PFAS_Data_for_AI_taxa_and_genomes.tsv
	@echo "Updating taxa and genomes table..."
	@echo "Searching NCBI for PFAS-relevant bacteria and archaea..."
	uv run python src/extend_pfas_data.py
	@echo "Adding annotation download URLs..."
	uv run python src/add_annotation_urls.py
	@echo "Taxa and genomes table updated successfully."
	@echo "Output: data/txt/sheet/PFAS_Data_for_AI_taxa_and_genomes_extended.tsv"

# Update biosamples table with PFAS-relevant samples
update-biosamples: install data/txt/sheet/PFAS_Data_for_AI_biosamples.tsv
	@echo "Updating biosamples table..."
	@echo "Searching NCBI for PFAS-relevant biosamples..."
	uv run python src/extend_pfas_data.py
	@echo "Biosamples table updated successfully."
	@echo "Output: data/txt/sheet/PFAS_Data_for_AI_biosamples_extended.tsv"

# Update pathways table with PFAS-relevant pathways
update-pathways: install data/txt/sheet/PFAS_Data_for_AI_pathways.tsv
	@echo "Updating pathways table..."
	@echo "Searching KEGG and MetaCyc for PFAS-relevant pathways..."
	uv run python src/extend_pathways.py
	@echo "Pathways table updated successfully."
	@echo "Output: data/txt/sheet/PFAS_Data_for_AI_pathways_extended.tsv"

# Update datasets table with database searches
update-datasets: install data/txt/sheet/PFAS_Data_for_AI_datasets.tsv
	@echo "Updating datasets table..."
	@echo "Searching multiple databases for PFAS-relevant datasets..."
	uv run python src/extend_datasets.py
	@echo "Datasets table updated successfully."
	@echo "Output: data/txt/sheet/PFAS_Data_for_AI_datasets_extended.tsv"

# Update transcriptomics table with SRA/GEO/ArrayExpress searches
update-transcriptomics: install data/txt/sheet/PFAS_Data_for_AI_transcriptomics.tsv
	@echo "Updating transcriptomics table..."
	@echo "Searching NCBI SRA, GEO, and ArrayExpress for RNA-seq datasets..."
	uv run python src/extend_transcriptomics.py
	@echo "Transcriptomics table updated successfully."
	@echo "Output: data/txt/sheet/PFAS_Data_for_AI_transcriptomics_extended.tsv"

# Update strains table with culture collection and procurement information
update-strains: install data/txt/sheet/PFAS_Data_for_AI_strains.tsv
	@echo "Updating strains table..."
	@echo "Querying KG-Microbe, NCBI Taxonomy, and BacDive for strain information..."
	uv run python src/extend_strains.py
	@echo "Strains table updated successfully."
	@echo "Output: data/txt/sheet/PFAS_Data_for_AI_strains_extended.tsv"

# Update growth media and media ingredients tables with curated formulations
update-media: install data/txt/sheet/PFAS_Data_for_AI_growth_media.tsv data/txt/sheet/PFAS_Data_for_AI_media_ingredients.tsv
	@echo "Creating curated growth media and ingredients tables..."
	@echo "Data sources: ATCC, DSMZ, and literature formulations..."
	uv run python src/extend_media.py
	@echo "Growth media tables updated successfully."
	@echo "Output: data/txt/sheet/PFAS_Data_for_AI_growth_media_extended.tsv"
	@echo "Output: data/txt/sheet/PFAS_Data_for_AI_media_ingredients_extended.tsv"

# Update genes and proteins table with UniProt/KEGG data
update-genes: install data/txt/sheet/PFAS_Data_for_AI_genes_and_proteins.tsv
	@echo "Updating genes and proteins table..."
	@echo "Searching UniProt, KEGG and curated databases..."
	uv run python src/extend_genes.py
	@echo "Genes and proteins table updated successfully."
	@echo "Output: data/txt/sheet/PFAS_Data_for_AI_genes_and_proteins_extended.tsv"

# Update macromolecular structures table with PDB data
update-structures: install data/txt/sheet/PFAS_Data_for_AI_macromolecular_structures.tsv
	@echo "Updating macromolecular structures table..."
	@echo "Searching PDB and structural databases..."
	uv run python src/extend_structures.py
	@echo "Structures table updated successfully."
	@echo "Output: data/txt/sheet/PFAS_Data_for_AI_macromolecular_structures_extended.tsv"

# Update publications table with literature searches
update-publications: install data/txt/sheet/PFAS_Data_for_AI_publications.tsv
	@echo "Updating publications table..."
	@echo "Searching PubMed, arXiv, bioRxiv and curated literature..."
	uv run python src/extend_publications.py
	@echo "Publications table updated successfully."
	@echo "Output: data/txt/sheet/PFAS_Data_for_AI_publications_extended.tsv"

# Comprehensive UniProt API integration across all tables
update-uniprot: install
	@echo "=========================================="
	@echo "UniProt API Integration - All Tables"
	@echo "=========================================="
	@echo ""
	@echo "This will extend the following tables with UniProt data:"
	@echo "  - Genes and proteins (comprehensive annotations)"
	@echo "  - Biological functions (EC, GO, Rhea, pathways, CHEBI)"
	@echo "  - Chemicals (CHEBI compounds)"
	@echo "  - Pathways (KEGG, Reactome, UniPathway)"
	@echo "  - Publications (literature citations)"
	@echo ""
	uv run python -m src.extend_uniprot
	@echo ""
	@echo "✓ UniProt integration completed!"
	@echo ""
	@echo "Output files:"
	@echo "  - data/txt/sheet/PFAS_Data_for_AI_genes_and_proteins_extended.tsv"
	@echo "  - data/txt/sheet/PFAS_Data_for_AI_biological_functions.tsv"
	@echo "  - data/txt/sheet/PFAS_Data_for_AI_chemicals_extended.tsv"
	@echo "  - data/txt/sheet/PFAS_Data_for_AI_pathways_extended.tsv"
	@echo "  - data/txt/sheet/PFAS_Data_for_AI_publications_extended.tsv"

# Extend tables using PFAS-degrading proteins as seeds
extend-from-pfas-degraders: install
	@echo ""
	@echo "=========================================="
	@echo "Extend from PFAS-Degrading Proteins"
	@echo "=========================================="
	@echo ""
	@echo "This will:"
	@echo "  1. Search UniProt for PFAS-degrading and dehalogenase proteins"
	@echo "  2. Extract comprehensive protein details"
	@echo "  3. Identify organisms with PFAS degradation proteins"
	@echo "  4. Extend genomes table with new organisms"
	@echo "  5. Extend proteins table with detailed annotations"
	@echo ""
	uv run python src/extend_from_pfas_degraders.py
	@echo ""
	@echo "✓ Extension from PFAS-degrading proteins completed!"
	@echo ""
	@echo "Output files:"
	@echo "  - data/txt/sheet/PFAS_Data_for_AI_taxa_and_genomes_extended.tsv"
	@echo "  - data/txt/sheet/PFAS_Data_for_AI_genes_and_proteins_extended.tsv"

# Mine extended proteins for pathways, chemicals, publications
mine-proteins: install
	@echo ""
	@echo "=========================================="
	@echo "Mine Extended Proteins"
	@echo "=========================================="
	@echo ""
	@echo "This will:"
	@echo "  1. Read extended proteins table"
	@echo "  2. Fetch UniProt data for each protein"
	@echo "  3. Extract pathways (KEGG, Reactome, etc.)"
	@echo "  4. Extract chemicals (CHEBI compounds)"
	@echo "  5. Extract publications (PubMed, DOIs)"
	@echo "  6. Extend corresponding tables"
	@echo ""
	uv run python src/mine_extended_proteins.py
	@echo ""
	@echo "✓ Mining completed!"
	@echo ""
	@echo "Output files:"
	@echo "  - data/txt/sheet/PFAS_Data_for_AI_pathways_extended.tsv"
	@echo "  - data/txt/sheet/PFAS_Data_for_AI_chemicals_extended.tsv"
	@echo "  - data/txt/sheet/PFAS_Data_for_AI_publications_extended.tsv"

# Update chemicals table with PubChem/CHEBI data
update-chemicals: install data/txt/sheet/PFAS_Data_for_AI_chemicals.tsv
	@echo "Updating chemicals table with PubChem/CHEBI data..."
	uv run python src/chemical_search.py --source-label extend1
	@echo "Chemicals table updated successfully."
	@echo "Output: data/txt/sheet/PFAS_Data_for_AI_chemicals_extended.tsv"

# Update assays table with curated protocols
update-assays: install data/txt/sheet/PFAS_Data_for_AI_assays.tsv
	@echo "Updating assays table with curated assay protocols..."
	uv run python src/assay_search.py --source-label extend1
	@echo "Assays table updated successfully."
	@echo "Output: data/txt/sheet/PFAS_Data_for_AI_assays_extended.tsv"

# Update reactions table with RHEA/KEGG reaction data
update-reactions: install
	@echo "Updating reactions table with biochemical reaction data..."
	uv run python src/extend_reactions.py --source-label extend1
	@echo "Reactions table updated successfully."
	@echo "Output: data/txt/sheet/PFAS_Data_for_AI_reactions.tsv"
	@echo "Output: data/txt/sheet/PFAS_Data_for_AI_reactions_extended.tsv"

# Merge category-specific reaction files from static reference data
# Note: PFAS_Reactions category files are now static reference data in data/txt/sheet/PFAS_Reactions/
# They are no longer extended dynamically - all extensions go to main reactions_extended.tsv
merge-reactions: install
	@echo ""
	@echo "Merging PFAS_Reactions category files (static reference data)..."
	uv run python scripts/merge_reaction_categories.py
	@echo ""
	@echo "✓ Unified reactions table created from reference data!"
	@echo "  Input:  data/txt/sheet/PFAS_Reactions/*_extended.tsv (static reference)"
	@echo "  Output: data/txt/sheet/PFAS_Data_for_AI_reactions_extended.tsv"

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
	@echo "Template available at: data/txt/sheet/PFAS_Data_for_AI_bioprocesses.tsv"
	@echo "Note: Automated bioprocess data extraction not yet implemented"

# Update screening results table (placeholder - manual data entry for now)
update-screening: install
	@echo "Screening results table: Manual data entry"
	@echo "Template available at: data/txt/sheet/PFAS_Data_for_AI_screening_results.tsv"
	@echo "Note: Automated screening data import not yet implemented"

# Update protocols table (placeholder - manual data entry for now)
update-protocols: install
	@echo "Protocols table: Manual data entry"
	@echo "Template available at: data/txt/sheet/PFAS_Data_for_AI_protocols.tsv"
	@echo "Note: Automated protocols.io search not yet implemented"

# Update all tables (full pipeline)
update-all: update-genomes update-biosamples update-pathways update-datasets update-transcriptomics update-strains update-media update-genes update-structures update-publications update-chemicals update-assays update-reactions update-bioprocesses update-screening update-protocols
	@echo ""
	@echo "Full data pipeline completed successfully!"
	@echo "Updated files:"
	@echo "  - data/txt/sheet/PFAS_Data_for_AI_taxa_and_genomes_extended.tsv"
	@echo "  - data/txt/sheet/PFAS_Data_for_AI_biosamples_extended.tsv"
	@echo "  - data/txt/sheet/PFAS_Data_for_AI_pathways_extended.tsv"
	@echo "  - data/txt/sheet/PFAS_Data_for_AI_datasets_extended.tsv"
	@echo "  - data/txt/sheet/PFAS_Data_for_AI_genes_and_proteins_extended.tsv"
	@echo "  - data/txt/sheet/PFAS_Data_for_AI_macromolecular_structures_extended.tsv"
	@echo "  - data/txt/sheet/PFAS_Data_for_AI_publications_extended.tsv"
	@wc -l data/txt/sheet/PFAS_Data_for_AI_*_extended.tsv

# Convert Excel files to TSV (prerequisite step)
convert-excel: install
	@echo "Converting Excel files to TSV format..."
	@mkdir -p data/txt/plan data/txt/sheet data/txt/proposal data/txt/publications
	uv run python src/convert_sheets.py
	@echo "Excel files converted successfully."

# Add annotation URLs to existing genomes table
add-annotations: install data/txt/sheet/PFAS_Data_for_AI_taxa_and_genomes_extended.tsv
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
	uv run gen-python schema/pfas_biodegradation.yaml > src/linkml_models.py
	@echo "Generated src/linkml_models.py successfully."

# Validate extended TSV data against LinkML schema
validate-schema: install gen-linkml-models
	@echo "Validating extended TSV data against LinkML schema..."
	@echo "Converting TSV files to LinkML YAML format..."
	uv run python src/tsv_to_linkml.py --data-dir data/txt/sheet --output data/linkml_database.yaml
	@echo ""
	@echo "Validating YAML data against schema..."
	uv run linkml-validate -s schema/pfas_biodegradation.yaml data/linkml_database.yaml
	@echo ""
	@echo "✓ Validation completed successfully!"
	@echo "  Data file: data/linkml_database.yaml"
	@echo "  Schema: schema/pfas_biodegradation.yaml"

# Validate cross-sheet consistency and referential integrity
validate-consistency: install
	@echo "Validating cross-sheet consistency and referential integrity..."
	@echo ""
	uv run python src/validate_consistency.py --data-dir data/txt/sheet
	@echo ""
	@echo "✓ Consistency validation completed!"

# Automatically fix validation issues
fix-validation: install
	@echo ""
	@echo "============================================================"
	@echo "AUTOMATED VALIDATION FIXES"
	@echo "============================================================"
	@echo ""
	@echo "This workflow automatically fixes common validation issues:"
	@echo "  • CHEBI IDs with duplicate prefix (CHEBI:CHEBI:12345 → CHEBI:12345)"
	@echo "  • PubChem IDs stored as floats (165668.0 → 165668)"
	@echo "  • Publication DOIs missing URL prefix (10.1111/... → https://doi.org/...)"
	@echo "  • Missing organism references (queries NCBI to add organisms from genes table)"
	@echo ""
	@echo "Starting automated fixes..."
	@echo ""
	uv run python src/fix_validation_issues.py --all --add-organisms
	@echo ""
	@echo "============================================================"
	@echo "✓ VALIDATION FIXES COMPLETE"
	@echo "============================================================"
	@echo ""
	@echo "Recommended next steps:"
	@echo "  1. Run validation again: make validate-consistency"
	@echo "  2. Review remaining warnings"
	@echo "  3. Manual fixes may be needed for:"
	@echo "     - Organism/protocol references"
	@echo "     - Truncated FTP URLs"
	@echo "     - Missing data coverage"

# Convert PDFs to markdown format
convert-pdfs-to-markdown: install
	@echo "Converting PDF publications to markdown..."
	@echo ""
	uv run python src/pdf_to_markdown.py --batch data/publications --output-dir data/publications
	@echo ""
	@echo "✓ PDF to markdown conversion completed!"
	@echo ""
	@echo "Checking PDF availability against publications TSV..."
	@echo ""
	-uv run python src/check_publication_pdfs.py
	@echo ""

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

# extend-api: Repeatable API-based extensions with round numbering
ROUND ?= 3
extend-api: install
	@echo ""
	@echo "============================================================"
	@echo "EXTEND-API WORKFLOW - Round $(ROUND)"
	@echo "============================================================"
	@echo ""
	@echo "This workflow queries external APIs for data extension:"
	@echo "  - chemicals: PubChem, CHEBI, UniProt"
	@echo "  - assays: protocols.io, OBI, BAO"
	@echo "  - protocols: protocols.io"
	@echo "  - media: protocols.io | KG-Microbe | ATCC | DSMZ"
	@echo "  - genomes/biosamples: NCBI Assembly, BioSample"
	@echo "  - pathways: KEGG, MetaCyc"
	@echo "  - genes: UniProt, KEGG, IntEnz"
	@echo "  - structures: PDB, AlphaFold DB"
	@echo "  - publications: PubMed, bioRxiv, arXiv"
	@echo "  - datasets: GEO, SRA, MetaboLights, Zenodo"
	@echo "  - transcriptomics: NCBI SRA, GEO, ArrayExpress"
	@echo "  - strains: KG-Microbe, NCBI Taxonomy, BacDive"
	@echo ""
	@echo "Source label: extend_api_round$(ROUND)"
	@echo "Repeatable: Deduplication prevents duplicates"
	@echo ""
	@echo "Starting API extensions..."
	@echo ""
	uv run python src/extend_api.py --round $(ROUND)
	@echo ""
	@echo "============================================================"
	@echo "✓ EXTEND-API ROUND $(ROUND) COMPLETED!"
	@echo "============================================================"
	@echo ""
	@echo "Data provenance tracking:"
	@echo "  - extend1 = Initial round (manual + database searches)"
	@echo "  - extend2 = Second round (PDF extraction)"
	@echo "  - extend_api_round$(ROUND) = API-based updates (round $(ROUND))"
	@echo ""
	@echo "Usage examples:"
	@echo "  make extend-api ROUND=3  # Run round 3 (default)"
	@echo "  make extend-api ROUND=4  # Run round 4"

# kg-update-genes: Update genes table from function KG
kg-update-genes: install
	@echo ""
	@echo "============================================================"
	@echo "KG-UPDATE: Genes/Proteins from Function KG"
	@echo "============================================================"
	@echo ""
	uv run python src/kg_update_genes.py
	@echo ""
	@echo "✓ Genes/proteins table updated from function KG"

# kg-update-pathways: Update pathways table from function KG
kg-update-pathways: install
	@echo ""
	@echo "============================================================"
	@echo "KG-UPDATE: Pathways from Function KG"
	@echo "============================================================"
	@echo ""
	uv run python src/kg_update_pathways.py
	@echo ""
	@echo "✓ Pathways table updated from function KG"

# kg-update-chemicals: Update chemicals table from function KG
kg-update-chemicals: install
	@echo ""
	@echo "============================================================"
	@echo "KG-UPDATE: Chemicals from Function KG"
	@echo "============================================================"
	@echo ""
	uv run python src/kg_update_chemicals.py
	@echo ""
	@echo "✓ Chemicals table updated from function KG"

# kg-update-genomes: Update taxa/genomes table from both KGs
kg-update-genomes: install
	@echo ""
	@echo "============================================================"
	@echo "KG-UPDATE: Taxa/Genomes from Both KGs"
	@echo "============================================================"
	@echo ""
	uv run python src/kg_update_genomes.py
	@echo ""
	@echo "✓ Taxa/genomes table updated from phenotypic + function KGs"

# kg-update-all: Run all KG updates (comprehensive)
kg-update-all: kg-update-genes kg-update-pathways kg-update-chemicals kg-update-genomes
	@echo ""
	@echo "============================================================"
	@echo "✓ KG-UPDATE COMPREHENSIVE UPDATE COMPLETED!"
	@echo "============================================================"
	@echo ""
	@echo "Summary: All tables updated from Knowledge Graphs"
	@echo "  - Genes/proteins from function KG"
	@echo "  - Pathways from function KG"
	@echo "  - Chemicals from function KG"
	@echo "  - Taxa/genomes from both KGs"

# kg-update: Run KG update workflow (master - same as kg-update-all)
kg-update: install
	@echo ""
	@echo "============================================================"
	@echo "KG-UPDATE WORKFLOW - Repeatable Knowledge Graph Mining"
	@echo "============================================================"
	@echo ""
	@echo "This workflow updates tables from local KG databases:"
	@echo "  - kg-microbe: 1.4M nodes (phenotypic data)"
	@echo "  - kg-microbe-function: 151M nodes (functional annotations)"
	@echo ""
	@echo "Repeatable: Deduplication prevents duplicate entries."
	@echo "Source label: All new records → source='kg_update'"
	@echo ""
	@echo "Starting KG mining..."
	@echo ""
	uv run python src/run_kg_update.py
	@echo ""
	@echo "============================================================"
	@echo "✓ KG-UPDATE WORKFLOW COMPLETED!"
	@echo "============================================================"
	@echo ""
	@echo "Data provenance tracking:"
	@echo "  - extend1 = Initial round (manual + API searches)"
	@echo "  - extend2 = Second round (PDF extraction)"
	@echo "  - kg_update = KG-based updates (repeatable)"

# annotate-kg: Annotate existing rows with KG node identifiers
annotate-kg: install
	@echo ""
	@echo "============================================================"
	@echo "ANNOTATE WITH KG NODE IDENTIFIERS"
	@echo "============================================================"
	@echo ""
	@echo "Adding kg_node_ids columns to existing data sheets:"
	@echo "  - Taxa/Genomes: NCBITaxon nodes"
	@echo "  - Genes/Proteins: UniprotKB/KEGG nodes"
	@echo "  - Pathways: KEGG/MetaCyc nodes"
	@echo "  - Chemicals: CHEBI nodes"
	@echo ""
	uv run python src/annotate_kg_identifiers.py --all
	@echo ""
	@echo "✓ KG annotation complete"
	@echo "  See: data/txt/sheet/KG_ANNOTATION_REPORT.md"

# crosslink: Cross-link related information across data sheets
crosslink: install
	@echo ""
	@echo "============================================================"
	@echo "CROSS-LINKING DATA SHEETS"
	@echo "============================================================"
	@echo ""
	@echo "Creating cross-references across related tables:"
	@echo "  - Genes → Genomes (organism name matching)"
	@echo "  - Pathways → Genomes (organism matching)"
	@echo "  - Pathways → Genes (gene name matching)"
	@echo "  - Structures → Genes (protein name matching)"
	@echo "  - Biosamples → Genomes (organism matching)"
	@echo ""
	@echo "This adds cross-reference columns to link related data."
	@echo "Repeatable: Safe to run multiple times (idempotent)."
	@echo ""
	uv run python src/crosslink_sheets.py --all
	@echo ""
	@echo "============================================================"
	@echo "✓ CROSS-LINKING COMPLETED!"
	@echo "============================================================"
	@echo ""
	@echo "New columns added:"
	@echo "  - genes: genome_ncbitaxon_id, genome_scientific_name"
	@echo "  - pathways: genome_ncbitaxon_ids, gene_protein_ids"
	@echo "  - biosamples: genome_ncbitaxon_id"
	@echo "  - structures: gene_protein_ids"
	@echo ""
	@echo "Use these columns to:"
	@echo "  - Query related data across tables"
	@echo "  - Build knowledge graphs"
	@echo "  - Validate data integrity"
	@echo "  - Generate reports"

# extendbypub workflow: Cross-reference publications with data sheets
extendbypub: install convert-pdfs-to-markdown
	@echo ""
	@echo "============================================================"
	@echo "PUBLICATION CROSS-REFERENCE WORKFLOW"
	@echo "============================================================"
	@echo ""
	@echo "This workflow:"
	@echo "  1. Reads markdown files converted from PDFs"
	@echo "  2. Checks if each publication is relevant to rows in data sheets"
	@echo "  3. Appends publication IDs to source columns with '|' delimiter"
	@echo ""
	@echo "Processing all sheets with source columns..."
	@echo ""
	uv run python src/extend_by_publication.py \
		--publications-file data/txt/sheet/PFAS_Data_for_AI_publications.tsv \
		--markdown-dir data/publications \
		--data-dir data/txt/sheet \
		--min-keyword-matches 3
	@echo ""
	@echo "============================================================"
	@echo "✓ PUBLICATION CROSS-REFERENCE COMPLETED!"
	@echo "============================================================"
	@echo ""
	@echo "Updated sheets:"
	@echo "  - Chemicals, Assays, Bioprocesses, Screening Results"
	@echo "  - Publication IDs appended to source columns"
	@echo ""
	@echo "Next steps:"
	@echo "  - Review source columns for accuracy"
	@echo "  - Run 'make validate-consistency' to check data integrity"

# compare-excel: Compare current Excel file with last version
compare-excel: install
	@echo ""
	@echo "============================================================"
	@echo "EXCEL FILE COMPARISON"
	@echo "============================================================"
	@echo ""
	@echo "Comparing:"
	@echo "  File 1: data/sheet/PFAS Data for AI.xlsx (current)"
	@echo "  File 2: data/sheet/PFAS Data for AI_last.xlsx (last version)"
	@echo ""
	uv run python src/compare_excel_files.py
	@echo ""

# compare-excel-tsv: Compare Excel file with existing TSV files
compare-excel-tsv: install
	@echo ""
	@echo "============================================================"
	@echo "EXCEL vs TSV COMPARISON"
	@echo "============================================================"
	@echo ""
	@echo "Comparing Excel sheets with corresponding TSV files..."
	@echo ""
	uv run python src/compare_excel_tsv.py \
		--excel-file "data/sheet/PFAS Data for AI.xlsx" \
		--tsv-dir data/txt/sheet
	@echo ""

# report-missing-pdfs: Generate report of missing publication PDFs
report-missing-pdfs: install
	@echo ""
	@echo "============================================================"
	@echo "MISSING PUBLICATION PDFs REPORT"
	@echo "============================================================"
	@echo ""
	@echo "Analyzing publications TSV and generating report..."
	@echo ""
	uv run python src/generate_missing_pdfs_report.py \
		--publications-file data/txt/sheet/PFAS_Data_for_AI_publications.tsv \
		--pdf-dir data/publications \
		--output MISSING_PUBLICATION_PDFS.md
	@echo ""
	@echo "Report saved to: MISSING_PUBLICATION_PDFS.md"
	@echo ""

# merge-excel workflow: Merge Excel updates while preserving generated data
merge-excel: install
	@echo ""
	@echo "============================================================"
	@echo "EXCEL MERGE WORKFLOW"
	@echo "============================================================"
	@echo ""
	@echo "This workflow:"
	@echo "  1. Backs up existing TSV files"
	@echo "  2. Reads new Excel file"
	@echo "  3. Intelligently merges schema and data"
	@echo "  4. Preserves publication references and extended rows"
	@echo "  5. Applies to both base and _extended files"
	@echo ""
	@echo "Running merge (use --dry-run to preview)..."
	@echo ""
	uv run python src/merge_excel_updates.py \
		--excel-file "data/sheet/PFAS Data for AI.xlsx" \
		--tsv-dir data/txt/sheet
	@echo ""
	@echo "============================================================"
	@echo "✓ EXCEL MERGE COMPLETED!"
	@echo "============================================================"
	@echo ""
	@echo "Next steps:"
	@echo "  - Review changes in updated TSV files"
	@echo "  - Run 'make validate-consistency' to check integrity"
	@echo "  - Run 'make validate-schema' to validate against LinkML"

# merge-excel-dry-run: Preview Excel merge without applying changes
merge-excel-dry-run: install
	@echo ""
	@echo "============================================================"
	@echo "EXCEL MERGE (DRY RUN - PREVIEW ONLY)"
	@echo "============================================================"
	@echo ""
	uv run python src/merge_excel_updates.py \
		--excel-file "data/sheet/PFAS Data for AI.xlsx" \
		--tsv-dir data/txt/sheet \
		--dry-run
	@echo ""
	@echo "To apply these changes, run: make merge-excel"

# Clean up temporary and output files
clean:
	@echo "Cleaning up temporary files..."
	rm -f *.log
	rm -f src/__pycache__/*.pyc
	rm -f data/txt/sheet/*.tsv.bak
	@echo "Cleanup completed."

# Clean extended output files (use with caution)
clean-extended:
	@echo "WARNING: This will delete extended data files!"
	@echo "Press Ctrl+C within 5 seconds to cancel..."
	@sleep 5
	rm -f data/txt/sheet/PFAS_Data_for_AI_*_extended.tsv
	@echo "Extended files removed."

# Check that input files exist
data/txt/sheet/PFAS_Data_for_AI_taxa_and_genomes.tsv:
	@echo "Error: Input file not found: $@"
	@echo "Please run 'make convert-excel' first to convert Excel files to TSV."
	@exit 1

data/txt/sheet/PFAS_Data_for_AI_biosamples.tsv:
	@echo "Error: Input file not found: $@"
	@echo "Please run 'make convert-excel' first to convert Excel files to TSV."
	@exit 1

data/txt/sheet/PFAS_Data_for_AI_pathways.tsv:
	@echo "Error: Input file not found: $@"
	@echo "Please run 'make convert-excel' first to convert Excel files to TSV."
	@exit 1

data/txt/sheet/PFAS_Data_for_AI_datasets.tsv:
	@echo "Error: Input file not found: $@"
	@echo "Please run 'make convert-excel' first to convert Excel files to TSV."
	@exit 1

data/txt/sheet/PFAS_Data_for_AI_transcriptomics.tsv:
	@echo "Error: Input file not found: $@"
	@echo "Please run 'make convert-excel' first to convert Excel files to TSV."
	@exit 1

data/txt/sheet/PFAS_Data_for_AI_strains.tsv:
	@echo "Error: Input file not found: $@"
	@echo "Please run 'make convert-excel' first to convert Excel files to TSV."
	@exit 1

data/txt/sheet/PFAS_Data_for_AI_genes_and_proteins.tsv:
	@echo "Error: Input file not found: $@"
	@echo "Please run 'make convert-excel' first to convert Excel files to TSV."
	@exit 1

data/txt/sheet/PFAS_Data_for_AI_macromolecular_structures.tsv:
	@echo "Error: Input file not found: $@"
	@echo "Please run 'make convert-excel' first to convert Excel files to TSV."
	@exit 1

data/txt/sheet/PFAS_Data_for_AI_publications.tsv:
	@echo "Error: Input file not found: $@"
	@echo "Please run 'make convert-excel' first to convert Excel files to TSV."
	@exit 1

data/txt/sheet/PFAS_Data_for_AI_taxa_and_genomes_extended.tsv:
	@echo "Error: Extended genomes file not found: $@"
	@echo "Please run 'make update-genomes' first to create extended table."
	@exit 1

# Show current data status
status:
	@echo "PFAS-AI Data Pipeline Status:"
	@echo "============================"
	@echo ""
	@echo "Input files:"
	@if [ -f "data/txt/sheet/PFAS_Data_for_AI_taxa_and_genomes.tsv" ]; then \
		echo "  ✓ Taxa and genomes TSV exists ($$(wc -l < data/txt/sheet/PFAS_Data_for_AI_taxa_and_genomes.tsv) lines)"; \
	else \
		echo "  ✗ Taxa and genomes TSV missing"; \
	fi
	@if [ -f "data/txt/sheet/PFAS_Data_for_AI_biosamples.tsv" ]; then \
		echo "  ✓ Biosamples TSV exists ($$(wc -l < data/txt/sheet/PFAS_Data_for_AI_biosamples.tsv) lines)"; \
	else \
		echo "  ✗ Biosamples TSV missing"; \
	fi
	@if [ -f "data/txt/sheet/PFAS_Data_for_AI_pathways.tsv" ]; then \
		echo "  ✓ Pathways TSV exists ($$(wc -l < data/txt/sheet/PFAS_Data_for_AI_pathways.tsv) lines)"; \
	else \
		echo "  ✗ Pathways TSV missing"; \
	fi
	@if [ -f "data/txt/sheet/PFAS_Data_for_AI_datasets.tsv" ]; then \
		echo "  ✓ Datasets TSV exists ($$(wc -l < data/txt/sheet/PFAS_Data_for_AI_datasets.tsv) lines)"; \
	else \
		echo "  ✗ Datasets TSV missing"; \
	fi
	@if [ -f "data/txt/sheet/PFAS_Data_for_AI_transcriptomics.tsv" ]; then \
		echo "  ✓ Transcriptomics TSV exists ($$(wc -l < data/txt/sheet/PFAS_Data_for_AI_transcriptomics.tsv) lines)"; \
	else \
		echo "  ✗ Transcriptomics TSV missing"; \
	fi
	@if [ -f "data/txt/sheet/PFAS_Data_for_AI_strains.tsv" ]; then \
		echo "  ✓ Strains TSV exists ($$(wc -l < data/txt/sheet/PFAS_Data_for_AI_strains.tsv) lines)"; \
	else \
		echo "  ✗ Strains TSV missing"; \
	fi
	@if [ -f "data/txt/sheet/PFAS_Data_for_AI_growth_media.tsv" ]; then \
		echo "  ✓ Growth media TSV exists ($$(wc -l < data/txt/sheet/PFAS_Data_for_AI_growth_media.tsv) lines)"; \
	else \
		echo "  ✗ Growth media TSV missing"; \
	fi
	@if [ -f "data/txt/sheet/PFAS_Data_for_AI_media_ingredients.tsv" ]; then \
		echo "  ✓ Media ingredients TSV exists ($$(wc -l < data/txt/sheet/PFAS_Data_for_AI_media_ingredients.tsv) lines)"; \
	else \
		echo "  ✗ Media ingredients TSV missing"; \
	fi
	@if [ -f "data/txt/sheet/PFAS_Data_for_AI_genes_and_proteins.tsv" ]; then \
		echo "  ✓ Genes and proteins TSV exists ($$(wc -l < data/txt/sheet/PFAS_Data_for_AI_genes_and_proteins.tsv) lines)"; \
	else \
		echo "  ✗ Genes and proteins TSV missing"; \
	fi
	@if [ -f "data/txt/sheet/PFAS_Data_for_AI_macromolecular_structures.tsv" ]; then \
		echo "  ✓ Structures TSV exists ($$(wc -l < data/txt/sheet/PFAS_Data_for_AI_macromolecular_structures.tsv) lines)"; \
	else \
		echo "  ✗ Structures TSV missing"; \
	fi
	@if [ -f "data/txt/sheet/PFAS_Data_for_AI_publications.tsv" ]; then \
		echo "  ✓ Publications TSV exists ($$(wc -l < data/txt/sheet/PFAS_Data_for_AI_publications.tsv) lines)"; \
	else \
		echo "  ✗ Publications TSV missing"; \
	fi
	@echo ""
	@echo "Extended files:"
	@if [ -f "data/txt/sheet/PFAS_Data_for_AI_taxa_and_genomes_extended.tsv" ]; then \
		echo "  ✓ Extended taxa and genomes exists ($$(wc -l < data/txt/sheet/PFAS_Data_for_AI_taxa_and_genomes_extended.tsv) lines)"; \
	else \
		echo "  ✗ Extended taxa and genomes missing"; \
	fi
	@if [ -f "data/txt/sheet/PFAS_Data_for_AI_biosamples_extended.tsv" ]; then \
		echo "  ✓ Extended biosamples exists ($$(wc -l < data/txt/sheet/PFAS_Data_for_AI_biosamples_extended.tsv) lines)"; \
	else \
		echo "  ✗ Extended biosamples missing"; \
	fi
	@if [ -f "data/txt/sheet/PFAS_Data_for_AI_pathways_extended.tsv" ]; then \
		echo "  ✓ Extended pathways exists ($$(wc -l < data/txt/sheet/PFAS_Data_for_AI_pathways_extended.tsv) lines)"; \
	else \
		echo "  ✗ Extended pathways missing"; \
	fi
	@if [ -f "data/txt/sheet/PFAS_Data_for_AI_datasets_extended.tsv" ]; then \
		echo "  ✓ Extended datasets exists ($$(wc -l < data/txt/sheet/PFAS_Data_for_AI_datasets_extended.tsv) lines)"; \
	else \
		echo "  ✗ Extended datasets missing"; \
	fi
	@if [ -f "data/txt/sheet/PFAS_Data_for_AI_transcriptomics_extended.tsv" ]; then \
		echo "  ✓ Extended transcriptomics exists ($$(wc -l < data/txt/sheet/PFAS_Data_for_AI_transcriptomics_extended.tsv) lines)"; \
	else \
		echo "  ✗ Extended transcriptomics missing"; \
	fi
	@if [ -f "data/txt/sheet/PFAS_Data_for_AI_strains_extended.tsv" ]; then \
		echo "  ✓ Extended strains exists ($$(wc -l < data/txt/sheet/PFAS_Data_for_AI_strains_extended.tsv) lines)"; \
	else \
		echo "  ✗ Extended strains missing"; \
	fi
	@if [ -f "data/txt/sheet/PFAS_Data_for_AI_growth_media_extended.tsv" ]; then \
		echo "  ✓ Extended growth media exists ($$(wc -l < data/txt/sheet/PFAS_Data_for_AI_growth_media_extended.tsv) lines)"; \
	else \
		echo "  ✗ Extended growth media missing"; \
	fi
	@if [ -f "data/txt/sheet/PFAS_Data_for_AI_media_ingredients_extended.tsv" ]; then \
		echo "  ✓ Extended media ingredients exists ($$(wc -l < data/txt/sheet/PFAS_Data_for_AI_media_ingredients_extended.tsv) lines)"; \
	else \
		echo "  ✗ Extended media ingredients missing"; \
	fi
	@if [ -f "data/txt/sheet/PFAS_Data_for_AI_genes_and_proteins_extended.tsv" ]; then \
		echo "  ✓ Extended genes and proteins exists ($$(wc -l < data/txt/sheet/PFAS_Data_for_AI_genes_and_proteins_extended.tsv) lines)"; \
	else \
		echo "  ✗ Extended genes and proteins missing"; \
	fi
	@if [ -f "data/txt/sheet/PFAS_Data_for_AI_macromolecular_structures_extended.tsv" ]; then \
		echo "  ✓ Extended structures exists ($$(wc -l < data/txt/sheet/PFAS_Data_for_AI_macromolecular_structures_extended.tsv) lines)"; \
	else \
		echo "  ✗ Extended structures missing"; \
	fi
	@if [ -f "data/txt/sheet/PFAS_Data_for_AI_publications_extended.tsv" ]; then \
		echo "  ✓ Extended publications exists ($$(wc -l < data/txt/sheet/PFAS_Data_for_AI_publications_extended.tsv) lines)"; \
	else \
		echo "  ✗ Extended publications missing"; \
	fi
	@echo ""
	@echo "Experimental data files:"
	@if [ -f "data/txt/sheet/PFAS_Data_for_AI_chemicals.tsv" ]; then \
		echo "  ✓ Chemicals TSV exists ($$(wc -l < data/txt/sheet/PFAS_Data_for_AI_chemicals.tsv) lines)"; \
	else \
		echo "  ✗ Chemicals TSV missing"; \
	fi
	@if [ -f "data/txt/sheet/PFAS_Data_for_AI_assays.tsv" ]; then \
		echo "  ✓ Assays TSV exists ($$(wc -l < data/txt/sheet/PFAS_Data_for_AI_assays.tsv) lines)"; \
	else \
		echo "  ✗ Assays TSV missing"; \
	fi
	@if [ -f "data/txt/sheet/PFAS_Data_for_AI_bioprocesses.tsv" ]; then \
		echo "  ✓ Bioprocesses TSV exists ($$(wc -l < data/txt/sheet/PFAS_Data_for_AI_bioprocesses.tsv) lines)"; \
	else \
		echo "  ✗ Bioprocesses TSV missing"; \
	fi
	@if [ -f "data/txt/sheet/PFAS_Data_for_AI_screening_results.tsv" ]; then \
		echo "  ✓ Screening results TSV exists ($$(wc -l < data/txt/sheet/PFAS_Data_for_AI_screening_results.tsv) lines)"; \
	else \
		echo "  ✗ Screening results TSV missing"; \
	fi
	@if [ -f "data/txt/sheet/PFAS_Data_for_AI_protocols.tsv" ]; then \
		echo "  ✓ Protocols TSV exists ($$(wc -l < data/txt/sheet/PFAS_Data_for_AI_protocols.tsv) lines)"; \
	else \
		echo "  ✗ Protocols TSV missing"; \
	fi

# Create DuckDB knowledge graph database
create-kg-db: install
	@echo "Creating knowledge graph database from TSV files..."
	@echo ""
	uv run python src/kg_database.py --create --stats
	@echo ""
	@echo "✓ Knowledge graph database created: data/kgm/kg-microbe.duckdb"
	@echo "  See data/kgm/README.md for usage examples"

# Run example knowledge graph queries
query-kg-db: install
	@echo "Running example knowledge graph queries..."
	@echo ""
	uv run python examples/query_knowledge_graph.py --example all
