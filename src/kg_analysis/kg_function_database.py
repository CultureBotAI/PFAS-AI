"""
Function Knowledge Graph Database using DuckDB

This module handles the larger function KG with 151M nodes and 555M edges,
providing specialized methods for querying functional annotations (EC numbers,
GO terms, pathways).
"""

import duckdb
from pathlib import Path
from typing import Optional, Dict, List, Any
import pandas as pd


class FunctionKnowledgeGraphDB:
    """DuckDB interface for the large-scale function knowledge graph."""

    def __init__(
        self,
        db_path: str = "data/kgm/kg-microbe-function.duckdb",
        nodes_file: str = "data/kgm/kg-microbe-function_nodes.tsv",
        edges_file: str = "data/kgm/kg-microbe-function_edges.tsv"
    ):
        """
        Initialize the function knowledge graph database.

        Args:
            db_path: Path to DuckDB database file
            nodes_file: Path to function nodes TSV (15GB, 151M nodes)
            edges_file: Path to function edges TSV (29GB, 555M edges)
        """
        self.db_path = Path(db_path)
        self.nodes_file = Path(nodes_file)
        self.edges_file = Path(edges_file)
        self.conn: Optional[duckdb.DuckDBPyConnection] = None

    def create_database(self, overwrite: bool = False, sample: bool = False) -> None:
        """
        Create DuckDB database and load TSV files.

        Args:
            overwrite: If True, delete existing database
            sample: If True, load only first 1M rows for testing
        """
        if overwrite and self.db_path.exists():
            self.db_path.unlink()
            print(f"Deleted existing database: {self.db_path}")

        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self.conn = duckdb.connect(str(self.db_path))

        # Load nodes (15GB file, may take ~5-10 minutes)
        print(f"Loading nodes from {self.nodes_file}...")
        print("This is a 15GB file with 151M nodes - may take several minutes...")

        sample_clause = "LIMIT 1000000" if sample else ""

        self.conn.execute(f"""
            CREATE OR REPLACE TABLE nodes AS
            SELECT * FROM read_csv_auto(
                '{self.nodes_file}',
                delim='\t',
                header=true,
                null_padding=true
            ) {sample_clause}
        """)

        # Load edges (29GB file, may take ~10-15 minutes)
        print(f"Loading edges from {self.edges_file}...")
        print("This is a 29GB file with 555M edges - may take 10-15 minutes...")

        self.conn.execute(f"""
            CREATE OR REPLACE TABLE edges AS
            SELECT * FROM read_csv_auto(
                '{self.edges_file}',
                delim='\t',
                header=true,
                null_padding=true,
                ignore_errors=true
            ) {sample_clause}
        """)

        # Create indexes for performance
        print("Creating indexes for fast queries...")
        self.conn.execute("CREATE INDEX IF NOT EXISTS idx_nodes_id ON nodes(id)")
        self.conn.execute("CREATE INDEX IF NOT EXISTS idx_nodes_category ON nodes(category)")
        self.conn.execute("CREATE INDEX IF NOT EXISTS idx_edges_subject ON edges(subject)")
        self.conn.execute("CREATE INDEX IF NOT EXISTS idx_edges_object ON edges(object)")
        self.conn.execute("CREATE INDEX IF NOT EXISTS idx_edges_predicate ON edges(predicate)")

        # Statistics
        node_count = self.conn.execute("SELECT COUNT(*) FROM nodes").fetchone()[0]
        edge_count = self.conn.execute("SELECT COUNT(*) FROM edges").fetchone()[0]

        print(f"\n✓ Function KG database created: {self.db_path}")
        print(f"  - Nodes: {node_count:,}")
        print(f"  - Edges: {edge_count:,}")

    def connect(self) -> duckdb.DuckDBPyConnection:
        """Connect to existing database."""
        if self.conn is None:
            if not self.db_path.exists():
                raise FileNotFoundError(
                    f"Database not found: {self.db_path}. "
                    "Run create_database() first."
                )
            self.conn = duckdb.connect(str(self.db_path))
        return self.conn

    def close(self) -> None:
        """Close database connection."""
        if self.conn:
            self.conn.close()
            self.conn = None

    def query(self, sql: str) -> pd.DataFrame:
        """Execute SQL query and return DataFrame."""
        conn = self.connect()
        return conn.execute(sql).df()

    def get_taxon_functions(
        self,
        taxon_ids: List[str],
        function_types: List[str] = None
    ) -> pd.DataFrame:
        """
        Get all functions associated with given taxa.

        Uses two-hop path: Taxon <- derives_from <- Protein -> participates_in/enables -> Function

        Args:
            taxon_ids: List of NCBITaxon IDs
            function_types: List of function ID prefixes (e.g., ['EC:', 'GO:', 'KEGG:'])

        Returns:
            DataFrame with taxon_id, function_id, function_name, function_type
        """
        if function_types is None:
            function_types = ['EC:', 'GO:', 'KEGG:', 'MetaCyc:', 'CHEBI:', 'RHEA:']

        taxa_list = ", ".join([f"'{tid}'" for tid in taxon_ids])
        type_conditions = " OR ".join([f"e2.object LIKE '{ft}%'" for ft in function_types])

        sql = f"""
        WITH taxon_proteins AS (
            -- Get all proteins from target taxa (UniProtKB -> derives_from -> NCBITaxon)
            SELECT DISTINCT
                e.subject as protein_id,
                e.object as taxon_id
            FROM edges e
            WHERE e.object IN ({taxa_list})
              AND e.predicate = 'biolink:derives_from'
        )
        SELECT DISTINCT
            tp.taxon_id,
            e2.object as function_id,
            n.name as function_name,
            n.category as function_category,
            e2.predicate,
            CASE
                WHEN e2.object LIKE 'EC:%' THEN 'Enzyme'
                WHEN e2.object LIKE 'GO:%' AND n.category LIKE '%BiologicalProcess%' THEN 'GO_Process'
                WHEN e2.object LIKE 'GO:%' AND n.category LIKE '%MolecularActivity%' THEN 'GO_Function'
                WHEN e2.object LIKE 'KEGG:%' OR e2.object LIKE 'MetaCyc:%' THEN 'Pathway'
                WHEN e2.object LIKE 'CHEBI:%' THEN 'Chemical'
                WHEN e2.object LIKE 'RHEA:%' THEN 'Reaction'
                ELSE 'Other'
            END as function_type
        FROM taxon_proteins tp
        JOIN edges e2 ON tp.protein_id = e2.subject
        JOIN nodes n ON e2.object = n.id
        WHERE ({type_conditions})
          AND e2.predicate IN ('biolink:participates_in', 'biolink:enables',
                                'biolink:located_in', 'biolink:related_to',
                                'biolink:has_participant', 'biolink:has_input',
                                'biolink:has_output')
        """

        return self.query(sql)

    def get_function_prevalence(
        self,
        function_ids: List[str],
        taxon_group: List[str]
    ) -> pd.DataFrame:
        """
        Calculate prevalence of functions across a group of taxa.

        Args:
            function_ids: List of function IDs to check
            taxon_group: List of NCBITaxon IDs

        Returns:
            DataFrame with function_id, taxa_count, prevalence
        """
        func_list = ", ".join([f"'{fid}'" for fid in function_ids])
        taxa_list = ", ".join([f"'{tid}'" for tid in taxon_group])

        sql = f"""
        SELECT
            e.object as function_id,
            n.name as function_name,
            COUNT(DISTINCT e.subject) as taxa_count,
            COUNT(DISTINCT e.subject) * 1.0 / {len(taxon_group)} as prevalence
        FROM edges e
        JOIN nodes n ON e.object = n.id
        WHERE e.object IN ({func_list})
          AND e.subject IN ({taxa_list})
        GROUP BY e.object, n.name
        ORDER BY taxa_count DESC
        """

        return self.query(sql)

    def compare_functions(
        self,
        target_taxa: List[str],
        reference_taxa: List[str],
        min_target_prevalence: float = 0.5,
        max_reference_prevalence: float = 0.05
    ) -> pd.DataFrame:
        """
        Find functions enriched in target taxa vs reference taxa.

        Uses two-hop path: Taxon <- derives_from <- Protein -> participates_in/enables -> Function

        Args:
            target_taxa: List of NCBITaxon IDs for target organisms
            reference_taxa: List of NCBITaxon IDs for reference organisms
            min_target_prevalence: Minimum fraction of target taxa (default 0.5 = 50%)
            max_reference_prevalence: Maximum fraction of reference taxa (default 0.05 = 5%)

        Returns:
            DataFrame with enriched functions and statistics
        """
        target_list = ", ".join([f"'{tid}'" for tid in target_taxa])
        ref_list = ", ".join([f"'{tid}'" for tid in reference_taxa])

        sql = f"""
        WITH target_proteins AS (
            -- Get all proteins from target taxa (UniProtKB -> derives_from -> NCBITaxon)
            SELECT DISTINCT
                e.subject as protein_id,
                e.object as taxon_id
            FROM edges e
            WHERE e.object IN ({target_list})
              AND e.predicate = 'biolink:derives_from'
        ),
        target_functions AS (
            -- Get functions for target proteins
            SELECT
                e2.object as function_id,
                n.name as function_name,
                n.category as function_category,
                COUNT(DISTINCT tp.taxon_id) as target_count,
                COUNT(DISTINCT tp.taxon_id) * 1.0 / {len(target_taxa)} as target_prevalence,
                CASE
                    WHEN e2.object LIKE 'EC:%' THEN 'Enzyme'
                    WHEN e2.object LIKE 'GO:%' AND n.category LIKE '%BiologicalProcess%' THEN 'GO_Process'
                    WHEN e2.object LIKE 'GO:%' AND n.category LIKE '%MolecularActivity%' THEN 'GO_Function'
                    WHEN e2.object LIKE 'KEGG:%' OR e2.object LIKE 'MetaCyc:%' THEN 'Pathway'
                    WHEN e2.object LIKE 'CHEBI:%' THEN 'Chemical'
                    WHEN e2.object LIKE 'RHEA:%' THEN 'Reaction'
                    ELSE 'Other'
                END as function_type
            FROM target_proteins tp
            JOIN edges e2 ON tp.protein_id = e2.subject
            JOIN nodes n ON e2.object = n.id
            WHERE (e2.object LIKE 'EC:%' OR e2.object LIKE 'GO:%'
                   OR e2.object LIKE 'KEGG:%' OR e2.object LIKE 'MetaCyc:%'
                   OR e2.object LIKE 'CHEBI:%' OR e2.object LIKE 'RHEA:%')
              AND e2.predicate IN ('biolink:participates_in', 'biolink:enables',
                                    'biolink:located_in', 'biolink:related_to',
                                    'biolink:has_participant', 'biolink:has_input',
                                    'biolink:has_output')
            GROUP BY e2.object, n.name, n.category
            HAVING COUNT(DISTINCT tp.taxon_id) * 1.0 / {len(target_taxa)} >= {min_target_prevalence}
        ),
        reference_proteins AS (
            -- Get all proteins from reference taxa
            SELECT DISTINCT
                e.subject as protein_id,
                e.object as taxon_id
            FROM edges e
            WHERE e.object IN ({ref_list})
              AND e.predicate = 'biolink:derives_from'
        ),
        reference_functions AS (
            -- Get functions for reference proteins
            SELECT
                e2.object as function_id,
                COUNT(DISTINCT rp.taxon_id) as reference_count,
                COUNT(DISTINCT rp.taxon_id) * 1.0 / {len(reference_taxa)} as reference_prevalence
            FROM reference_proteins rp
            JOIN edges e2 ON rp.protein_id = e2.subject
            WHERE (e2.object LIKE 'EC:%' OR e2.object LIKE 'GO:%'
                   OR e2.object LIKE 'KEGG:%' OR e2.object LIKE 'MetaCyc:%'
                   OR e2.object LIKE 'CHEBI:%' OR e2.object LIKE 'RHEA:%')
              AND e2.predicate IN ('biolink:participates_in', 'biolink:enables',
                                    'biolink:located_in', 'biolink:related_to',
                                    'biolink:has_participant', 'biolink:has_input',
                                    'biolink:has_output')
            GROUP BY e2.object
        )
        SELECT
            tf.function_id,
            tf.function_name,
            tf.function_type,
            tf.function_category,
            tf.target_count,
            tf.target_prevalence,
            COALESCE(rf.reference_count, 0) as reference_count,
            COALESCE(rf.reference_prevalence, 0) as reference_prevalence,
            tf.target_prevalence / GREATEST(COALESCE(rf.reference_prevalence, 0.001), 0.001) as enrichment_ratio
        FROM target_functions tf
        LEFT JOIN reference_functions rf ON tf.function_id = rf.function_id
        WHERE COALESCE(rf.reference_prevalence, 0) <= {max_reference_prevalence}
        ORDER BY tf.target_prevalence DESC, enrichment_ratio DESC
        """

        return self.query(sql)

    def get_statistics(self) -> Dict[str, Any]:
        """Get database statistics."""
        conn = self.connect()

        stats = {
            "total_nodes": conn.execute("SELECT COUNT(*) FROM nodes").fetchone()[0],
            "total_edges": conn.execute("SELECT COUNT(*) FROM edges").fetchone()[0],
            "function_counts": conn.execute("""
                SELECT
                    CASE
                        WHEN ANY_VALUE(id) LIKE 'EC:%' THEN 'Enzymes (EC)'
                        WHEN ANY_VALUE(id) LIKE 'GO:%' AND ANY_VALUE(category) LIKE '%BiologicalProcess%' THEN 'GO Biological Process'
                        WHEN ANY_VALUE(id) LIKE 'GO:%' AND ANY_VALUE(category) LIKE '%MolecularActivity%' THEN 'GO Molecular Function'
                        WHEN ANY_VALUE(id) LIKE 'KEGG:%' THEN 'KEGG Pathways'
                        WHEN ANY_VALUE(id) LIKE 'MetaCyc:%' THEN 'MetaCyc Pathways'
                        WHEN ANY_VALUE(id) LIKE 'NCBITaxon:%' THEN 'Taxa'
                        ELSE 'Other'
                    END as category,
                    COUNT(*) as count
                FROM nodes
                GROUP BY
                    CASE
                        WHEN id LIKE 'EC:%' THEN 'Enzymes (EC)'
                        WHEN id LIKE 'GO:%' AND category LIKE '%BiologicalProcess%' THEN 'GO Biological Process'
                        WHEN id LIKE 'GO:%' AND category LIKE '%MolecularActivity%' THEN 'GO Molecular Function'
                        WHEN id LIKE 'KEGG:%' THEN 'KEGG Pathways'
                        WHEN id LIKE 'MetaCyc:%' THEN 'MetaCyc Pathways'
                        WHEN id LIKE 'NCBITaxon:%' THEN 'Taxa'
                        ELSE 'Other'
                    END
                ORDER BY count DESC
            """).df().to_dict('records')
        }

        return stats

    def __enter__(self):
        """Context manager entry."""
        self.connect()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.close()


