"""NCBI search functions for finding bacteria and archaea relevant to lanthanide bioprocessing."""

import time
from typing import Dict, List, Optional, Set, Tuple
import requests
import pandas as pd
from Bio import Entrez
import xml.etree.ElementTree as ET
from pathlib import Path
import re


# Configure Entrez with email (required by NCBI)
Entrez.email = "your.email@example.com"  # Should be configured by user


def get_biosample_download_url(sample_id: str) -> str:
    """Generate download URL for biosample data.
    
    Args:
        sample_id: NCBI BioSample accession (e.g., SAMN44800722)
        
    Returns:
        Download URL for biosample SRA data or metadata
        
    Examples:
        >>> url = get_biosample_download_url("SAMN44800722")
        >>> "ncbi.nlm.nih.gov" in url
        True
    """
    if not sample_id or not sample_id.startswith('SAM'):
        return ""
    
    # NCBI BioSample data can be linked to SRA runs
    # Primary URL is the BioSample page with links to associated data
    biosample_url = f"https://www.ncbi.nlm.nih.gov/biosample/{sample_id}"
    
    return biosample_url


def get_annotation_download_url(assembly_accession: str, assembly_name: str = "") -> str:
    """Generate download URL for genome annotations.
    
    Args:
        assembly_accession: GenBank/RefSeq assembly accession (e.g., GCF_000333655.1)
        assembly_name: Assembly name for constructing full filename
        
    Returns:
        Direct download URL for GFF3 annotation file
        
    Examples:
        >>> url = get_annotation_download_url("GCF_000333655.1")
        >>> "ftp.ncbi.nlm.nih.gov" in url
        True
    """
    if not assembly_accession:
        return ""
    
    # Handle both GCF and GCA accessions
    if not (assembly_accession.startswith('GCF_') or assembly_accession.startswith('GCA_')):
        return ""
    
    # NCBI FTP structure: ftp://ftp.ncbi.nlm.nih.gov/genomes/all/GCF/000/333/655/GCF_000333655.1_ASM33365v1/
    parts = assembly_accession.split('_')
    if len(parts) < 2:
        return ""
    
    prefix = parts[0]  # GCF or GCA
    accession_number = parts[1].split('.')[0]  # Remove version for directory structure: 000333655
    
    # Pad accession number to ensure it's at least 9 digits
    accession_number = accession_number.zfill(9)
    
    # Split into groups of 3 digits: 000/333/655
    path_parts = [accession_number[i:i+3] for i in range(0, len(accession_number), 3)]
    
    # Construct FTP path
    ftp_base = f"ftp://ftp.ncbi.nlm.nih.gov/genomes/all/{prefix}/{'/'.join(path_parts)}"
    
    # For the filename, we need the full accession with assembly name
    # Format: GCF_000333655.1_ASM33365v1_genomic.gff.gz
    # Since we might not have the exact assembly name, we'll provide the directory URL
    # and let users find the specific *_genomic.gff.gz file
    
    return f"{ftp_base}/{assembly_accession}_*/{assembly_accession}_*_genomic.gff.gz"


