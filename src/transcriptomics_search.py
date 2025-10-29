"""Transcriptomics search functions for extending PFAS bioprocessing RNA-seq datasets.

This module searches NCBI SRA, GEO, and ArrayExpress for transcriptomics experiments
related to organisms in the taxa_and_genomes table.
"""

import time
from typing import Dict, List, Optional
import pandas as pd
import requests
from pathlib import Path
from Bio import Entrez
import xml.etree.ElementTree as ET

# Configure Entrez
Entrez.email = "your.email@example.com"  # Should be configured


def load_target_organisms(genomes_file: str = "data/txt/sheet/PFAS_Data_for_AI_taxa_and_genomes_extended.tsv") -> List[str]:
    """Load organism names from the genomes table for targeted searching.

    Args:
        genomes_file: Path to the taxa and genomes TSV file

    Returns:
        List of unique organism names (genus + species)
    """
    try:
        genomes_df = pd.read_csv(genomes_file, sep='\t')

        # Extract organism names from "Scientific name" column
        organisms = genomes_df['Scientific name'].dropna().unique().tolist()

        # Clean up organism names (remove strain info, keep genus + species)
        cleaned_organisms = set()
        for org in organisms:
            if isinstance(org, str) and org.strip():
                # Take first two words (genus + species)
                parts = org.split()
                if len(parts) >= 2:
                    cleaned_organisms.add(f"{parts[0]} {parts[1]}")
                elif len(parts) == 1:
                    cleaned_organisms.add(parts[0])

        return sorted(list(cleaned_organisms))

    except Exception as e:
        print(f"Error loading organisms from {genomes_file}: {e}")
        # Fallback to common methylotrophs
        return [
            "Methylobacterium aquaticum",
            "Methylobacterium extorquens",
            "Methylorubrum extorquens",
            "Paracoccus denitrificans"
        ]


def search_ncbi_sra_transcriptomics(organisms: List[str]) -> List[Dict]:
    """Search NCBI SRA for transcriptomics datasets from target organisms.

    Args:
        organisms: List of organism names to search for

    Returns:
        List of SRA transcriptomics records with metadata
    """
    transcriptomics_data = []

    print(f"Searching NCBI SRA for {len(organisms)} organisms...")

    for organism in organisms[:20]:  # Limit to avoid excessive API calls
        try:
            # Search SRA for RNA-seq experiments
            search_term = f'{organism}[Organism] AND biomol_rna[Properties] AND "rna seq"[Strategy]'

            handle = Entrez.esearch(
                db="sra",
                term=search_term,
                retmax=10,
                sort="relevance"
            )
            search_results = Entrez.read(handle)
            handle.close()

            if not search_results["IdList"]:
                continue

            print(f"  Found {len(search_results['IdList'])} SRA experiments for {organism}")

            # Fetch details for top results
            handle = Entrez.efetch(
                db="sra",
                id=",".join(search_results["IdList"][:5]),
                rettype="xml"
            )
            xml_data = handle.read()
            handle.close()

            # Parse XML
            root = ET.fromstring(xml_data)

            for exp_package in root.findall(".//EXPERIMENT_PACKAGE"):
                try:
                    # Extract experiment metadata
                    exp = exp_package.find(".//EXPERIMENT")
                    study = exp_package.find(".//STUDY")
                    sample = exp_package.find(".//SAMPLE")
                    run = exp_package.find(".//RUN")

                    if exp is None:
                        continue

                    experiment_id = exp.get("accession", "")
                    study_id = study.get("accession", "") if study is not None else ""
                    sample_id = sample.get("accession", "") if sample is not None else ""

                    # Extract organism name
                    organism_name = organism
                    if sample is not None:
                        sci_name = sample.find(".//SCIENTIFIC_NAME")
                        if sci_name is not None and sci_name.text:
                            organism_name = sci_name.text

                    # Extract project title
                    project_title = ""
                    if study is not None:
                        study_title = study.find(".//STUDY_TITLE")
                        if study_title is not None and study_title.text:
                            project_title = study_title.text

                    # Extract sample description
                    sample_description = ""
                    if sample is not None:
                        sample_title = sample.find(".//TITLE")
                        if sample_title is not None and sample_title.text:
                            sample_description = sample_title.text

                    # Extract platform and library strategy
                    platform = ""
                    if exp is not None:
                        platform_elem = exp.find(".//PLATFORM")
                        if platform_elem is not None:
                            # Get the actual sequencer type (ILLUMINA, etc.)
                            for child in platform_elem:
                                platform = child.tag
                                break

                    library_strategy = exp.find(".//LIBRARY_STRATEGY")
                    data_type = library_strategy.text if library_strategy is not None else "RNA-Seq"

                    # Build download URL (FTP link to FASTQ)
                    download_url = ""
                    if run is not None:
                        run_acc = run.get("accession", "")
                        if run_acc:
                            # SRA FTP pattern: ftp://ftp.sra.ebi.ac.uk/vol1/fastq/{SRR first 6}/{SRR full}/{SRR full}.fastq.gz
                            download_url = f"ftp://ftp.sra.ebi.ac.uk/vol1/fastq/{run_acc[:6]}/{run_acc}/{run_acc}.fastq.gz"

                    # Extract size info if available
                    size = ""
                    if run is not None:
                        total_spots = run.get("total_spots", "")
                        if total_spots:
                            size = f"{total_spots} spots"

                    transcriptomics_data.append({
                        "experiment_id": experiment_id,
                        "study_id": study_id,
                        "sample_id": sample_id,
                        "organism": organism_name,
                        "project_title": project_title,
                        "sample_description": sample_description,
                        "condition": "",  # Not easily extractable from SRA XML
                        "data_type": data_type,
                        "sra_accession": experiment_id,
                        "geo_accession": "",
                        "arrayexpress_accession": "",
                        "size": size,
                        "publication": "",
                        "license": "SRA Public",
                        "download_url": download_url,
                        "source": "extend1"
                    })

                except Exception as e:
                    print(f"    Error parsing experiment: {e}")
                    continue

            # Rate limiting
            time.sleep(1.0)

        except Exception as e:
            print(f"  Error searching SRA for {organism}: {e}")
            time.sleep(1.0)
            continue

    return transcriptomics_data


