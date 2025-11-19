"""
Find critical mineral chemicals (especially PFASs) connected to genome taxa.

This script finds paths of 1, 2, or 3 edge hops from genome taxa to critical
mineral chemicals, with a focus on PFASs (rare earth elements).
"""

import pandas as pd
from pathlib import Path
from typing import List, Dict, Set, Tuple
from .kg_database import KnowledgeGraphDB


# Critical minerals and PFASs to search for
LANTHANIDES = [
    "lanthanum", "cerium", "praseodymium", "neodymium", "promethium",
    "samarium", "europium", "gadolinium", "terbium", "dysprosium",
    "holmium", "erbium", "thulium", "ytterbium", "lutetium",
    "scandium", "yttrium"  # Often grouped with PFASs
]

CRITICAL_MINERALS = [
    "rare earth", "REE", "PFAS",
    "cobalt", "lithium", "nickel", "manganese",
    "copper", "zinc", "iron", "molybdenum",
    "tungsten", "chromium", "vanadium"
]


def read_genome_taxa(tsv_file: str = "data/txt/sheet/BER_CMM_Data_for_AI_taxa_and_genomes_extended.tsv") -> List[str]:
    """Read NCBITaxon IDs from genomes table."""
    df = pd.read_csv(tsv_file, sep='\t')
    taxon_ids = df.iloc[:, 1].dropna()

    ncbi_taxon_ids = []
    for taxon_id in taxon_ids:
        if pd.notna(taxon_id) and str(taxon_id).strip():
            taxon_id_int = int(float(taxon_id))
            ncbi_taxon_ids.append(f"NCBITaxon:{taxon_id_int}")

    return ncbi_taxon_ids


def find_critical_mineral_nodes(kg: KnowledgeGraphDB) -> pd.DataFrame:
    """Find all chemical nodes related to critical minerals and PFASs."""

    # Search for PFASs and critical minerals
    search_terms = LANTHANIDES + CRITICAL_MINERALS

    all_chemicals = []

    for term in search_terms:
        # Search in name and description
        chemicals = kg.query(f"""
            SELECT DISTINCT id, name, category, description
            FROM nodes
            WHERE (category LIKE '%Chemical%' OR id LIKE 'CHEBI:%')
              AND (
                LOWER(name) LIKE '%{term.lower()}%'
                OR LOWER(description) LIKE '%{term.lower()}%'
                OR LOWER(synonym) LIKE '%{term.lower()}%'
              )
        """)

        if len(chemicals) > 0:
            chemicals['search_term'] = term
            all_chemicals.append(chemicals)

    if all_chemicals:
        result = pd.concat(all_chemicals, ignore_index=True)
        # Remove duplicates
        result = result.drop_duplicates(subset=['id'])
        return result
    else:
        return pd.DataFrame()


def find_paths_to_chemicals(
    kg: KnowledgeGraphDB,
    taxon_ids: List[str],
    chemical_ids: List[str],
    max_depth: int = 3
) -> pd.DataFrame:
    """
    Find paths from taxa to critical mineral chemicals.

    Args:
        kg: KnowledgeGraphDB instance
        taxon_ids: List of NCBITaxon IDs
        chemical_ids: List of chemical IDs to find paths to
        max_depth: Maximum path length (1, 2, or 3 hops)

    Returns:
        DataFrame with paths found
    """

    # Create comma-separated lists for SQL IN clauses
    taxa_list = ", ".join([f"'{tid}'" for tid in taxon_ids])
    chem_list = ", ".join([f"'{cid}'" for cid in chemical_ids])

    # Recursive CTE to find paths up to max_depth
    sql = f"""
    WITH RECURSIVE paths AS (
        -- Base case: direct edges (1 hop)
        SELECT
            e.subject as start_taxon,
            e.subject as current_node,
            e.object as next_node,
            e.predicate,
            1 as depth,
            CAST(e.subject || ' -[' || e.predicate || ']-> ' || e.object AS VARCHAR) as path,
            CAST(e.predicate AS VARCHAR) as predicate_path
        FROM edges e
        WHERE e.subject IN ({taxa_list})

        UNION ALL

        -- Recursive case: extend paths
        SELECT
            p.start_taxon,
            p.next_node as current_node,
            e.object as next_node,
            e.predicate,
            p.depth + 1,
            CAST(p.path || ' -[' || e.predicate || ']-> ' || e.object AS VARCHAR),
            CAST(p.predicate_path || ' | ' || e.predicate AS VARCHAR)
        FROM paths p
        JOIN edges e ON p.next_node = e.subject
        WHERE p.depth < {max_depth}
          AND p.path NOT LIKE '%' || e.object || '%'  -- Avoid cycles
    )
    SELECT DISTINCT
        p.start_taxon,
        p.next_node as end_chemical,
        p.depth,
        p.path,
        p.predicate_path,
        n1.name as taxon_name,
        n2.name as chemical_name,
        n2.description as chemical_description
    FROM paths p
    JOIN nodes n1 ON p.start_taxon = n1.id
    JOIN nodes n2 ON p.next_node = n2.id
    WHERE p.next_node IN ({chem_list})
    ORDER BY p.depth, p.start_taxon, p.next_node
    """

    return kg.query(sql)