def search_ncbi_assembly(
    query: str, 
    retmax: int = 100,
    domain_filter: Optional[str] = None
) -> List[Dict]:
    """Search NCBI Assembly database for genomes.
    
    Args:
        query: Search query string
        retmax: Maximum number of results to return
        domain_filter: Filter by domain (bacteria, archaea, etc.)
        
    Returns:
        List of assembly records with metadata
        
    Examples:
        >>> # Search for lanthanide-related bacteria
        >>> results = search_ncbi_assembly("lanthanide bacteria", retmax=10)  # doctest: +SKIP
        >>> len(results) > 0  # doctest: +SKIP
        True
    """
    try:
        # Build search query
        search_query = query
        if domain_filter:
            search_query += f" AND {domain_filter}[Organism]"
            
        # Search assembly database
        handle = Entrez.esearch(
            db="assembly",
            term=search_query,
            retmax=retmax,
            sort="relevance"
        )
        search_results = Entrez.read(handle)
        handle.close()
        
        if not search_results["IdList"]:
            return []
            
        # Fetch detailed records
        handle = Entrez.esummary(
            db="assembly",
            id=",".join(search_results["IdList"])
        )
        summaries = Entrez.read(handle)
        handle.close()
        
        assemblies = []
        for summary in summaries["DocumentSummarySet"]["DocumentSummary"]:
            assembly_id = summary.get("AssemblyAccession", "")
            assemblies.append({
                "assembly_id": assembly_id,
                "organism": summary.get("SpeciesName", ""),
                "strain": summary.get("Biosource", {}).get("InfraspeciesList", [{}])[0].get("Sub_value", "") if summary.get("Biosource", {}).get("InfraspeciesList") else "",
                "taxid": summary.get("SpeciesTaxid", ""),
                "assembly_level": summary.get("AssemblyLevel", ""),
                "genome_size": summary.get("TotalSequenceLength", ""),
                "contigs": summary.get("ContigN50", ""),
                "submission_date": summary.get("SubmissionDate", ""),
                "sequencing_tech": summary.get("SequencingTechnology", ""),
                "coverage": summary.get("Coverage", ""),
                "annotation_url": get_annotation_download_url(assembly_id)
            })
            
        return assemblies
        
    except Exception as e:
        print(f"Error searching NCBI Assembly: {e}")
        return []


def search_ncbi_biosample(
    query: str, 
    retmax: int = 100,
    organism_filter: Optional[str] = None
) -> List[Dict]:
    """Search NCBI BioSample database for samples.
    
    Args:
        query: Search query string
        retmax: Maximum number of results to return
        organism_filter: Filter by organism name
        
    Returns:
        List of biosample records with metadata
        
    Examples:
        >>> # Search for lanthanide-related biosamples
        >>> results = search_ncbi_biosample("lanthanide", retmax=10)  # doctest: +SKIP
        >>> len(results) >= 0  # doctest: +SKIP
        True
    """
    try:
        # Build search query
        search_query = query
        if organism_filter:
            search_query += f" AND {organism_filter}[Organism]"
            
        # Search biosample database
        handle = Entrez.esearch(
            db="biosample",
            term=search_query,
            retmax=retmax,
            sort="relevance"
        )
        search_results = Entrez.read(handle)
        handle.close()
        
        if not search_results["IdList"]:
            return []
            
        # Fetch detailed records
        handle = Entrez.efetch(
            db="biosample",
            id=",".join(search_results["IdList"]),
            rettype="xml"
        )
        xml_data = handle.read()
        handle.close()
        
        # Parse XML
        root = ET.fromstring(xml_data)
        
        biosamples = []
        for biosample in root.findall(".//BioSample"):
            sample_id = biosample.get("accession", "")
            
            # Extract organism
            organism_elem = biosample.find(".//Organism")
            organism = organism_elem.get("taxonomy_name", "") if organism_elem is not None else ""
            
            # Extract sample name/title
            title_elem = biosample.find(".//Title")
            title = title_elem.text if title_elem is not None else ""
            
            # Extract attributes
            attributes = {}
            for attr in biosample.findall(".//Attribute"):
                attr_name = attr.get("attribute_name", "")
                attr_value = attr.text or ""
                attributes[attr_name] = attr_value
            
            biosamples.append({
                "sample_id": sample_id,
                "sample_name": title,
                "organism": organism,
                "isolation_source": attributes.get("isolation_source", ""),
                "geo_loc_name": attributes.get("geo_loc_name", ""),
                "collection_date": attributes.get("collection_date", ""),
                "host": attributes.get("host", ""),
                "env_broad_scale": attributes.get("env_broad_scale", ""),
                "env_local_scale": attributes.get("env_local_scale", ""),
                "env_medium": attributes.get("env_medium", ""),
                "temp": attributes.get("temp", ""),
                "ph": attributes.get("ph", ""),
                "attributes": attributes,
                "download_url": get_biosample_download_url(sample_id)
            })
            
        return biosamples
        
    except Exception as e:
        print(f"Error searching NCBI BioSample: {e}")
        return []