def search_geo_transcriptomics(organisms: List[str]) -> List[Dict]:
    """Search NCBI GEO for gene expression datasets from target organisms.

    Args:
        organisms: List of organism names to search for

    Returns:
        List of GEO dataset records with metadata
    """
    transcriptomics_data = []

    print(f"Searching NCBI GEO for {len(organisms)} organisms...")

    for organism in organisms[:20]:  # Limit to avoid excessive API calls
        try:
            # Search GEO DataSets
            search_term = f'{organism}[Organism] AND "expression profiling by high throughput sequencing"[DataSet Type]'

            handle = Entrez.esearch(
                db="gds",
                term=search_term,
                retmax=5,
                sort="relevance"
            )
            search_results = Entrez.read(handle)
            handle.close()

            if not search_results["IdList"]:
                continue

            print(f"  Found {len(search_results['IdList'])} GEO datasets for {organism}")

            # Fetch details
            handle = Entrez.esummary(
                db="gds",
                id=",".join(search_results["IdList"])
            )
            summaries = Entrez.read(handle)
            handle.close()

            for summary in summaries:
                try:
                    accession = summary.get("Accession", "")
                    title = summary.get("title", "")
                    organism_name = summary.get("taxon", organism)
                    summary_text = summary.get("summary", "")

                    # GEO datasets link to SRA
                    sra_info = summary.get("ExtRelations", [])
                    sra_accession = ""
                    for rel in sra_info:
                        if rel.get("RelationType") == "SRA":
                            sra_accession = rel.get("TargetObject", "")
                            break

                    # Build GEO download URL
                    download_url = f"https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc={accession}"

                    transcriptomics_data.append({
                        "experiment_id": accession,
                        "study_id": accession,
                        "sample_id": "",
                        "organism": organism_name,
                        "project_title": title,
                        "sample_description": summary_text[:200],  # Truncate to 200 chars
                        "condition": "",
                        "data_type": "RNA-Seq",
                        "sra_accession": sra_accession,
                        "geo_accession": accession,
                        "arrayexpress_accession": "",
                        "size": "",
                        "publication": "",
                        "license": "GEO Public",
                        "download_url": download_url,
                        "source": "extend1"
                    })

                except Exception as e:
                    print(f"    Error parsing GEO record: {e}")
                    continue

            # Rate limiting
            time.sleep(1.0)

        except Exception as e:
            print(f"  Error searching GEO for {organism}: {e}")
            time.sleep(1.0)
            continue

    return transcriptomics_data


def search_arrayexpress_transcriptomics(organisms: List[str]) -> List[Dict]:
    """Search ArrayExpress for transcriptomics datasets from target organisms.

    Args:
        organisms: List of organism names to search for

    Returns:
        List of ArrayExpress dataset records with metadata
    """
    transcriptomics_data = []

    print(f"Searching ArrayExpress for {len(organisms)} organisms...")

    # ArrayExpress REST API endpoint
    base_url = "https://www.ebi.ac.uk/arrayexpress/json/v3/experiments"

    for organism in organisms[:10]:  # Limit to avoid excessive API calls
        try:
            # Search ArrayExpress
            params = {
                "keywords": organism,
                "exptype[]": "rna-seq",
                "pagesize": 5,
                "sortby": "releasedate",
                "sortorder": "descending"
            }

            response = requests.get(base_url, params=params, timeout=30)
            response.raise_for_status()

            data = response.json()
            experiments = data.get("experiments", {}).get("experiment", [])

            if not experiments:
                continue

            print(f"  Found {len(experiments)} ArrayExpress experiments for {organism}")

            for exp in experiments:
                try:
                    accession = exp.get("accession", "")
                    title = exp.get("name", "")
                    organism_name = exp.get("organism", [organism])[0] if exp.get("organism") else organism
                    description = exp.get("description", [{"text": ""}])[0].get("text", "")

                    # Extract sample count
                    sample_count = exp.get("samples", 0)
                    size = f"{sample_count} samples" if sample_count else ""

                    # Build download URL
                    download_url = f"https://www.ebi.ac.uk/arrayexpress/experiments/{accession}/files/"

                    transcriptomics_data.append({
                        "experiment_id": accession,
                        "study_id": accession,
                        "sample_id": "",
                        "organism": organism_name,
                        "project_title": title,
                        "sample_description": description[:200],  # Truncate
                        "condition": "",
                        "data_type": "RNA-Seq",
                        "sra_accession": "",
                        "geo_accession": "",
                        "arrayexpress_accession": accession,
                        "size": size,
                        "publication": "",
                        "license": "Public",
                        "download_url": download_url,
                        "source": "extend1"
                    })

                except Exception as e:
                    print(f"    Error parsing ArrayExpress record: {e}")
                    continue

            # Rate limiting
            time.sleep(1.0)

        except Exception as e:
            print(f"  Error searching ArrayExpress for {organism}: {e}")
            time.sleep(1.0)
            continue

    return transcriptomics_data


