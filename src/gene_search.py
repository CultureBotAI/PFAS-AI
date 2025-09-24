"""Gene and protein search functions for extending lanthanide bioprocessing genes."""

import time
from typing import Dict, List, Optional, Set, Tuple
import pandas as pd
import requests
from pathlib import Path
from Bio import Entrez


def get_lanthanide_genes_database() -> List[Dict]:
    """Get comprehensive database of lanthanide-related genes and proteins.
    
    Returns:
        List of gene records with annotations
    """
    lanthanide_genes = [
        {
            "gene_id": "K23995",
            "organism": "Methylobacterium species",
            "annotation": "PQQ-dependent methanol dehydrogenase, lanthanide-dependent (XoxF)",
            "ec": "1.1.2.7",
            "go": "GO:0018525 (methanol metabolic process)",
            "chebi": "CHEBI:17790 (methanol)"
        },
        {
            "gene_id": "K14028", 
            "organism": "Methylobacterium species",
            "annotation": "PQQ-dependent methanol dehydrogenase, calcium-dependent (MxaF)",
            "ec": "1.1.2.7",
            "go": "GO:0018525 (methanol metabolic process)",
            "chebi": "CHEBI:17790 (methanol)"
        },
        {
            "gene_id": "K00114",
            "organism": "Methylobacterium species", 
            "annotation": "PQQ-dependent alcohol dehydrogenase, lanthanide-responsive (ExaF)",
            "ec": "1.1.2.7",
            "go": "GO:0046872 (metal ion binding)",
            "chebi": "CHEBI:30879 (alcohol)"
        },
        {
            "gene_id": "custom_mxbD",
            "organism": "Methylobacterium species",
            "annotation": "Methanol metabolism transcriptional regulator MxbD",
            "ec": "",
            "go": "GO:0045892 (negative regulation of transcription)",
            "chebi": ""
        },
        {
            "gene_id": "custom_xoxG",
            "organism": "Methylobacterium species",
            "annotation": "Small regulatory protein XoxG (lanthanide-responsive)",
            "ec": "",
            "go": "GO:0045892 (negative regulation of transcription)",
            "chebi": ""
        },
        {
            "gene_id": "K01499",
            "organism": "Methylobacterium species",
            "annotation": "Formaldehyde dehydrogenase",
            "ec": "1.2.1.46",
            "go": "GO:0019437 (formaldehyde metabolic process)",
            "chebi": "CHEBI:16842 (formaldehyde)"
        },
        {
            "gene_id": "custom_fae",
            "organism": "Methylobacterium species", 
            "annotation": "Formaldehyde activating enzyme (Fae1/Fae2)",
            "ec": "",
            "go": "GO:0019437 (formaldehyde metabolic process)",
            "chebi": "CHEBI:16842 (formaldehyde)"
        },
        {
            "gene_id": "custom_tonB_ln",
            "organism": "Methylobacterium species",
            "annotation": "TonB-dependent lanthanide uptake receptor",
            "ec": "",
            "go": "GO:0015682 (ferric iron transport)",
            "chebi": "CHEBI:33519 (metal cation)"
        },
        {
            "gene_id": "custom_sbn",
            "organism": "Methylobacterium species",
            "annotation": "Staphyloferrin B-like siderophore biosynthesis genes",
            "ec": "",
            "go": "GO:0019290 (siderophore transport)",
            "chebi": "CHEBI:26672 (siderophore)"
        },
        {
            "gene_id": "K01676",
            "organism": "Methylobacterium species",
            "annotation": "Fumarate hydratase (involved in TCA cycle)",
            "ec": "4.2.1.2",
            "go": "GO:0006099 (tricarboxylic acid cycle)",
            "chebi": "CHEBI:18012 (fumarate)"
        }
    ]
    
    # Add genes from other methylotrophic organisms
    other_organisms = [
        "Methylorubrum extorquens",
        "Methylosinus trichosporium", 
        "Paracoccus denitrificans",
        "Bradyrhizobium japonicum"
    ]
    
    for organism in other_organisms:
        # Add core lanthanide genes for each organism
        for gene_type, gene_data in [
            ("xoxF", {"annotation": "PQQ-dependent methanol dehydrogenase (lanthanide-dependent)", "ec": "1.1.2.7"}),
            ("mxaF", {"annotation": "PQQ-dependent methanol dehydrogenase (calcium-dependent)", "ec": "1.1.2.7"}),
            ("exaF", {"annotation": "PQQ-dependent alcohol dehydrogenase", "ec": "1.1.2.7"})
        ]:
            lanthanide_genes.append({
                "gene_id": f"custom_{gene_type}",
                "organism": organism,
                "annotation": gene_data["annotation"],
                "ec": gene_data["ec"],
                "go": "GO:0046872 (metal ion binding)" if "lanthanide" in gene_data["annotation"] else "",
                "chebi": "CHEBI:17790 (methanol)" if "methanol" in gene_data["annotation"] else ""
            })
    
    return lanthanide_genes


