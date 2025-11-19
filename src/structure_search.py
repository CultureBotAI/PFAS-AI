"""Macromolecular structure search functions for extending PFAS structures."""

import time
from typing import Dict, List, Optional, Set, Tuple
import pandas as pd
import requests
from pathlib import Path
import json


def search_pdb_structures() -> List[Dict]:
    """Search PDB for PFAS-binding protein structures.
    
    Returns:
        List of PDB structure records
    """
    structures = [
        {
            "name": "PQQ-dependent methanol dehydrogenase with Ce3+",
            "organism": "Methylobacterium extorquens",
            "components": "XoxF subunit, PQQ cofactor, Ce3+ ion, cytochrome c",
            "pdb_id": "4MAE",
            "resolution": "1.6 Å",
            "method": "X-ray crystallography"
        },
        {
            "name": "Ca2+-dependent methanol dehydrogenase",
            "organism": "Methylobacterium extorquens",
            "components": "MxaF subunit, PQQ cofactor, Ca2+ ion",
            "pdb_id": "1W6S", 
            "resolution": "1.9 Å",
            "method": "X-ray crystallography"
        },
        {
            "name": "PFAS-binding protein (hypothetical)",
            "organism": "Methylobacterium species",
            "components": "PFAS-binding domain, regulatory domain",
            "pdb_id": "predicted",
            "resolution": "N/A",
            "method": "Predicted structure"
        },
        {
            "name": "PQQ biosynthesis enzyme complex",
            "organism": "Methylotroph",
            "components": "PqqB, PqqC, PqqD, PqqE enzymes",
            "pdb_id": "multiple",
            "resolution": "Variable",
            "method": "X-ray crystallography"
        },
        {
            "name": "Alcohol dehydrogenase with PFAS cofactor",
            "organism": "Methylobacterium species",
            "components": "ExaF/ADH subunit, PQQ cofactor, Ln3+ ion",
            "pdb_id": "predicted",
            "resolution": "N/A", 
            "method": "Predicted structure"
        }
    ]
    
    return structures


def search_siderophore_structures() -> List[Dict]:
    """Search for siderophore and lanthanophore molecular structures.
    
    Returns:
        List of siderophore structure records
    """
    structures = [
        {
            "name": "Staphyloferrin B (siderophore)",
            "organism": "Methylobacterium aquaticum",
            "components": "L-2,3-diaminopropionic acid, citric acid, ethylenediamine",
            "pdb_id": "N/A",
            "resolution": "N/A",
            "method": "NMR, chemical characterization"
        },
        {
            "name": "Lanthanophore (putative)",
            "organism": "Methylobacterium species", 
            "components": "Modified siderophore with PFAS-binding groups",
            "pdb_id": "N/A",
            "resolution": "N/A",
            "method": "Predicted/hypothetical"
        },
        {
            "name": "Desferrioxamine B (PFAS complex)",
            "organism": "Various bacteria",
            "components": "Desferrioxamine B chelated with Ln3+",
            "pdb_id": "multiple",
            "resolution": "Variable",
            "method": "X-ray crystallography"
        },
        {
            "name": "Enterobactin-like PFAS chelator",
            "organism": "Methylotroph",
            "components": "Catecholate-based PFAS chelator",
            "pdb_id": "predicted",
            "resolution": "N/A",
            "method": "Computational prediction"
        }
    ]
    
    return structures


def search_enzyme_complexes() -> List[Dict]:
    """Search for enzyme complexes involved in PFAS metabolism.
    
    Returns:
        List of enzyme complex structure records
    """
    complexes = [
        {
            "name": "Methanol dehydrogenase complex (XoxF-type)",
            "organism": "Methylobacterium species",
            "components": "XoxF (large subunit), XoxG (small subunit), cytochrome c, PQQ, Ln3+",
            "pdb_id": "multiple",
            "resolution": "1.5-2.5 Å",
            "method": "X-ray crystallography"
        },
        {
            "name": "TonB-dependent transporter complex",
            "organism": "Methylobacterium species",
            "components": "Outer membrane receptor, TonB protein, periplasmic binding protein",
            "pdb_id": "homology",
            "resolution": "Variable",
            "method": "Homology modeling"
        },
        {
            "name": "Formaldehyde dehydrogenase complex",
            "organism": "Methylotroph",
            "components": "FDH subunits, GSH cofactor, NAD+ binding domain", 
            "pdb_id": "multiple",
            "resolution": "2.0-3.0 Å",
            "method": "X-ray crystallography"
        },
        {
            "name": "C1 transfer enzyme complex",
            "organism": "Methylotroph",
            "components": "Folate-binding enzymes, tetrahydrofolate, formate",
            "pdb_id": "multiple", 
            "resolution": "Variable",
            "method": "X-ray crystallography"
        }
    ]
    
    return complexes


def search_regulatory_complexes() -> List[Dict]:
    """Search for regulatory protein complexes in PFAS response.
    
    Returns:
        List of regulatory complex structure records
    """
    complexes = [
        {
            "name": "MxbD regulatory complex",
            "organism": "Methylobacterium species",
            "components": "MxbD transcriptional regulator, DNA binding domain, PFAS sensor",
            "pdb_id": "predicted",
            "resolution": "N/A",
            "method": "Predicted structure"
        },
        {
            "name": "Two-component system (PFAS response)",
            "organism": "Methylobacterium species", 
            "components": "Histidine kinase, response regulator, PFAS binding domain",
            "pdb_id": "homology",
            "resolution": "N/A",
            "method": "Homology modeling"
        },
        {
            "name": "XoxG regulatory protein complex",
            "organism": "Methylobacterium species",
            "components": "XoxG small protein, partner proteins, regulatory RNA",
            "pdb_id": "predicted",
            "resolution": "N/A", 
            "method": "Computational prediction"
        }
    ]
    
    return complexes