def create_extended_transcriptomics_table(
    input_file: str,
    output_dir: str = "data/txt/sheet"
) -> None:
    """Create extended transcriptomics table by searching SRA, GEO, and ArrayExpress.

    Args:
        input_file: Path to existing transcriptomics TSV file
        output_dir: Directory to save extended table
    """
    print("=" * 80)
    print("TRANSCRIPTOMICS DATA EXTENSION")
    print("=" * 80)
    print()

    # Load target organisms from genomes table
    print("Loading target organisms from genomes table...")
    organisms = load_target_organisms()
    print(f"  Found {len(organisms)} unique organisms to search for")
    print()

    # Read existing transcriptomics data
    print(f"Reading existing transcriptomics data from {input_file}...")
    transcriptomics_df = pd.read_csv(input_file, sep='\t')
    print(f"  Existing records: {len(transcriptomics_df)}")
    print()

    # Add source column if missing
    if "Source" not in transcriptomics_df.columns:
        transcriptomics_df["Source"] = ""

    # Collect from different sources
    all_new_data = []

    # Search SRA
    print("Step 1: Searching NCBI SRA...")
    print("-" * 80)
    sra_data = search_ncbi_sra_transcriptomics(organisms)
    all_new_data.extend(sra_data)
    print(f"  SRA: Found {len(sra_data)} experiments")
    print()

    # Search GEO
    print("Step 2: Searching NCBI GEO...")
    print("-" * 80)
    geo_data = search_geo_transcriptomics(organisms)
    all_new_data.extend(geo_data)
    print(f"  GEO: Found {len(geo_data)} datasets")
    print()

    # Search ArrayExpress
    print("Step 3: Searching ArrayExpress...")
    print("-" * 80)
    ae_data = search_arrayexpress_transcriptomics(organisms)
    all_new_data.extend(ae_data)
    print(f"  ArrayExpress: Found {len(ae_data)} experiments")
    print()

    print("=" * 80)
    print(f"Total new records found: {len(all_new_data)}")
    print("=" * 80)
    print()

    if not all_new_data:
        print("No new transcriptomics data found.")
        return

    # Convert to DataFrame
    new_data_df = pd.DataFrame([
        {
            "Experiment ID": exp["experiment_id"],
            "Study ID": exp["study_id"],
            "Sample ID": exp["sample_id"],
            "Organism": exp["organism"],
            "Project Title": exp["project_title"],
            "Sample Description": exp["sample_description"],
            "Condition": exp["condition"],
            "Data Type": exp["data_type"],
            "SRA Accession": exp["sra_accession"],
            "GEO Accession": exp["geo_accession"],
            "ArrayExpress Accession": exp["arrayexpress_accession"],
            "Size": exp["size"],
            "Publication": exp["publication"],
            "License": exp["license"],
            "Download URL": exp["download_url"],
            "Source": exp["source"]
        }
        for exp in all_new_data
    ])

    # Combine with existing
    combined_df = pd.concat([transcriptomics_df, new_data_df], ignore_index=True)

    # Deduplicate by Experiment ID
    print("Deduplicating by Experiment ID...")
    combined_df = combined_df.drop_duplicates(subset=["Experiment ID"], keep="first")

    # Save
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    output_file = output_dir / "PFAS_Data_for_AI_transcriptomics_extended.tsv"
    combined_df.to_csv(output_file, sep='\t', index=False)

    print()
    print("=" * 80)
    print("EXTENSION COMPLETE")
    print("=" * 80)
    print(f"  Output file: {output_file}")
    print(f"  Original records: {len(transcriptomics_df)}")
    print(f"  Extended records: {len(combined_df)}")
    print(f"  New records added: {len(combined_df) - len(transcriptomics_df)}")
    print()
    print("Breakdown by source:")
    print(f"  SRA: {len(sra_data)}")
    print(f"  GEO: {len(geo_data)}")
    print(f"  ArrayExpress: {len(ae_data)}")
    print("=" * 80)


if __name__ == "__main__":
    """Run transcriptomics search when executed directly."""
    create_extended_transcriptomics_table(
        "data/txt/sheet/PFAS_Data_for_AI_transcriptomics.tsv"
    )