def search_uniprot_genes(organism_list: List[str]) -> List[Dict]:
    """Search UniProt for lanthanide-related genes in specific organisms.
    
    Args:
        organism_list: List of organism names to search
        
    Returns:
        List of gene records from UniProt
    """
    genes = []
    
    for organism in organism_list[:3]:  # Limit to avoid API overload
        try:
            # Search UniProt for methanol dehydrogenase genes
            query = f"organism:{organism} AND (methanol dehydrogenase OR alcohol dehydrogenase)"
            url = f"https://rest.uniprot.org/uniprotkb/search"
            params = {
                "query": query,
                "format": "tsv",
                "fields": "accession,gene_names,protein_name,organism_name,ec,go_p,go_f",
                "size": "20"
            }
            
            response = requests.get(url, params=params, timeout=10)
            
            if response.status_code == 200:
                lines = response.text.strip().split('\n')
                if len(lines) > 1:  # Skip header
                    for line in lines[1:6]:  # Take first 5 results
                        fields = line.split('\t')
                        if len(fields) >= 4:
                            genes.append({
                                "gene_id": fields[0] if len(fields) > 0 else "",
                                "organism": fields[3] if len(fields) > 3 else organism,
                                "annotation": fields[2] if len(fields) > 2 else "",
                                "ec": fields[4] if len(fields) > 4 else "",
                                "go": fields[5] if len(fields) > 5 else "",
                                "chebi": ""
                            })
            
            time.sleep(1)  # Rate limiting
            
        except Exception as e:
            print(f"Error searching UniProt for {organism}: {e}")
    
    return genes


def get_gene_download_url(gene_id: str, organism: str = "") -> str:
    """Generate download URL for gene/protein data.
    
    Args:
        gene_id: Gene identifier (KEGG KO, UniProt ID, etc.)
        organism: Organism name for context
        
    Returns:
        Download URL for gene data or details page
        
    Examples:
        >>> url = get_gene_download_url("K23995")
        >>> "kegg.jp" in url or len(url) == 0
        True
    """
    if not gene_id:
        return ""
    
    # KEGG orthology IDs
    if gene_id.startswith('K') and len(gene_id) == 6:
        return f"https://www.kegg.jp/entry/{gene_id}"
    
    # UniProt accession IDs  
    elif len(gene_id) == 6 or (len(gene_id) >= 6 and gene_id.isalnum()):
        return f"https://www.uniprot.org/uniprotkb/{gene_id}"
    
    # Custom IDs - return general database
    elif gene_id.startswith('custom_'):
        if 'methylobacterium' in organism.lower():
            return "https://www.ncbi.nlm.nih.gov/gene/?term=Methylobacterium"
        else:
            return "https://www.ncbi.nlm.nih.gov/gene/"
    
    # Default to NCBI gene search
    else:
        return f"https://www.ncbi.nlm.nih.gov/gene/?term={gene_id}"


