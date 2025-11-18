"""
Analyze knowledge graph nodes connected to NCBITaxon IDs from genomes table.

This script finds all nodes in the knowledge graph that have edges to the
NCBITaxon IDs present in the taxa_and_genomes_extended.tsv file, excluding
subclass relationships to other NCBITaxon nodes.
"""

import pandas as pd
from pathlib import Path
from typing import List, Dict, Any
from .kg_database import KnowledgeGraphDB


def read_genome_taxa(tsv_file: str = "data/txt/sheet/BER_CMM_Data_for_AI_taxa_and_genomes_extended.tsv") -> List[str]:
    """
    Read NCBITaxon IDs from the genomes table.

    Args:
        tsv_file: Path to the genomes TSV file

    Returns:
        List of NCBITaxon IDs (as strings with NCBITaxon: prefix)
    """
    df = pd.read_csv(tsv_file, sep='\t')

    # Extract NCBITaxon ids (second column), filter out empty/NaN values
    taxon_ids = df.iloc[:, 1].dropna()

    # Convert to NCBITaxon: format and filter valid IDs
    ncbi_taxon_ids = []
    for taxon_id in taxon_ids:
        if pd.notna(taxon_id) and str(taxon_id).strip():
            # Handle both formats: "270351" or "NCBITaxon:270351"
            taxon_id_str = str(taxon_id).strip()
            if not taxon_id_str.startswith("NCBITaxon:"):
                # Convert to int to remove .0, then back to string
                try:
                    taxon_id_int = int(float(taxon_id_str))
                    taxon_id_str = f"NCBITaxon:{taxon_id_int}"
                except (ValueError, TypeError):
                    # If conversion fails, use as-is
                    taxon_id_str = f"NCBITaxon:{taxon_id_str}"
            ncbi_taxon_ids.append(taxon_id_str)

    return ncbi_taxon_ids


def get_taxa_in_kg(kg: KnowledgeGraphDB, taxon_ids: List[str]) -> List[str]:
    """
    Find which taxa have any edges in the knowledge graph.

    Args:
        kg: KnowledgeGraphDB instance
        taxon_ids: List of NCBITaxon IDs to check

    Returns:
        List of NCBITaxon IDs that exist in the KG
    """
    taxon_ids_quoted = ", ".join([f"'{tid}'" for tid in taxon_ids])

    sql = f"""
    SELECT DISTINCT taxon_id
    FROM (
        SELECT subject as taxon_id FROM edges WHERE subject IN ({taxon_ids_quoted})
        UNION
        SELECT object as taxon_id FROM edges WHERE object IN ({taxon_ids_quoted})
    )
    """

    result = kg.query(sql)
    return result['taxon_id'].tolist()


def get_connected_nodes(kg: KnowledgeGraphDB, taxon_ids: List[str]) -> pd.DataFrame:
    """
    Find all nodes connected to the given NCBITaxon IDs, excluding
    subclass_of relationships to other NCBITaxon nodes.

    Args:
        kg: KnowledgeGraphDB instance
        taxon_ids: List of NCBITaxon IDs to query

    Returns:
        DataFrame with connected nodes and edge information
    """
    # Create a SQL query to find all edges involving these taxon IDs
    # but exclude subclass_of edges to other NCBITaxon nodes

    # Simpler approach: use IN clause
    taxon_ids_quoted = ", ".join([f"'{tid}'" for tid in taxon_ids])

    sql = f"""
    WITH all_edges AS (
        -- Edges where taxon is the subject
        SELECT
            e.subject,
            e.predicate,
            e.object,
            e.relation,
            e.knowledge_source,
            'outgoing' as direction,
            n.id as connected_node_id,
            n.name as connected_node_name,
            n.category as connected_node_category,
            n.description as connected_node_description
        FROM edges e
        JOIN nodes n ON e.object = n.id
        WHERE e.subject IN ({taxon_ids_quoted})
          AND NOT (
              e.predicate = 'biolink:subclass_of'
              AND n.id LIKE 'NCBITaxon:%'
          )

        UNION ALL

        -- Edges where taxon is the object
        SELECT
            e.subject,
            e.predicate,
            e.object,
            e.relation,
            e.knowledge_source,
            'incoming' as direction,
            n.id as connected_node_id,
            n.name as connected_node_name,
            n.category as connected_node_category,
            n.description as connected_node_description
        FROM edges e
        JOIN nodes n ON e.subject = n.id
        WHERE e.object IN ({taxon_ids_quoted})
          AND NOT (
              e.predicate = 'biolink:subclass_of'
              AND n.id LIKE 'NCBITaxon:%'
          )
    )
    SELECT
        subject,
        predicate,
        object,
        direction,
        connected_node_id,
        connected_node_name,
        connected_node_category,
        connected_node_description,
        relation,
        knowledge_source
    FROM all_edges
    ORDER BY predicate, connected_node_category, connected_node_name
    """

    return kg.query(sql)


