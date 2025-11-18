"""
Knowledge Graph Database using DuckDB

This module creates and manages a DuckDB database for the lanthanide bioprocessing
knowledge graph, providing convenient query methods for exploring nodes and edges.

Usage:
    >>> from src.kg_database import KnowledgeGraphDB
    >>> kg = KnowledgeGraphDB()
    >>> kg.create_database()
    >>> nodes = kg.query_nodes(category="biolink:Enzyme")
    >>> edges = kg.query_edges(predicate="biolink:consumes")
"""

import duckdb
from pathlib import Path
from typing import Optional, Dict, List, Any
import pandas as pd


class KnowledgeGraphDB:
    """DuckDB interface for the microbe knowledge graph."""

    def __init__(
        self,
        db_path: str = "data/kgm/kg-microbe.duckdb",
        nodes_file: str = "data/kgm/kg-microbe_nodes.tsv",
        edges_file: str = "data/kgm/kg-microbe_edges.tsv"
    ):
        """
        Initialize the knowledge graph database.

        Args:
            db_path: Path to DuckDB database file (will be created if doesn't exist)
            nodes_file: Path to TSV file containing knowledge graph nodes
            edges_file: Path to TSV file containing knowledge graph edges
        """
        self.db_path = Path(db_path)
        self.nodes_file = Path(nodes_file)
        self.edges_file = Path(edges_file)
        self.conn: Optional[duckdb.DuckDBPyConnection] = None

    def create_database(self, overwrite: bool = False) -> None:
        """
        Create DuckDB database and load TSV files into tables.

        Args:
            overwrite: If True, delete existing database and create new one
        """
        if overwrite and self.db_path.exists():
            self.db_path.unlink()
            print(f"Deleted existing database: {self.db_path}")

        # Create directory if it doesn't exist
        self.db_path.parent.mkdir(parents=True, exist_ok=True)

        # Connect to database
        self.conn = duckdb.connect(str(self.db_path))

        # Load nodes table
        print(f"Loading nodes from {self.nodes_file}...")
        self.conn.execute(f"""
            CREATE OR REPLACE TABLE nodes AS
            SELECT * FROM read_csv_auto('{self.nodes_file}', delim='\t', header=true)
        """)

        # Load edges table (with lenient parsing for inconsistent columns)
        print(f"Loading edges from {self.edges_file}...")
        self.conn.execute(f"""
            CREATE OR REPLACE TABLE edges AS
            SELECT * FROM read_csv_auto(
                '{self.edges_file}',
                delim='\t',
                header=true,
                null_padding=true,
                ignore_errors=true
            )
        """)

        # Create indexes for faster queries
        print("Creating indexes...")
        self.conn.execute("CREATE INDEX IF NOT EXISTS idx_nodes_id ON nodes(id)")
        self.conn.execute("CREATE INDEX IF NOT EXISTS idx_nodes_category ON nodes(category)")
        self.conn.execute("CREATE INDEX IF NOT EXISTS idx_edges_subject ON edges(subject)")
        self.conn.execute("CREATE INDEX IF NOT EXISTS idx_edges_object ON edges(object)")
        self.conn.execute("CREATE INDEX IF NOT EXISTS idx_edges_predicate ON edges(predicate)")

        # Print statistics
        node_count = self.conn.execute("SELECT COUNT(*) FROM nodes").fetchone()[0]
        edge_count = self.conn.execute("SELECT COUNT(*) FROM edges").fetchone()[0]

        print(f"\n✓ Database created: {self.db_path}")
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
        """
        Execute SQL query and return results as DataFrame.

        Args:
            sql: SQL query string

        Returns:
            pandas DataFrame with query results
        """
        conn = self.connect()
        return conn.execute(sql).df()

    def query_nodes(
        self,
        category: Optional[str] = None,
        id_prefix: Optional[str] = None,
        name_contains: Optional[str] = None,
        limit: Optional[int] = None
    ) -> pd.DataFrame:
        """
        Query nodes with optional filters.

        Args:
            category: Filter by category (e.g., "biolink:Enzyme")
            id_prefix: Filter by ID prefix (e.g., "CHEBI:", "EC:")
            name_contains: Filter by name containing text (case-insensitive)
            limit: Maximum number of results

        Returns:
            DataFrame containing matching nodes

        Examples:
            >>> kg = KnowledgeGraphDB()
            >>> kg.connect()
            >>> enzymes = kg.query_nodes(category="biolink:Enzyme")
            >>> chemicals = kg.query_nodes(id_prefix="CHEBI:")
            >>> tryptophan = kg.query_nodes(name_contains="tryptophan")
        """
        conditions = []

        if category:
            # Handle both single category and multiple categories (separated by |)
            conditions.append(f"category LIKE '%{category}%'")

        if id_prefix:
            conditions.append(f"id LIKE '{id_prefix}%'")

        if name_contains:
            conditions.append(f"LOWER(name) LIKE '%{name_contains.lower()}%'")

        where_clause = " AND ".join(conditions) if conditions else "1=1"
        limit_clause = f"LIMIT {limit}" if limit else ""

        sql = f"""
            SELECT * FROM nodes
            WHERE {where_clause}
            {limit_clause}
        """

        return self.query(sql)

    def query_edges(
        self,
        subject: Optional[str] = None,
        predicate: Optional[str] = None,
        object: Optional[str] = None,
        limit: Optional[int] = None
    ) -> pd.DataFrame:
        """
        Query edges with optional filters.

        Args:
            subject: Filter by subject node ID
            predicate: Filter by predicate (e.g., "biolink:consumes")
            object: Filter by object node ID
            limit: Maximum number of results

        Returns:
            DataFrame containing matching edges

        Examples:
            >>> kg = KnowledgeGraphDB()
            >>> kg.connect()
            >>> consumption = kg.query_edges(predicate="biolink:consumes")
            >>> enzyme_edges = kg.query_edges(subject="EC:4.1.99.1")
        """
        conditions = []

        if subject:
            conditions.append(f"subject = '{subject}'")

        if predicate:
            conditions.append(f"predicate = '{predicate}'")

        if object:
            conditions.append(f"object = '{object}'")

        where_clause = " AND ".join(conditions) if conditions else "1=1"
        limit_clause = f"LIMIT {limit}" if limit else ""

        sql = f"""
            SELECT * FROM edges
            WHERE {where_clause}
            {limit_clause}
        """

        return self.query(sql)

    def get_node(self, node_id: str) -> Optional[Dict[str, Any]]:
        """
        Get a single node by ID.

        Args:
            node_id: Node identifier (e.g., "CHEBI:16828", "EC:4.1.99.1")

        Returns:
            Dictionary with node data or None if not found
        """
        result = self.query(f"SELECT * FROM nodes WHERE id = '{node_id}'")
        if len(result) == 0:
            return None
        return result.iloc[0].to_dict()

    def get_neighbors(
        self,
        node_id: str,
        predicate: Optional[str] = None,
        direction: str = "both"
    ) -> pd.DataFrame:
        """
        Get neighboring nodes connected via edges.

        Args:
            node_id: Node identifier
            predicate: Optional predicate filter
            direction: "outgoing", "incoming", or "both"

        Returns:
            DataFrame with neighbor nodes and their connecting edges
        """
        pred_filter = f"AND e.predicate = '{predicate}'" if predicate else ""

        if direction == "outgoing":
            sql = f"""
                SELECT e.*, n.name as object_name, n.category as object_category
                FROM edges e
                JOIN nodes n ON e.object = n.id
                WHERE e.subject = '{node_id}' {pred_filter}
            """
        elif direction == "incoming":
            sql = f"""
                SELECT e.*, n.name as subject_name, n.category as subject_category
                FROM edges e
                JOIN nodes n ON e.subject = n.id
                WHERE e.object = '{node_id}' {pred_filter}
            """
        else:  # both
            sql = f"""
                SELECT e.*,
                       CASE WHEN e.subject = '{node_id}' THEN n.name END as object_name,
                       CASE WHEN e.object = '{node_id}' THEN n.name END as subject_name,
                       CASE WHEN e.subject = '{node_id}' THEN n.category END as object_category,
                       CASE WHEN e.object = '{node_id}' THEN n.category END as subject_category
                FROM edges e
                LEFT JOIN nodes n ON (e.object = n.id OR e.subject = n.id)
                WHERE (e.subject = '{node_id}' OR e.object = '{node_id}') {pred_filter}
            """

        return self.query(sql)

    def find_paths(
        self,
        start_node: str,
        end_node: str,
        max_depth: int = 3
    ) -> pd.DataFrame:
        """
        Find paths between two nodes in the knowledge graph.

        Args:
            start_node: Starting node ID
            end_node: Ending node ID
            max_depth: Maximum path length

        Returns:
            DataFrame with paths found
        """
        # Recursive CTE to find paths
        sql = f"""
            WITH RECURSIVE paths AS (
                -- Base case: direct edges
                SELECT
                    subject,
                    object,
                    predicate,
                    1 as depth,
                    CAST(subject || ' -> ' || object AS VARCHAR) as path
                FROM edges
                WHERE subject = '{start_node}'

                UNION ALL

                -- Recursive case: extend paths
                SELECT
                    p.subject,
                    e.object,
                    e.predicate,
                    p.depth + 1,
                    CAST(p.path || ' -> ' || e.object AS VARCHAR)
                FROM paths p
                JOIN edges e ON p.object = e.subject
                WHERE p.depth < {max_depth}
                  AND p.path NOT LIKE '%' || e.object || '%'  -- Avoid cycles
            )
            SELECT * FROM paths
            WHERE object = '{end_node}'
            ORDER BY depth, path
        """

        return self.query(sql)

    def get_statistics(self) -> Dict[str, Any]:
        """
        Get database statistics.

        Returns:
            Dictionary with statistics
        """
        conn = self.connect()

        stats = {
            "total_nodes": conn.execute("SELECT COUNT(*) FROM nodes").fetchone()[0],
            "total_edges": conn.execute("SELECT COUNT(*) FROM edges").fetchone()[0],
            "node_categories": conn.execute("""
                SELECT category, COUNT(*) as count
                FROM nodes
                GROUP BY category
                ORDER BY count DESC
            """).df().to_dict('records'),
            "edge_predicates": conn.execute("""
                SELECT predicate, COUNT(*) as count
                FROM edges
                GROUP BY predicate
                ORDER BY count DESC
            """).df().to_dict('records'),
            "id_prefixes": conn.execute("""
                SELECT SUBSTRING(id, 1, POSITION(':' IN id)) as prefix, COUNT(*) as count
                FROM nodes
                WHERE POSITION(':' IN id) > 0
                GROUP BY prefix
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
    """Create database and run example queries."""
    import argparse

    parser = argparse.ArgumentParser(
        description="Create and query the microbe knowledge graph database"
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
        "--stats",
        action="store_true",
        help="Show database statistics"
    )

    args = parser.parse_args()

    kg = KnowledgeGraphDB()

    if args.create:
        kg.create_database(overwrite=args.overwrite)

    if args.stats:
        stats = kg.get_statistics()
        print("\n=== Knowledge Graph Statistics ===\n")
        print(f"Total Nodes: {stats['total_nodes']:,}")
        print(f"Total Edges: {stats['total_edges']:,}")

        print("\nNode Categories:")
        for cat in stats['node_categories'][:10]:
            print(f"  {cat['category']}: {cat['count']:,}")

        print("\nEdge Predicates:")
        for pred in stats['edge_predicates'][:10]:
            print(f"  {pred['predicate']}: {pred['count']:,}")

        print("\nID Prefixes:")
        for prefix in stats['id_prefixes'][:10]:
            print(f"  {prefix['prefix']}: {prefix['count']:,}")

    kg.close()


if __name__ == "__main__":
    main()