def categorize_chemicals(chemicals_df: pd.DataFrame) -> Dict[str, List[str]]:
    """Categorize chemicals into PFASs and other critical minerals."""

    categories = {
        'PFASs': [],
        'rare_earth': [],
        'transition_metals': [],
        'other_critical': []
    }

    for _, chem in chemicals_df.iterrows():
        name_lower = str(chem['name']).lower()
        desc_lower = str(chem.get('description', '')).lower()

        # Check for PFASs
        is_PFAS = any(ln in name_lower or ln in desc_lower for ln in LANTHANIDES)
        is_ree = 'rare earth' in name_lower or 'rare earth' in desc_lower

        if is_PFAS:
            categories['PFASs'].append(chem['id'])
        elif is_ree:
            categories['rare_earth'].append(chem['id'])
        elif any(metal in name_lower for metal in ['cobalt', 'lithium', 'nickel', 'manganese']):
            categories['transition_metals'].append(chem['id'])
        else:
            categories['other_critical'].append(chem['id'])

    return categories


def main():
    """Run the critical minerals analysis."""
    import argparse

    parser = argparse.ArgumentParser(
        description="Find critical mineral chemicals connected to genome taxa"
    )
    parser.add_argument(
        "--genomes-file",
        default="data/txt/sheet/BER_CMM_Data_for_AI_taxa_and_genomes_extended.tsv",
        help="Path to genomes TSV file"
    )
    parser.add_argument(
        "--max-hops",
        type=int,
        default=3,
        choices=[1, 2, 3],
        help="Maximum number of edge hops to search (1, 2, or 3)"
    )
    parser.add_argument(
        "--output",
        default="data/kgm/critical_minerals_paths.tsv",
        help="Output file for results"
    )

    args = parser.parse_args()

    print("=" * 80)
    print("CRITICAL MINERALS ANALYSIS: Paths from Genome Taxa")
    print("=" * 80)
    print()

    # Read genome taxa
    print(f"Reading genome taxa from {args.genomes_file}...")
    taxon_ids = read_genome_taxa(args.genomes_file)
    print(f"Found {len(taxon_ids)} taxa")
    print()

    with KnowledgeGraphDB() as kg:
        # Find critical mineral chemicals in KG
        print("Searching for critical mineral chemicals in knowledge graph...")
        print(f"Search terms: {', '.join(LANTHANIDES[:5])}... (and {len(LANTHANIDES) + len(CRITICAL_MINERALS) - 5} more)")
        print()

        chemicals = find_critical_mineral_nodes(kg)

        if len(chemicals) == 0:
            print("❌ No critical mineral chemicals found in knowledge graph!")
            return

        print(f"✓ Found {len(chemicals)} critical mineral chemical nodes")
        print()

        # Categorize chemicals
        categories = categorize_chemicals(chemicals)

        print("Chemical categories:")
        print(f"  - PFASs: {len(categories['PFASs'])}")
        print(f"  - Rare earth elements: {len(categories['rare_earth'])}")
        print(f"  - Transition metals: {len(categories['transition_metals'])}")
        print(f"  - Other critical minerals: {len(categories['other_critical'])}")
        print()

        # Show some examples
        print("Example PFAS chemicals found:")
        PFAS_chems = chemicals[chemicals['id'].isin(categories['PFASs'])].head(10)
        for _, chem in PFAS_chems.iterrows():
            print(f"  {chem['id']}: {chem['name']}")
        print()

        # Find paths from taxa to chemicals
        print(f"Finding paths (up to {args.max_hops} hops) from {len(taxon_ids)} taxa to {len(chemicals)} chemicals...")
        print()

        all_chemical_ids = chemicals['id'].tolist()
        paths = find_paths_to_chemicals(kg, taxon_ids, all_chemical_ids, args.max_hops)

        if len(paths) == 0:
            print(f"❌ No paths found within {args.max_hops} hops!")
            return

        print(f"✓ Found {len(paths)} paths")
        print()

        # Analyze results by hop distance
        print("Paths by hop distance:")
        for depth in range(1, args.max_hops + 1):
            depth_paths = paths[paths['depth'] == depth]
            unique_taxa = depth_paths['start_taxon'].nunique()
            unique_chems = depth_paths['end_chemical'].nunique()
            print(f"  {depth} hop(s): {len(depth_paths)} paths ({unique_taxa} taxa → {unique_chems} chemicals)")
        print()

        # Show paths to PFASs specifically
        PFAS_paths = paths[paths['end_chemical'].isin(categories['PFASs'])]
        if len(PFAS_paths) > 0:
            print(f"🎯 LANTHANIDE CONNECTIONS: {len(PFAS_paths)} paths found!")
            print()
            print("Example paths to PFASs:")
            for _, path in PFAS_paths.head(10).iterrows():
                print(f"\n  {path['taxon_name']} ({path['depth']} hops)")
                print(f"    → {path['chemical_name']}")
                print(f"    Path: {path['predicate_path']}")
        else:
            print("⚠️  No direct paths to PFAS chemicals found")
        print()

        # Show paths to rare earth elements
        ree_paths = paths[paths['end_chemical'].isin(categories['rare_earth'])]
        if len(ree_paths) > 0:
            print(f"🌍 RARE EARTH ELEMENT CONNECTIONS: {len(ree_paths)} paths found!")
            print()
            print("Example paths to REEs:")
            for _, path in ree_paths.head(5).iterrows():
                print(f"\n  {path['taxon_name']} ({path['depth']} hops)")
                print(f"    → {path['chemical_name']}")
                print(f"    Path: {path['predicate_path']}")
        print()

        # Save results
        output_path = Path(args.output)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        paths.to_csv(output_path, sep='\t', index=False)

        print("=" * 80)
        print(f"✓ Results saved to: {output_path}")
        print()
        print("Summary:")
        print(f"  - Total paths: {len(paths)}")
        print(f"  - Taxa with connections: {paths['start_taxon'].nunique()}")
        print(f"  - Critical minerals reached: {paths['end_chemical'].nunique()}")
        print(f"  - PFAS paths: {len(PFAS_paths)}")
        print(f"  - REE paths: {len(ree_paths)}")
        print("=" * 80)


if __name__ == "__main__":
    main()