def analyze_connected_nodes(df: pd.DataFrame, all_taxon_ids: List[str]) -> Dict[str, Any]:
    """
    Analyze the connected nodes and generate summary statistics.

    Args:
        df: DataFrame of connected nodes
        all_taxon_ids: All NCBITaxon IDs from table (to calculate coverage)

    Returns:
        Dictionary with analysis results
    """
    # Get unique taxa with data
    taxa_in_results = set(df['subject'].tolist() + df['object'].tolist())
    taxa_with_functional_data = [t for t in taxa_in_results if t in all_taxon_ids]

    stats = {
        "total_edges": len(df),
        "unique_nodes": df['connected_node_id'].nunique(),
        "total_taxa_in_table": len(all_taxon_ids),
        "taxa_with_data": len(taxa_with_functional_data),
        "by_direction": df.groupby('direction').size().to_dict(),
        "by_predicate": df.groupby('predicate').size().sort_values(ascending=False).to_dict(),
        "by_category": df.groupby('connected_node_category').size().sort_values(ascending=False).to_dict(),
        "by_relation": df.groupby('relation').size().sort_values(ascending=False).to_dict(),
    }

    # Count taxa per predicate (for prevalence calculations)
    stats['taxa_per_predicate'] = {}
    for pred in df['predicate'].unique():
        pred_df = df[df['predicate'] == pred]
        unique_taxa = set(pred_df['subject'].tolist() + pred_df['object'].tolist())
        taxa_count = len([t for t in unique_taxa if t in all_taxon_ids])
        stats['taxa_per_predicate'][pred] = {
            'taxa_count': taxa_count,
            'prevalence': taxa_count / len(taxa_with_functional_data) if taxa_with_functional_data else 0
        }

    # Count taxa per category
    stats['taxa_per_category'] = {}
    for cat in df['connected_node_category'].unique():
        cat_df = df[df['connected_node_category'] == cat]
        unique_taxa = set(cat_df['subject'].tolist() + cat_df['object'].tolist())
        taxa_count = len([t for t in unique_taxa if t in all_taxon_ids])
        stats['taxa_per_category'][cat] = {
            'taxa_count': taxa_count,
            'prevalence': taxa_count / len(taxa_with_functional_data) if taxa_with_functional_data else 0
        }

    return stats


def print_summary(stats: Dict[str, Any]):
    """Print a summary of the analysis."""
    print("=" * 80)
    print("KNOWLEDGE GRAPH ANALYSIS: NCBITaxon Connections")
    print("=" * 80)
    print()
    print(f"Total taxa in genomes table: {stats['total_taxa_in_table']}")
    print(f"Taxa with functional data in KG: {stats['taxa_with_data']} ({stats['taxa_with_data']/stats['total_taxa_in_table']*100:.1f}%)")
    print(f"Found {stats['total_edges']:,} edges to {stats['unique_nodes']:,} unique nodes")
    print()
    print(f"*Note: Prevalence percentages are calculated based on {stats['taxa_with_data']} taxa with data*")
    print()

    print("By Direction:")
    for direction, count in stats['by_direction'].items():
        print(f"  {direction}: {count:,}")
    print()

    print("Top 15 Predicates (Relationship Types):")
    for i, (pred, count) in enumerate(list(stats['by_predicate'].items())[:15], 1):
        pred_stats = stats['taxa_per_predicate'].get(pred, {})
        taxa_count = pred_stats.get('taxa_count', 0)
        prevalence = pred_stats.get('prevalence', 0)
        print(f"  {i:2}. {pred}: {count:,} edges ({taxa_count} taxa, {prevalence*100:.0f}%)")
    print()

    print("Top 15 Connected Node Categories:")
    for i, (cat, count) in enumerate(list(stats['by_category'].items())[:15], 1):
        cat_stats = stats['taxa_per_category'].get(cat, {})
        taxa_count = cat_stats.get('taxa_count', 0)
        prevalence = cat_stats.get('prevalence', 0)
        print(f"  {i:2}. {cat}: {count:,} nodes ({taxa_count} taxa, {prevalence*100:.0f}%)")
    print()

    print("Top 10 Relation Types:")
    for i, (rel, count) in enumerate(list(stats['by_relation'].items())[:10], 1):
        if pd.notna(rel) and rel:
            print(f"  {i:2}. {rel}: {count:,}")


def main():
    """Run the analysis."""
    import argparse

    parser = argparse.ArgumentParser(
        description="Analyze knowledge graph connections to genome NCBITaxon IDs"
    )
    parser.add_argument(
        "--genomes-file",
        default="data/txt/sheet/BER_CMM_Data_for_AI_taxa_and_genomes_extended.tsv",
        help="Path to genomes TSV file"
    )
    parser.add_argument(
        "--output",
        default="data/kgm/genome_taxa_connections.tsv",
        help="Output file for full results"
    )
    parser.add_argument(
        "--limit",
        type=int,
        help="Limit number of NCBITaxon IDs to analyze (for testing)"
    )

    args = parser.parse_args()

    # Read NCBITaxon IDs from genomes table
    print(f"Reading NCBITaxon IDs from {args.genomes_file}...")
    taxon_ids = read_genome_taxa(args.genomes_file)

    if args.limit:
        taxon_ids = taxon_ids[:args.limit]

    print(f"Found {len(taxon_ids)} NCBITaxon IDs")
    print()

    # Connect to knowledge graph
    with KnowledgeGraphDB() as kg:
        print("Querying knowledge graph for connected nodes...")
        print("(Excluding subclass_of edges to other NCBITaxon nodes)")
        print()

        # Get connected nodes
        results = get_connected_nodes(kg, taxon_ids)

        # Analyze results
        stats = analyze_connected_nodes(results, taxon_ids)

        # Print summary
        print_summary(stats)

        # Save full results
        output_path = Path(args.output)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        results.to_csv(output_path, sep='\t', index=False)

        print()
        print("=" * 80)
        print(f"✓ Full results saved to: {output_path}")
        print(f"  {len(results):,} edges to {results['connected_node_id'].nunique():,} unique nodes")


if __name__ == "__main__":
    main()
