"""Pathway search functions for extending PFAS biodegradation pathways."""

import time
from typing import Dict, List, Optional, Set, Tuple
import pandas as pd
import requests
from pathlib import Path


def search_kegg_pathways(keywords: List[str]) -> List[Dict]:
    """Search KEGG database for pathways related to keywords.
    
    Args:
        keywords: List of keywords to search for
        
    Returns:
        List of pathway records with metadata
        
    Examples:
        >>> # Search for dehalogenation pathways
        >>> pathways = search_kegg_pathways(["dehalogenation", "fluoride"])  # doctest: +SKIP
        >>> len(pathways) >= 0  # doctest: +SKIP
        True
    """
    pathways = []
    
    for keyword in keywords:
        try:
            # Search KEGG pathway database
            search_url = f"http://rest.kegg.jp/find/pathway/{keyword}"
            response = requests.get(search_url, timeout=10)
            
            if response.status_code == 200:
                lines = response.text.strip().split('\n')
                for line in lines:
                    if line and '\t' in line:
                        pathway_id, description = line.split('\t', 1)
                        pathways.append({
                            "pathway_id": pathway_id,
                            "pathway_name": description.strip(),
                            "search_keyword": keyword,
                            "database": "KEGG"
                        })
            
            time.sleep(0.5)  # Rate limiting for KEGG API
            
        except Exception as e:
            print(f"Error searching KEGG for {keyword}: {e}")
    
    # Remove duplicates
    seen = set()
    unique_pathways = []
    for pathway in pathways:
        key = (pathway["pathway_id"], pathway["pathway_name"])
        if key not in seen:
            seen.add(key)
            unique_pathways.append(pathway)
    
    return unique_pathways


def search_metacyc_pathways() -> List[Dict]:
    """Search for MetaCyc pathways relevant to PFAS biodegradation.

    Returns:
        List of MetaCyc pathway records

    Note:
        This function provides known PFAS-relevant MetaCyc pathways
        since direct API access is limited.
    """
    # Known PFAS-relevant MetaCyc pathways
    metacyc_pathways = [
        {
            "pathway_id": "PWY-5134",
            "pathway_name": "reductive dehalogenation",
            "description": "Reductive dechlorination pathway (potential for C-F bond cleavage)",
            "organisms": "Dehalococcoides, Desulfitobacterium",
            "database": "MetaCyc"
        },
        {
            "pathway_id": "PWY-7003",
            "pathway_name": "haloacid dehalogenase pathway",
            "description": "Hydrolytic dehalogenation of halogenated acids",
            "organisms": "Pseudomonas, Rhodococcus",
            "database": "MetaCyc"
        },
        {
            "pathway_id": "PWY-6353",
            "pathway_name": "fluoroacetate degradation",
            "description": "Degradation of fluoroacetate via dehalogenation",
            "organisms": "Rhodopseudomonas palustris",
            "database": "MetaCyc"
        },
        {
            "pathway_id": "PWY-6173",
            "pathway_name": "aromatic compound degradation",
            "description": "Aromatic ring cleavage (relevant for PFAS backbone degradation)",
            "organisms": "Pseudomonas, Rhodococcus",
            "database": "MetaCyc"
        },
        {
            "pathway_id": "PWY-5188",
            "pathway_name": "tetrachloroethene degradation",
            "description": "Reductive dechlorination of chlorinated ethenes",
            "organisms": "Dehalococcoides mccartyi",
            "database": "MetaCyc"
        },
        {
            "pathway_id": "PWY-6520",
            "pathway_name": "naphthalene degradation",
            "description": "Aerobic degradation of polycyclic aromatic hydrocarbons",
            "organisms": "Pseudomonas putida",
            "database": "MetaCyc"
        }
    ]
    
    return metacyc_pathways


