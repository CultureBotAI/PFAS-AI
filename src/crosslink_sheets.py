#!/usr/bin/env python3
"""
Cross-link information across data sheets.

This script adds cross-reference columns to TSV sheets by linking related data:
- Genes → Genomes (organism name matching)
- Pathways → Genomes (organism matching)
- Pathways → Genes (gene name matching)
- Structures → Genes (protein name matching)
- Biosamples → Genomes (organism matching)
- Chemicals → Referenced in other tables

The script is idempotent and can be run multiple times safely.
"""

import argparse
import pandas as pd
from pathlib import Path
from typing import Dict, List, Set, Tuple
import re


def normalize_organism_name(name: str, level: str = 'exact') -> str:
    """
    Normalize organism name for matching at different taxonomic levels.

    Args:
        name: Organism name
        level: 'exact', 'species' (genus+species), or 'genus'
    """
    if pd.isna(name):
        return ""

    name = str(name).strip().lower()

    # Remove strain designations
    name = re.sub(r'\s+strain[:\s]+.*', '', name, flags=re.IGNORECASE)
    name = re.sub(r'\s+str\.\s+.*', '', name, flags=re.IGNORECASE)

    parts = name.split()

    if level == 'exact':
        return name
    elif level == 'species' and len(parts) >= 2:
        # Genus + species only
        return f"{parts[0]} {parts[1]}"
    elif level == 'genus' and len(parts) >= 1:
        # Genus only
        return parts[0]

    return name


def hierarchical_match_organism(query: str, genomes_df: pd.DataFrame) -> Dict[str, any]:
    """
    Match organism name to genomes table using hierarchical matching.

    Tries in order:
    1. Exact match (including strain)
    2. Species-level match (genus + species)
    3. Genus-level match (as fallback)

    Returns dict with:
        - exact_matches: [(name, taxon_id), ...]
        - closest_match: (name, taxon_id, match_level) or None
    """
    if pd.isna(query) or not str(query).strip():
        return {"exact_matches": [], "closest_match": None}

    query_str = str(query).strip()
    exact_matches = []
    species_matches = []
    genus_matches = []

    # Normalize query at different levels
    query_exact = normalize_organism_name(query_str, 'exact')
    query_species = normalize_organism_name(query_str, 'species')
    query_genus = normalize_organism_name(query_str, 'genus')

    # Search through genomes
    for idx, row in genomes_df.iterrows():
        genome_name = row.get("Scientific name", "")
        taxon_id = row.get("NCBITaxon id")

        if pd.isna(taxon_id):
            continue

        taxon_id_str = str(int(float(taxon_id)))

        # Exact match
        genome_exact = normalize_organism_name(genome_name, 'exact')
        if query_exact == genome_exact:
            exact_matches.append((genome_name, taxon_id_str))
            continue

        # Species-level match
        genome_species = normalize_organism_name(genome_name, 'species')
        if query_species and genome_species and query_species == genome_species:
            species_matches.append((genome_name, taxon_id_str))
            continue

        # Genus-level match
        genome_genus = normalize_organism_name(genome_name, 'genus')
        if query_genus and genome_genus and query_genus == genome_genus:
            genus_matches.append((genome_name, taxon_id_str))

    # Determine closest match
    closest_match = None
    if exact_matches:
        closest_match = (exact_matches[0][0], exact_matches[0][1], 'exact')
    elif species_matches:
        closest_match = (species_matches[0][0], species_matches[0][1], 'species')
    elif genus_matches:
        closest_match = (genus_matches[0][0], genus_matches[0][1], 'genus')

    return {
        "exact_matches": exact_matches,
        "closest_match": closest_match
    }