def main():
    """Create database and show statistics."""
    import argparse

    parser = argparse.ArgumentParser(
        description="Create and manage function knowledge graph database"
    )
    parser.add_argument(
        "--create",
        action="store_true",
        help="Create/recreate the database from TSV files"
    )
    parser.add_argument(
        "--overwrite",
        action="store_true",
        help="Overwrite existing database"
    )
    parser.add_argument(
        "--sample",
        action="store_true",
        help="Load only 1M rows for testing (much faster)"
    )
    parser.add_argument(
        "--stats",
        action="store_true",
        help="Show database statistics"
    )

    args = parser.parse_args()

    kg = FunctionKnowledgeGraphDB()

    if args.create:
        print("=" * 80)
        print("CREATING FUNCTION KNOWLEDGE GRAPH DATABASE")
        print("=" * 80)
        print()
        if args.sample:
            print("⚠️  SAMPLE MODE: Loading only 1M rows for testing")
        else:
            print("⚠️  FULL MODE: Loading 151M nodes + 555M edges")
            print("This will take 15-30 minutes and create a ~40GB database")
        print()

        kg.create_database(overwrite=args.overwrite, sample=args.sample)

    if args.stats:
        with kg:
            stats = kg.get_statistics()
            print("\n=== Function Knowledge Graph Statistics ===\n")
            print(f"Total Nodes: {stats['total_nodes']:,}")
            print(f"Total Edges: {stats['total_edges']:,}")
            print("\nNode Types:")
            for cat in stats['function_counts']:
                print(f"  {cat['category']}: {cat['count']:,}")

    kg.close()


if __name__ == "__main__":
    main()