def get_lanthanide_pathway_genes() -> List[Dict]:
    """Get genes associated with lanthanide bioprocessing pathways.
    
    Returns:
        List of gene records with pathway associations
    """
    lanthanide_genes = [
        {
            "gene_symbol": "xoxF",
            "gene_name": "PQQ-dependent methanol dehydrogenase (lanthanide-dependent)",
            "kegg_ko": "K23995",
            "ec_number": "1.1.2.7",
            "function": "Primary lanthanide-dependent methanol dehydrogenase",
            "pathway_relevance": "Core enzyme for lanthanide-dependent methanol oxidation"
        },
        {
            "gene_symbol": "mxaF",
            "gene_name": "PQQ-dependent methanol dehydrogenase (calcium-dependent)", 
            "kegg_ko": "K14028",
            "ec_number": "1.1.2.7",
            "function": "Calcium-dependent methanol dehydrogenase",
            "pathway_relevance": "Alternative to lanthanide-dependent enzyme"
        },
        {
            "gene_symbol": "exaF",
            "gene_name": "PQQ-dependent ethanol dehydrogenase",
            "kegg_ko": "K00114",
            "ec_number": "1.1.2.7",
            "function": "Lanthanide-responsive alcohol dehydrogenase",
            "pathway_relevance": "Broader alcohol oxidation, responds to lanthanides"
        },
        {
            "gene_symbol": "mxbD",
            "gene_name": "Methanol metabolism regulator",
            "kegg_ko": "",
            "ec_number": "",
            "function": "Regulator of methanol metabolism genes",
            "pathway_relevance": "Controls expression of lanthanide-dependent pathways"
        },
        {
            "gene_symbol": "fae1/fae2",
            "gene_name": "Formaldehyde activating enzyme",
            "kegg_ko": "",
            "ec_number": "",
            "function": "Formaldehyde detoxification/metabolism",
            "pathway_relevance": "Downstream of methanol oxidation"
        },
        {
            "gene_symbol": "mch",
            "gene_name": "H4MPT-pathway methylenetetrahydrofolate dehydrogenase",
            "kegg_ko": "",
            "ec_number": "",
            "function": "H4MPT-dependent C1 metabolism",
            "pathway_relevance": "One-carbon metabolism downstream of methanol"
        },
        {
            "gene_symbol": "hgd",
            "gene_name": "GSH-dependent formaldehyde dehydrogenase",
            "kegg_ko": "",
            "ec_number": "",
            "function": "Formaldehyde oxidation via glutathione pathway",
            "pathway_relevance": "Alternative formaldehyde oxidation pathway"
        }
    ]
    
    return lanthanide_genes


def get_pathway_download_url(pathway_id: str, database: str = "KEGG") -> str:
    """Generate download URL for pathway data.
    
    Args:
        pathway_id: Pathway identifier (e.g., ko00680, PWY-5506)
        database: Database name (KEGG, MetaCyc, Custom)
        
    Returns:
        Download URL for pathway data or details page
        
    Examples:
        >>> url = get_pathway_download_url("ko00680", "KEGG")
        >>> "kegg.jp" in url
        True
    """
    if not pathway_id:
        return ""
    
    if database == "KEGG":
        if pathway_id.startswith("ko"):
            return f"https://www.kegg.jp/pathway/{pathway_id}"
        else:
            return f"https://www.kegg.jp/entry/{pathway_id}"
    elif database == "MetaCyc":
        return f"https://metacyc.org/META/NEW-IMAGE?type=PATHWAY&object={pathway_id}"
    else:
        # For custom pathways, return a general reference
        return f"https://www.kegg.jp/kegg/pathway.html"


