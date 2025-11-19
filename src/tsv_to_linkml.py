"""Convert extended TSV files to LinkML-compatible YAML format.

This script reads the extended TSV tables and converts them to LinkML database format
for validation against the PFAS bioprocessing schema.
"""

import argparse
import sys
from pathlib import Path
from typing import Optional

import pandas as pd
from linkml_runtime.dumpers import yaml_dumper

# Import generated LinkML models
try:
    from linkml_models import (
        PFASBioprocessingDatabase,
        GenomeRecord,
        BiosampleRecord,
        PathwayRecord,
        GeneProteinRecord,
        MacromolecularStructureRecord,
        PublicationRecord,
        DatasetRecord,
        ChemicalCompoundRecord,
        AssayMeasurementRecord,
        BioprocessConditionsRecord,
        ScreeningResultRecord,
        ProtocolRecord,
        StructureMethodEnum,
        DataTypeEnum,
        CompoundTypeEnum,
        AssayTypeEnum,
        ProcessTypeEnum,
        HitClassificationEnum,
        ProtocolTypeEnum,
    )
except ImportError:
    print("Error: LinkML models not found. Run 'uv run gen-python schema/PFAS_bioprocessing.yaml > src/linkml_models.py' first.")
    sys.exit(1)


def convert_genomes(tsv_path: Path) -> list[GenomeRecord]:
    """Convert genomes TSV to GenomeRecord list.

    Args:
        tsv_path: Path to taxa_and_genomes_extended.tsv

    Returns:
        List of GenomeRecord instances
    """
    df = pd.read_csv(tsv_path, sep='\t', dtype=str, keep_default_na=False); df = df.replace('', pd.NA)
    records = []

    for _, row in df.iterrows():
        # Skip rows with missing required fields
        if pd.isna(row.get('Scientific name')) or not row.get('Scientific name'):
            continue

        record = GenomeRecord(
            scientific_name=str(row['Scientific name']),
            ncbi_taxon_id=int(row['NCBITaxon id']) if pd.notna(row.get('NCBITaxon id')) else None,
            genome_identifier=str(row['Genome identifier (GenBank, IMG etc)']) if pd.notna(row.get('Genome identifier (GenBank, IMG etc)')) else None,
            annotation_download_url=str(row['Annotation download URL']) if pd.notna(row.get('Annotation download URL')) else None
        )
        records.append(record)

    return records


def convert_biosamples(tsv_path: Path) -> list[BiosampleRecord]:
    """Convert biosamples TSV to BiosampleRecord list.

    Args:
        tsv_path: Path to biosamples_extended.tsv

    Returns:
        List of BiosampleRecord instances
    """
    df = pd.read_csv(tsv_path, sep='\t', dtype=str, keep_default_na=False); df = df.replace('', pd.NA)
    records = []

    for _, row in df.iterrows():
        # Skip rows with missing Sample ID
        if pd.isna(row.get('Sample ID')) or not row.get('Sample ID'):
            continue

        record = BiosampleRecord(
            sample_id=str(row['Sample ID']),
            sample_name=str(row['Sample Name']) if pd.notna(row.get('Sample Name')) else None,
            organism=str(row['Organism']) if pd.notna(row.get('Organism')) else None,
            download_url=str(row['Download URL']) if pd.notna(row.get('Download URL')) else None
        )
        records.append(record)

    return records


