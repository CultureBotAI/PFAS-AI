"""
Comparative Functional Genomics Analysis

Find functions unique to lanthanide-metabolizing organisms (Methylobacterium,
Methylorubrum, Paracoccus, Methylosinus) compared to other bacteria.
"""

import pandas as pd
from pathlib import Path
from typing import List, Dict, Set, Tuple
from .kg_function_database import FunctionKnowledgeGraphDB


TARGET_GENERA = [
    "Methylobacterium",
    "Methylorubrum",
    "Paracoccus",
    "Methylosinus"
]


def read_genome_taxa(tsv_file: str = "data/txt/sheet/BER_CMM_Data_for_AI_taxa_and_genomes_extended.tsv") -> pd.DataFrame:
    """
    Read genome taxa from extended table.

    Returns:
        DataFrame with columns: scientific_name, ncbi_taxon_id, taxon_id_formatted
    """
    df = pd.read_csv(tsv_file, sep='\t')

    # Extract scientific name and NCBITaxon ID
    taxa_data = []
    for _, row in df.iterrows():
        sci_name = row.iloc[0]  # Scientific name
        taxon_id_raw = row.iloc[1]  # NCBITaxon id

        if pd.notna(taxon_id_raw) and str(taxon_id_raw).strip():
            taxon_id_int = int(float(taxon_id_raw))
            taxon_id = f"NCBITaxon:{taxon_id_int}"

            taxa_data.append({
                'scientific_name': sci_name,
                'ncbi_taxon_id': taxon_id_int,
                'taxon_id': taxon_id
            })

    return pd.DataFrame(taxa_data)


def filter_target_taxa(taxa_df: pd.DataFrame, target_genera: List[str] = TARGET_GENERA) -> pd.DataFrame:
    """
    Filter to target genera only.

    Args:
        taxa_df: DataFrame from read_genome_taxa()
        target_genera: List of genus names to include

    Returns:
        Filtered DataFrame
    """
    # Check if scientific name starts with any target genus
    mask = taxa_df['scientific_name'].apply(
        lambda name: any(name.startswith(genus) for genus in target_genera)
    )

    filtered = taxa_df[mask].copy()
    filtered['genus'] = filtered['scientific_name'].apply(
        lambda name: name.split()[0] if pd.notna(name) else None
    )

    return filtered


def get_all_bacterial_taxa(kg: FunctionKnowledgeGraphDB) -> List[str]:
    """
    Get all bacterial NCBITaxon IDs from the knowledge graph.

    Args:
        kg: FunctionKnowledgeGraphDB instance

    Returns:
        List of NCBITaxon IDs
    """
    # Query for all NCBITaxon nodes that have proteins (UniProtKB derives_from NCBITaxon)
    # These taxa have functional annotations via their proteins
    result = kg.query("""
        SELECT DISTINCT object as taxon_id
        FROM edges
        WHERE object LIKE 'NCBITaxon:%'
          AND predicate = 'biolink:derives_from'
    """)

    return result['taxon_id'].tolist()