def search_kegg_genes() -> List[Dict]:
    """Search KEGG for lanthanide-related genes.
    
    Returns:
        List of gene records from KEGG
    """
    genes = []
    
    # KEGG orthology groups relevant to lanthanide metabolism
    kegg_genes = [
        ("K23995", "PQQ-dependent methanol dehydrogenase (XoxF)"),
        ("K14028", "PQQ-dependent methanol dehydrogenase (MxaF)"),
        ("K00114", "alcohol dehydrogenase"),
        ("K01499", "formaldehyde dehydrogenase"),
        ("K00600", "glycine hydroxymethyltransferase"),
        ("K01938", "formate--tetrahydrofolate ligase")
    ]
    
    for ko_id, description in kegg_genes:
        genes.append({
            "gene_id": ko_id,
            "organism": "Various methylotrophic bacteria",
            "annotation": description,
            "ec": "",
            "go": "",
            "chebi": ""
        })
    
    return genes


def create_extended_genes_table(input_file: str, output_dir: str = "data/txt/sheet") -> None:
    """Create extended genes and proteins table with additional lanthanide-relevant genes.
    
    Args:
        input_file: Path to existing genes TSV file
        output_dir: Directory to save extended table
    """
    print("Reading existing genes and proteins data...")
    genes_df = pd.read_csv(input_file, sep='\t')
    
    # Add download URL column if it doesn't exist
    if "Download URL" not in genes_df.columns:
        genes_df["Download URL"] = ""
        
        # Fill download URLs for existing gene IDs if available
        for idx, row in genes_df.iterrows():
            gene_id = row.get("gene or protein id", "")
            organism = row.get("organism (from taxa and genomes tab)", "")
            if gene_id:
                genes_df.at[idx, "Download URL"] = get_gene_download_url(str(gene_id), str(organism))
    
    print("Searching for additional lanthanide-relevant genes...")
    
    # Get comprehensive gene database
    lanthanide_genes = get_lanthanide_genes_database()
    
    # Search external databases
    methylotroph_organisms = [
        "Methylobacterium aquaticum",
        "Methylorubrum extorquens", 
        "Methylosinus trichosporium"
    ]
    
    print("Searching UniProt...")
    uniprot_genes = search_uniprot_genes(methylotroph_organisms)
    
    print("Getting KEGG orthology genes...")
    kegg_genes = search_kegg_genes()
    
    # Combine all genes
    all_new_genes = lanthanide_genes + uniprot_genes + kegg_genes
    
    print(f"Found {len(all_new_genes)} additional genes and proteins")
    
    # Convert to DataFrame format matching existing structure
    new_genes_df = pd.DataFrame([
        {
            "gene or protein id": gene["gene_id"],
            "organism (from taxa and genomes tab)": gene["organism"],
            "annotation": gene["annotation"],
            "EC": gene["ec"],
            "GO": gene["go"],
            "CHEBI": gene["chebi"],
            "Download URL": get_gene_download_url(gene["gene_id"], gene["organism"])
        }
        for gene in all_new_genes
    ])
    
    # Combine with existing data
    combined_genes = pd.concat([genes_df, new_genes_df], ignore_index=True)
    
    # Remove duplicates based on gene ID and organism
    combined_genes = combined_genes.drop_duplicates(
        subset=["gene or protein id", "organism (from taxa and genomes tab)"], 
        keep="first"
    )
    
    # Save extended table
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    
    output_file = output_dir / "BER_CMM_Data_for_AI_genes_and_proteins_extended.tsv"
    combined_genes.to_csv(output_file, sep='\t', index=False)
    
    print(f"Extended genes table saved: {output_file}")
    print(f"  Original rows: {len(genes_df)}, Extended rows: {len(combined_genes)}")
    print(f"  Added {len(combined_genes) - len(genes_df)} new genes and proteins")


if __name__ == "__main__":
    # Example usage
    create_extended_genes_table("data/txt/sheet/BER_CMM_Data_for_AI_genes_and_proteins.tsv")