def convert_pathways(tsv_path: Path) -> list[PathwayRecord]:
    """Convert pathways TSV to PathwayRecord list.

    Args:
        tsv_path: Path to pathways_extended.tsv

    Returns:
        List of PathwayRecord instances
    """
    df = pd.read_csv(tsv_path, sep='\t', dtype=str, keep_default_na=False); df = df.replace('', pd.NA)
    records = []

    for _, row in df.iterrows():
        # Skip rows with missing required fields
        if pd.isna(row.get('pathway id')) or pd.isna(row.get('pathway name')):
            continue

        # Extract first pathway ID from potentially multi-value field
        pathway_id_str = str(row['pathway id'])
        import re
        # Try to extract first valid pathway ID
        ko_match = re.search(r'ko\d+|path:map\d+|PWY-?\d+|Custom_[A-Z0-9]+', pathway_id_str)
        pathway_id = ko_match.group(0) if ko_match else pathway_id_str.split(';')[0].split(',')[0].strip()

        # Parse genes from column (may be delimited)
        genes = None
        if pd.notna(row.get('genes (from genes and proteins tab)')):
            genes_str = str(row['genes (from genes and proteins tab)'])
            # Split on common delimiters
            genes = [g.strip() for g in genes_str.replace(';', ',').replace('/', ',').split(',') if g.strip()]

        # Parse KEGG genes
        genes_kegg = None
        if pd.notna(row.get('genes (from genes & proteins tab)')):
            kegg_str = str(row['genes (from genes & proteins tab)'])
            # Extract K numbers
            genes_kegg = re.findall(r'K\d+', kegg_str)

        # Extract first valid URL from download_url field
        download_url = None
        if pd.notna(row.get('Download URL')):
            url_str = str(row['Download URL'])
            # Extract first HTTP/HTTPS URL
            urls = re.findall(r'https?://[^\s;,()]+', url_str)
            download_url = urls[0] if urls else None

        record = PathwayRecord(
            pathway_id=pathway_id,
            pathway_name=str(row['pathway name']),
            organism=str(row['organism']) if pd.notna(row.get('organism')) else None,
            genes=genes if genes else None,
            genes_kegg=genes_kegg if genes_kegg else None,
            download_url=download_url
        )
        records.append(record)

    return records


def convert_genes_proteins(tsv_path: Path) -> list[GeneProteinRecord]:
    """Convert genes/proteins TSV to GeneProteinRecord list.

    Args:
        tsv_path: Path to genes_and_proteins_extended.tsv

    Returns:
        List of GeneProteinRecord instances
    """
    df = pd.read_csv(tsv_path, sep='\t', dtype=str, keep_default_na=False); df = df.replace('', pd.NA)
    records = []
    seen_ids = set()
    row_counter = {}

    for _, row in df.iterrows():
        # Skip rows with missing required fields
        gene_id = row.get('gene or protein id')
        if pd.isna(gene_id) or not str(gene_id).strip():
            continue
        if pd.isna(row.get('annotation')):
            continue

        # Make gene_id unique by adding organism suffix if duplicate
        base_id = str(gene_id)
        unique_id = base_id
        organism = str(row['organism (from taxa and genomes tab)']) if pd.notna(row.get('organism (from taxa and genomes tab)')) else None

        if base_id in seen_ids:
            # Add counter to make it unique
            if base_id not in row_counter:
                row_counter[base_id] = 1
            row_counter[base_id] += 1
            # Create unique ID with organism or counter
            if organism:
                org_short = organism.split()[0][:10]  # First 10 chars of genus
                unique_id = f"{base_id}_{org_short}"
            else:
                unique_id = f"{base_id}_{row_counter[base_id]}"

        seen_ids.add(unique_id)

        # Parse GO terms
        go_terms = None
        if pd.notna(row.get('GO')):
            import re
            go_terms = re.findall(r'GO:\d{7}', str(row['GO']))

        # Parse CHEBI terms
        chebi_terms = None
        if pd.notna(row.get('CHEBI')):
            import re
            chebi_terms = re.findall(r'CHEBI:\d+', str(row['CHEBI']))

        record = GeneProteinRecord(
            gene_protein_id=unique_id,
            organism=organism,
            annotation=str(row['annotation']),
            ec_number=str(row['EC']) if pd.notna(row.get('EC')) and str(row['EC']).strip() else None,
            go_terms=go_terms if go_terms else None,
            chebi_terms=chebi_terms if chebi_terms else None,
            download_url=str(row['Download URL']) if pd.notna(row.get('Download URL')) else None
        )
        records.append(record)

    return records