def analyze_comparative_functions(
    kg: FunctionKnowledgeGraphDB,
    target_taxa: List[str],
    min_target_prevalence: float = 0.5,
    max_nontarget_prevalence: float = 0.05
) -> Dict[str, pd.DataFrame]:
    """
    Perform comparative functional analysis.

    Args:
        kg: FunctionKnowledgeGraphDB instance
        target_taxa: List of target NCBITaxon IDs (all genomes from table)
        min_target_prevalence: Minimum fraction of target taxa (0.5 = 50%)
        max_nontarget_prevalence: Maximum fraction of non-target taxa (0.05 = 5%)

    Returns:
        Dictionary with DataFrames for enzymes, go_processes, pathways
    """
    print(f"Total target taxa from table: {len(target_taxa)}")

    # Get all bacterial taxa with proteins in KG
    print("Identifying all bacterial taxa in knowledge graph...")
    all_taxa = get_all_bacterial_taxa(kg)
    print(f"Found {len(all_taxa)} total bacterial taxa with proteins")

    # Filter target taxa to only those present in KG
    target_set = set(target_taxa)
    target_taxa_in_kg = [t for t in all_taxa if t in target_set]
    print(f"Target taxa with proteins in KG: {len(target_taxa_in_kg)}/{len(target_taxa)}")

    if len(target_taxa_in_kg) == 0:
        print("ERROR: No target taxa found in knowledge graph!")
        return {
            'enzymes': pd.DataFrame(),
            'go_processes': pd.DataFrame(),
            'pathways': pd.DataFrame(),
            'chemicals': pd.DataFrame(),
            'reactions': pd.DataFrame(),
            'all': pd.DataFrame()
        }

    # Non-target taxa = all taxa in KG - target taxa in KG
    nontarget_taxa = [t for t in all_taxa if t not in target_set]
    print(f"Non-target taxa: {len(nontarget_taxa)}")

    # Compare functions (using only taxa present in KG)
    print(f"\nComparing functions:")
    print(f"  Target taxa analyzed: {len(target_taxa_in_kg)} (with protein data)")
    print(f"  Target prevalence: ≥{min_target_prevalence*100}% (≥{int(min_target_prevalence * len(target_taxa_in_kg))} taxa)")
    print(f"  Non-target prevalence: ≤{max_nontarget_prevalence*100}% (≤{int(max_nontarget_prevalence * len(nontarget_taxa))} taxa)")
    print()

    print("Running comparative analysis...")
    all_unique_functions = kg.compare_functions(
        target_taxa=target_taxa_in_kg,  # Use only taxa present in KG
        reference_taxa=nontarget_taxa,
        min_target_prevalence=min_target_prevalence,
        max_reference_prevalence=max_nontarget_prevalence
    )

    # Split by function type
    results = {
        'enzymes': all_unique_functions[all_unique_functions['function_type'] == 'Enzyme'].copy(),
        'go_processes': all_unique_functions[all_unique_functions['function_type'] == 'GO_Process'].copy(),
        'pathways': all_unique_functions[all_unique_functions['function_type'] == 'Pathway'].copy(),
        'chemicals': all_unique_functions[all_unique_functions['function_type'] == 'Chemical'].copy(),
        'reactions': all_unique_functions[all_unique_functions['function_type'] == 'Reaction'].copy(),
        'all': all_unique_functions
    }

    # Add metadata
    for df_key, df in results.items():
        if len(df) > 0:
            df['total_target_taxa'] = len(target_taxa_in_kg)  # Taxa with data in KG
            df['total_nontarget_taxa'] = len(nontarget_taxa)
            df['total_target_taxa_in_table'] = len(target_taxa)  # All taxa from table

    return results


def generate_summary_stats(
    target_taxa_df: pd.DataFrame,
    results: Dict[str, pd.DataFrame]
) -> Dict[str, any]:
    """Generate summary statistics."""

    stats = {
        'target_organisms': {
            'total': len(target_taxa_df),
            'by_genus': target_taxa_df.groupby('genus').size().to_dict()
        },
        'unique_functions': {
            'enzymes': len(results['enzymes']),
            'go_processes': len(results['go_processes']),
            'pathways': len(results['pathways']),
            'chemicals': len(results['chemicals']),
            'reactions': len(results['reactions']),
            'total': len(results['all'])
        }
    }

    # Top functions by prevalence
    for func_type in ['enzymes', 'go_processes', 'pathways', 'chemicals', 'reactions']:
        df = results[func_type]
        if len(df) > 0:
            stats[f'top_{func_type}'] = df.nlargest(10, 'target_prevalence')[
                ['function_id', 'function_name', 'target_prevalence', 'enrichment_ratio']
            ].to_dict('records')

    return stats