def search_lanthanide_organisms() -> Tuple[List[Dict], List[Dict]]:
    """Search for bacteria and archaea relevant to lanthanide bioprocessing.
    
    Returns:
        Tuple of (assembly_results, biosample_results)
    """
    # Lanthanide-related search terms
    lanthanide_terms = [
        "lanthanide",
        "cerium", "lanthanum", "praseodymium", "neodymium",
        "europium", "gadolinium", "terbium", "dysprosium",
        "rare earth element", "REE",
        "methylotroph lanthanide", "XoxF", "MDH",
        "methanol dehydrogenase lanthanide"
    ]
    
    # Organism groups known for lanthanide use
    lanthanide_organisms = [
        "Methylobacterium", "Methylorubrum", "Methylosinus",
        "Paracoccus", "Pseudomonas", "Bradyrhizobium",
        "Methylocystis", "Methylomicrobium"
    ]
    
    all_assemblies = []
    all_biosamples = []
    
    print("Searching for lanthanide-related organisms...")
    
    # Search with lanthanide terms
    for term in lanthanide_terms[:3]:  # Limit to avoid rate limiting
        print(f"  Searching assemblies for: {term}")
        assemblies = search_ncbi_assembly(
            f"{term} AND (bacteria[Filter] OR archaea[Filter])", 
            retmax=50
        )
        all_assemblies.extend(assemblies)
        time.sleep(0.5)  # Rate limiting
        
        print(f"  Searching biosamples for: {term}")
        biosamples = search_ncbi_biosample(term, retmax=50)
        all_biosamples.extend(biosamples)
        time.sleep(0.5)  # Rate limiting
    
    # Search known lanthanide-using organisms
    for organism in lanthanide_organisms[:4]:  # Limit to avoid rate limiting
        print(f"  Searching assemblies for organism: {organism}")
        assemblies = search_ncbi_assembly(
            f"{organism} AND (bacteria[Filter] OR archaea[Filter])", 
            retmax=30
        )
        all_assemblies.extend(assemblies)
        time.sleep(0.5)  # Rate limiting
    
    # Remove duplicates
    seen_assembly_ids = set()
    unique_assemblies = []
    for assembly in all_assemblies:
        if assembly["assembly_id"] and assembly["assembly_id"] not in seen_assembly_ids:
            seen_assembly_ids.add(assembly["assembly_id"])
            unique_assemblies.append(assembly)
    
    seen_sample_ids = set()
    unique_biosamples = []
    for sample in all_biosamples:
        if sample["sample_id"] and sample["sample_id"] not in seen_sample_ids:
            seen_sample_ids.add(sample["sample_id"])
            unique_biosamples.append(sample)
    
    print(f"Found {len(unique_assemblies)} unique assemblies and {len(unique_biosamples)} unique biosamples")
    
    return unique_assemblies, unique_biosamples


def enhance_existing_data(existing_df: pd.DataFrame, data_type: str = "genome") -> pd.DataFrame:
    """Enhance existing data by filling missing information from NCBI.
    
    Args:
        existing_df: DataFrame with existing data
        data_type: Type of data ("genome" or "biosample")
        
    Returns:
        Enhanced DataFrame with filled information
    """
    enhanced_df = existing_df.copy()
    
    if data_type == "genome":
        # Add annotation URL column if it doesn't exist
        if "Annotation download URL" not in enhanced_df.columns:
            enhanced_df["Annotation download URL"] = ""
        
        # Fill missing genome identifiers, taxon IDs, and annotation URLs
        for idx, row in enhanced_df.iterrows():
            genome_id = row.get("Genome identifier (GenBank, IMG etc)", "")
            
            # Add annotation URL for existing genome IDs
            if genome_id and pd.isna(row.get("Annotation download URL", "")):
                enhanced_df.at[idx, "Annotation download URL"] = get_annotation_download_url(str(genome_id))
            
            # Search for missing information
            if pd.isna(genome_id) or pd.isna(row.get("NCBITaxon id", "")):
                organism = row.get("Scientific name", "")
                if organism:
                    print(f"  Searching for genome info for: {organism}")
                    assemblies = search_ncbi_assembly(f'"{organism}"', retmax=5)
                    if assemblies:
                        best_match = assemblies[0]  # Take first/best match
                        if pd.isna(genome_id):
                            enhanced_df.at[idx, "Genome identifier (GenBank, IMG etc)"] = best_match["assembly_id"]
                            enhanced_df.at[idx, "Annotation download URL"] = best_match["annotation_url"]
                        if pd.isna(row.get("NCBITaxon id", "")):
                            enhanced_df.at[idx, "NCBITaxon id"] = best_match["taxid"]
                    time.sleep(0.5)  # Rate limiting
    
    elif data_type == "biosample":
        # Add download URL column if it doesn't exist
        if "Download URL" not in enhanced_df.columns:
            enhanced_df["Download URL"] = ""
        
        # Fill download URLs for existing sample IDs
        for idx, row in enhanced_df.iterrows():
            sample_id = row.get("Sample ID", "")
            
            # Add download URL for existing sample IDs
            if sample_id and pd.isna(row.get("Download URL", "")):
                enhanced_df.at[idx, "Download URL"] = get_biosample_download_url(str(sample_id))
    
    return enhanced_df