def convert_structures(tsv_path: Path) -> list[MacromolecularStructureRecord]:
    """Convert structures TSV to MacromolecularStructureRecord list.

    Args:
        tsv_path: Path to macromolecular_structures_extended.tsv

    Returns:
        List of MacromolecularStructureRecord instances
    """
    df = pd.read_csv(tsv_path, sep='\t', dtype=str, keep_default_na=False); df = df.replace('', pd.NA)
    records = []

    for _, row in df.iterrows():
        # Skip rows with missing Name
        if pd.isna(row.get('Name')) or not row.get('Name'):
            continue

        # Map method string to enum
        method = None
        if pd.notna(row.get('Method')):
            method_str = str(row['Method'])
            # Try to map to enum values
            method_mapping = {
                'X-ray crystallography': StructureMethodEnum['X-ray crystallography'],
                'NMR': StructureMethodEnum['NMR spectroscopy'],
                'NMR spectroscopy': StructureMethodEnum['NMR spectroscopy'],
                'Cryo-EM': StructureMethodEnum['Cryo-EM'],
                'Predicted structure': StructureMethodEnum['Predicted structure'],
                'Homology modeling': StructureMethodEnum['Homology modeling'],
                'Computational prediction': StructureMethodEnum['Computational prediction'],
                'Chemical characterization': StructureMethodEnum['Chemical characterization'],
            }
            method = method_mapping.get(method_str, StructureMethodEnum['Multiple methods'])

        record = MacromolecularStructureRecord(
            structure_name=str(row['Name']),
            organism=str(row['Organism']) if pd.notna(row.get('Organism')) else None,
            components=str(row['Components']) if pd.notna(row.get('Components')) else None,
            pdb_id=str(row['PDB_ID']) if pd.notna(row.get('PDB_ID')) and str(row['PDB_ID']) not in ['N/A', 'predicted', 'multiple'] else None,
            resolution=str(row['Resolution']) if pd.notna(row.get('Resolution')) else None,
            method=method,
            download_url=str(row['Download URL']) if pd.notna(row.get('Download URL')) else None
        )
        records.append(record)

    return records


def convert_publications(tsv_path: Path) -> list[PublicationRecord]:
    """Convert publications TSV to PublicationRecord list.

    Args:
        tsv_path: Path to publications_extended.tsv

    Returns:
        List of PublicationRecord instances
    """
    df = pd.read_csv(tsv_path, sep='\t', dtype=str, keep_default_na=False); df = df.replace('', pd.NA)
    records = []

    for _, row in df.iterrows():
        # Skip rows with missing URL or Title
        if pd.isna(row.get('URL')) or pd.isna(row.get('Title')):
            continue
        if not str(row['URL']).strip() or not str(row['Title']).strip():
            continue

        record = PublicationRecord(
            url=str(row['URL']),
            title=str(row['Title']),
            journal=str(row['Journal']) if pd.notna(row.get('Journal')) else None,
            year=int(row['Year']) if pd.notna(row.get('Year')) and str(row['Year']).isdigit() else None,
            authors=str(row['Authors']) if pd.notna(row.get('Authors')) else None,
            download_url=str(row['Download URL']) if pd.notna(row.get('Download URL')) else None
        )
        records.append(record)

    return records


def convert_datasets(tsv_path: Path) -> list[DatasetRecord]:
    """Convert datasets TSV to DatasetRecord list.

    Args:
        tsv_path: Path to datasets_extended.tsv

    Returns:
        List of DatasetRecord instances
    """
    df = pd.read_csv(tsv_path, sep='\t', dtype=str, keep_default_na=False); df = df.replace('', pd.NA)
    records = []

    for _, row in df.iterrows():
        # Skip rows with missing Dataset name
        if pd.isna(row.get('Dataset name')) or not row.get('Dataset name'):
            continue

        # Map data type to enum
        data_type = None
        if pd.notna(row.get('Data Type')):
            dt_str = str(row['Data Type'])
            # Try exact match first
            try:
                data_type = DataTypeEnum[dt_str]
            except KeyError:
                # Map common variations
                dt_mapping = {
                    'genomic DNA sequencing': DataTypeEnum['genomic DNA sequencing'],
                    'RNA-seq': DataTypeEnum['RNA-seq'],
                    'transcriptomics': DataTypeEnum['transcriptomics'],
                    'proteomics': DataTypeEnum['proteomics'],
                    'metabolomics': DataTypeEnum['metabolomics'],
                    'metagenomics': DataTypeEnum['metagenomics'],
                    'protein sequences': DataTypeEnum['protein sequences'],
                    'pathways': DataTypeEnum['pathways'],
                    'thermodynamics': DataTypeEnum['thermodynamics'],
                }
                data_type = dt_mapping.get(dt_str)

        record = DatasetRecord(
            dataset_name=str(row['Dataset name']),
            data_type=data_type,
            url=str(row['URL']) if pd.notna(row.get('URL')) else None,
            size=str(row['Size (rows or MB)']) if pd.notna(row.get('Size (rows or MB)')) else None,
            publication=str(row['Publication']) if pd.notna(row.get('Publication')) else None,
            license=str(row['License']) if pd.notna(row.get('License')) else None,
            download_url=str(row['Download URL']) if pd.notna(row.get('Download URL')) else None
        )
        records.append(record)

    return records


