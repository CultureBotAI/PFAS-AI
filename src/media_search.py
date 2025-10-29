"""Growth media search functions for microbial culture collections.

This module provides curated growth media formulations for methylotrophs and
related organisms, with detailed ingredient lists including ontology IDs,
chemical formulas, and concentrations.
"""

import time
import re
from typing import Dict, List, Optional, Tuple
import pandas as pd
import requests
from pathlib import Path

# Import KG-Microbe database interface
try:
    from kg_analysis.kg_database import KnowledgeGraphDB
except (ImportError, AttributeError) as e:
    print(f"Warning: Could not import KnowledgeGraphDB: {e}")
    print("KG-Microbe mapping will be unavailable.")
    KnowledgeGraphDB = None


def query_kg_microbe_for_ingredient(ontology_id: str, ingredient_name: str) -> List[str]:
    """Query KG-Microbe for nodes matching the ingredient.

    Searches for ingredient:, solution:, CHEBI:, CAS-RN:, PUBCHEM: node types.

    Args:
        ontology_id: CHEBI ID (e.g., CHEBI:17790)
        ingredient_name: Common name of ingredient (e.g., Methanol)

    Returns:
        List of matching KG-Microbe node IDs
    """
    if KnowledgeGraphDB is None:
        return []

    try:
        kg = KnowledgeGraphDB("data/kgm/kg-microbe.duckdb")
        matched_nodes = []

        # Query 1: Match by CHEBI ID
        if ontology_id:
            chebi_query = f"""
                SELECT DISTINCT id, name
                FROM nodes
                WHERE id = '{ontology_id}'
                   OR id LIKE '%{ontology_id}%'
                LIMIT 5
            """
            results = kg.query(chebi_query)
            if not results.empty:
                for _, row in results.iterrows():
                    matched_nodes.append(row['id'])

        # Query 2: Match by ingredient name for ingredient:, solution:, CAS-RN:, PUBCHEM: nodes
        if ingredient_name and len(matched_nodes) < 10:
            # Escape quotes for SQL
            safe_ingredient_name = ingredient_name.replace("'", "''")

            name_query = f"""
                SELECT DISTINCT id, name
                FROM nodes
                WHERE (id LIKE 'ingredient:%'
                       OR id LIKE 'solution:%'
                       OR id LIKE 'CAS-RN:%'
                       OR id LIKE 'PUBCHEM:%')
                  AND (LOWER(name) = LOWER('{safe_ingredient_name}')
                       OR LOWER(name) LIKE LOWER('%{safe_ingredient_name}%'))
                LIMIT 10
            """
            results = kg.query(name_query)
            if not results.empty:
                for _, row in results.iterrows():
                    node_id = row['id']
                    if node_id not in matched_nodes:
                        matched_nodes.append(node_id)

        kg.close()
        return matched_nodes[:10]  # Limit to 10 nodes

    except Exception as e:
        print(f"  Warning: KG-Microbe query failed for {ingredient_name}: {e}")
        return []


def query_kg_microbe_for_medium(media_id: str, media_name: str) -> List[str]:
    """Query KG-Microbe for nodes matching the growth medium.

    Searches for medium: node types.

    Args:
        media_id: Medium identifier (e.g., ATCC:1306, NMS)
        media_name: Name of medium (e.g., "ATCC Medium 1306")

    Returns:
        List of matching KG-Microbe node IDs
    """
    if KnowledgeGraphDB is None:
        return []

    try:
        kg = KnowledgeGraphDB("data/kgm/kg-microbe.duckdb")
        matched_nodes = []

        # Query: Match by media name for medium: nodes
        if media_name:
            # Escape quotes for SQL
            safe_media_name = media_name.replace("'", "''")
            safe_media_id = media_id.replace("'", "''")

            name_query = f"""
                SELECT DISTINCT id, name
                FROM nodes
                WHERE id LIKE 'medium:%'
                  AND (LOWER(name) LIKE LOWER('%{safe_media_name}%')
                       OR LOWER(name) LIKE LOWER('%{safe_media_id}%'))
                LIMIT 10
            """
            results = kg.query(name_query)
            if not results.empty:
                for _, row in results.iterrows():
                    matched_nodes.append(row['id'])

        kg.close()
        return matched_nodes[:10]  # Limit to 10 nodes

    except Exception as e:
        print(f"  Warning: KG-Microbe medium query failed for {media_name}: {e}")
        return []