def crosslink_genes_to_genomes(
    genes_file: str,
    genomes_file: str,
    output_file: str
) -> None:
    """Link genes/proteins to their source genomes with hierarchical matching."""
    print("\n" + "=" * 80)
    print("Cross-linking Genes → Genomes")
    print("=" * 80)

    genes_df = pd.read_csv(genes_file, sep='\t')
    genomes_df = pd.read_csv(genomes_file, sep='\t')

    print(f"Loaded {len(genes_df)} genes and {len(genomes_df)} genomes")

    # Add cross-reference columns if they don't exist
    if 'genome_ncbitaxon_id' not in genes_df.columns:
        genes_df['genome_ncbitaxon_id'] = ""
    if 'genome_scientific_name' not in genes_df.columns:
        genes_df['genome_scientific_name'] = ""
    if 'closest_genome_ncbitaxon_id' not in genes_df.columns:
        genes_df['closest_genome_ncbitaxon_id'] = ""
    if 'closest_genome_name' not in genes_df.columns:
        genes_df['closest_genome_name'] = ""
    if 'genome_match_level' not in genes_df.columns:
        genes_df['genome_match_level'] = ""

    # Match each gene to its genome
    exact_count = 0
    species_count = 0
    genus_count = 0

    for idx, row in genes_df.iterrows():
        organism = row.get("organism (from taxa and genomes tab)")
        if pd.isna(organism):
            continue

        match_result = hierarchical_match_organism(organism, genomes_df)
        exact_matches = match_result["exact_matches"]
        closest_match = match_result["closest_match"]

        # Fill in exact match columns (only for exact matches)
        if exact_matches:
            genome_name, taxon_id = exact_matches[0]
            genes_df.at[idx, 'genome_ncbitaxon_id'] = taxon_id
            genes_df.at[idx, 'genome_scientific_name'] = genome_name
            exact_count += 1

        # Fill in closest match columns (for any match)
        if closest_match:
            genome_name, taxon_id, match_level = closest_match
            genes_df.at[idx, 'closest_genome_ncbitaxon_id'] = taxon_id
            genes_df.at[idx, 'closest_genome_name'] = genome_name
            genes_df.at[idx, 'genome_match_level'] = match_level

            if match_level == 'species':
                species_count += 1
            elif match_level == 'genus':
                genus_count += 1

    # Save
    genes_df.to_csv(output_file, sep='\t', index=False)

    total_linked = exact_count + species_count + genus_count
    print(f"✓ Linked {total_linked}/{len(genes_df)} genes to genomes")
    print(f"  - Exact matches: {exact_count}")
    print(f"  - Species-level: {species_count}")
    print(f"  - Genus-level: {genus_count}")
    print(f"✓ Saved to {output_file}")


def crosslink_pathways_to_genomes(
    pathways_file: str,
    genomes_file: str,
    output_file: str
) -> None:
    """Link pathways to their source genomes with hierarchical matching."""
    print("\n" + "=" * 80)
    print("Cross-linking Pathways → Genomes")
    print("=" * 80)

    pathways_df = pd.read_csv(pathways_file, sep='\t')
    genomes_df = pd.read_csv(genomes_file, sep='\t')

    print(f"Loaded {len(pathways_df)} pathways and {len(genomes_df)} genomes")

    # Add cross-reference columns
    if 'genome_ncbitaxon_ids' not in pathways_df.columns:
        pathways_df['genome_ncbitaxon_ids'] = ""
    if 'closest_genome_ncbitaxon_ids' not in pathways_df.columns:
        pathways_df['closest_genome_ncbitaxon_ids'] = ""
    if 'genome_match_level' not in pathways_df.columns:
        pathways_df['genome_match_level'] = ""

    # Match each pathway to genomes
    exact_count = 0
    species_count = 0
    genus_count = 0

    for idx, row in pathways_df.iterrows():
        organism = row.get("organism")
        if pd.isna(organism):
            continue

        match_result = hierarchical_match_organism(organism, genomes_df)
        exact_matches = match_result["exact_matches"]
        closest_match = match_result["closest_match"]

        # Fill in exact match IDs (all exact matches)
        if exact_matches:
            taxon_ids = [taxon_id for _, taxon_id in exact_matches]
            pathways_df.at[idx, 'genome_ncbitaxon_ids'] = "; ".join(taxon_ids)
            exact_count += 1

        # Fill in closest match info
        if closest_match:
            genome_name, taxon_id, match_level = closest_match
            pathways_df.at[idx, 'closest_genome_ncbitaxon_ids'] = taxon_id
            pathways_df.at[idx, 'genome_match_level'] = match_level

            if match_level == 'species':
                species_count += 1
            elif match_level == 'genus':
                genus_count += 1

    # Save
    pathways_df.to_csv(output_file, sep='\t', index=False)

    total_linked = exact_count + species_count + genus_count
    print(f"✓ Linked {total_linked}/{len(pathways_df)} pathways to genomes")
    print(f"  - Exact matches: {exact_count}")
    print(f"  - Species-level: {species_count}")
    print(f"  - Genus-level: {genus_count}")
    print(f"✓ Saved to {output_file}")