def convert_chemicals(tsv_path: Path) -> list[ChemicalCompoundRecord]:
    """Convert chemicals TSV to ChemicalCompoundRecord list.

    Args:
        tsv_path: Path to chemicals.tsv

    Returns:
        List of ChemicalCompoundRecord instances
    """
    df = pd.read_csv(tsv_path, sep='\t', dtype=str, keep_default_na=False); df = df.replace('', pd.NA)
    records = []

    for _, row in df.iterrows():
        # Skip rows with missing required fields
        if pd.isna(row.get('chemical_id')) or pd.isna(row.get('chemical_name')):
            continue

        # Map compound type to enum
        compound_type = None
        if pd.notna(row.get('compound_type')):
            ct_str = str(row['compound_type'])
            try:
                compound_type = CompoundTypeEnum[ct_str]
            except KeyError:
                # Map common variations
                ct_mapping = {
                    'PFAS': CompoundTypeEnum.PFAS,
                    'lanthanophore': CompoundTypeEnum.lanthanophore,
                    'chelator': CompoundTypeEnum.chelator,
                    'substrate': CompoundTypeEnum.substrate,
                    'product': CompoundTypeEnum.product,
                    'metabolite': CompoundTypeEnum.metabolite,
                    'cofactor': CompoundTypeEnum.cofactor,
                    'extractant': CompoundTypeEnum.extractant,
                    'sensitizer': CompoundTypeEnum.sensitizer,
                }
                compound_type = ct_mapping.get(ct_str)

        # Parse molecular weight
        molecular_weight = None
        if pd.notna(row.get('molecular_weight')):
            try:
                molecular_weight = float(row['molecular_weight'])
            except (ValueError, TypeError):
                pass

        record = ChemicalCompoundRecord(
            chemical_id=str(row['chemical_id']),
            chemical_name=str(row['chemical_name']),
            compound_type=compound_type,
            molecular_formula=str(row['molecular_formula']) if pd.notna(row.get('molecular_formula')) else None,
            molecular_weight=molecular_weight,
            role_in_bioprocess=str(row['role_in_bioprocess']) if pd.notna(row.get('role_in_bioprocess')) else None,
            chebi_id=str(row['chebi_id']) if pd.notna(row.get('chebi_id')) else None,
            pubchem_id=str(row['pubchem_id']) if pd.notna(row.get('pubchem_id')) else None,
            chembl_id=str(row['chembl_id']) if pd.notna(row.get('chembl_id')) else None,
            properties=str(row['properties']) if pd.notna(row.get('properties')) else None,
            download_url=str(row['Download URL']) if pd.notna(row.get('Download URL')) else None
        )
        records.append(record)

    return records


def convert_assays(tsv_path: Path) -> list[AssayMeasurementRecord]:
    """Convert assays TSV to AssayMeasurementRecord list.

    Args:
        tsv_path: Path to assays.tsv

    Returns:
        List of AssayMeasurementRecord instances
    """
    df = pd.read_csv(tsv_path, sep='\t', dtype=str, keep_default_na=False); df = df.replace('', pd.NA)
    records = []

    for _, row in df.iterrows():
        # Skip rows with missing required fields
        if pd.isna(row.get('assay_id')) or pd.isna(row.get('assay_name')):
            continue

        # Map assay type to enum
        assay_type = None
        if pd.notna(row.get('assay_type')):
            at_str = str(row['assay_type'])
            try:
                assay_type = AssayTypeEnum[at_str]
            except KeyError:
                # Map common variations
                at_mapping = {
                    'time-resolved luminescence (TRL)': AssayTypeEnum['time-resolved luminescence (TRL)'],
                    'TRL': AssayTypeEnum['time-resolved luminescence (TRL)'],
                    'ICP-OES': AssayTypeEnum['ICP-OES'],
                    'ICP-MS': AssayTypeEnum['ICP-MS'],
                    'FACS': AssayTypeEnum['FACS'],
                    'fluorescence spectroscopy': AssayTypeEnum['fluorescence spectroscopy'],
                }
                assay_type = at_mapping.get(at_str)

        record = AssayMeasurementRecord(
            assay_id=str(row['assay_id']),
            assay_name=str(row['assay_name']),
            assay_type=assay_type,
            target_analytes=str(row['target_analytes']) if pd.notna(row.get('target_analytes')) else None,
            detection_method=str(row['detection_method']) if pd.notna(row.get('detection_method')) else None,
            detection_limit=str(row['detection_limit']) if pd.notna(row.get('detection_limit')) else None,
            dynamic_range=str(row['dynamic_range']) if pd.notna(row.get('dynamic_range')) else None,
            protocol_reference=str(row['protocol_reference']) if pd.notna(row.get('protocol_reference')) else None,
            equipment_required=str(row['equipment_required']) if pd.notna(row.get('equipment_required')) else None,
            sample_preparation=str(row['sample_preparation']) if pd.notna(row.get('sample_preparation')) else None,
            data_output_format=str(row['data_output_format']) if pd.notna(row.get('data_output_format')) else None,
            download_url=str(row['Download URL']) if pd.notna(row.get('Download URL')) else None
        )
        records.append(record)

    return records