def format_report(
    target_taxa_df: pd.DataFrame,
    results: Dict[str, pd.DataFrame],
    stats: Dict
) -> str:
    """Generate markdown report."""

    report = []

    # Get actual counts from results metadata
    if len(results['all']) > 0:
        total_target_in_kg = results['all']['total_target_taxa'].iloc[0]
        total_target_in_table = results['all']['total_target_taxa_in_table'].iloc[0]
    else:
        total_target_in_kg = 0
        total_target_in_table = stats['target_organisms']['total']

    # Header
    report.append("# Comparative Functional Genomics Analysis")
    report.append("")
    report.append("## Executive Summary")
    report.append("")
    report.append(f"**Analysis Date**: {pd.Timestamp.now().strftime('%Y-%m-%d')}")
    report.append(f"**Genomes in Table**: {total_target_in_table} taxa from lanthanide-metabolizing genera")
    report.append(f"**Taxa with Protein Data**: {total_target_in_kg} taxa analyzed ({total_target_in_kg/total_target_in_table*100:.1f}% coverage)")
    report.append(f"**Unique Functions Identified**: {stats['unique_functions']['total']}")
    report.append("")
    report.append("### Key Findings")
    report.append("")
    report.append(f"- **{stats['unique_functions']['enzymes']} unique enzymes** (EC numbers)")
    report.append(f"- **{stats['unique_functions']['go_processes']} unique biological processes** (GO terms)")
    report.append(f"- **{stats['unique_functions']['pathways']} unique pathways** (KEGG/MetaCyc)")
    report.append(f"- **{stats['unique_functions']['chemicals']} unique chemicals** (CHEBI)")
    report.append(f"- **{stats['unique_functions']['reactions']} unique reactions** (RHEA)")
    report.append("")

    # Methods
    report.append("## Methods")
    report.append("")
    report.append("### Target Organisms")
    report.append("")
    report.append(f"**Genomes in table**: {total_target_in_table} bacterial taxa from four genera:")
    report.append("")
    for genus, count in stats['target_organisms']['by_genus'].items():
        report.append(f"- **{genus}**: {count} taxa")
    report.append("")
    report.append(f"**Taxa with protein data in function KG**: {total_target_in_kg} ({total_target_in_kg/total_target_in_table*100:.1f}% coverage)")
    report.append("")
    report.append(f"*Note: Prevalence calculations are based on the {total_target_in_kg} taxa with protein annotations, not the full set of {total_target_in_table} genomes.*")
    report.append("")

    report.append("### Analysis Criteria")
    report.append("")
    report.append("Functions were identified as unique to target organisms if:")
    report.append(f"1. Present in ≥50% of target taxa **with protein data** (≥{int(0.5 * total_target_in_kg)} of {total_target_in_kg} taxa)")
    report.append("2. Present in ≤5% of non-target bacterial taxa")
    report.append("3. Function type: Enzyme (EC), GO Biological Process, Pathway (KEGG/MetaCyc), Chemical (CHEBI), or Reaction (RHEA)")
    report.append("")

    # Results - Enzymes
    report.append("## Results")
    report.append("")
    report.append("### Unique Enzymes (EC Numbers)")
    report.append("")
    report.append(f"**{len(results['enzymes'])} enzymes** uniquely associated with target organisms.")
    report.append("")

    if len(results['enzymes']) > 0:
        report.append("#### Top 10 Unique Enzymes")
        report.append("")
        report.append("| EC Number | Enzyme Name | Target Prevalence | Enrichment |")
        report.append("|-----------|-------------|-------------------|------------|")

        for _, row in results['enzymes'].head(10).iterrows():
            ec = row['function_id']
            name = row['function_name'] if pd.notna(row['function_name']) else "Unknown"
            prev = f"{row['target_prevalence']*100:.1f}%"
            enrich = f"{row['enrichment_ratio']:.1f}x"
            report.append(f"| {ec} | {name} | {prev} | {enrich} |")

        report.append("")

    # Results - GO Processes
    report.append("### Unique Biological Processes (GO Terms)")
    report.append("")
    report.append(f"**{len(results['go_processes'])} GO biological processes** uniquely associated with target organisms.")
    report.append("")

    if len(results['go_processes']) > 0:
        report.append("#### Top 10 Unique Biological Processes")
        report.append("")
        report.append("| GO Term | Process Name | Target Prevalence | Enrichment |")
        report.append("|---------|--------------|-------------------|------------|")

        for _, row in results['go_processes'].head(10).iterrows():
            go_id = row['function_id']
            name = row['function_name'] if pd.notna(row['function_name']) else "Unknown"
            # Truncate long names
            if len(name) > 60:
                name = name[:57] + "..."
            prev = f"{row['target_prevalence']*100:.1f}%"
            enrich = f"{row['enrichment_ratio']:.1f}x"
            report.append(f"| {go_id} | {name} | {prev} | {enrich} |")

        report.append("")

    # Results - Pathways
    report.append("### Unique Pathways (KEGG/MetaCyc)")
    report.append("")
    report.append(f"**{len(results['pathways'])} pathways** uniquely associated with target organisms.")
    report.append("")

    if len(results['pathways']) > 0:
        report.append("#### Top 10 Unique Pathways")
        report.append("")
        report.append("| Pathway ID | Pathway Name | Target Prevalence | Enrichment |")
        report.append("|------------|--------------|-------------------|------------|")

        for _, row in results['pathways'].head(10).iterrows():
            path_id = row['function_id']
            name = row['function_name'] if pd.notna(row['function_name']) else "Unknown"
            if len(name) > 60:
                name = name[:57] + "..."
            prev = f"{row['target_prevalence']*100:.1f}%"
            enrich = f"{row['enrichment_ratio']:.1f}x"
            report.append(f"| {path_id} | {name} | {prev} | {enrich} |")

        report.append("")

    # Results - Chemicals
    report.append("### Unique Chemicals (CHEBI)")
    report.append("")
    report.append(f"**{len(results['chemicals'])} chemicals** uniquely associated with target organisms.")
    report.append("")

    if len(results['chemicals']) > 0:
        report.append("#### Top 10 Unique Chemicals")
        report.append("")
        report.append("| CHEBI ID | Chemical Name | Target Prevalence | Enrichment |")
        report.append("|----------|---------------|-------------------|------------|")

        for _, row in results['chemicals'].head(10).iterrows():
            chem_id = row['function_id']
            name = row['function_name'] if pd.notna(row['function_name']) else "Unknown"
            if len(name) > 60:
                name = name[:57] + "..."
            prev = f"{row['target_prevalence']*100:.1f}%"
            enrich = f"{row['enrichment_ratio']:.1f}x"
            report.append(f"| {chem_id} | {name} | {prev} | {enrich} |")

        report.append("")

    # Results - Reactions
    report.append("### Unique Reactions (RHEA)")
    report.append("")
    report.append(f"**{len(results['reactions'])} reactions** uniquely associated with target organisms.")
    report.append("")

    if len(results['reactions']) > 0:
        report.append("#### Top 10 Unique Reactions")
        report.append("")
        report.append("| RHEA ID | Reaction Name | Target Prevalence | Enrichment |")
        report.append("|---------|---------------|-------------------|------------|")

        for _, row in results['reactions'].head(10).iterrows():
            rhea_id = row['function_id']
            name = row['function_name'] if pd.notna(row['function_name']) else "Unknown"
            if len(name) > 60:
                name = name[:57] + "..."
            prev = f"{row['target_prevalence']*100:.1f}%"
            enrich = f"{row['enrichment_ratio']:.1f}x"
            report.append(f"| {rhea_id} | {name} | {prev} | {enrich} |")

        report.append("")

    # Biological Interpretation
    report.append("## Biological Interpretation")
    report.append("")
    report.append("### Functional Specialization")
    report.append("")
    report.append("These unique functions reflect the specialized metabolism of methylotrophic")
    report.append("and lanthanide-utilizing organisms:")
    report.append("")
    report.append("1. **Methylotrophy**: C1 compound metabolism (methanol, methylamine)")
    report.append("2. **Phototrophy**: Aerobic anoxygenic photosynthesis capabilities")
    report.append("3. **Denitrification**: Alternative respiratory pathways")
    report.append("4. **Environmental Adaptation**: Specialized stress responses")
    report.append("")

    # Data Files
    report.append("## Data Files")
    report.append("")
    report.append("Full results available in TSV format:")
    report.append("- `function_comparative_analysis.tsv` - All unique functions")
    report.append("- `unique_enzymes.tsv` - Enzyme-specific results")
    report.append("- `unique_pathways.tsv` - Pathway-specific results")
    report.append("- `unique_go_processes.tsv` - GO process-specific results")
    report.append("- `unique_chemicals.tsv` - CHEBI chemical-specific results")
    report.append("- `unique_reactions.tsv` - RHEA reaction-specific results")
    report.append("")

    # Reproducibility
    report.append("## Reproducibility")
    report.append("")
    report.append("```bash")
    report.append("# Run analysis")
    report.append("uv run python -m src.duckdb.comparative_functions")
    report.append("```")
    report.append("")

    return "\n".join(report)