def crosslink_pathways_to_genes(
    pathways_file: str,
    genes_file: str,
    output_file: str
) -> None:
    """Link pathways to specific gene/protein IDs."""
    print("\n" + "=" * 80)
    print("Cross-linking Pathways → Genes")
    print("=" * 80)
    
    pathways_df = pd.read_csv(pathways_file, sep='\t')
    genes_df = pd.read_csv(genes_file, sep='\t')
    
    print(f"Loaded {len(pathways_df)} pathways and {len(genes_df)} genes")
    
    # Build gene ID lookup
    gene_id_map = {}  # gene_name -> gene_id
    for idx, row in genes_df.iterrows():
        gene_id = row.get("gene or protein id")
        annotation = row.get("annotation", "")
        if pd.notna(gene_id):
            gene_id_str = str(gene_id).strip()
            # Map from annotation keywords
            if pd.notna(annotation):
                annotation_lower = str(annotation).lower()
                # Extract key terms
                if "xoxf" in annotation_lower:
                    gene_id_map["xoxf"] = gene_id_str
                if "mxaf" in annotation_lower:
                    gene_id_map["mxaf"] = gene_id_str
                if "exaf" in annotation_lower:
                    gene_id_map["exaf"] = gene_id_str
                if "mxbd" in annotation_lower:
                    gene_id_map["mxbd"] = gene_id_str
                if "fae" in annotation_lower:
                    gene_id_map["fae"] = gene_id_str
    
    # Add cross-reference columns
    if 'gene_protein_ids' not in pathways_df.columns:
        pathways_df['gene_protein_ids'] = ""
    
    # Match pathways to genes
    linked_count = 0
    for idx, row in pathways_df.iterrows():
        genes_col = row.get("genes (from genes and proteins tab)", "")
        if pd.isna(genes_col):
            genes_col = row.get("genes (from genes & proteins tab)", "")
        
        if pd.isna(genes_col):
            continue
        
        genes_str = str(genes_col).lower()
        found_gene_ids = []
        
        # Look for gene names in the genes column
        for gene_name, gene_id in gene_id_map.items():
            if gene_name in genes_str:
                found_gene_ids.append(gene_id)
        
        if found_gene_ids:
            pathways_df.at[idx, 'gene_protein_ids'] = "; ".join(sorted(set(found_gene_ids)))
            linked_count += 1
    
    # Save
    pathways_df.to_csv(output_file, sep='\t', index=False)
    print(f"✓ Linked {linked_count}/{len(pathways_df)} pathways to genes")
    print(f"✓ Saved to {output_file}")