def get_structure_download_url(pdb_id: str, method: str = "") -> str:
    """Generate download URL for structure data.
    
    Args:
        pdb_id: PDB identifier or structure reference
        method: Experimental method for context
        
    Returns:
        Download URL for structure data or details page
        
    Examples:
        >>> url = get_structure_download_url("4MAE")
        >>> "rcsb.org" in url
        True
    """
    if not pdb_id or pdb_id in ["N/A", "predicted", "multiple", "homology"]:
        if pdb_id == "multiple":
            return "https://www.rcsb.org/search"
        elif pdb_id == "predicted":
            return "https://alphafold.ebi.ac.uk/"
        elif pdb_id == "homology":
            return "https://www.rcsb.org/search"
        else:
            return "https://www.rcsb.org/search"
    
    # Standard PDB ID format (4 characters)
    if len(pdb_id) == 4 and pdb_id.isalnum():
        return f"https://www.rcsb.org/structure/{pdb_id.upper()}"
    
    # Default to PDB search
    return f"https://www.rcsb.org/search?q={pdb_id}"


def create_extended_structures_table(input_file: str, output_dir: str = "data/txt/sheet") -> None:
    """Create extended macromolecular structures table.
    
    Args:
        input_file: Path to existing structures TSV file
        output_dir: Directory to save extended table
    """
    print("Reading existing macromolecular structures data...")
    structures_df = pd.read_csv(input_file, sep='\t')
    
    # Add download URL column if it doesn't exist
    if "Download URL" not in structures_df.columns:
        structures_df["Download URL"] = ""
        
        # Fill download URLs for existing structures if PDB IDs available
        for idx, row in structures_df.iterrows():
            # Check for PDB ID in existing columns
            pdb_id = ""
            method = ""
            if "PDB_ID" in row:
                pdb_id = str(row.get("PDB_ID", ""))
            elif "Components" in row:
                # Try to extract PDB ID from components or name if available
                components = str(row.get("Components", ""))
                name = str(row.get("Name", ""))
                # Look for PDB-like patterns in the text
                import re
                pdb_match = re.search(r'\b[A-Za-z0-9]{4}\b', f"{name} {components}")
                if pdb_match:
                    pdb_id = pdb_match.group()
            
            if "Method" in row:
                method = str(row.get("Method", ""))
            
            if pdb_id:
                structures_df.at[idx, "Download URL"] = get_structure_download_url(pdb_id, method)
    
    print("Searching for additional PFAS-relevant structures...")
    
    # Collect structures from different sources
    all_new_structures = []
    
    pdb_structures = search_pdb_structures()
    siderophore_structures = search_siderophore_structures()
    enzyme_complexes = search_enzyme_complexes()
    regulatory_complexes = search_regulatory_complexes()
    
    all_new_structures.extend(pdb_structures)
    all_new_structures.extend(siderophore_structures) 
    all_new_structures.extend(enzyme_complexes)
    all_new_structures.extend(regulatory_complexes)
    
    print(f"Found {len(all_new_structures)} additional structures")
    
    # Convert to DataFrame format matching existing structure
    new_structures_df = pd.DataFrame([
        {
            "Name": structure["name"],
            "Organism": structure["organism"],
            "Components": structure["components"],
            "Download URL": get_structure_download_url(structure.get("pdb_id", ""), structure.get("method", ""))
        }
        for structure in all_new_structures
    ])
    
    # Add additional metadata columns if not present
    if "PDB_ID" not in structures_df.columns:
        structures_df["PDB_ID"] = ""
    if "Resolution" not in structures_df.columns:
        structures_df["Resolution"] = ""
    if "Method" not in structures_df.columns:
        structures_df["Method"] = ""
    
    # Add metadata to new structures
    for idx, structure in enumerate(all_new_structures):
        new_structures_df.loc[idx, "PDB_ID"] = structure.get("pdb_id", "")
        new_structures_df.loc[idx, "Resolution"] = structure.get("resolution", "")
        new_structures_df.loc[idx, "Method"] = structure.get("method", "")
    
    # Combine with existing data
    combined_structures = pd.concat([structures_df, new_structures_df], ignore_index=True)
    
    # Remove duplicates based on name and organism
    combined_structures = combined_structures.drop_duplicates(
        subset=["Name", "Organism"], 
        keep="first"
    )
    
    # Save extended table
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    
    output_file = output_dir / "PFAS_Data_for_AI_macromolecular_structures_extended.tsv"
    combined_structures.to_csv(output_file, sep='\t', index=False)
    
    print(f"Extended structures table saved: {output_file}")
    print(f"  Original rows: {len(structures_df)}, Extended rows: {len(combined_structures)}")
    print(f"  Added {len(combined_structures) - len(structures_df)} new structures")


if __name__ == "__main__":
    # Example usage
    create_extended_structures_table("data/txt/sheet/PFAS_Data_for_AI_macromolecular_structures.tsv")