def main():
    """Run the comparative functional analysis."""
    import argparse

    parser = argparse.ArgumentParser(
        description="Comparative functional genomics analysis"
    )
    parser.add_argument(
        "--genomes-file",
        default="data/txt/sheet/BER_CMM_Data_for_AI_taxa_and_genomes_extended.tsv",
        help="Path to genomes TSV file"
    )
    parser.add_argument(
        "--min-target-prevalence",
        type=float,
        default=0.5,
        help="Minimum prevalence in target taxa (default: 0.5 = 50%%)"
    )
    parser.add_argument(
        "--max-nontarget-prevalence",
        type=float,
        default=0.05,
        help="Maximum prevalence in non-target taxa (default: 0.05 = 5%%)"
    )
    parser.add_argument(
        "--output-dir",
        default="data/kgm",
        help="Output directory for results"
    )

    args = parser.parse_args()

    print("=" * 80)
    print("COMPARATIVE FUNCTIONAL GENOMICS ANALYSIS")
    print("=" * 80)
    print()

    # Read genome taxa
    print(f"Reading genome taxa from {args.genomes_file}...")
    all_taxa_df = read_genome_taxa(args.genomes_file)
    print(f"Found {len(all_taxa_df)} total taxa")

    # Filter to target genera
    print(f"\nFiltering to target genera: {', '.join(TARGET_GENERA)}...")
    target_taxa_df = filter_target_taxa(all_taxa_df)
    print(f"Target taxa: {len(target_taxa_df)}")
    print("\nBreakdown by genus:")
    for genus, count in target_taxa_df.groupby('genus').size().items():
        print(f"  {genus}: {count}")
    print()

    # Connect to function KG
    with FunctionKnowledgeGraphDB() as kg:
        # Run analysis
        results = analyze_comparative_functions(
            kg=kg,
            target_taxa=target_taxa_df['taxon_id'].tolist(),
            min_target_prevalence=args.min_target_prevalence,
            max_nontarget_prevalence=args.max_nontarget_prevalence
        )

        # Generate statistics
        stats = generate_summary_stats(target_taxa_df, results)

        # Print summary
        print("\n" + "=" * 80)
        print("RESULTS SUMMARY")
        print("=" * 80)
        print()
        print(f"Total unique functions: {stats['unique_functions']['total']}")
        print(f"  - Enzymes (EC): {stats['unique_functions']['enzymes']}")
        print(f"  - GO Processes: {stats['unique_functions']['go_processes']}")
        print(f"  - Pathways: {stats['unique_functions']['pathways']}")
        print(f"  - Chemicals (CHEBI): {stats['unique_functions']['chemicals']}")
        print(f"  - Reactions (RHEA): {stats['unique_functions']['reactions']}")
        print()

        # Save results
        output_dir = Path(args.output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)

        # Save TSV files
        results['all'].to_csv(
            output_dir / "function_comparative_analysis.tsv",
            sep='\t',
            index=False
        )
        results['enzymes'].to_csv(
            output_dir / "unique_enzymes.tsv",
            sep='\t',
            index=False
        )
        results['go_processes'].to_csv(
            output_dir / "unique_go_processes.tsv",
            sep='\t',
            index=False
        )
        results['pathways'].to_csv(
            output_dir / "unique_pathways.tsv",
            sep='\t',
            index=False
        )
        results['chemicals'].to_csv(
            output_dir / "unique_chemicals.tsv",
            sep='\t',
            index=False
        )
        results['reactions'].to_csv(
            output_dir / "unique_reactions.tsv",
            sep='\t',
            index=False
        )

        # Generate and save report
        report = format_report(target_taxa_df, results, stats)
        report_path = output_dir / "COMPARATIVE_FUNCTIONS_REPORT.md"
        with open(report_path, 'w') as f:
            f.write(report)

        print("=" * 80)
        print("✓ Analysis complete!")
        print("=" * 80)
        print()
        print("Output files:")
        print(f"  - {output_dir / 'COMPARATIVE_FUNCTIONS_REPORT.md'}")
        print(f"  - {output_dir / 'function_comparative_analysis.tsv'}")
        print(f"  - {output_dir / 'unique_enzymes.tsv'}")
        print(f"  - {output_dir / 'unique_go_processes.tsv'}")
        print(f"  - {output_dir / 'unique_pathways.tsv'}")
        print(f"  - {output_dir / 'unique_chemicals.tsv'}")
        print(f"  - {output_dir / 'unique_reactions.tsv'}")
        print()


if __name__ == "__main__":
    main()