def create_extended_pathways_table(input_file: str, output_dir: str = "data/txt/sheet") -> None:
    """Create extended pathways table with additional lanthanide-relevant pathways.
    
    Args:
        input_file: Path to existing pathways TSV file
        output_dir: Directory to save extended table
    """
    print("Reading existing pathways data...")
    pathways_df = pd.read_csv(input_file, sep='\t')
    
    # Add download URL column if it doesn't exist
    if "Download URL" not in pathways_df.columns:
        pathways_df["Download URL"] = ""
        
        # Fill download URLs for existing pathway IDs if available
        for idx, row in pathways_df.iterrows():
            pathway_id = row.get("pathway id", "")
            if pathway_id:
                pathways_df.at[idx, "Download URL"] = get_pathway_download_url(str(pathway_id), "KEGG")
    
    print("Searching for additional lanthanide-relevant pathways...")
    
    # Search KEGG for relevant pathways
    kegg_keywords = [
        "methanol", "methane", "methylotroph", "formaldehyde", 
        "C1 metabolism", "one-carbon"
    ]
    
    kegg_pathways = search_kegg_pathways(kegg_keywords)
    metacyc_pathways = search_metacyc_pathways()
    lanthanide_genes = get_lanthanide_pathway_genes()
    
    print(f"Found {len(kegg_pathways)} KEGG pathways and {len(metacyc_pathways)} MetaCyc pathways")
    
    # Create new pathway entries
    new_pathways = []
    
    # Add KEGG pathways
    for pathway in kegg_pathways:
        if any(term in pathway["pathway_name"].lower() for term in 
               ["methanol", "methane", "methylotroph", "c1", "one-carbon", "formaldehyde"]):
            
            # Find relevant genes for this pathway
            relevant_genes = [g["gene_symbol"] for g in lanthanide_genes 
                            if any(term in g["function"].lower() for term in 
                                  ["methanol", "formaldehyde", "alcohol"])]
            
            new_pathways.append({
                "pathway name": pathway["pathway_name"],
                "pathway id": pathway["pathway_id"],
                "organism": "Methylotrophic bacteria (Methylobacterium, Methylorubrum, Paracoccus)",
                "genes (from genes and proteins tab)": "; ".join(relevant_genes[:5]) if relevant_genes else "",
                "genes (from genes & proteins tab)": f"KEGG pathway with genes: {'; '.join(relevant_genes)}" if relevant_genes else "See KEGG database for detailed gene annotations",
                "Download URL": get_pathway_download_url(pathway["pathway_id"], "KEGG")
            })
    
    # Add MetaCyc pathways
    for pathway in metacyc_pathways:
        relevant_genes = [g["gene_symbol"] for g in lanthanide_genes 
                        if "methanol" in g["function"].lower() or "formaldehyde" in g["function"].lower()]
        
        new_pathways.append({
            "pathway name": pathway["pathway_name"],
            "pathway id": pathway["pathway_id"],
            "organism": pathway["organisms"],
            "genes (from genes and proteins tab)": "; ".join(relevant_genes[:5]) if relevant_genes else "",
            "genes (from genes & proteins tab)": pathway["description"],
            "Download URL": get_pathway_download_url(pathway["pathway_id"], "MetaCyc")
        })
    
    # Add specific lanthanide-responsive pathways
    lanthanide_specific_pathways = [
        {
            "pathway name": "Lanthanide uptake and homeostasis",
            "pathway id": "Custom_LN001",
            "organism": "Methylobacterium, Methylorubrum, Bradyrhizobium species",
            "genes (from genes and proteins tab)": "tonB-like receptors; siderophore biosynthesis genes; lanthanophore genes",
            "genes (from genes & proteins tab)": "TonB-dependent transporters for lanthanide uptake; siderophore/lanthanophore biosynthesis clusters (sbn genes, etc.); lanthanide binding proteins",
            "Download URL": get_pathway_download_url("Custom_LN001", "Custom")
        },
        {
            "pathway name": "Rare earth element-responsive gene regulation",
            "pathway id": "Custom_LN002", 
            "organism": "Methylotrophic bacteria with XoxF systems",
            "genes (from genes and proteins tab)": "mxbD; xoxG; regulatory RNAs; lanthanide sensors",
            "genes (from genes & proteins tab)": "MxbD-family regulators; XoxG (small protein regulator); lanthanide-responsive regulatory elements; two-component systems",
            "Download URL": get_pathway_download_url("Custom_LN002", "Custom")
        },
        {
            "pathway name": "PQQ biosynthesis (cofactor for lanthanide-dependent enzymes)",
            "pathway id": "ko00790",
            "organism": "PQQ-producing methylotrophs",
            "genes (from genes and proteins tab)": "pqqA; pqqB; pqqC; pqqD; pqqE; pqqF",
            "genes (from genes & proteins tab)": "PQQ biosynthesis genes: pqqA (precursor peptide), pqqB-F (modification enzymes). PQQ is essential cofactor for XoxF and MxaF methanol dehydrogenases.",
            "Download URL": get_pathway_download_url("ko00790", "KEGG")
        }
    ]
    
    new_pathways.extend(lanthanide_specific_pathways)
    
    # Convert to DataFrame and combine
    if new_pathways:
        new_pathways_df = pd.DataFrame(new_pathways)
        combined_pathways = pd.concat([pathways_df, new_pathways_df], ignore_index=True)
        
        # Remove duplicates based on pathway name
        combined_pathways = combined_pathways.drop_duplicates(subset=["pathway name"], keep="first")
    else:
        combined_pathways = pathways_df
    
    # Save extended table
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    
    output_file = output_dir / "PFAS_Data_for_AI_pathways_extended.tsv"
    combined_pathways.to_csv(output_file, sep='\t', index=False)
    
    print(f"Extended pathways table saved: {output_file}")
    print(f"  Original rows: {len(pathways_df)}, Extended rows: {len(combined_pathways)}")
    print(f"  Added {len(combined_pathways) - len(pathways_df)} new pathways")


if __name__ == "__main__":
    # Example usage
    create_extended_pathways_table("data/txt/sheet/PFAS_Data_for_AI_pathways.tsv")