def crosslink_biosamples_to_genomes(
    biosamples_file: str,
    genomes_file: str,
    output_file: str
) -> None:
    """Link biosamples to their source genomes with hierarchical matching."""
    print("\n" + "=" * 80)
    print("Cross-linking Biosamples → Genomes")
    print("=" * 80)

    biosamples_df = pd.read_csv(biosamples_file, sep='\t')
    genomes_df = pd.read_csv(genomes_file, sep='\t')

    print(f"Loaded {len(biosamples_df)} biosamples and {len(genomes_df)} genomes")

    # Add cross-reference columns
    if 'genome_ncbitaxon_id' not in biosamples_df.columns:
        biosamples_df['genome_ncbitaxon_id'] = ""
    if 'genome_scientific_name' not in biosamples_df.columns:
        biosamples_df['genome_scientific_name'] = ""
    if 'closest_genome_ncbitaxon_id' not in biosamples_df.columns:
        biosamples_df['closest_genome_ncbitaxon_id'] = ""
    if 'closest_genome_name' not in biosamples_df.columns:
        biosamples_df['closest_genome_name'] = ""
    if 'genome_match_level' not in biosamples_df.columns:
        biosamples_df['genome_match_level'] = ""

    # Match each biosample to genome
    exact_count = 0
    species_count = 0
    genus_count = 0

    for idx, row in biosamples_df.iterrows():
        organism = row.get("organism")
        if pd.isna(organism):
            organism = row.get("Organism")

        if pd.isna(organism):
            continue

        match_result = hierarchical_match_organism(organism, genomes_df)
        exact_matches = match_result["exact_matches"]
        closest_match = match_result["closest_match"]

        # Fill in exact match columns
        if exact_matches:
            genome_name, taxon_id = exact_matches[0]
            biosamples_df.at[idx, 'genome_ncbitaxon_id'] = taxon_id
            biosamples_df.at[idx, 'genome_scientific_name'] = genome_name
            exact_count += 1

        # Fill in closest match columns
        if closest_match:
            genome_name, taxon_id, match_level = closest_match
            biosamples_df.at[idx, 'closest_genome_ncbitaxon_id'] = taxon_id
            biosamples_df.at[idx, 'closest_genome_name'] = genome_name
            biosamples_df.at[idx, 'genome_match_level'] = match_level

            if match_level == 'species':
                species_count += 1
            elif match_level == 'genus':
                genus_count += 1

    # Save
    biosamples_df.to_csv(output_file, sep='\t', index=False)

    total_linked = exact_count + species_count + genus_count
    print(f"✓ Linked {total_linked}/{len(biosamples_df)} biosamples to genomes")
    print(f"  - Exact matches: {exact_count}")
    print(f"  - Species-level: {species_count}")
    print(f"  - Genus-level: {genus_count}")
    print(f"✓ Saved to {output_file}")


def crosslink_structures_to_genes(
    structures_file: str,
    genes_file: str,
    output_file: str
) -> None:
    """Link structures to gene/protein entries."""
    print("\n" + "=" * 80)
    print("Cross-linking Structures → Genes")
    print("=" * 80)
    
    structures_df = pd.read_csv(structures_file, sep='\t')
    genes_df = pd.read_csv(genes_file, sep='\t')
    
    print(f"Loaded {len(structures_df)} structures and {len(genes_df)} genes")
    
    # Build protein name lookup
    protein_map = {}  # protein_keyword -> gene_id
    for idx, row in genes_df.iterrows():
        gene_id = row.get("gene or protein id")
        annotation = row.get("annotation", "")
        if pd.notna(gene_id) and pd.notna(annotation):
            annotation_lower = str(annotation).lower()
            if "xoxf" in annotation_lower or "methanol dehydrogenase" in annotation_lower:
                protein_map["xoxf"] = str(gene_id)
                protein_map["methanol dehydrogenase"] = str(gene_id)
    
    # Add cross-reference columns
    if 'gene_protein_ids' not in structures_df.columns:
        structures_df['gene_protein_ids'] = ""
    
    # Match structures to genes
    linked_count = 0
    for idx, row in structures_df.iterrows():
        structure_name = row.get("Structure name", "")
        components = row.get("Components", "")
        
        search_text = f"{structure_name} {components}".lower()
        found_gene_ids = []
        
        for keyword, gene_id in protein_map.items():
            if keyword in search_text:
                found_gene_ids.append(gene_id)
        
        if found_gene_ids:
            structures_df.at[idx, 'gene_protein_ids'] = "; ".join(sorted(set(found_gene_ids)))
            linked_count += 1
    
    # Save
    structures_df.to_csv(output_file, sep='\t', index=False)
    print(f"✓ Linked {linked_count}/{len(structures_df)} structures to genes")
    print(f"✓ Saved to {output_file}")