def convert_bioprocesses(tsv_path: Path) -> list[BioprocessConditionsRecord]:
    """Convert bioprocesses TSV to BioprocessConditionsRecord list.

    Args:
        tsv_path: Path to bioprocesses.tsv

    Returns:
        List of BioprocessConditionsRecord instances
    """
    df = pd.read_csv(tsv_path, sep='\t', dtype=str, keep_default_na=False); df = df.replace('', pd.NA)
    records = []

    for _, row in df.iterrows():
        # Skip rows with missing required fields
        if pd.isna(row.get('process_id')) or pd.isna(row.get('process_name')):
            continue

        # Map process type to enum
        process_type = None
        if pd.notna(row.get('process_type')):
            pt_str = str(row['process_type'])
            try:
                process_type = ProcessTypeEnum[pt_str]
            except KeyError:
                # Map common variations
                pt_mapping = {
                    'bioleaching': ProcessTypeEnum.bioleaching,
                    'biomineralization': ProcessTypeEnum.biomineralization,
                    'biosorption': ProcessTypeEnum.biosorption,
                    'bioaccumulation': ProcessTypeEnum.bioaccumulation,
                    'fermentation': ProcessTypeEnum.fermentation,
                    'bioextraction': ProcessTypeEnum.bioextraction,
                }
                process_type = pt_mapping.get(pt_str)

        # Parse numeric fields
        pH = None
        if pd.notna(row.get('pH')):
            try:
                pH = float(row['pH'])
            except (ValueError, TypeError):
                pass

        temperature = None
        if pd.notna(row.get('temperature')):
            temp_str = str(row['temperature']).replace('°C', '').replace('C', '').strip()
            try:
                temperature = float(temp_str)
            except (ValueError, TypeError):
                pass

        record = BioprocessConditionsRecord(
            process_id=str(row['process_id']),
            process_name=str(row['process_name']),
            process_type=process_type,
            strain_used=str(row['strain_used']) if pd.notna(row.get('strain_used')) else None,
            organism_used=str(row['organism_used']) if pd.notna(row.get('organism_used')) else None,
            growth_conditions=str(row['growth_conditions']) if pd.notna(row.get('growth_conditions')) else None,
            ree_concentration=str(row['ree_concentration']) if pd.notna(row.get('ree_concentration')) else None,
            contact_time=str(row['contact_time']) if pd.notna(row.get('contact_time')) else None,
            pH=pH,
            temperature=temperature,
            competing_ions=str(row['competing_ions']) if pd.notna(row.get('competing_ions')) else None,
            process_parameters=str(row['process_parameters']) if pd.notna(row.get('process_parameters')) else None,
            optimization_history=str(row['optimization_history']) if pd.notna(row.get('optimization_history')) else None,
            download_url=str(row['Download URL']) if pd.notna(row.get('Download URL')) else None
        )
        records.append(record)

    return records


