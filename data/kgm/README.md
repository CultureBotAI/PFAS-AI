# KG-Microbe Knowledge Graph Database

This directory contains the DuckDB database for the PFAS biodegradation knowledge graph, derived from the [KG-Microbe](https://github.com/Knowledge-Graph-Hub/kg-microbe) project.

## Overview

The knowledge graph integrates data from multiple sources to link:
- **Microbial strains** (NCBITaxon IDs, BacDive IDs)
- **Growth media formulations** (ATCC, DSMZ catalogs)
- **Chemical compounds** (CHEBI, PubChem)
- **Enzymes** (EC numbers)
- **Metabolic pathways** (KEGG, MetaCyc)

## Files

- `kg-microbe.duckdb` - DuckDB database (generated, not in git)
- `kg-microbe_nodes.tsv` - Knowledge graph nodes (to be populated)
- `kg-microbe_edges.tsv` - Knowledge graph edges (to be populated)

## Setup

### 1. Obtain KG-Microbe Data

Download the latest KG-Microbe knowledge graph files:

```bash
# Download from KG-Hub releases (example)
wget https://kg-hub.berkeleybop.io/kg-microbe/current/kg-microbe_nodes.tsv.gz
wget https://kg-hub.berkeleybop.io/kg-microbe/current/kg-microbe_edges.tsv.gz

# Decompress
gunzip kg-microbe_nodes.tsv.gz
gunzip kg-microbe_edges.tsv.gz

# Move to data/kgm/
mv kg-microbe_nodes.tsv data/kgm/
mv kg-microbe_edges.tsv data/kgm/
```

### 2. Create Database

```bash
# Create DuckDB database from TSV files
make create-kg-db

# Or manually:
uv run python src/kg_analysis/kg_database.py --create --stats
```

## Usage

### Python API

```python
from src.kg_analysis.kg_database import KnowledgeGraphDB

# Connect to database
kg = KnowledgeGraphDB()
kg.connect()

# Query nodes
enzymes = kg.query_nodes(category="biolink:Enzyme", limit=10)
dehalogenases = kg.query_nodes(name_contains="dehalogenase")
chebi_compounds = kg.query_nodes(id_prefix="CHEBI:")

# Query edges
reactions = kg.query_edges(predicate="biolink:catalyzes")

# Get node details
node = kg.get_node("EC:3.8.1.8")  # Haloalkane dehalogenase

# Find neighbors
neighbors = kg.get_neighbors("EC:3.8.1.8", direction="outgoing")

# Find paths
paths = kg.find_paths("EC:3.8.1.8", "CHEBI:17295", max_depth=3)

# Get statistics
stats = kg.get_statistics()
print(f"Total nodes: {stats['total_nodes']:,}")
print(f"Total edges: {stats['total_edges']:,}")

kg.close()
```

### Command Line

```bash
# Show database statistics
uv run python src/kg_analysis/kg_database.py --stats

# Recreate database (overwrite existing)
uv run python src/kg_analysis/kg_database.py --create --overwrite
```

## PFAS-Relevant Node Types

### Strains
- **ID prefix**: `strain:bacdive_*`, `NCBITaxon:*`
- **Category**: `biolink:OrganismTaxon`
- **Example queries**:
  - Pseudomonas strains: `kg.query_nodes(name_contains="Pseudomonas")`
  - PFAS degraders: `kg.query_nodes(name_contains="Acidimicrobium")`

### Media & Ingredients
- **ID prefix**: `medium:*`, `ingredient:*`, `solution:*`
- **Category**: varies
- **Example queries**:
  - Mineral salts media: `kg.query_nodes(name_contains="mineral salts")`
  - Methanol as ingredient: `kg.query_nodes(id_prefix="CHEBI:", name_contains="methanol")`

### Enzymes & Chemicals
- **ID prefix**: `EC:*`, `CHEBI:*`, `PUBCHEM:*`
- **Category**: `biolink:Enzyme`, `biolink:ChemicalEntity`
- **Example queries**:
  - Dehalogenases: `kg.query_nodes(category="biolink:Enzyme", name_contains="dehalogenase")`
  - Fluoride compounds: `kg.query_nodes(id_prefix="CHEBI:", name_contains="fluoride")`

## Integration with Extension Pipelines

The knowledge graph is used by:

1. **`src/strain_search.py`** - Enriches strains with KG-Microbe nodes
2. **`src/media_search.py`** - Links media ingredients to CHEBI/chemical nodes
3. **`src/transcriptomics_search.py`** - Cross-references organisms with KG nodes

### Example: Strain Enrichment

```python
from src.kg_analysis.kg_database import KnowledgeGraphDB

def query_kg_microbe_for_strain(taxon_id: int, organism_name: str) -> str:
    """Find KG-Microbe nodes for a strain."""
    kg = KnowledgeGraphDB()

    # Try NCBITaxon ID
    ncbi_node = kg.get_node(f"NCBITaxon:{taxon_id}")

    # Try organism name
    name_nodes = kg.query_nodes(name_contains=organism_name, limit=5)

    # Return node IDs as pipe-separated string
    node_ids = [ncbi_node['id']] if ncbi_node else []
    node_ids.extend(name_nodes['id'].tolist())

    kg.close()
    return "|".join(node_ids) if node_ids else ""
```

## Node and Edge Schema

### Node Columns
- `id`: Unique identifier (e.g., "CHEBI:16828", "EC:3.8.1.8", "NCBITaxon:419610")
- `name`: Human-readable name
- `category`: Biolink category (e.g., "biolink:Enzyme", "biolink:ChemicalEntity")
- Additional metadata columns vary by node type

### Edge Columns
- `subject`: Subject node ID
- `predicate`: Relationship type (e.g., "biolink:catalyzes", "biolink:consumes")
- `object`: Object node ID
- Additional metadata columns for evidence, publications, etc.

## Database Statistics

After creating the database, you should see statistics like:

```
=== Knowledge Graph Statistics ===

Total Nodes: 1,234,567
Total Edges: 2,345,678

Node Categories:
  biolink:ChemicalEntity: 500,000
  biolink:Gene: 300,000
  biolink:Protein: 200,000
  biolink:Pathway: 50,000
  biolink:Enzyme: 40,000
  ...

Edge Predicates:
  biolink:part_of: 800,000
  biolink:related_to: 600,000
  biolink:catalyzes: 100,000
  biolink:consumes: 80,000
  ...

ID Prefixes:
  CHEBI:: 450,000
  UniProtKB:: 300,000
  EC:: 45,000
  KEGG.COMPOUND:: 30,000
  NCBITaxon:: 25,000
  ...
```

## Troubleshooting

### Database File Too Large
The DuckDB file can be 1-5 GB. Add to `.gitignore`:
```
data/kgm/kg-microbe.duckdb
data/kgm/*.tsv
```

### Missing TSV Files
If `kg-microbe_nodes.tsv` or `kg-microbe_edges.tsv` don't exist, download them from KG-Hub or create placeholder files:

```bash
# Placeholder nodes
echo -e "id\tname\tcategory" > data/kgm/kg-microbe_nodes.tsv

# Placeholder edges
echo -e "subject\tpredicate\tobject" > data/kgm/kg-microbe_edges.tsv
```

### Query Performance
DuckDB automatically creates indexes on ID columns. For large queries:
- Use `limit` parameter to restrict results
- Filter by `category` or `id_prefix` before `name_contains`
- Consider pre-computing frequently used queries

## References

- **KG-Microbe**: https://github.com/Knowledge-Graph-Hub/kg-microbe
- **DuckDB**: https://duckdb.org/docs/
- **Biolink Model**: https://biolink.github.io/biolink-model/

## License

KG-Microbe data is licensed under CC0 1.0 Universal. See KG-Hub for details.
