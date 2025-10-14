# Lanthanide Bioprocessing LinkML Schema

This directory contains the LinkML schema for modeling lanthanide bioprocessing research data.

## Schema File

**`lanthanide_bioprocessing.yaml`**: Main schema defining data models for:
- Genomes (bacterial/archaeal)
- Biosamples (environmental/cultured)
- Pathways (metabolic)
- Genes/Proteins
- Macromolecular structures
- Publications
- Datasets

## Ontology Mappings

The schema integrates these ontologies and vocabularies:

- **NCBITaxon**: Organism taxonomy identifiers
- **SRA**: NCBI Sequence Read Archive
- **CHEBI**: Chemical Entities of Biological Interest (substrates, cofactors, lanthanides)
- **ENVO**: Environment Ontology
- **MIXS**: Minimum Information about any (x) Sequence
- **UniProtKB**: Universal Protein Resource
- **GO**: Gene Ontology (molecular function, biological process, cellular component)
- **EC**: Enzyme Commission classification
- **RHEA**: Biochemical reaction database
- **KEGG**: Kyoto Encyclopedia of Genes and Genomes
- **MetaCyc**: Metabolic pathway database

## Usage

### Validate Schema

```bash
uv run gen-linkml --validate schema/lanthanide_bioprocessing.yaml
```

### Generate Python Dataclasses

```bash
uv run gen-python schema/lanthanide_bioprocessing.yaml > src/models.py
```

### Generate JSON Schema

```bash
uv run gen-json-schema schema/lanthanide_bioprocessing.yaml > schema/schema.json
```

### Generate SQL DDL

```bash
uv run gen-sqldl schema/lanthanide_bioprocessing.yaml > schema/schema.sql
```

### Generate GraphQL Schema

```bash
uv run gen-graphql schema/lanthanide_bioprocessing.yaml > schema/schema.graphql
```

### Generate OWL Ontology

```bash
uv run gen-owl schema/lanthanide_bioprocessing.yaml > schema/schema.owl
```

### Validate Data

```bash
# Validate YAML data file
uv run linkml-validate -s schema/lanthanide_bioprocessing.yaml data/example.yaml

# Validate JSON data file
uv run linkml-validate -s schema/lanthanide_bioprocessing.yaml -f json data/example.json
```

## Schema Classes

### LanthanideBioprocessingDatabase (root)
Container for all data types

### GenomeRecord
- `scientific_name`: Organism name
- `ncbi_taxon_id`: NCBI Taxonomy ID (identifier)
- `genome_identifier`: GenBank/RefSeq accession
- `annotation_download_url`: FTP URL to GFF3 file

### BiosampleRecord
- `sample_id`: NCBI BioSample accession (identifier)
- `sample_name`: Human-readable name
- `organism`: Organism or environmental type
- `download_url`: URL to biosample page/SRA data

### PathwayRecord
- `pathway_id`: KEGG or MetaCyc ID (identifier)
- `pathway_name`: Descriptive name
- `organism`: Host organism(s)
- `genes`: Gene symbols (multivalued)
- `genes_kegg`: KEGG K numbers (multivalued)
- `download_url`: Pathway diagram/data URL

### GeneProteinRecord
- `gene_protein_id`: KEGG K#/UniProt ID/custom (identifier)
- `organism`: Source organism
- `annotation`: Functional description
- `ec_number`: EC classification
- `go_terms`: GO annotations (multivalued)
- `chebi_terms`: Chemical entities (multivalued)
- `download_url`: Sequence data URL

### MacromolecularStructureRecord
- `structure_name`: Structure identifier (identifier)
- `organism`: Source organism
- `components`: Molecular components
- `pdb_id`: PDB accession
- `resolution`: Structure resolution
- `method`: Determination method (enum)
- `download_url`: Structure file URL

### PublicationRecord
- `url`: Primary URL - DOI/PMID/arXiv (identifier)
- `title`: Article title
- `journal`: Publication venue
- `year`: Publication year
- `authors`: Author list
- `download_url`: Direct download URL

### DatasetRecord
- `dataset_name`: Dataset name (identifier)
- `data_type`: Dataset type (enum)
- `url`: Primary dataset URL
- `size`: Dataset size
- `publication`: Associated publication
- `license`: Data license
- `download_url`: Direct download URL

## Enumerations

### StructureMethodEnum
- X-ray crystallography
- NMR spectroscopy
- Cryo-EM
- Predicted structure (AlphaFold, etc.)
- Homology modeling
- Computational prediction
- Chemical characterization
- Multiple methods

### DataTypeEnum
- genomic DNA sequencing
- RNA-seq
- transcriptomics
- proteomics
- metabolomics
- metagenomics
- 16S rRNA
- protein sequences
- metabolic compounds
- pathways
- thermodynamics
- mass spectrometry
- annotated genomes
- 3D protein structures

## Validation Patterns

The schema includes regex patterns for validating identifiers:

- **Genome identifiers**: `^(GC[AF]_\d+\.\d+|\d+\.\d+)?$`
- **BioSample IDs**: `^SAM[NDE][A-Z]?\d+$`
- **Pathway IDs**: `^(ko\d+|path:map\d+|PWY-\d+|PWY\d+|Custom_[A-Z0-9]+)$`
- **Gene/Protein IDs**: KEGG K numbers, UniProt accessions, or custom IDs
- **EC numbers**: `^\d+\.\d+\.\d+\.\d+$`
- **GO terms**: `^GO:\d{7}`
- **CHEBI terms**: `^CHEBI:\d+`
- **PDB IDs**: `^[0-9][A-Za-z0-9]{3}$`

## Design Principles

1. **Ontology-first**: All fields map to standard ontologies where applicable
2. **Flexible identifiers**: Support for multiple ID systems (KEGG, UniProt, GenBank, custom)
3. **Validation**: Regex patterns ensure data quality
4. **Extensibility**: Easy to add new record types or fields
5. **Interoperability**: Uses schema.org URIs for common properties
6. **Multivalued support**: Handle multiple annotations per record

## Future Extensions

Potential schema enhancements:

- Environmental parameters (ENVO/MIXS terms)
- Experimental conditions (temperature, pH, metal concentrations)
- Siderophore/lanthanophore structures (CHEBI)
- Regulatory elements and binding sites
- Quantitative measurements (activity assays, KD values)
- Phylogenetic relationships
- Sequence features and domains