def convert_screening_results(tsv_path: Path) -> list[ScreeningResultRecord]:
    """Convert screening results TSV to ScreeningResultRecord list.

    Args:
        tsv_path: Path to screening_results.tsv

    Returns:
        List of ScreeningResultRecord instances
    """
    df = pd.read_csv(tsv_path, sep='\t', dtype=str, keep_default_na=False); df = df.replace('', pd.NA)
    records = []

    for _, row in df.iterrows():
        # Skip rows with missing required fields
        if pd.isna(row.get('experiment_id')):
            continue

        # Map hit classification to enum
        hit_classification = None
        if pd.notna(row.get('hit_classification')):
            hc_str = str(row['hit_classification'])
            try:
                hit_classification = HitClassificationEnum[hc_str]
            except KeyError:
                # Map common variations
                hc_mapping = {
                    'positive': HitClassificationEnum.positive,
                    'negative': HitClassificationEnum.negative,
                    'borderline': HitClassificationEnum.borderline,
                    'false positive': HitClassificationEnum['false positive'],
                    'validated': HitClassificationEnum.validated,
                }
                hit_classification = hc_mapping.get(hc_str)

        record = ScreeningResultRecord(
            experiment_id=str(row['experiment_id']),
            plate_coordinates=str(row['plate_coordinates']) if pd.notna(row.get('plate_coordinates')) else None,
            strain_barcode=str(row['strain_barcode']) if pd.notna(row.get('strain_barcode')) else None,
            screening_assay=str(row['screening_assay']) if pd.notna(row.get('screening_assay')) else None,
            target_ree=str(row['target_ree']) if pd.notna(row.get('target_ree')) else None,
            measurement_values=str(row['measurement_values']) if pd.notna(row.get('measurement_values')) else None,
            hit_classification=hit_classification,
            validation_status=str(row['validation_status']) if pd.notna(row.get('validation_status')) else None,
            follow_up_experiments=str(row['follow_up_experiments']) if pd.notna(row.get('follow_up_experiments')) else None,
            assay_reference=str(row['assay_reference']) if pd.notna(row.get('assay_reference')) else None,
            download_url=str(row['Download URL']) if pd.notna(row.get('Download URL')) else None
        )
        records.append(record)

    return records


def convert_protocols(tsv_path: Path) -> list[ProtocolRecord]:
    """Convert protocols TSV to ProtocolRecord list.

    Args:
        tsv_path: Path to protocols.tsv

    Returns:
        List of ProtocolRecord instances
    """
    df = pd.read_csv(tsv_path, sep='\t', dtype=str, keep_default_na=False); df = df.replace('', pd.NA)
    records = []

    for _, row in df.iterrows():
        # Skip rows with missing required fields
        if pd.isna(row.get('protocol_id')) or pd.isna(row.get('protocol_name')):
            continue

        # Map protocol type to enum
        protocol_type = None
        if pd.notna(row.get('protocol_type')):
            pt_str = str(row['protocol_type'])
            try:
                protocol_type = ProtocolTypeEnum[pt_str]
            except KeyError:
                # Map common variations
                pt_mapping = {
                    'assay protocol': ProtocolTypeEnum['assay protocol'],
                    'cultivation protocol': ProtocolTypeEnum['cultivation protocol'],
                    'extraction protocol': ProtocolTypeEnum['extraction protocol'],
                    'transformation protocol': ProtocolTypeEnum['transformation protocol'],
                    'screening protocol': ProtocolTypeEnum['screening protocol'],
                    'sample preparation': ProtocolTypeEnum['sample preparation'],
                    'quality control': ProtocolTypeEnum['quality control'],
                }
                protocol_type = pt_mapping.get(pt_str)

        record = ProtocolRecord(
            protocol_id=str(row['protocol_id']),
            protocol_name=str(row['protocol_name']),
            protocol_type=protocol_type,
            protocol_version=str(row['protocol_version']) if pd.notna(row.get('protocol_version')) else None,
            protocol_doi=str(row['protocol_doi']) if pd.notna(row.get('protocol_doi')) else None,
            protocol_url=str(row['protocol_url']) if pd.notna(row.get('protocol_url')) else None,
            associated_assays=str(row['associated_assays']) if pd.notna(row.get('associated_assays')) else None,
            equipment_list=str(row['equipment_list']) if pd.notna(row.get('equipment_list')) else None,
            success_criteria=str(row['success_criteria']) if pd.notna(row.get('success_criteria')) else None,
            quality_control=str(row['quality_control']) if pd.notna(row.get('quality_control')) else None,
            dbtl_iteration=str(row['dbtl_iteration']) if pd.notna(row.get('dbtl_iteration')) else None,
            validation_status=str(row['validation_status']) if pd.notna(row.get('validation_status')) else None,
            user_notes=str(row['user_notes']) if pd.notna(row.get('user_notes')) else None,
            download_url=str(row['Download URL']) if pd.notna(row.get('Download URL')) else None
        )
        records.append(record)

    return records


