"""
Knowledge Graph Mining Utilities for extend3

Shared utilities for querying Knowledge Graph databases and preparing data
for extend3 table extension with proper source labeling.

This module provides:
- Database connection management for kg-microbe and kg-microbe-function
- Common query patterns for organisms, proteins, pathways, chemicals
- Result caching and batching utilities
- Source label helpers for extend3_* variants
- TSV export utilities
"""

from pathlib import Path
from typing import List, Dict, Any, Optional, Set, Tuple
import pandas as pd
from src.kg_analysis.kg_database import KnowledgeGraphDB
from src.kg_analysis.kg_function_database import FunctionKnowledgeGraphDB


class KGMiningSession:
    """
    Session manager for Knowledge Graph mining with connection pooling
    and result caching.
    """

    def __init__(
        self,
        use_function_kg: bool = True,
        use_phenotype_kg: bool = True
    ):
        """
        Initialize KG mining session.

        Args:
            use_function_kg: Enable kg-microbe-function database
            use_phenotype_kg: Enable kg-microbe database
        """
        self.use_function_kg = use_function_kg
        self.use_phenotype_kg = use_phenotype_kg
        self.function_kg: Optional[FunctionKnowledgeGraphDB] = None
        self.phenotype_kg: Optional[KnowledgeGraphDB] = None
        self._cache: Dict[str, Any] = {}

    def __enter__(self):
        """Context manager entry - connect to databases."""
        if self.use_function_kg:
            self.function_kg = FunctionKnowledgeGraphDB()
            self.function_kg.connect()
            print("✓ Connected to kg-microbe-function (151M nodes, 555M edges)")

        if self.use_phenotype_kg:
            self.phenotype_kg = KnowledgeGraphDB()
            self.phenotype_kg.connect()
            print("✓ Connected to kg-microbe (1.4M nodes, 3.3M edges)")

        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit - close connections."""
        if self.function_kg:
            self.function_kg.close()
        if self.phenotype_kg:
            self.phenotype_kg.close()

    def cache_get(self, key: str) -> Optional[Any]:
        """Get value from cache."""
        return self._cache.get(key)

    def cache_set(self, key: str, value: Any) -> None:
        """Set value in cache."""
        self._cache[key] = value

    def clear_cache(self) -> None:
        """Clear all cached results."""
        self._cache.clear()


def load_taxon_ids(
    taxa_file: str = "data/txt/sheet/BER_CMM_Data_for_AI_taxa_and_genomes.tsv"
) -> List[str]:
    """
    Load NCBITaxon IDs from taxa_and_genomes table.

    Args:
        taxa_file: Path to taxa TSV file

    Returns:
        List of NCBITaxon IDs formatted as "NCBITaxon:12345"

    Example:
        >>> taxon_ids = load_taxon_ids()
        >>> len(taxon_ids) > 0
        True
        >>> all(tid.startswith("NCBITaxon:") for tid in taxon_ids)
        True
    """
    df = pd.read_csv(taxa_file, sep='\t')

    # Extract NCBITaxon ids (column: "NCBITaxon id")
    taxon_ids = []
    for idx, row in df.iterrows():
        taxon_id = row.get("NCBITaxon id")
        if pd.notna(taxon_id):
            # Handle both string and numeric formats
            tid = str(int(float(taxon_id)))  # Convert to int first to remove .0
            taxon_ids.append(f"NCBITaxon:{tid}")

    print(f"Loaded {len(taxon_ids)} NCBITaxon IDs from {taxa_file}")
    return taxon_ids


def load_existing_gene_ids(
    genes_file: str = "data/txt/sheet/extended/BER_CMM_Data_for_AI_genes_and_proteins_extended.tsv"
) -> Set[str]:
    """
    Load existing gene/protein IDs to avoid duplicates.

    Args:
        genes_file: Path to genes TSV file

    Returns:
        Set of existing gene_protein_id values
    """
    if not Path(genes_file).exists():
        print(f"⚠️  File not found: {genes_file}")
        return set()

    df = pd.read_csv(genes_file, sep='\t')
    gene_ids = set(df["gene_protein_id"].dropna().unique())
    print(f"Loaded {len(gene_ids)} existing gene IDs from {genes_file}")
    return gene_ids


def load_existing_pathway_ids(
    pathways_file: str = "data/txt/sheet/extended/BER_CMM_Data_for_AI_pathways_extended.tsv"
) -> Set[str]:
    """
    Load existing pathway IDs to avoid duplicates.

    Args:
        pathways_file: Path to pathways TSV file

    Returns:
        Set of existing pathway_id values
    """
    if not Path(pathways_file).exists():
        print(f"⚠️  File not found: {pathways_file}")
        return set()

    df = pd.read_csv(pathways_file, sep='\t')
    pathway_ids = set(df["pathway_id"].dropna().unique())
    print(f"Loaded {len(pathway_ids)} existing pathway IDs from {pathways_file}")
    return pathway_ids


def load_existing_chemical_ids(
    chemicals_file: str = "data/txt/sheet/extended/BER_CMM_Data_for_AI_chemicals_extended.tsv"
) -> Set[str]:
    """
    Load existing chemical IDs to avoid duplicates.

    Args:
        chemicals_file: Path to chemicals TSV file

    Returns:
        Set of existing chemical_id values
    """
    if not Path(chemicals_file).exists():
        print(f"⚠️  File not found: {chemicals_file}")
        return set()

    df = pd.read_csv(chemicals_file, sep='\t')
    chemical_ids = set(df["chemical_id"].dropna().unique())
    print(f"Loaded {len(chemical_ids)} existing chemical IDs from {chemicals_file}")
    return chemical_ids


def format_source_label(
    base_source: str,
    additional_refs: Optional[List[str]] = None
) -> str:
    """
    Format source label with optional additional references.

    Args:
        base_source: Base source label (e.g., "extend3_kg_function")
        additional_refs: Additional references to append (DOIs, PMIDs, etc.)

    Returns:
        Formatted source string

    Example:
        >>> format_source_label("extend3_kg_function")
        'extend3_kg_function'
        >>> format_source_label("extend3_kg_function", ["PMID:12345"])
        'extend3_kg_function|PMID:12345'
    """
    if not additional_refs:
        return base_source

    refs = "|".join(additional_refs)
    return f"{base_source}|{refs}"


def batch_query_taxa(
    session: KGMiningSession,
    taxon_ids: List[str],
    batch_size: int = 50,
    function_types: Optional[List[str]] = None
) -> pd.DataFrame:
    """
    Query function KG for multiple taxa in batches.

    Args:
        session: Active KG mining session
        taxon_ids: List of NCBITaxon IDs
        batch_size: Number of taxa per batch
        function_types: Function ID prefixes to query

    Returns:
        Combined DataFrame with all results
    """
    if not session.function_kg:
        raise RuntimeError("Function KG not enabled in session")

    all_results = []

    for i in range(0, len(taxon_ids), batch_size):
        batch = taxon_ids[i:i+batch_size]
        print(f"Querying batch {i//batch_size + 1} ({len(batch)} taxa)...")

        results = session.function_kg.get_taxon_functions(
            taxon_ids=batch,
            function_types=function_types
        )
        all_results.append(results)

    if not all_results:
        return pd.DataFrame()

    combined = pd.concat(all_results, ignore_index=True)
    print(f"Retrieved {len(combined)} total function associations")
    return combined


def extract_ec_numbers(df: pd.DataFrame) -> pd.DataFrame:
    """
    Extract and format EC numbers from KG query results.

    Args:
        df: DataFrame with function_id and function_name columns

    Returns:
        DataFrame with ec_number column added
    """
    df = df.copy()
    df["ec_number"] = df["function_id"].apply(
        lambda x: x.replace("EC:", "") if str(x).startswith("EC:") else None
    )
    return df


def extract_go_terms(df: pd.DataFrame) -> pd.DataFrame:
    """
    Extract and format GO terms from KG query results.

    Args:
        df: DataFrame with function_id and function_name columns

    Returns:
        DataFrame with go_terms column added
    """
    df = df.copy()
    df["go_term"] = df["function_id"].apply(
        lambda x: x if str(x).startswith("GO:") else None
    )
    return df


def extract_chebi_terms(df: pd.DataFrame) -> pd.DataFrame:
    """
    Extract and format CHEBI terms from KG query results.

    Args:
        df: DataFrame with function_id and function_name columns

    Returns:
        DataFrame with chebi_terms column added
    """
    df = df.copy()
    df["chebi_term"] = df["function_id"].apply(
        lambda x: x if str(x).startswith("CHEBI:") else None
    )
    return df


def deduplicate_and_merge(
    new_data: pd.DataFrame,
    existing_ids: Set[str],
    id_column: str
) -> pd.DataFrame:
    """
    Remove duplicates based on existing IDs.

    Args:
        new_data: New records to add
        existing_ids: Set of existing IDs to exclude
        id_column: Name of ID column

    Returns:
        Deduplicated DataFrame
    """
    original_count = len(new_data)
    new_data = new_data[~new_data[id_column].isin(existing_ids)]
    removed_count = original_count - len(new_data)

    if removed_count > 0:
        print(f"Removed {removed_count} duplicate entries")

    return new_data


def save_extended_table(
    df: pd.DataFrame,
    output_file: str,
    append: bool = False
) -> None:
    """
    Save extended table to TSV file.

    Args:
        df: DataFrame to save
        output_file: Output TSV file path
        append: If True, append to existing file
    """
    output_path = Path(output_file)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    if append and output_path.exists():
        # Load existing data and concatenate
        existing = pd.read_csv(output_path, sep='\t')
        df = pd.concat([existing, df], ignore_index=True)

    df.to_csv(output_path, sep='\t', index=False)
    print(f"✓ Saved {len(df)} records to {output_file}")


def get_uniprot_ids_from_function_kg(
    session: KGMiningSession,
    taxon_ids: List[str]
) -> pd.DataFrame:
    """
    Get UniProt IDs for proteins from target taxa via function KG.

    Args:
        session: Active KG mining session
        taxon_ids: List of NCBITaxon IDs

    Returns:
        DataFrame with protein_id (UniProtKB IDs) and taxon_id
    """
    if not session.function_kg:
        raise RuntimeError("Function KG not enabled in session")

    taxa_list = ", ".join([f"'{tid}'" for tid in taxon_ids])

    sql = f"""
    SELECT DISTINCT
        e.subject as protein_id,
        e.object as taxon_id
    FROM edges e
    WHERE e.object IN ({taxa_list})
      AND e.predicate = 'biolink:derives_from'
      AND e.subject LIKE 'UniProtKB:%'
    LIMIT 10000
    """

    df = session.function_kg.query(sql)
    print(f"Retrieved {len(df)} UniProt IDs for {len(taxon_ids)} taxa")
    return df


def summarize_extraction(
    table_name: str,
    original_count: int,
    new_count: int,
    source_label: str
) -> None:
    """
    Print summary of data extraction.

    Args:
        table_name: Name of table being extended
        original_count: Original row count
        new_count: New row count added
        source_label: Source label used
    """
    print("\n" + "="*60)
    print(f"EXTRACTION SUMMARY: {table_name}")
    print("="*60)
    print(f"New records added: {new_count}")
    print(f"Source label: {source_label}")
    if original_count > 0:
        increase_pct = (new_count / original_count) * 100
        print(f"Data increase: +{increase_pct:.1f}%")
    print("="*60 + "\n")