# Curated media formulations for methylotrophs and related organisms
CURATED_MEDIA = {
    "ATCC:1306": {
        "media_name": "ATCC Medium 1306 (Methanol mineral salts)",
        "media_type": "minimal",
        "alternative_names": "Methanol mineral salts medium; MMM",
        "description": "Minimal medium with methanol as sole carbon source for methylotrophs",
        "target_organisms": "Methylobacterium; Methylorubrum; methylotrophs",
        "ph": "6.8-7.0",
        "sterilization_method": "Autoclave base medium, filter-sterilize methanol separately",
        "references": "ATCC",
        "ingredients": [
            {"name": "Methanol", "formula": "CH3OH", "concentration": 0.5, "unit": "% (v/v)", "role": "carbon source", "chebi": "CHEBI:17790"},
            {"name": "Potassium nitrate", "formula": "KNO3", "concentration": 2.0, "unit": "g/L", "role": "nitrogen source", "chebi": "CHEBI:63043"},
            {"name": "Magnesium sulfate heptahydrate", "formula": "MgSO4·7H2O", "concentration": 0.2, "unit": "g/L", "role": "mineral", "chebi": "CHEBI:32599"},
            {"name": "Calcium chloride dihydrate", "formula": "CaCl2·2H2O", "concentration": 0.02, "unit": "g/L", "role": "mineral", "chebi": "CHEBI:64583"},
            {"name": "Dipotassium phosphate", "formula": "K2HPO4", "concentration": 0.8, "unit": "g/L", "role": "buffer", "chebi": "CHEBI:32030"},
            {"name": "Potassium dihydrogen phosphate", "formula": "KH2PO4", "concentration": 0.54, "unit": "g/L", "role": "buffer", "chebi": "CHEBI:63036"},
            {"name": "Ferrous sulfate heptahydrate", "formula": "FeSO4·7H2O", "concentration": 0.005, "unit": "g/L", "role": "trace element", "chebi": "CHEBI:31139"},
            {"name": "Agar", "formula": "", "concentration": 15.0, "unit": "g/L", "role": "solidifying agent", "chebi": "CHEBI:2509"},
        ]
    },

    "NMS": {
        "media_name": "NMS medium (Nitrate mineral salts)",
        "media_type": "minimal",
        "alternative_names": "Nitrate mineral salts medium; Methanotrophic NMS medium",
        "description": "Minimal medium for methanotrophs and methylotrophs with nitrate as nitrogen source",
        "target_organisms": "Methylosinus; Methylococcus; methanotrophs",
        "ph": "6.8",
        "sterilization_method": "Autoclave",
        "references": "Whittenbury et al. (1970)",
        "ingredients": [
            {"name": "Magnesium sulfate heptahydrate", "formula": "MgSO4·7H2O", "concentration": 1.0, "unit": "g/L", "role": "mineral", "chebi": "CHEBI:32599"},
            {"name": "Calcium chloride dihydrate", "formula": "CaCl2·2H2O", "concentration": 0.2, "unit": "g/L", "role": "mineral", "chebi": "CHEBI:64583"},
            {"name": "Potassium nitrate", "formula": "KNO3", "concentration": 1.0, "unit": "g/L", "role": "nitrogen source", "chebi": "CHEBI:63043"},
            {"name": "Dipotassium phosphate", "formula": "K2HPO4", "concentration": 0.54, "unit": "g/L", "role": "buffer", "chebi": "CHEBI:32030"},
            {"name": "Potassium dihydrogen phosphate", "formula": "KH2PO4", "concentration": 0.27, "unit": "g/L", "role": "buffer", "chebi": "CHEBI:63036"},
            {"name": "Iron(III) EDTA solution", "formula": "", "concentration": 2.0, "unit": "mL/L", "role": "trace element", "chebi": ""},
            {"name": "Trace element solution", "formula": "", "concentration": 1.0, "unit": "mL/L", "role": "trace element", "chebi": ""},
        ]
    },

    "AMS": {
        "media_name": "AMS medium (Ammonium mineral salts)",
        "media_type": "minimal",
        "alternative_names": "Ammonium mineral salts medium; Methanotrophic AMS medium",
        "description": "Minimal medium for methanotrophs with ammonium as nitrogen source",
        "target_organisms": "Methylosinus; Methylococcus; methanotrophs",
        "ph": "6.8",
        "sterilization_method": "Autoclave",
        "references": "Whittenbury et al. (1970)",
        "ingredients": [
            {"name": "Magnesium sulfate heptahydrate", "formula": "MgSO4·7H2O", "concentration": 1.0, "unit": "g/L", "role": "mineral", "chebi": "CHEBI:32599"},
            {"name": "Calcium chloride dihydrate", "formula": "CaCl2·2H2O", "concentration": 0.2, "unit": "g/L", "role": "mineral", "chebi": "CHEBI:64583"},
            {"name": "Ammonium chloride", "formula": "NH4Cl", "concentration": 0.5, "unit": "g/L", "role": "nitrogen source", "chebi": "CHEBI:31206"},
            {"name": "Dipotassium phosphate", "formula": "K2HPO4", "concentration": 0.54, "unit": "g/L", "role": "buffer", "chebi": "CHEBI:32030"},
            {"name": "Potassium dihydrogen phosphate", "formula": "KH2PO4", "concentration": 0.27, "unit": "g/L", "role": "buffer", "chebi": "CHEBI:63036"},
            {"name": "Iron(III) EDTA solution", "formula": "", "concentration": 2.0, "unit": "mL/L", "role": "trace element", "chebi": ""},
            {"name": "Trace element solution", "formula": "", "concentration": 1.0, "unit": "mL/L", "role": "trace element", "chebi": ""},
        ]
    },

    "DSMZ:88": {
        "media_name": "DSMZ Medium 88 (SM medium for Paracoccus)",
        "media_type": "complex",
        "alternative_names": "SM medium; Succinate medium",
        "description": "Complex medium with succinate for Paracoccus and related organisms",
        "target_organisms": "Paracoccus; methylotrophs",
        "ph": "7.0",
        "sterilization_method": "Autoclave",
        "references": "DSMZ",
        "ingredients": [
            {"name": "Disodium succinate hexahydrate", "formula": "C4H4Na2O4·6H2O", "concentration": 2.7, "unit": "g/L", "role": "carbon source", "chebi": "CHEBI:16810"},
            {"name": "Ammonium chloride", "formula": "NH4Cl", "concentration": 1.0, "unit": "g/L", "role": "nitrogen source", "chebi": "CHEBI:31206"},
            {"name": "Dipotassium phosphate", "formula": "K2HPO4", "concentration": 1.5, "unit": "g/L", "role": "buffer", "chebi": "CHEBI:32030"},
            {"name": "Potassium dihydrogen phosphate", "formula": "KH2PO4", "concentration": 0.5, "unit": "g/L", "role": "buffer", "chebi": "CHEBI:63036"},
            {"name": "Magnesium sulfate heptahydrate", "formula": "MgSO4·7H2O", "concentration": 0.2, "unit": "g/L", "role": "mineral", "chebi": "CHEBI:32599"},
            {"name": "Yeast extract", "formula": "", "concentration": 1.0, "unit": "g/L", "role": "vitamin source", "chebi": ""},
            {"name": "Trace element solution SL-6", "formula": "", "concentration": 1.0, "unit": "mL/L", "role": "trace element", "chebi": ""},
        ]
    },

    "LB": {
        "media_name": "LB medium (Luria-Bertani)",
        "media_type": "complex",
        "alternative_names": "Luria broth; Lysogeny broth; Lennox broth",
        "description": "Rich complex medium for general bacterial cultivation",
        "target_organisms": "General bacteria",
        "ph": "7.0",
        "sterilization_method": "Autoclave",
        "references": "Bertani (1951)",
        "ingredients": [
            {"name": "Tryptone", "formula": "", "concentration": 10.0, "unit": "g/L", "role": "protein source", "chebi": ""},
            {"name": "Yeast extract", "formula": "", "concentration": 5.0, "unit": "g/L", "role": "vitamin source", "chebi": ""},
            {"name": "Sodium chloride", "formula": "NaCl", "concentration": 10.0, "unit": "g/L", "role": "salt", "chebi": "CHEBI:26710"},
            {"name": "Agar", "formula": "", "concentration": 15.0, "unit": "g/L", "role": "solidifying agent", "chebi": "CHEBI:2509"},
        ]
    },

    "R2A": {
        "media_name": "R2A medium (Reasoner's 2A agar)",
        "media_type": "complex",
        "alternative_names": "Reasoner's 2A agar",
        "description": "Low-nutrient medium for cultivation of oligotrophic bacteria",
        "target_organisms": "Environmental bacteria; Methylobacterium",
        "ph": "7.2",
        "sterilization_method": "Autoclave",
        "references": "Reasoner and Geldreich (1985)",
        "ingredients": [
            {"name": "Yeast extract", "formula": "", "concentration": 0.5, "unit": "g/L", "role": "vitamin source", "chebi": ""},
            {"name": "Proteose peptone", "formula": "", "concentration": 0.5, "unit": "g/L", "role": "protein source", "chebi": ""},
            {"name": "Casamino acids", "formula": "", "concentration": 0.5, "unit": "g/L", "role": "amino acid source", "chebi": ""},
            {"name": "Glucose", "formula": "C6H12O6", "concentration": 0.5, "unit": "g/L", "role": "carbon source", "chebi": "CHEBI:17234"},
            {"name": "Soluble starch", "formula": "(C6H10O5)n", "concentration": 0.5, "unit": "g/L", "role": "carbon source", "chebi": "CHEBI:28017"},
            {"name": "Dipotassium phosphate", "formula": "K2HPO4", "concentration": 0.3, "unit": "g/L", "role": "buffer", "chebi": "CHEBI:32030"},
            {"name": "Magnesium sulfate heptahydrate", "formula": "MgSO4·7H2O", "concentration": 0.05, "unit": "g/L", "role": "mineral", "chebi": "CHEBI:32599"},
            {"name": "Sodium pyruvate", "formula": "C3H3NaO3", "concentration": 0.3, "unit": "g/L", "role": "carbon source", "chebi": "CHEBI:77991"},
            {"name": "Agar", "formula": "", "concentration": 15.0, "unit": "g/L", "role": "solidifying agent", "chebi": "CHEBI:2509"},
        ]
    },

    "MPYG": {
        "media_name": "MPYG medium (Methanol-Peptone-Yeast extract-Glucose)",
        "media_type": "complex",
        "alternative_names": "Methanol enrichment medium",
        "description": "Enrichment medium for methylotrophs combining methanol with complex nutrients",
        "target_organisms": "Methylobacterium; Methylorubrum",
        "ph": "7.0",
        "sterilization_method": "Autoclave base medium, add methanol aseptically",
        "references": "Green and Bousfield (1983)",
        "ingredients": [
            {"name": "Methanol", "formula": "CH3OH", "concentration": 0.5, "unit": "% (v/v)", "role": "carbon source", "chebi": "CHEBI:17790"},
            {"name": "Peptone", "formula": "", "concentration": 3.0, "unit": "g/L", "role": "protein source", "chebi": ""},
            {"name": "Yeast extract", "formula": "", "concentration": 3.0, "unit": "g/L", "role": "vitamin source", "chebi": ""},
            {"name": "Glucose", "formula": "C6H12O6", "concentration": 5.0, "unit": "g/L", "role": "carbon source", "chebi": "CHEBI:17234"},
            {"name": "Dipotassium phosphate", "formula": "K2HPO4", "concentration": 0.6, "unit": "g/L", "role": "buffer", "chebi": "CHEBI:32030"},
            {"name": "Agar", "formula": "", "concentration": 15.0, "unit": "g/L", "role": "solidifying agent", "chebi": "CHEBI:2509"},
        ]
    },
}


