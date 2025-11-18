#!/usr/bin/env python3
"""
Update chemicals table using Knowledge Graph mining (extend3)

This script queries kg-microbe-function to extract:
- CHEBI terms for substrates, products, cofactors
- Chemical compounds associated with target taxa proteins
- Molecular formulas and properties

All new records are labeled with source='kg_update'.
"""

from pathlib import Path
from typing import Dict, List, Set, Optional
import pandas as pd
import argparse
import json
from src.kg_mining_utils import (
    KGMiningSession,
    load_taxon_ids,
    load_existing_chemical_ids,
    deduplicate_and_merge,
    save_extended_table,
    summarize_extraction,
    format_source_label
)


def query_chemicals_from_function_kg(
    session: KGMiningSession,
    taxon_ids: List[str]
) -> pd.DataFrame:
    """
    Query function KG for CHEBI chemicals from target taxa.

    Uses three-hop path: NCBITaxon <- derives_from <- UniProtKB -> has_input/output -> CHEBI

    Args:
        session: Active KG mining session
        taxon_ids: List of NCBITaxon IDs

    Returns:
        DataFrame with chebi_id, chemical_name, protein_id, taxon_id, predicate
    """
    if not session.function_kg:
        raise RuntimeError("Function KG not enabled in session")

    print(f"\nQuerying chemicals for {len(taxon_ids)} taxa...")

    taxa_list = ", ".join([f"'{tid}'" for tid in taxon_ids])

    # Three-hop query: Taxa -> Proteins -> Chemicals (CHEBI)
    sql = f"""
    WITH taxon_proteins AS (
        -- Get proteins from target taxa
        SELECT DISTINCT
            e.subject as protein_id,
            e.object as taxon_id
        FROM edges e
        WHERE e.object IN ({taxa_list})
          AND e.predicate = 'biolink:derives_from'
          AND e.subject LIKE 'UniProtKB:%'
    )
    SELECT DISTINCT
        e2.object as chebi_id,
        n.name as chemical_name,
        n.category as chemical_category,
        tp.protein_id,
        tp.taxon_id,
        e2.predicate,
        COUNT(DISTINCT tp.protein_id) OVER (PARTITION BY e2.object) as protein_count
    FROM taxon_proteins tp
    JOIN edges e2 ON tp.protein_id = e2.subject
    JOIN nodes n ON e2.object = n.id
    WHERE e2.object LIKE 'CHEBI:%'
      AND e2.predicate IN ('biolink:has_input', 'biolink:has_output',
                            'biolink:has_participant', 'biolink:related_to')
    ORDER BY protein_count DESC, chebi_id
    """

    df = session.function_kg.query(sql)
    print(f"Retrieved {len(df)} chemical associations")

    # Count unique chemicals
    unique_chemicals = df['chebi_id'].nunique()
    print(f"Found {unique_chemicals} unique CHEBI compounds")

    return df


def infer_compound_type_from_predicate(predicate: str) -> str:
    """
    Infer compound type from edge predicate.

    Args:
        predicate: Biolink predicate (e.g., "biolink:has_input")

    Returns:
        Compound type string
    """
    if "input" in predicate.lower() or "substrate" in predicate.lower():
        return "substrate"
    elif "output" in predicate.lower() or "product" in predicate.lower():
        return "product"
    elif "cofactor" in predicate.lower():
        return "cofactor"
    else:
        return "metabolite"


def infer_role_from_predicate(predicate: str) -> str:
    """
    Infer role in bioprocess from edge predicate.

    Args:
        predicate: Biolink predicate

    Returns:
        Role description string
    """
    if "input" in predicate.lower():
        return "substrate"
    elif "output" in predicate.lower():
        return "product"
    elif "participant" in predicate.lower():
        return "reaction participant"
    else:
        return "metabolite"