def create_extended_tables(
    existing_genomes_path: str,
    existing_biosamples_path: str,
    output_dir: str = "data/txt/sheet"
) -> None:
    """Create extended tables with lanthanide-relevant organisms.
    
    Args:
        existing_genomes_path: Path to existing genomes TSV
        existing_biosamples_path: Path to existing biosamples TSV
        output_dir: Directory to save extended tables
    """
    print("Reading existing data...")
    genomes_df = pd.read_csv(existing_genomes_path, sep='\t')
    biosamples_df = pd.read_csv(existing_biosamples_path, sep='\t')
    
    print("Enhancing existing data...")
    enhanced_genomes = enhance_existing_data(genomes_df, "genome")
    enhanced_biosamples = enhance_existing_data(biosamples_df, "biosample")
    
    print("Searching for new lanthanide-related organisms...")
    new_assemblies, new_biosamples = search_lanthanide_organisms()
    
    # Convert new assemblies to DataFrame matching existing structure
    if new_assemblies:
        new_genomes_df = pd.DataFrame([
            {
                "Scientific name": assembly["organism"],
                "NCBITaxon id": assembly["taxid"],
                "Genome identifier (GenBank, IMG etc)": assembly["assembly_id"],
                "Annotation download URL": assembly["annotation_url"]
            }
            for assembly in new_assemblies
        ])
        
        # Combine with existing data
        combined_genomes = pd.concat([enhanced_genomes, new_genomes_df], ignore_index=True)
        # Remove duplicates based on organism name
        combined_genomes = combined_genomes.drop_duplicates(subset=["Scientific name"], keep="first")
    else:
        combined_genomes = enhanced_genomes
    
    # Convert new biosamples to DataFrame matching existing structure
    if new_biosamples:
        new_biosamples_df = pd.DataFrame([
            {
                "Sample Name": sample["sample_name"][:50] if sample["sample_name"] else sample["sample_id"],  # Truncate long names
                "Sample ID": sample["sample_id"],
                "Organism": sample["organism"],
                "Download URL": sample.get("download_url", "")
            }
            for sample in new_biosamples
        ])
        
        # Combine with existing data
        combined_biosamples = pd.concat([enhanced_biosamples, new_biosamples_df], ignore_index=True)
        # Remove duplicates based on sample ID
        combined_biosamples = combined_biosamples.drop_duplicates(subset=["Sample ID"], keep="first")
    else:
        combined_biosamples = enhanced_biosamples
    
    # Save extended tables
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    
    genomes_output = output_dir / "BER_CMM_Data_for_AI_taxa_and_genomes_extended.tsv"
    biosamples_output = output_dir / "BER_CMM_Data_for_AI_biosamples_extended.tsv"
    
    combined_genomes.to_csv(genomes_output, sep='\t', index=False)
    combined_biosamples.to_csv(biosamples_output, sep='\t', index=False)
    
    print(f"Extended genomes table saved: {genomes_output}")
    print(f"  Original rows: {len(genomes_df)}, Extended rows: {len(combined_genomes)}")
    print(f"Extended biosamples table saved: {biosamples_output}")
    print(f"  Original rows: {len(biosamples_df)}, Extended rows: {len(combined_biosamples)}")


if __name__ == "__main__":
    # Example usage
    create_extended_tables(
        "data/txt/sheet/BER_CMM_Data_for_AI_taxa_and_genomes.tsv",
        "data/txt/sheet/BER_CMM_Data_for_AI_biosamples.tsv"
    )