def create_media_records() -> Tuple[List[Dict], List[Dict]]:
    """Create growth media and media ingredient records from curated formulations.

    Returns:
        Tuple of (media_records, ingredient_records)
    """
    media_records = []
    ingredient_records = []

    for media_id, media_data in CURATED_MEDIA.items():
        # Create ingredient records with KG-Microbe node mapping
        media_ingredients = []
        for idx, ingredient in enumerate(media_data["ingredients"]):
            ingredient_id = f"{media_id}_ING_{idx+1:03d}"

            # Query KG-Microbe for ingredient nodes (ingredient:, solution:, CHEBI:, CAS-RN:, PUBCHEM:)
            kg_nodes = query_kg_microbe_for_ingredient(
                ingredient.get("chebi", ""),
                ingredient["name"]
            )

            ingredient_record = {
                "ingredient_id": ingredient_id,
                "ingredient_name": ingredient["name"],
                "media_id": media_id,
                "media_name": media_data["media_name"],
                "ontology_id": ingredient.get("chebi", ""),
                "ontology_label": ingredient["name"],
                "chemical_formula": ingredient.get("formula", ""),
                "concentration": ingredient.get("concentration", ""),
                "unit": ingredient.get("unit", ""),
                "role": ingredient.get("role", ""),
                "kg_microbe_nodes": "; ".join(kg_nodes) if kg_nodes else "",
                "notes": "",
                "source": "extend"
            }
            ingredient_records.append(ingredient_record)

        # Query KG-Microbe for medium: nodes
        medium_kg_nodes = query_kg_microbe_for_medium(media_id, media_data["media_name"])

        media_record = {
            "media_id": media_id,
            "media_name": media_data["media_name"],
            "media_type": media_data["media_type"],
            "alternative_names": media_data["alternative_names"],
            "description": media_data["description"],
            "target_organisms": media_data["target_organisms"],
            "ph": media_data["ph"],
            "sterilization_method": media_data["sterilization_method"],
            "references": media_data["references"],
            "kg_microbe_nodes": "; ".join(medium_kg_nodes) if medium_kg_nodes else "",
            "notes": "",
            "source": "extend"
        }
        media_records.append(media_record)

    return media_records, ingredient_records