def format_chemical_records(
    df: pd.DataFrame,
    source_label: str = "kg_update"
) -> pd.DataFrame:
    """
    Format KG query results into chemicals table schema.

    Schema:
    - chemical_id
    - chemical_name
    - compound_type
    - molecular_formula
    - molecular_weight
    - role_in_bioprocess
    - chebi_id
    - pubchem_id
    - chembl_id
    - properties
    - Download URL
    - source

    Args:
        df: Raw KG query results
        source_label: Source label for new records

    Returns:
        Formatted DataFrame matching chemicals table schema
    """
    # Group by chebi_id to aggregate protein associations
    records = []

    for chebi_id, group in df.groupby('chebi_id'):
        chemical_name = group.iloc[0]['chemical_name']

        # Count proteins using this chemical
        protein_count = group['protein_id'].nunique()

        # Infer compound type from most common predicate
        predicates = group['predicate'].value_counts()
        main_predicate = predicates.index[0] if len(predicates) > 0 else "biolink:related_to"
        compound_type = infer_compound_type_from_predicate(main_predicate)
        role = infer_role_from_predicate(main_predicate)

        # Extract CHEBI ID (remove "CHEBI:" prefix)
        chebi_accession = chebi_id.replace("CHEBI:", "")

        # Create properties JSON
        properties = {
            "protein_count": protein_count,
            "source": "KG mining from function database",
            "predicates": list(group['predicate'].unique())
        }

        # Generate CHEBI download URL
        download_url = f"https://www.ebi.ac.uk/chebi/searchId.do?chebiId={chebi_id}"

        records.append({
            "chemical_id": chebi_id,
            "chemical_name": chemical_name if pd.notna(chemical_name) else "",
            "compound_type": compound_type,
            "molecular_formula": "",  # Not available in KG
            "molecular_weight": "",  # Not available in KG
            "role_in_bioprocess": role,
            "chebi_id": chebi_id,
            "pubchem_id": "",  # Not available in KG
            "chembl_id": "",  # Not available in KG
            "properties": json.dumps(properties),
            "Download URL": download_url,
            "source": source_label
        })

    result_df = pd.DataFrame(records)
    print(f"Formatted {len(result_df)} unique chemical records")

    return result_df


def extend_chemicals_from_kg(
    output_file: str = "data/txt/sheet/extended/BER_CMM_Data_for_AI_chemicals_extended.tsv",
    source_label: str = "kg_update",
    append: bool = True
) -> pd.DataFrame:
    """
    Main workflow: Update chemicals table using function KG mining.

    Args:
        output_file: Output TSV file path
        source_label: Source label for new records
        append: If True, append to existing file

    Returns:
        DataFrame with new chemical records
    """
    print("=" * 80)
    print("KG-UPDATE: Knowledge Graph Mining for Chemicals")
    print("=" * 80)

    # Load target taxa
    taxon_ids = load_taxon_ids()
    if not taxon_ids:
        print("❌ No taxon IDs found!")
        return pd.DataFrame()

    # Load existing chemical IDs to avoid duplicates
    existing_ids = load_existing_chemical_ids(output_file)

    # Query function KG
    with KGMiningSession(use_function_kg=True, use_phenotype_kg=False) as session:
        # Get chemicals and associated proteins
        chemical_df = query_chemicals_from_function_kg(session, taxon_ids)

        if chemical_df.empty:
            print("⚠️  No chemicals found in KG for target taxa")
            return pd.DataFrame()

        # Format into chemicals table schema
        chemical_records = format_chemical_records(chemical_df, source_label)

        # Deduplicate against existing chemical IDs
        chemical_records = deduplicate_and_merge(
            chemical_records,
            existing_ids,
            id_column="chemical_id"
        )

        if chemical_records.empty:
            print("⚠️  No new unique chemicals to add (all duplicates)")
            return pd.DataFrame()

        # Save results
        save_extended_table(chemical_records, output_file, append=append)

        # Summary
        summarize_extraction(
            "chemicals",
            len(existing_ids),
            len(chemical_records),
            source_label
        )

        return chemical_records


def main():
    """Command-line interface."""
    parser = argparse.ArgumentParser(
        description="Update chemicals table using Knowledge Graph mining"
    )
    parser.add_argument(
        "--output",
        default="data/txt/sheet/extended/BER_CMM_Data_for_AI_chemicals_extended.tsv",
        help="Output TSV file path"
    )
    parser.add_argument(
        "--source-label",
        default="kg_update",
        help="Source label for new records"
    )
    parser.add_argument(
        "--no-append",
        action="store_true",
        help="Overwrite instead of append"
    )

    args = parser.parse_args()

    extend_chemicals_from_kg(
        output_file=args.output,
        source_label=args.source_label,
        append=not args.no_append
    )


if __name__ == "__main__":
    main()