def convert_all_tsvs(data_dir: Path, output_path: Optional[Path] = None) -> PFASBioprocessingDatabase:
    """Convert all TSV files to LinkML database.

    Args:
        data_dir: Directory containing extended TSV files
        output_path: Optional path to save YAML output

    Returns:
        PFASBioprocessingDatabase instance
    """
    print(f"Converting TSV files from {data_dir}...")

    # Convert each table
    genomes = convert_genomes(data_dir / "PFAS_Data_for_AI_taxa_and_genomes_extended.tsv")
    print(f"  Converted {len(genomes)} genome records")

    biosamples = convert_biosamples(data_dir / "PFAS_Data_for_AI_biosamples_extended.tsv")
    print(f"  Converted {len(biosamples)} biosample records")

    pathways = convert_pathways(data_dir / "PFAS_Data_for_AI_pathways_extended.tsv")
    print(f"  Converted {len(pathways)} pathway records")

    genes_proteins = convert_genes_proteins(data_dir / "PFAS_Data_for_AI_genes_and_proteins_extended.tsv")
    print(f"  Converted {len(genes_proteins)} gene/protein records")

    structures = convert_structures(data_dir / "PFAS_Data_for_AI_macromolecular_structures_extended.tsv")
    print(f"  Converted {len(structures)} structure records")

    publications = convert_publications(data_dir / "PFAS_Data_for_AI_publications_extended.tsv")
    print(f"  Converted {len(publications)} publication records")

    datasets = convert_datasets(data_dir / "PFAS_Data_for_AI_datasets_extended.tsv")
    print(f"  Converted {len(datasets)} dataset records")

    # Convert new experimental data tables
    chemicals = []
    chemicals_file = data_dir / "PFAS_Data_for_AI_chemicals.tsv"
    if chemicals_file.exists():
        chemicals = convert_chemicals(chemicals_file)
        print(f"  Converted {len(chemicals)} chemical records")

    assays = []
    assays_file = data_dir / "PFAS_Data_for_AI_assays.tsv"
    if assays_file.exists():
        assays = convert_assays(assays_file)
        print(f"  Converted {len(assays)} assay records")

    bioprocesses = []
    bioprocesses_file = data_dir / "PFAS_Data_for_AI_bioprocesses.tsv"
    if bioprocesses_file.exists():
        bioprocesses = convert_bioprocesses(bioprocesses_file)
        print(f"  Converted {len(bioprocesses)} bioprocess records")

    screening_results = []
    screening_file = data_dir / "PFAS_Data_for_AI_screening_results.tsv"
    if screening_file.exists():
        screening_results = convert_screening_results(screening_file)
        print(f"  Converted {len(screening_results)} screening result records")

    protocols = []
    protocols_file = data_dir / "PFAS_Data_for_AI_protocols.tsv"
    if protocols_file.exists():
        protocols = convert_protocols(protocols_file)
        print(f"  Converted {len(protocols)} protocol records")

    # Create database
    database = PFASBioprocessingDatabase(
        genomes=genomes,
        biosamples=biosamples,
        pathways=pathways,
        genes_proteins=genes_proteins,
        structures=structures,
        publications=publications,
        datasets=datasets,
        chemicals=chemicals,
        assays=assays,
        bioprocesses=bioprocesses,
        screening_results=screening_results,
        protocols=protocols
    )

    # Save if output path provided
    if output_path:
        yaml_dumper.dump(database, str(output_path))
        print(f"\nDatabase saved to {output_path}")

    return database


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Convert extended TSV files to LinkML YAML format"
    )
    parser.add_argument(
        '--data-dir',
        type=Path,
        default=Path('data/txt/sheet'),
        help='Directory containing extended TSV files (default: data/txt/sheet)'
    )
    parser.add_argument(
        '--output',
        type=Path,
        default=Path('data/linkml_database.yaml'),
        help='Output YAML file path (default: data/linkml_database.yaml)'
    )

    args = parser.parse_args()

    # Convert all TSVs
    database = convert_all_tsvs(args.data_dir, args.output)

    print(f"\nConversion complete!")
    total_records = (
        len(database.genomes) + len(database.biosamples) + len(database.pathways) +
        len(database.genes_proteins) + len(database.structures) + len(database.publications) +
        len(database.datasets) + len(database.chemicals) + len(database.assays) +
        len(database.bioprocesses) + len(database.screening_results) + len(database.protocols)
    )
    print(f"Total records: {total_records}")


if __name__ == "__main__":
    main()