def main():
    """Command-line interface."""
    parser = argparse.ArgumentParser(
        description="Cross-link information across data sheets",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Cross-link all tables
  python src/crosslink_sheets.py --all

  # Cross-link specific relationship
  python src/crosslink_sheets.py --link genes-to-genomes

Cross-linking relationships:
  genes-to-genomes     - Link genes to source genomes
  pathways-to-genomes  - Link pathways to source genomes
  pathways-to-genes    - Link pathways to specific genes
  biosamples-to-genomes - Link biosamples to genomes
  structures-to-genes  - Link structures to genes
"""
    )

    parser.add_argument(
        "--link",
        choices=[
            "genes-to-genomes",
            "pathways-to-genomes",
            "pathways-to-genes",
            "biosamples-to-genomes",
            "structures-to-genes"
        ],
        help="Specific cross-linking relationship to create"
    )
    parser.add_argument(
        "--all",
        action="store_true",
        help="Cross-link all relationships"
    )
    parser.add_argument(
        "--data-dir",
        default="data/txt/sheet",
        help="Data directory (default: data/txt/sheet)"
    )

    args = parser.parse_args()

    data_dir = Path(args.data_dir)

    if not args.all and not args.link:
        parser.error("Must specify either --link or --all")

    # Define cross-linking operations
    operations = {
        "genes-to-genomes": {
            "genes_file": data_dir / "BER_CMM_Data_for_AI_genes_and_proteins.tsv",
            "genomes_file": data_dir / "BER_CMM_Data_for_AI_taxa_and_genomes.tsv",
            "output_file": data_dir / "BER_CMM_Data_for_AI_genes_and_proteins.tsv",
            "func": crosslink_genes_to_genomes
        },
        "pathways-to-genomes": {
            "pathways_file": data_dir / "BER_CMM_Data_for_AI_pathways.tsv",
            "genomes_file": data_dir / "BER_CMM_Data_for_AI_taxa_and_genomes.tsv",
            "output_file": data_dir / "BER_CMM_Data_for_AI_pathways.tsv",
            "func": crosslink_pathways_to_genomes
        },
        "pathways-to-genes": {
            "pathways_file": data_dir / "BER_CMM_Data_for_AI_pathways.tsv",
            "genes_file": data_dir / "BER_CMM_Data_for_AI_genes_and_proteins.tsv",
            "output_file": data_dir / "BER_CMM_Data_for_AI_pathways.tsv",
            "func": crosslink_pathways_to_genes
        },
        "biosamples-to-genomes": {
            "biosamples_file": data_dir / "BER_CMM_Data_for_AI_biosamples.tsv",
            "genomes_file": data_dir / "BER_CMM_Data_for_AI_taxa_and_genomes.tsv",
            "output_file": data_dir / "BER_CMM_Data_for_AI_biosamples.tsv",
            "func": crosslink_biosamples_to_genomes
        },
        "structures-to-genes": {
            "structures_file": data_dir / "BER_CMM_Data_for_AI_structures.tsv",
            "genes_file": data_dir / "BER_CMM_Data_for_AI_genes_and_proteins.tsv",
            "output_file": data_dir / "BER_CMM_Data_for_AI_structures.tsv",
            "func": crosslink_structures_to_genes
        }
    }

    # Determine which operations to run
    if args.all:
        ops_to_run = operations.keys()
    else:
        ops_to_run = [args.link]

    print("=" * 80)
    print("CROSS-LINKING DATA SHEETS")
    print("=" * 80)
    print(f"Data directory: {data_dir}")
    print(f"Operations: {', '.join(ops_to_run)}")
    print("=" * 80)

    # Run operations
    for op_name in ops_to_run:
        op_info = operations[op_name]

        # Check if all input files exist
        missing_files = []
        for key, path in op_info.items():
            if key not in ["func", "output_file"] and not path.exists():
                missing_files.append(str(path))

        if missing_files:
            print(f"\n⚠️  Skipping {op_name}: missing files")
            for f in missing_files:
                print(f"   - {f}")
            continue

        # Run cross-linking function
        try:
            func = op_info["func"]
            func_args = {k: str(v) for k, v in op_info.items() if k != "func"}
            func(**func_args)
        except Exception as e:
            print(f"\n❌ Error in {op_name}: {e}")
            import traceback
            traceback.print_exc()

    print("\n" + "=" * 80)
    print("✓ CROSS-LINKING COMPLETE")
    print("=" * 80)


if __name__ == "__main__":
    main()