def create_extended_media_tables(
    output_dir: str = "data/txt/sheet"
) -> None:
    """Create extended media and media_ingredients tables.

    Args:
        output_dir: Directory to save extended tables
    """
    print("=" * 80)
    print("GROWTH MEDIA DATA CURATION")
    print("=" * 80)
    print()

    print("Creating curated media and ingredient records...")
    media_records, ingredient_records = create_media_records()

    print(f"  Created {len(media_records)} media records")
    print(f"  Created {len(ingredient_records)} ingredient records")
    print()

    # Convert to DataFrames
    media_df = pd.DataFrame(media_records)
    ingredients_df = pd.DataFrame(ingredient_records)

    # Save to files
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    media_file = output_dir / "PFAS_Data_for_AI_growth_media_extended.tsv"
    ingredients_file = output_dir / "PFAS_Data_for_AI_media_ingredients_extended.tsv"

    media_df.to_csv(media_file, sep='\t', index=False)
    ingredients_df.to_csv(ingredients_file, sep='\t', index=False)

    print(f"Extended growth media table saved: {media_file}")
    print(f"  Total media: {len(media_df)}")
    print()

    print(f"Extended media ingredients table saved: {ingredients_file}")
    print(f"  Total ingredients: {len(ingredients_df)}")
    print()

    # Summary by media type
    print("Media by type:")
    for media_type in media_df['media_type'].value_counts().items():
        print(f"  {media_type[0]}: {media_type[1]} media")
    print()

    # Summary by ingredient role
    print("Top ingredient roles:")
    for role in ingredients_df['role'].value_counts().head(10).items():
        print(f"  {role[0]}: {role[1]} ingredients")


if __name__ == "__main__":
    """Run media curation when executed directly."""
    create_extended_media_tables()
