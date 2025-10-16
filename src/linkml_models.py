# Auto generated from lanthanide_bioprocessing.yaml by pythongen.py version: 0.0.1
# Generation date: 2025-10-15T21:26:11
# Schema: lanthanide-bioprocessing-schema
#
# id: https://w3id.org/cmm-ai/lanthanide-bioprocessing
# description: LinkML schema for lanthanide bioprocessing research data, integrating bacterial genomes,
#   biosamples, metabolic pathways, genes/proteins, macromolecular structures, publications,
#   and datasets related to rare earth element-dependent biological processes.
#
#   This schema models data for lanthanide-dependent methylotrophy, particularly focusing on
#   XoxF methanol dehydrogenase systems, lanthanophore transport, and rare earth element
#   metabolism in methylotrophic bacteria.
# license: MIT

import dataclasses
import re
from dataclasses import dataclass
from datetime import (
    date,
    datetime,
    time
)
from typing import (
    Any,
    ClassVar,
    Dict,
    List,
    Optional,
    Union
)

from jsonasobj2 import (
    JsonObj,
    as_dict
)
from linkml_runtime.linkml_model.meta import (
    EnumDefinition,
    PermissibleValue,
    PvFormulaOptions
)
from linkml_runtime.utils.curienamespace import CurieNamespace
from linkml_runtime.utils.enumerations import EnumDefinitionImpl
from linkml_runtime.utils.formatutils import (
    camelcase,
    sfx,
    underscore
)
from linkml_runtime.utils.metamodelcore import (
    bnode,
    empty_dict,
    empty_list
)
from linkml_runtime.utils.slot import Slot
from linkml_runtime.utils.yamlutils import (
    YAMLRoot,
    extended_float,
    extended_int,
    extended_str
)
from rdflib import (
    Namespace,
    URIRef
)

from linkml_runtime.linkml_model.types import Integer, String, Uri
from linkml_runtime.utils.metamodelcore import URI

metamodel_version = "1.7.0"
version = "0.1.0"

# Namespaces
BAO = CurieNamespace('BAO', 'http://www.bioassayontology.org/bao#BAO_')
CHEBI = CurieNamespace('CHEBI', 'http://purl.obolibrary.org/obo/CHEBI_')
CHEMBL = CurieNamespace('ChEMBL', 'https://www.ebi.ac.uk/chembl/compound_report_card/')
DOI = CurieNamespace('DOI', 'https://doi.org/')
EC = CurieNamespace('EC', 'https://www.enzyme-database.org/query.php?ec=')
ENVO = CurieNamespace('ENVO', 'http://purl.obolibrary.org/obo/ENVO_')
GO = CurieNamespace('GO', 'http://purl.obolibrary.org/obo/GO_')
KEGG = CurieNamespace('KEGG', 'https://www.kegg.jp/entry/')
MIXS = CurieNamespace('MIXS', 'http://purl.obolibrary.org/obo/MIXS_')
METACYC = CurieNamespace('MetaCyc', 'https://metacyc.org/META/NEW-IMAGE?type=PATHWAY&object=')
NCBI = CurieNamespace('NCBI', 'https://www.ncbi.nlm.nih.gov/')
NCBITAXON = CurieNamespace('NCBITaxon', 'http://purl.obolibrary.org/obo/NCBITaxon_')
OBI = CurieNamespace('OBI', 'http://purl.obolibrary.org/obo/OBI_')
PDB = CurieNamespace('PDB', 'https://www.rcsb.org/structure/')
PMID = CurieNamespace('PMID', 'http://www.ncbi.nlm.nih.gov/pubmed/')
PUBCHEM = CurieNamespace('PubChem', 'https://pubchem.ncbi.nlm.nih.gov/compound/')
RHEA = CurieNamespace('RHEA', 'https://www.rhea-db.org/rhea/')
SRA = CurieNamespace('SRA', 'https://www.ncbi.nlm.nih.gov/sra/')
UNIPROTKB = CurieNamespace('UniProtKB', 'http://purl.uniprot.org/uniprot/')
CMM = CurieNamespace('cmm', 'https://w3id.org/cmm-ai/lanthanide-bioprocessing/')
LINKML = CurieNamespace('linkml', 'https://w3id.org/linkml/')
SCHEMA = CurieNamespace('schema', 'http://schema.org/')
DEFAULT_ = CMM


# Types

# Class references
class GenomeRecordScientificName(extended_str):
    pass


class BiosampleRecordSampleId(extended_str):
    pass


class PathwayRecordPathwayId(extended_str):
    pass


class GeneProteinRecordGeneProteinId(extended_str):
    pass


class MacromolecularStructureRecordStructureName(extended_str):
    pass


class PublicationRecordUrl(URI):
    pass


class DatasetRecordDatasetName(extended_str):
    pass


class ChemicalCompoundRecordChemicalId(extended_str):
    pass


class AssayMeasurementRecordAssayId(extended_str):
    pass


class BioprocessConditionsRecordProcessId(extended_str):
    pass


class ScreeningResultRecordExperimentId(extended_str):
    pass


class ProtocolRecordProtocolId(extended_str):
    pass


@dataclass(repr=False)
class LanthanideBioprocessingDatabase(YAMLRoot):
    """
    Root container for all lanthanide bioprocessing research data
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = CMM["LanthanideBioprocessingDatabase"]
    class_class_curie: ClassVar[str] = "cmm:LanthanideBioprocessingDatabase"
    class_name: ClassVar[str] = "LanthanideBioprocessingDatabase"
    class_model_uri: ClassVar[URIRef] = CMM.LanthanideBioprocessingDatabase

    genomes: Optional[Union[dict[Union[str, GenomeRecordScientificName], Union[dict, "GenomeRecord"]], list[Union[dict, "GenomeRecord"]]]] = empty_dict()
    biosamples: Optional[Union[dict[Union[str, BiosampleRecordSampleId], Union[dict, "BiosampleRecord"]], list[Union[dict, "BiosampleRecord"]]]] = empty_dict()
    pathways: Optional[Union[dict[Union[str, PathwayRecordPathwayId], Union[dict, "PathwayRecord"]], list[Union[dict, "PathwayRecord"]]]] = empty_dict()
    genes_proteins: Optional[Union[dict[Union[str, GeneProteinRecordGeneProteinId], Union[dict, "GeneProteinRecord"]], list[Union[dict, "GeneProteinRecord"]]]] = empty_dict()
    structures: Optional[Union[dict[Union[str, MacromolecularStructureRecordStructureName], Union[dict, "MacromolecularStructureRecord"]], list[Union[dict, "MacromolecularStructureRecord"]]]] = empty_dict()
    publications: Optional[Union[dict[Union[str, PublicationRecordUrl], Union[dict, "PublicationRecord"]], list[Union[dict, "PublicationRecord"]]]] = empty_dict()
    datasets: Optional[Union[dict[Union[str, DatasetRecordDatasetName], Union[dict, "DatasetRecord"]], list[Union[dict, "DatasetRecord"]]]] = empty_dict()
    chemicals: Optional[Union[dict[Union[str, ChemicalCompoundRecordChemicalId], Union[dict, "ChemicalCompoundRecord"]], list[Union[dict, "ChemicalCompoundRecord"]]]] = empty_dict()
    assays: Optional[Union[dict[Union[str, AssayMeasurementRecordAssayId], Union[dict, "AssayMeasurementRecord"]], list[Union[dict, "AssayMeasurementRecord"]]]] = empty_dict()
    bioprocesses: Optional[Union[dict[Union[str, BioprocessConditionsRecordProcessId], Union[dict, "BioprocessConditionsRecord"]], list[Union[dict, "BioprocessConditionsRecord"]]]] = empty_dict()
    screening_results: Optional[Union[dict[Union[str, ScreeningResultRecordExperimentId], Union[dict, "ScreeningResultRecord"]], list[Union[dict, "ScreeningResultRecord"]]]] = empty_dict()
    protocols: Optional[Union[dict[Union[str, ProtocolRecordProtocolId], Union[dict, "ProtocolRecord"]], list[Union[dict, "ProtocolRecord"]]]] = empty_dict()

    def __post_init__(self, *_: str, **kwargs: Any):
        self._normalize_inlined_as_list(slot_name="genomes", slot_type=GenomeRecord, key_name="scientific_name", keyed=True)

        self._normalize_inlined_as_list(slot_name="biosamples", slot_type=BiosampleRecord, key_name="sample_id", keyed=True)

        self._normalize_inlined_as_list(slot_name="pathways", slot_type=PathwayRecord, key_name="pathway_id", keyed=True)

        self._normalize_inlined_as_list(slot_name="genes_proteins", slot_type=GeneProteinRecord, key_name="gene_protein_id", keyed=True)

        self._normalize_inlined_as_list(slot_name="structures", slot_type=MacromolecularStructureRecord, key_name="structure_name", keyed=True)

        self._normalize_inlined_as_list(slot_name="publications", slot_type=PublicationRecord, key_name="url", keyed=True)

        self._normalize_inlined_as_list(slot_name="datasets", slot_type=DatasetRecord, key_name="dataset_name", keyed=True)

        self._normalize_inlined_as_list(slot_name="chemicals", slot_type=ChemicalCompoundRecord, key_name="chemical_id", keyed=True)

        self._normalize_inlined_as_list(slot_name="assays", slot_type=AssayMeasurementRecord, key_name="assay_id", keyed=True)

        self._normalize_inlined_as_list(slot_name="bioprocesses", slot_type=BioprocessConditionsRecord, key_name="process_id", keyed=True)

        self._normalize_inlined_as_list(slot_name="screening_results", slot_type=ScreeningResultRecord, key_name="experiment_id", keyed=True)

        self._normalize_inlined_as_list(slot_name="protocols", slot_type=ProtocolRecord, key_name="protocol_id", keyed=True)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class GenomeRecord(YAMLRoot):
    """
    Bacterial or archaeal genome record with taxonomy and annotation information
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = CMM["GenomeRecord"]
    class_class_curie: ClassVar[str] = "cmm:GenomeRecord"
    class_name: ClassVar[str] = "GenomeRecord"
    class_model_uri: ClassVar[URIRef] = CMM.GenomeRecord

    scientific_name: Union[str, GenomeRecordScientificName] = None
    ncbi_taxon_id: Optional[int] = None
    genome_identifier: Optional[str] = None
    annotation_download_url: Optional[Union[str, URI]] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self._is_empty(self.scientific_name):
            self.MissingRequiredField("scientific_name")
        if not isinstance(self.scientific_name, GenomeRecordScientificName):
            self.scientific_name = GenomeRecordScientificName(self.scientific_name)

        if self.ncbi_taxon_id is not None and not isinstance(self.ncbi_taxon_id, int):
            self.ncbi_taxon_id = int(self.ncbi_taxon_id)

        if self.genome_identifier is not None and not isinstance(self.genome_identifier, str):
            self.genome_identifier = str(self.genome_identifier)

        if self.annotation_download_url is not None and not isinstance(self.annotation_download_url, URI):
            self.annotation_download_url = URI(self.annotation_download_url)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class BiosampleRecord(YAMLRoot):
    """
    Environmental or cultured biological sample with metadata
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = CMM["BiosampleRecord"]
    class_class_curie: ClassVar[str] = "cmm:BiosampleRecord"
    class_name: ClassVar[str] = "BiosampleRecord"
    class_model_uri: ClassVar[URIRef] = CMM.BiosampleRecord

    sample_id: Union[str, BiosampleRecordSampleId] = None
    sample_name: Optional[str] = None
    organism: Optional[str] = None
    download_url: Optional[Union[str, URI]] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self._is_empty(self.sample_id):
            self.MissingRequiredField("sample_id")
        if not isinstance(self.sample_id, BiosampleRecordSampleId):
            self.sample_id = BiosampleRecordSampleId(self.sample_id)

        if self.sample_name is not None and not isinstance(self.sample_name, str):
            self.sample_name = str(self.sample_name)

        if self.organism is not None and not isinstance(self.organism, str):
            self.organism = str(self.organism)

        if self.download_url is not None and not isinstance(self.download_url, URI):
            self.download_url = URI(self.download_url)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class PathwayRecord(YAMLRoot):
    """
    Metabolic pathway involved in lanthanide bioprocessing or methylotrophy
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = CMM["PathwayRecord"]
    class_class_curie: ClassVar[str] = "cmm:PathwayRecord"
    class_name: ClassVar[str] = "PathwayRecord"
    class_model_uri: ClassVar[URIRef] = CMM.PathwayRecord

    pathway_id: Union[str, PathwayRecordPathwayId] = None
    pathway_name: str = None
    organism: Optional[str] = None
    genes: Optional[Union[str, list[str]]] = empty_list()
    genes_kegg: Optional[Union[str, list[str]]] = empty_list()
    download_url: Optional[Union[str, URI]] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self._is_empty(self.pathway_id):
            self.MissingRequiredField("pathway_id")
        if not isinstance(self.pathway_id, PathwayRecordPathwayId):
            self.pathway_id = PathwayRecordPathwayId(self.pathway_id)

        if self._is_empty(self.pathway_name):
            self.MissingRequiredField("pathway_name")
        if not isinstance(self.pathway_name, str):
            self.pathway_name = str(self.pathway_name)

        if self.organism is not None and not isinstance(self.organism, str):
            self.organism = str(self.organism)

        if not isinstance(self.genes, list):
            self.genes = [self.genes] if self.genes is not None else []
        self.genes = [v if isinstance(v, str) else str(v) for v in self.genes]

        if not isinstance(self.genes_kegg, list):
            self.genes_kegg = [self.genes_kegg] if self.genes_kegg is not None else []
        self.genes_kegg = [v if isinstance(v, str) else str(v) for v in self.genes_kegg]

        if self.download_url is not None and not isinstance(self.download_url, URI):
            self.download_url = URI(self.download_url)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class GeneProteinRecord(YAMLRoot):
    """
    Gene or protein sequence with functional annotations
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = CMM["GeneProteinRecord"]
    class_class_curie: ClassVar[str] = "cmm:GeneProteinRecord"
    class_name: ClassVar[str] = "GeneProteinRecord"
    class_model_uri: ClassVar[URIRef] = CMM.GeneProteinRecord

    gene_protein_id: Union[str, GeneProteinRecordGeneProteinId] = None
    annotation: str = None
    organism: Optional[str] = None
    ec_number: Optional[str] = None
    go_terms: Optional[Union[str, list[str]]] = empty_list()
    chebi_terms: Optional[Union[str, list[str]]] = empty_list()
    download_url: Optional[Union[str, URI]] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self._is_empty(self.gene_protein_id):
            self.MissingRequiredField("gene_protein_id")
        if not isinstance(self.gene_protein_id, GeneProteinRecordGeneProteinId):
            self.gene_protein_id = GeneProteinRecordGeneProteinId(self.gene_protein_id)

        if self._is_empty(self.annotation):
            self.MissingRequiredField("annotation")
        if not isinstance(self.annotation, str):
            self.annotation = str(self.annotation)

        if self.organism is not None and not isinstance(self.organism, str):
            self.organism = str(self.organism)

        if self.ec_number is not None and not isinstance(self.ec_number, str):
            self.ec_number = str(self.ec_number)

        if not isinstance(self.go_terms, list):
            self.go_terms = [self.go_terms] if self.go_terms is not None else []
        self.go_terms = [v if isinstance(v, str) else str(v) for v in self.go_terms]

        if not isinstance(self.chebi_terms, list):
            self.chebi_terms = [self.chebi_terms] if self.chebi_terms is not None else []
        self.chebi_terms = [v if isinstance(v, str) else str(v) for v in self.chebi_terms]

        if self.download_url is not None and not isinstance(self.download_url, URI):
            self.download_url = URI(self.download_url)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class MacromolecularStructureRecord(YAMLRoot):
    """
    3D structure of protein, complex, or small molecule
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = CMM["MacromolecularStructureRecord"]
    class_class_curie: ClassVar[str] = "cmm:MacromolecularStructureRecord"
    class_name: ClassVar[str] = "MacromolecularStructureRecord"
    class_model_uri: ClassVar[URIRef] = CMM.MacromolecularStructureRecord

    structure_name: Union[str, MacromolecularStructureRecordStructureName] = None
    organism: Optional[str] = None
    components: Optional[str] = None
    download_url: Optional[Union[str, URI]] = None
    pdb_id: Optional[str] = None
    resolution: Optional[str] = None
    method: Optional[Union[str, "StructureMethodEnum"]] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self._is_empty(self.structure_name):
            self.MissingRequiredField("structure_name")
        if not isinstance(self.structure_name, MacromolecularStructureRecordStructureName):
            self.structure_name = MacromolecularStructureRecordStructureName(self.structure_name)

        if self.organism is not None and not isinstance(self.organism, str):
            self.organism = str(self.organism)

        if self.components is not None and not isinstance(self.components, str):
            self.components = str(self.components)

        if self.download_url is not None and not isinstance(self.download_url, URI):
            self.download_url = URI(self.download_url)

        if self.pdb_id is not None and not isinstance(self.pdb_id, str):
            self.pdb_id = str(self.pdb_id)

        if self.resolution is not None and not isinstance(self.resolution, str):
            self.resolution = str(self.resolution)

        if self.method is not None and not isinstance(self.method, StructureMethodEnum):
            self.method = StructureMethodEnum(self.method)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class PublicationRecord(YAMLRoot):
    """
    Scientific publication (peer-reviewed article, preprint, etc.)
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = CMM["PublicationRecord"]
    class_class_curie: ClassVar[str] = "cmm:PublicationRecord"
    class_name: ClassVar[str] = "PublicationRecord"
    class_model_uri: ClassVar[URIRef] = CMM.PublicationRecord

    url: Union[str, PublicationRecordUrl] = None
    title: str = None
    download_url: Optional[Union[str, URI]] = None
    journal: Optional[str] = None
    year: Optional[int] = None
    authors: Optional[str] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self._is_empty(self.url):
            self.MissingRequiredField("url")
        if not isinstance(self.url, PublicationRecordUrl):
            self.url = PublicationRecordUrl(self.url)

        if self._is_empty(self.title):
            self.MissingRequiredField("title")
        if not isinstance(self.title, str):
            self.title = str(self.title)

        if self.download_url is not None and not isinstance(self.download_url, URI):
            self.download_url = URI(self.download_url)

        if self.journal is not None and not isinstance(self.journal, str):
            self.journal = str(self.journal)

        if self.year is not None and not isinstance(self.year, int):
            self.year = int(self.year)

        if self.authors is not None and not isinstance(self.authors, str):
            self.authors = str(self.authors)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class DatasetRecord(YAMLRoot):
    """
    Research dataset from repositories (SRA, GEO, MetaboLights, etc.)
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = CMM["DatasetRecord"]
    class_class_curie: ClassVar[str] = "cmm:DatasetRecord"
    class_name: ClassVar[str] = "DatasetRecord"
    class_model_uri: ClassVar[URIRef] = CMM.DatasetRecord

    dataset_name: Union[str, DatasetRecordDatasetName] = None
    data_type: Optional[Union[str, "DataTypeEnum"]] = None
    url: Optional[Union[str, URI]] = None
    size: Optional[str] = None
    publication: Optional[str] = None
    license: Optional[str] = None
    download_url: Optional[Union[str, URI]] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self._is_empty(self.dataset_name):
            self.MissingRequiredField("dataset_name")
        if not isinstance(self.dataset_name, DatasetRecordDatasetName):
            self.dataset_name = DatasetRecordDatasetName(self.dataset_name)

        if self.data_type is not None and not isinstance(self.data_type, DataTypeEnum):
            self.data_type = DataTypeEnum(self.data_type)

        if self.url is not None and not isinstance(self.url, URI):
            self.url = URI(self.url)

        if self.size is not None and not isinstance(self.size, str):
            self.size = str(self.size)

        if self.publication is not None and not isinstance(self.publication, str):
            self.publication = str(self.publication)

        if self.license is not None and not isinstance(self.license, str):
            self.license = str(self.license)

        if self.download_url is not None and not isinstance(self.download_url, URI):
            self.download_url = URI(self.download_url)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class ChemicalCompoundRecord(YAMLRoot):
    """
    Chemical compound relevant to lanthanide bioprocessing (lanthanides, chelators, substrates, metabolites)
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = CMM["ChemicalCompoundRecord"]
    class_class_curie: ClassVar[str] = "cmm:ChemicalCompoundRecord"
    class_name: ClassVar[str] = "ChemicalCompoundRecord"
    class_model_uri: ClassVar[URIRef] = CMM.ChemicalCompoundRecord

    chemical_id: Union[str, ChemicalCompoundRecordChemicalId] = None
    chemical_name: str = None
    compound_type: Optional[Union[str, "CompoundTypeEnum"]] = None
    molecular_formula: Optional[str] = None
    molecular_weight: Optional[str] = None
    role_in_bioprocess: Optional[str] = None
    chebi_id: Optional[str] = None
    pubchem_id: Optional[int] = None
    chembl_id: Optional[str] = None
    properties: Optional[str] = None
    download_url: Optional[Union[str, URI]] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self._is_empty(self.chemical_id):
            self.MissingRequiredField("chemical_id")
        if not isinstance(self.chemical_id, ChemicalCompoundRecordChemicalId):
            self.chemical_id = ChemicalCompoundRecordChemicalId(self.chemical_id)

        if self._is_empty(self.chemical_name):
            self.MissingRequiredField("chemical_name")
        if not isinstance(self.chemical_name, str):
            self.chemical_name = str(self.chemical_name)

        if self.compound_type is not None and not isinstance(self.compound_type, CompoundTypeEnum):
            self.compound_type = CompoundTypeEnum(self.compound_type)

        if self.molecular_formula is not None and not isinstance(self.molecular_formula, str):
            self.molecular_formula = str(self.molecular_formula)

        if self.molecular_weight is not None and not isinstance(self.molecular_weight, str):
            self.molecular_weight = str(self.molecular_weight)

        if self.role_in_bioprocess is not None and not isinstance(self.role_in_bioprocess, str):
            self.role_in_bioprocess = str(self.role_in_bioprocess)

        if self.chebi_id is not None and not isinstance(self.chebi_id, str):
            self.chebi_id = str(self.chebi_id)

        if self.pubchem_id is not None and not isinstance(self.pubchem_id, int):
            self.pubchem_id = int(self.pubchem_id)

        if self.chembl_id is not None and not isinstance(self.chembl_id, str):
            self.chembl_id = str(self.chembl_id)

        if self.properties is not None and not isinstance(self.properties, str):
            self.properties = str(self.properties)

        if self.download_url is not None and not isinstance(self.download_url, URI):
            self.download_url = URI(self.download_url)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class AssayMeasurementRecord(YAMLRoot):
    """
    Analytical assay or measurement method for REE detection/quantification
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = CMM["AssayMeasurementRecord"]
    class_class_curie: ClassVar[str] = "cmm:AssayMeasurementRecord"
    class_name: ClassVar[str] = "AssayMeasurementRecord"
    class_model_uri: ClassVar[URIRef] = CMM.AssayMeasurementRecord

    assay_id: Union[str, AssayMeasurementRecordAssayId] = None
    assay_name: str = None
    assay_type: Optional[Union[str, "AssayTypeEnum"]] = None
    target_analytes: Optional[Union[str, list[str]]] = empty_list()
    detection_method: Optional[str] = None
    detection_limit: Optional[str] = None
    dynamic_range: Optional[str] = None
    protocol_reference: Optional[str] = None
    equipment_required: Optional[Union[str, list[str]]] = empty_list()
    sample_preparation: Optional[str] = None
    data_output_format: Optional[str] = None
    download_url: Optional[Union[str, URI]] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self._is_empty(self.assay_id):
            self.MissingRequiredField("assay_id")
        if not isinstance(self.assay_id, AssayMeasurementRecordAssayId):
            self.assay_id = AssayMeasurementRecordAssayId(self.assay_id)

        if self._is_empty(self.assay_name):
            self.MissingRequiredField("assay_name")
        if not isinstance(self.assay_name, str):
            self.assay_name = str(self.assay_name)

        if self.assay_type is not None and not isinstance(self.assay_type, AssayTypeEnum):
            self.assay_type = AssayTypeEnum(self.assay_type)

        if not isinstance(self.target_analytes, list):
            self.target_analytes = [self.target_analytes] if self.target_analytes is not None else []
        self.target_analytes = [v if isinstance(v, str) else str(v) for v in self.target_analytes]

        if self.detection_method is not None and not isinstance(self.detection_method, str):
            self.detection_method = str(self.detection_method)

        if self.detection_limit is not None and not isinstance(self.detection_limit, str):
            self.detection_limit = str(self.detection_limit)

        if self.dynamic_range is not None and not isinstance(self.dynamic_range, str):
            self.dynamic_range = str(self.dynamic_range)

        if self.protocol_reference is not None and not isinstance(self.protocol_reference, str):
            self.protocol_reference = str(self.protocol_reference)

        if not isinstance(self.equipment_required, list):
            self.equipment_required = [self.equipment_required] if self.equipment_required is not None else []
        self.equipment_required = [v if isinstance(v, str) else str(v) for v in self.equipment_required]

        if self.sample_preparation is not None and not isinstance(self.sample_preparation, str):
            self.sample_preparation = str(self.sample_preparation)

        if self.data_output_format is not None and not isinstance(self.data_output_format, str):
            self.data_output_format = str(self.data_output_format)

        if self.download_url is not None and not isinstance(self.download_url, URI):
            self.download_url = URI(self.download_url)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class BioprocessConditionsRecord(YAMLRoot):
    """
    Experimental conditions for REE biorecovery processes (bioleaching, biomineralization, biosorption)
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = CMM["BioprocessConditionsRecord"]
    class_class_curie: ClassVar[str] = "cmm:BioprocessConditionsRecord"
    class_name: ClassVar[str] = "BioprocessConditionsRecord"
    class_model_uri: ClassVar[URIRef] = CMM.BioprocessConditionsRecord

    process_id: Union[str, BioprocessConditionsRecordProcessId] = None
    process_name: str = None
    process_type: Optional[Union[str, "ProcessTypeEnum"]] = None
    strain_used: Optional[str] = None
    organism_used: Optional[str] = None
    growth_conditions: Optional[str] = None
    ree_concentration: Optional[str] = None
    contact_time: Optional[str] = None
    pH: Optional[str] = None
    temperature: Optional[str] = None
    competing_ions: Optional[Union[str, list[str]]] = empty_list()
    process_parameters: Optional[str] = None
    optimization_history: Optional[str] = None
    download_url: Optional[Union[str, URI]] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self._is_empty(self.process_id):
            self.MissingRequiredField("process_id")
        if not isinstance(self.process_id, BioprocessConditionsRecordProcessId):
            self.process_id = BioprocessConditionsRecordProcessId(self.process_id)

        if self._is_empty(self.process_name):
            self.MissingRequiredField("process_name")
        if not isinstance(self.process_name, str):
            self.process_name = str(self.process_name)

        if self.process_type is not None and not isinstance(self.process_type, ProcessTypeEnum):
            self.process_type = ProcessTypeEnum(self.process_type)

        if self.strain_used is not None and not isinstance(self.strain_used, str):
            self.strain_used = str(self.strain_used)

        if self.organism_used is not None and not isinstance(self.organism_used, str):
            self.organism_used = str(self.organism_used)

        if self.growth_conditions is not None and not isinstance(self.growth_conditions, str):
            self.growth_conditions = str(self.growth_conditions)

        if self.ree_concentration is not None and not isinstance(self.ree_concentration, str):
            self.ree_concentration = str(self.ree_concentration)

        if self.contact_time is not None and not isinstance(self.contact_time, str):
            self.contact_time = str(self.contact_time)

        if self.pH is not None and not isinstance(self.pH, str):
            self.pH = str(self.pH)

        if self.temperature is not None and not isinstance(self.temperature, str):
            self.temperature = str(self.temperature)

        if not isinstance(self.competing_ions, list):
            self.competing_ions = [self.competing_ions] if self.competing_ions is not None else []
        self.competing_ions = [v if isinstance(v, str) else str(v) for v in self.competing_ions]

        if self.process_parameters is not None and not isinstance(self.process_parameters, str):
            self.process_parameters = str(self.process_parameters)

        if self.optimization_history is not None and not isinstance(self.optimization_history, str):
            self.optimization_history = str(self.optimization_history)

        if self.download_url is not None and not isinstance(self.download_url, URI):
            self.download_url = URI(self.download_url)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class ScreeningResultRecord(YAMLRoot):
    """
    High-throughput screening result from automated strain/condition testing
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = CMM["ScreeningResultRecord"]
    class_class_curie: ClassVar[str] = "cmm:ScreeningResultRecord"
    class_name: ClassVar[str] = "ScreeningResultRecord"
    class_model_uri: ClassVar[URIRef] = CMM.ScreeningResultRecord

    experiment_id: Union[str, ScreeningResultRecordExperimentId] = None
    plate_coordinates: Optional[str] = None
    strain_barcode: Optional[str] = None
    screening_assay: Optional[str] = None
    target_ree: Optional[Union[str, list[str]]] = empty_list()
    measurement_values: Optional[str] = None
    hit_classification: Optional[Union[str, "HitClassificationEnum"]] = None
    validation_status: Optional[str] = None
    follow_up_experiments: Optional[Union[str, list[str]]] = empty_list()
    assay_reference: Optional[str] = None
    download_url: Optional[Union[str, URI]] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self._is_empty(self.experiment_id):
            self.MissingRequiredField("experiment_id")
        if not isinstance(self.experiment_id, ScreeningResultRecordExperimentId):
            self.experiment_id = ScreeningResultRecordExperimentId(self.experiment_id)

        if self.plate_coordinates is not None and not isinstance(self.plate_coordinates, str):
            self.plate_coordinates = str(self.plate_coordinates)

        if self.strain_barcode is not None and not isinstance(self.strain_barcode, str):
            self.strain_barcode = str(self.strain_barcode)

        if self.screening_assay is not None and not isinstance(self.screening_assay, str):
            self.screening_assay = str(self.screening_assay)

        if not isinstance(self.target_ree, list):
            self.target_ree = [self.target_ree] if self.target_ree is not None else []
        self.target_ree = [v if isinstance(v, str) else str(v) for v in self.target_ree]

        if self.measurement_values is not None and not isinstance(self.measurement_values, str):
            self.measurement_values = str(self.measurement_values)

        if self.hit_classification is not None and not isinstance(self.hit_classification, HitClassificationEnum):
            self.hit_classification = HitClassificationEnum(self.hit_classification)

        if self.validation_status is not None and not isinstance(self.validation_status, str):
            self.validation_status = str(self.validation_status)

        if not isinstance(self.follow_up_experiments, list):
            self.follow_up_experiments = [self.follow_up_experiments] if self.follow_up_experiments is not None else []
        self.follow_up_experiments = [v if isinstance(v, str) else str(v) for v in self.follow_up_experiments]

        if self.assay_reference is not None and not isinstance(self.assay_reference, str):
            self.assay_reference = str(self.assay_reference)

        if self.download_url is not None and not isinstance(self.download_url, URI):
            self.download_url = URI(self.download_url)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class ProtocolRecord(YAMLRoot):
    """
    Experimental protocol or standard operating procedure (SOP)
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = CMM["ProtocolRecord"]
    class_class_curie: ClassVar[str] = "cmm:ProtocolRecord"
    class_name: ClassVar[str] = "ProtocolRecord"
    class_model_uri: ClassVar[URIRef] = CMM.ProtocolRecord

    protocol_id: Union[str, ProtocolRecordProtocolId] = None
    protocol_name: str = None
    protocol_type: Optional[Union[str, "ProtocolTypeEnum"]] = None
    protocol_version: Optional[str] = None
    protocol_doi: Optional[str] = None
    protocol_url: Optional[Union[str, URI]] = None
    associated_assays: Optional[Union[str, list[str]]] = empty_list()
    equipment_list: Optional[Union[str, list[str]]] = empty_list()
    success_criteria: Optional[str] = None
    quality_control: Optional[str] = None
    dbtl_iteration: Optional[str] = None
    validation_status: Optional[str] = None
    user_notes: Optional[str] = None
    download_url: Optional[Union[str, URI]] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self._is_empty(self.protocol_id):
            self.MissingRequiredField("protocol_id")
        if not isinstance(self.protocol_id, ProtocolRecordProtocolId):
            self.protocol_id = ProtocolRecordProtocolId(self.protocol_id)

        if self._is_empty(self.protocol_name):
            self.MissingRequiredField("protocol_name")
        if not isinstance(self.protocol_name, str):
            self.protocol_name = str(self.protocol_name)

        if self.protocol_type is not None and not isinstance(self.protocol_type, ProtocolTypeEnum):
            self.protocol_type = ProtocolTypeEnum(self.protocol_type)

        if self.protocol_version is not None and not isinstance(self.protocol_version, str):
            self.protocol_version = str(self.protocol_version)

        if self.protocol_doi is not None and not isinstance(self.protocol_doi, str):
            self.protocol_doi = str(self.protocol_doi)

        if self.protocol_url is not None and not isinstance(self.protocol_url, URI):
            self.protocol_url = URI(self.protocol_url)

        if not isinstance(self.associated_assays, list):
            self.associated_assays = [self.associated_assays] if self.associated_assays is not None else []
        self.associated_assays = [v if isinstance(v, str) else str(v) for v in self.associated_assays]

        if not isinstance(self.equipment_list, list):
            self.equipment_list = [self.equipment_list] if self.equipment_list is not None else []
        self.equipment_list = [v if isinstance(v, str) else str(v) for v in self.equipment_list]

        if self.success_criteria is not None and not isinstance(self.success_criteria, str):
            self.success_criteria = str(self.success_criteria)

        if self.quality_control is not None and not isinstance(self.quality_control, str):
            self.quality_control = str(self.quality_control)

        if self.dbtl_iteration is not None and not isinstance(self.dbtl_iteration, str):
            self.dbtl_iteration = str(self.dbtl_iteration)

        if self.validation_status is not None and not isinstance(self.validation_status, str):
            self.validation_status = str(self.validation_status)

        if self.user_notes is not None and not isinstance(self.user_notes, str):
            self.user_notes = str(self.user_notes)

        if self.download_url is not None and not isinstance(self.download_url, URI):
            self.download_url = URI(self.download_url)

        super().__post_init__(**kwargs)


# Enumerations
class StructureMethodEnum(EnumDefinitionImpl):
    """
    Method for structure determination
    """
    _defn = EnumDefinition(
        name="StructureMethodEnum",
        description="Method for structure determination",
    )

    @classmethod
    def _addvals(cls):
        setattr(cls, "X-ray crystallography",
            PermissibleValue(
                text="X-ray crystallography",
                description="X-ray diffraction of crystallized molecules"))
        setattr(cls, "NMR spectroscopy",
            PermissibleValue(
                text="NMR spectroscopy",
                description="Nuclear magnetic resonance spectroscopy"))
        setattr(cls, "Cryo-EM",
            PermissibleValue(
                text="Cryo-EM",
                description="Cryo-electron microscopy"))
        setattr(cls, "Predicted structure",
            PermissibleValue(
                text="Predicted structure",
                description="Computational prediction (e.g., AlphaFold)"))
        setattr(cls, "Homology modeling",
            PermissibleValue(
                text="Homology modeling",
                description="Model based on homologous structures"))
        setattr(cls, "Computational prediction",
            PermissibleValue(
                text="Computational prediction",
                description="Ab initio or other computational methods"))
        setattr(cls, "Chemical characterization",
            PermissibleValue(
                text="Chemical characterization",
                description="Chemical analysis methods"))
        setattr(cls, "Multiple methods",
            PermissibleValue(
                text="Multiple methods",
                description="Combination of experimental methods"))

class DataTypeEnum(EnumDefinitionImpl):
    """
    Type of research dataset
    """
    transcriptomics = PermissibleValue(
        text="transcriptomics",
        description="Transcriptome analysis data")
    proteomics = PermissibleValue(
        text="proteomics",
        description="Protein expression/identification data")
    metabolomics = PermissibleValue(
        text="metabolomics",
        description="Metabolite profiling data")
    metagenomics = PermissibleValue(
        text="metagenomics",
        description="Metagenomic sequencing data")
    pathways = PermissibleValue(
        text="pathways",
        description="Metabolic pathway databases")
    thermodynamics = PermissibleValue(
        text="thermodynamics",
        description="Thermodynamic data")

    _defn = EnumDefinition(
        name="DataTypeEnum",
        description="Type of research dataset",
    )

    @classmethod
    def _addvals(cls):
        setattr(cls, "genomic DNA sequencing",
            PermissibleValue(
                text="genomic DNA sequencing",
                description="Whole genome sequencing data"))
        setattr(cls, "RNA-seq",
            PermissibleValue(
                text="RNA-seq",
                description="RNA sequencing data"))
        setattr(cls, "16S rRNA",
            PermissibleValue(
                text="16S rRNA",
                description="16S ribosomal RNA amplicon data"))
        setattr(cls, "protein sequences",
            PermissibleValue(
                text="protein sequences",
                description="Protein sequence databases"))
        setattr(cls, "metabolic compounds",
            PermissibleValue(
                text="metabolic compounds",
                description="Chemical compound databases"))
        setattr(cls, "mass spectrometry",
            PermissibleValue(
                text="mass spectrometry",
                description="MS/MS or LC-MS data"))
        setattr(cls, "annotated genomes",
            PermissibleValue(
                text="annotated genomes",
                description="Annotated genome assemblies"))
        setattr(cls, "3D protein structures",
            PermissibleValue(
                text="3D protein structures",
                description="Structural biology data"))

class CompoundTypeEnum(EnumDefinitionImpl):
    """
    Type of chemical compound
    """
    lanthanide = PermissibleValue(
        text="lanthanide",
        description="Rare earth element (La, Ce, Nd, Eu, Tb, Gd, etc.)")
    lanthanophore = PermissibleValue(
        text="lanthanophore",
        description="Lanthanide-chelating siderophore")
    chelator = PermissibleValue(
        text="chelator",
        description="Metal-chelating compound")
    substrate = PermissibleValue(
        text="substrate",
        description="Metabolic substrate")
    product = PermissibleValue(
        text="product",
        description="Metabolic product")
    metabolite = PermissibleValue(
        text="metabolite",
        description="Intermediate metabolite")
    cofactor = PermissibleValue(
        text="cofactor",
        description="Enzymatic cofactor")
    extractant = PermissibleValue(
        text="extractant",
        description="Solvent extraction reagent")
    sensitizer = PermissibleValue(
        text="sensitizer",
        description="Luminescence sensitizer")

    _defn = EnumDefinition(
        name="CompoundTypeEnum",
        description="Type of chemical compound",
    )

class AssayTypeEnum(EnumDefinitionImpl):
    """
    Type of analytical assay
    """
    FACS = PermissibleValue(
        text="FACS",
        description="Fluorescence-activated cell sorting")
    HPLC = PermissibleValue(
        text="HPLC",
        description="High-performance liquid chromatography")

    _defn = EnumDefinition(
        name="AssayTypeEnum",
        description="Type of analytical assay",
    )

    @classmethod
    def _addvals(cls):
        setattr(cls, "time-resolved luminescence (TRL)",
            PermissibleValue(
                text="time-resolved luminescence (TRL)",
                description="Time-resolved lanthanide luminescence"))
        setattr(cls, "ICP-OES",
            PermissibleValue(
                text="ICP-OES",
                description="Inductively coupled plasma optical emission spectrometry"))
        setattr(cls, "ICP-MS",
            PermissibleValue(
                text="ICP-MS",
                description="Inductively coupled plasma mass spectrometry"))
        setattr(cls, "fluorescence spectroscopy",
            PermissibleValue(
                text="fluorescence spectroscopy",
                description="Fluorescence emission spectroscopy"))
        setattr(cls, "absorbance spectroscopy",
            PermissibleValue(
                text="absorbance spectroscopy",
                description="UV-Vis absorbance spectroscopy"))
        setattr(cls, "mass spectrometry",
            PermissibleValue(
                text="mass spectrometry",
                description="General mass spectrometry"))
        setattr(cls, "LC-MS",
            PermissibleValue(
                text="LC-MS",
                description="Liquid chromatography-mass spectrometry"))
        setattr(cls, "confocal microscopy",
            PermissibleValue(
                text="confocal microscopy",
                description="Confocal fluorescence microscopy"))
        setattr(cls, "electron microscopy",
            PermissibleValue(
                text="electron microscopy",
                description="SEM or TEM imaging"))
        setattr(cls, "growth assay",
            PermissibleValue(
                text="growth assay",
                description="Microbial growth measurement"))
        setattr(cls, "viability assay",
            PermissibleValue(
                text="viability assay",
                description="Cell viability assessment"))

class ProcessTypeEnum(EnumDefinitionImpl):
    """
    Type of bioprocess
    """
    bioleaching = PermissibleValue(
        text="bioleaching",
        description="Microbial leaching of REEs from solid substrates")
    biomineralization = PermissibleValue(
        text="biomineralization",
        description="Microbial precipitation of REE minerals")
    biosorption = PermissibleValue(
        text="biosorption",
        description="Surface adsorption of REEs by biomass")
    bioaccumulation = PermissibleValue(
        text="bioaccumulation",
        description="Intracellular accumulation of REEs")
    fermentation = PermissibleValue(
        text="fermentation",
        description="Fermentative production of metabolites")
    bioextraction = PermissibleValue(
        text="bioextraction",
        description="Combined bio-based extraction process")

    _defn = EnumDefinition(
        name="ProcessTypeEnum",
        description="Type of bioprocess",
    )

class HitClassificationEnum(EnumDefinitionImpl):
    """
    Classification of screening hits
    """
    positive = PermissibleValue(
        text="positive",
        description="Strong positive hit")
    negative = PermissibleValue(
        text="negative",
        description="Negative control or no activity")
    borderline = PermissibleValue(
        text="borderline",
        description="Weak or borderline hit")
    validated = PermissibleValue(
        text="validated",
        description="Validated positive hit")

    _defn = EnumDefinition(
        name="HitClassificationEnum",
        description="Classification of screening hits",
    )

    @classmethod
    def _addvals(cls):
        setattr(cls, "false positive",
            PermissibleValue(
                text="false positive",
                description="Suspected false positive"))

class ProtocolTypeEnum(EnumDefinitionImpl):
    """
    Type of experimental protocol
    """
    _defn = EnumDefinition(
        name="ProtocolTypeEnum",
        description="Type of experimental protocol",
    )

    @classmethod
    def _addvals(cls):
        setattr(cls, "assay protocol",
            PermissibleValue(
                text="assay protocol",
                description="Analytical assay procedure"))
        setattr(cls, "cultivation protocol",
            PermissibleValue(
                text="cultivation protocol",
                description="Microbial cultivation procedure"))
        setattr(cls, "extraction protocol",
            PermissibleValue(
                text="extraction protocol",
                description="Extraction/purification procedure"))
        setattr(cls, "transformation protocol",
            PermissibleValue(
                text="transformation protocol",
                description="Genetic transformation procedure"))
        setattr(cls, "screening protocol",
            PermissibleValue(
                text="screening protocol",
                description="High-throughput screening procedure"))
        setattr(cls, "sample preparation",
            PermissibleValue(
                text="sample preparation",
                description="Sample preparation procedure"))
        setattr(cls, "quality control",
            PermissibleValue(
                text="quality control",
                description="QC/validation procedure"))

# Slots
class slots:
    pass

slots.scientific_name = Slot(uri=SCHEMA.scientificName, name="scientific_name", curie=SCHEMA.curie('scientificName'),
                   model_uri=CMM.scientific_name, domain=None, range=Optional[str])

slots.ncbi_taxon_id = Slot(uri=NCBITAXON.id, name="ncbi_taxon_id", curie=NCBITAXON.curie('id'),
                   model_uri=CMM.ncbi_taxon_id, domain=None, range=Optional[int])

slots.genome_identifier = Slot(uri=CMM.genome_identifier, name="genome_identifier", curie=CMM.curie('genome_identifier'),
                   model_uri=CMM.genome_identifier, domain=None, range=Optional[str],
                   pattern=re.compile(r'^(GC[AF]_\d+\.\d+|\d+\.\d+)?$'))

slots.annotation_download_url = Slot(uri=CMM.annotation_download_url, name="annotation_download_url", curie=CMM.curie('annotation_download_url'),
                   model_uri=CMM.annotation_download_url, domain=None, range=Optional[Union[str, URI]])

slots.sample_name = Slot(uri=SCHEMA.name, name="sample_name", curie=SCHEMA.curie('name'),
                   model_uri=CMM.sample_name, domain=None, range=Optional[str])

slots.sample_id = Slot(uri=CMM.sample_id, name="sample_id", curie=CMM.curie('sample_id'),
                   model_uri=CMM.sample_id, domain=None, range=Optional[str],
                   pattern=re.compile(r'^SAM[NDE][A-Z]?\d+$'))

slots.organism = Slot(uri=SCHEMA.organism, name="organism", curie=SCHEMA.curie('organism'),
                   model_uri=CMM.organism, domain=None, range=Optional[str])

slots.pathway_name = Slot(uri=SCHEMA.name, name="pathway_name", curie=SCHEMA.curie('name'),
                   model_uri=CMM.pathway_name, domain=None, range=Optional[str])

slots.pathway_id = Slot(uri=CMM.pathway_id, name="pathway_id", curie=CMM.curie('pathway_id'),
                   model_uri=CMM.pathway_id, domain=None, range=Optional[str],
                   pattern=re.compile(r'^(ko\d+|path:map\d+|PWY-\d+|PWY\d+|Custom_[A-Z0-9]+)$'))

slots.genes = Slot(uri=CMM.genes, name="genes", curie=CMM.curie('genes'),
                   model_uri=CMM.genes, domain=None, range=Optional[Union[str, list[str]]])

slots.genes_kegg = Slot(uri=CMM.genes_kegg, name="genes_kegg", curie=CMM.curie('genes_kegg'),
                   model_uri=CMM.genes_kegg, domain=None, range=Optional[Union[str, list[str]]])

slots.gene_protein_id = Slot(uri=CMM.gene_protein_id, name="gene_protein_id", curie=CMM.curie('gene_protein_id'),
                   model_uri=CMM.gene_protein_id, domain=None, range=Optional[str],
                   pattern=re.compile(r'^(K\d+(_[A-Za-z0-9]+)?|[OPQ][0-9][A-Z0-9]{3}[0-9]|[A-NR-Z][0-9]([A-Z][A-Z0-9]{2}[0-9]){1,2}|custom_[\w]+)?$'))

slots.annotation = Slot(uri=SCHEMA.description, name="annotation", curie=SCHEMA.curie('description'),
                   model_uri=CMM.annotation, domain=None, range=Optional[str])

slots.ec_number = Slot(uri=CMM.ec_number, name="ec_number", curie=CMM.curie('ec_number'),
                   model_uri=CMM.ec_number, domain=None, range=Optional[str],
                   pattern=re.compile(r'^\d+\.\d+\.\d+\.\d+$'))

slots.go_terms = Slot(uri=CMM.go_terms, name="go_terms", curie=CMM.curie('go_terms'),
                   model_uri=CMM.go_terms, domain=None, range=Optional[Union[str, list[str]]],
                   pattern=re.compile(r'^GO:\d{7}'))

slots.chebi_terms = Slot(uri=CMM.chebi_terms, name="chebi_terms", curie=CMM.curie('chebi_terms'),
                   model_uri=CMM.chebi_terms, domain=None, range=Optional[Union[str, list[str]]],
                   pattern=re.compile(r'^CHEBI:\d+'))

slots.structure_name = Slot(uri=SCHEMA.name, name="structure_name", curie=SCHEMA.curie('name'),
                   model_uri=CMM.structure_name, domain=None, range=Optional[str])

slots.components = Slot(uri=CMM.components, name="components", curie=CMM.curie('components'),
                   model_uri=CMM.components, domain=None, range=Optional[str])

slots.pdb_id = Slot(uri=CMM.pdb_id, name="pdb_id", curie=CMM.curie('pdb_id'),
                   model_uri=CMM.pdb_id, domain=None, range=Optional[str])

slots.resolution = Slot(uri=CMM.resolution, name="resolution", curie=CMM.curie('resolution'),
                   model_uri=CMM.resolution, domain=None, range=Optional[str])

slots.method = Slot(uri=CMM.method, name="method", curie=CMM.curie('method'),
                   model_uri=CMM.method, domain=None, range=Optional[Union[str, "StructureMethodEnum"]])

slots.url = Slot(uri=SCHEMA.url, name="url", curie=SCHEMA.curie('url'),
                   model_uri=CMM.url, domain=None, range=Optional[Union[str, URI]])

slots.title = Slot(uri=SCHEMA.headline, name="title", curie=SCHEMA.curie('headline'),
                   model_uri=CMM.title, domain=None, range=Optional[str])

slots.journal = Slot(uri=SCHEMA.publisher, name="journal", curie=SCHEMA.curie('publisher'),
                   model_uri=CMM.journal, domain=None, range=Optional[str])

slots.year = Slot(uri=SCHEMA.datePublished, name="year", curie=SCHEMA.curie('datePublished'),
                   model_uri=CMM.year, domain=None, range=Optional[int])

slots.authors = Slot(uri=SCHEMA.author, name="authors", curie=SCHEMA.curie('author'),
                   model_uri=CMM.authors, domain=None, range=Optional[str])

slots.dataset_name = Slot(uri=SCHEMA.name, name="dataset_name", curie=SCHEMA.curie('name'),
                   model_uri=CMM.dataset_name, domain=None, range=Optional[str])

slots.data_type = Slot(uri=CMM.data_type, name="data_type", curie=CMM.curie('data_type'),
                   model_uri=CMM.data_type, domain=None, range=Optional[Union[str, "DataTypeEnum"]])

slots.size = Slot(uri=CMM.size, name="size", curie=CMM.curie('size'),
                   model_uri=CMM.size, domain=None, range=Optional[str])

slots.publication = Slot(uri=CMM.publication, name="publication", curie=CMM.curie('publication'),
                   model_uri=CMM.publication, domain=None, range=Optional[str])

slots.license = Slot(uri=SCHEMA.license, name="license", curie=SCHEMA.curie('license'),
                   model_uri=CMM.license, domain=None, range=Optional[str])

slots.download_url = Slot(uri=SCHEMA.contentUrl, name="download_url", curie=SCHEMA.curie('contentUrl'),
                   model_uri=CMM.download_url, domain=None, range=Optional[Union[str, URI]])

slots.chemical_id = Slot(uri=SCHEMA.identifier, name="chemical_id", curie=SCHEMA.curie('identifier'),
                   model_uri=CMM.chemical_id, domain=None, range=Optional[str])

slots.chemical_name = Slot(uri=SCHEMA.name, name="chemical_name", curie=SCHEMA.curie('name'),
                   model_uri=CMM.chemical_name, domain=None, range=Optional[str])

slots.compound_type = Slot(uri=CMM.compound_type, name="compound_type", curie=CMM.curie('compound_type'),
                   model_uri=CMM.compound_type, domain=None, range=Optional[Union[str, "CompoundTypeEnum"]])

slots.molecular_formula = Slot(uri=CMM.molecular_formula, name="molecular_formula", curie=CMM.curie('molecular_formula'),
                   model_uri=CMM.molecular_formula, domain=None, range=Optional[str])

slots.molecular_weight = Slot(uri=CMM.molecular_weight, name="molecular_weight", curie=CMM.curie('molecular_weight'),
                   model_uri=CMM.molecular_weight, domain=None, range=Optional[str])

slots.role_in_bioprocess = Slot(uri=CMM.role_in_bioprocess, name="role_in_bioprocess", curie=CMM.curie('role_in_bioprocess'),
                   model_uri=CMM.role_in_bioprocess, domain=None, range=Optional[str])

slots.chebi_id = Slot(uri=CMM.chebi_id, name="chebi_id", curie=CMM.curie('chebi_id'),
                   model_uri=CMM.chebi_id, domain=None, range=Optional[str],
                   pattern=re.compile(r'^CHEBI:\d+$'))

slots.pubchem_id = Slot(uri=CMM.pubchem_id, name="pubchem_id", curie=CMM.curie('pubchem_id'),
                   model_uri=CMM.pubchem_id, domain=None, range=Optional[int])

slots.chembl_id = Slot(uri=CMM.chembl_id, name="chembl_id", curie=CMM.curie('chembl_id'),
                   model_uri=CMM.chembl_id, domain=None, range=Optional[str],
                   pattern=re.compile(r'^CHEMBL\d+$'))

slots.properties = Slot(uri=CMM.properties, name="properties", curie=CMM.curie('properties'),
                   model_uri=CMM.properties, domain=None, range=Optional[str])

slots.assay_id = Slot(uri=SCHEMA.identifier, name="assay_id", curie=SCHEMA.curie('identifier'),
                   model_uri=CMM.assay_id, domain=None, range=Optional[str])

slots.assay_name = Slot(uri=SCHEMA.name, name="assay_name", curie=SCHEMA.curie('name'),
                   model_uri=CMM.assay_name, domain=None, range=Optional[str])

slots.assay_type = Slot(uri=CMM.assay_type, name="assay_type", curie=CMM.curie('assay_type'),
                   model_uri=CMM.assay_type, domain=None, range=Optional[Union[str, "AssayTypeEnum"]])

slots.target_analytes = Slot(uri=CMM.target_analytes, name="target_analytes", curie=CMM.curie('target_analytes'),
                   model_uri=CMM.target_analytes, domain=None, range=Optional[Union[str, list[str]]])

slots.detection_method = Slot(uri=CMM.detection_method, name="detection_method", curie=CMM.curie('detection_method'),
                   model_uri=CMM.detection_method, domain=None, range=Optional[str])

slots.detection_limit = Slot(uri=CMM.detection_limit, name="detection_limit", curie=CMM.curie('detection_limit'),
                   model_uri=CMM.detection_limit, domain=None, range=Optional[str])

slots.dynamic_range = Slot(uri=CMM.dynamic_range, name="dynamic_range", curie=CMM.curie('dynamic_range'),
                   model_uri=CMM.dynamic_range, domain=None, range=Optional[str])

slots.protocol_reference = Slot(uri=CMM.protocol_reference, name="protocol_reference", curie=CMM.curie('protocol_reference'),
                   model_uri=CMM.protocol_reference, domain=None, range=Optional[str])

slots.equipment_required = Slot(uri=CMM.equipment_required, name="equipment_required", curie=CMM.curie('equipment_required'),
                   model_uri=CMM.equipment_required, domain=None, range=Optional[Union[str, list[str]]])

slots.sample_preparation = Slot(uri=CMM.sample_preparation, name="sample_preparation", curie=CMM.curie('sample_preparation'),
                   model_uri=CMM.sample_preparation, domain=None, range=Optional[str])

slots.data_output_format = Slot(uri=CMM.data_output_format, name="data_output_format", curie=CMM.curie('data_output_format'),
                   model_uri=CMM.data_output_format, domain=None, range=Optional[str])

slots.process_id = Slot(uri=SCHEMA.identifier, name="process_id", curie=SCHEMA.curie('identifier'),
                   model_uri=CMM.process_id, domain=None, range=Optional[str])

slots.process_name = Slot(uri=SCHEMA.name, name="process_name", curie=SCHEMA.curie('name'),
                   model_uri=CMM.process_name, domain=None, range=Optional[str])

slots.process_type = Slot(uri=CMM.process_type, name="process_type", curie=CMM.curie('process_type'),
                   model_uri=CMM.process_type, domain=None, range=Optional[Union[str, "ProcessTypeEnum"]])

slots.strain_used = Slot(uri=CMM.strain_used, name="strain_used", curie=CMM.curie('strain_used'),
                   model_uri=CMM.strain_used, domain=None, range=Optional[str])

slots.organism_used = Slot(uri=CMM.organism_used, name="organism_used", curie=CMM.curie('organism_used'),
                   model_uri=CMM.organism_used, domain=None, range=Optional[str])

slots.growth_conditions = Slot(uri=CMM.growth_conditions, name="growth_conditions", curie=CMM.curie('growth_conditions'),
                   model_uri=CMM.growth_conditions, domain=None, range=Optional[str])

slots.ree_concentration = Slot(uri=CMM.ree_concentration, name="ree_concentration", curie=CMM.curie('ree_concentration'),
                   model_uri=CMM.ree_concentration, domain=None, range=Optional[str])

slots.contact_time = Slot(uri=CMM.contact_time, name="contact_time", curie=CMM.curie('contact_time'),
                   model_uri=CMM.contact_time, domain=None, range=Optional[str])

slots.pH = Slot(uri=CMM.pH, name="pH", curie=CMM.curie('pH'),
                   model_uri=CMM.pH, domain=None, range=Optional[str])

slots.temperature = Slot(uri=CMM.temperature, name="temperature", curie=CMM.curie('temperature'),
                   model_uri=CMM.temperature, domain=None, range=Optional[str])

slots.competing_ions = Slot(uri=CMM.competing_ions, name="competing_ions", curie=CMM.curie('competing_ions'),
                   model_uri=CMM.competing_ions, domain=None, range=Optional[Union[str, list[str]]])

slots.process_parameters = Slot(uri=CMM.process_parameters, name="process_parameters", curie=CMM.curie('process_parameters'),
                   model_uri=CMM.process_parameters, domain=None, range=Optional[str])

slots.optimization_history = Slot(uri=CMM.optimization_history, name="optimization_history", curie=CMM.curie('optimization_history'),
                   model_uri=CMM.optimization_history, domain=None, range=Optional[str])

slots.experiment_id = Slot(uri=SCHEMA.identifier, name="experiment_id", curie=SCHEMA.curie('identifier'),
                   model_uri=CMM.experiment_id, domain=None, range=Optional[str])

slots.plate_coordinates = Slot(uri=CMM.plate_coordinates, name="plate_coordinates", curie=CMM.curie('plate_coordinates'),
                   model_uri=CMM.plate_coordinates, domain=None, range=Optional[str])

slots.strain_barcode = Slot(uri=CMM.strain_barcode, name="strain_barcode", curie=CMM.curie('strain_barcode'),
                   model_uri=CMM.strain_barcode, domain=None, range=Optional[str])

slots.screening_assay = Slot(uri=CMM.screening_assay, name="screening_assay", curie=CMM.curie('screening_assay'),
                   model_uri=CMM.screening_assay, domain=None, range=Optional[str])

slots.target_ree = Slot(uri=CMM.target_ree, name="target_ree", curie=CMM.curie('target_ree'),
                   model_uri=CMM.target_ree, domain=None, range=Optional[Union[str, list[str]]])

slots.measurement_values = Slot(uri=CMM.measurement_values, name="measurement_values", curie=CMM.curie('measurement_values'),
                   model_uri=CMM.measurement_values, domain=None, range=Optional[str])

slots.hit_classification = Slot(uri=CMM.hit_classification, name="hit_classification", curie=CMM.curie('hit_classification'),
                   model_uri=CMM.hit_classification, domain=None, range=Optional[Union[str, "HitClassificationEnum"]])

slots.validation_status = Slot(uri=CMM.validation_status, name="validation_status", curie=CMM.curie('validation_status'),
                   model_uri=CMM.validation_status, domain=None, range=Optional[str])

slots.follow_up_experiments = Slot(uri=CMM.follow_up_experiments, name="follow_up_experiments", curie=CMM.curie('follow_up_experiments'),
                   model_uri=CMM.follow_up_experiments, domain=None, range=Optional[Union[str, list[str]]])

slots.assay_reference = Slot(uri=CMM.assay_reference, name="assay_reference", curie=CMM.curie('assay_reference'),
                   model_uri=CMM.assay_reference, domain=None, range=Optional[str])

slots.protocol_id = Slot(uri=SCHEMA.identifier, name="protocol_id", curie=SCHEMA.curie('identifier'),
                   model_uri=CMM.protocol_id, domain=None, range=Optional[str])

slots.protocol_name = Slot(uri=SCHEMA.name, name="protocol_name", curie=SCHEMA.curie('name'),
                   model_uri=CMM.protocol_name, domain=None, range=Optional[str])

slots.protocol_type = Slot(uri=CMM.protocol_type, name="protocol_type", curie=CMM.curie('protocol_type'),
                   model_uri=CMM.protocol_type, domain=None, range=Optional[Union[str, "ProtocolTypeEnum"]])

slots.protocol_version = Slot(uri=CMM.protocol_version, name="protocol_version", curie=CMM.curie('protocol_version'),
                   model_uri=CMM.protocol_version, domain=None, range=Optional[str])

slots.protocol_doi = Slot(uri=CMM.protocol_doi, name="protocol_doi", curie=CMM.curie('protocol_doi'),
                   model_uri=CMM.protocol_doi, domain=None, range=Optional[str])

slots.protocol_url = Slot(uri=CMM.protocol_url, name="protocol_url", curie=CMM.curie('protocol_url'),
                   model_uri=CMM.protocol_url, domain=None, range=Optional[Union[str, URI]])

slots.associated_assays = Slot(uri=CMM.associated_assays, name="associated_assays", curie=CMM.curie('associated_assays'),
                   model_uri=CMM.associated_assays, domain=None, range=Optional[Union[str, list[str]]])

slots.equipment_list = Slot(uri=CMM.equipment_list, name="equipment_list", curie=CMM.curie('equipment_list'),
                   model_uri=CMM.equipment_list, domain=None, range=Optional[Union[str, list[str]]])

slots.success_criteria = Slot(uri=CMM.success_criteria, name="success_criteria", curie=CMM.curie('success_criteria'),
                   model_uri=CMM.success_criteria, domain=None, range=Optional[str])

slots.quality_control = Slot(uri=CMM.quality_control, name="quality_control", curie=CMM.curie('quality_control'),
                   model_uri=CMM.quality_control, domain=None, range=Optional[str])

slots.dbtl_iteration = Slot(uri=CMM.dbtl_iteration, name="dbtl_iteration", curie=CMM.curie('dbtl_iteration'),
                   model_uri=CMM.dbtl_iteration, domain=None, range=Optional[str])

slots.user_notes = Slot(uri=CMM.user_notes, name="user_notes", curie=CMM.curie('user_notes'),
                   model_uri=CMM.user_notes, domain=None, range=Optional[str])

slots.lanthanideBioprocessingDatabase__genomes = Slot(uri=CMM.genomes, name="lanthanideBioprocessingDatabase__genomes", curie=CMM.curie('genomes'),
                   model_uri=CMM.lanthanideBioprocessingDatabase__genomes, domain=None, range=Optional[Union[dict[Union[str, GenomeRecordScientificName], Union[dict, GenomeRecord]], list[Union[dict, GenomeRecord]]]])

slots.lanthanideBioprocessingDatabase__biosamples = Slot(uri=CMM.biosamples, name="lanthanideBioprocessingDatabase__biosamples", curie=CMM.curie('biosamples'),
                   model_uri=CMM.lanthanideBioprocessingDatabase__biosamples, domain=None, range=Optional[Union[dict[Union[str, BiosampleRecordSampleId], Union[dict, BiosampleRecord]], list[Union[dict, BiosampleRecord]]]])

slots.lanthanideBioprocessingDatabase__pathways = Slot(uri=CMM.pathways, name="lanthanideBioprocessingDatabase__pathways", curie=CMM.curie('pathways'),
                   model_uri=CMM.lanthanideBioprocessingDatabase__pathways, domain=None, range=Optional[Union[dict[Union[str, PathwayRecordPathwayId], Union[dict, PathwayRecord]], list[Union[dict, PathwayRecord]]]])

slots.lanthanideBioprocessingDatabase__genes_proteins = Slot(uri=CMM.genes_proteins, name="lanthanideBioprocessingDatabase__genes_proteins", curie=CMM.curie('genes_proteins'),
                   model_uri=CMM.lanthanideBioprocessingDatabase__genes_proteins, domain=None, range=Optional[Union[dict[Union[str, GeneProteinRecordGeneProteinId], Union[dict, GeneProteinRecord]], list[Union[dict, GeneProteinRecord]]]])

slots.lanthanideBioprocessingDatabase__structures = Slot(uri=CMM.structures, name="lanthanideBioprocessingDatabase__structures", curie=CMM.curie('structures'),
                   model_uri=CMM.lanthanideBioprocessingDatabase__structures, domain=None, range=Optional[Union[dict[Union[str, MacromolecularStructureRecordStructureName], Union[dict, MacromolecularStructureRecord]], list[Union[dict, MacromolecularStructureRecord]]]])

slots.lanthanideBioprocessingDatabase__publications = Slot(uri=CMM.publications, name="lanthanideBioprocessingDatabase__publications", curie=CMM.curie('publications'),
                   model_uri=CMM.lanthanideBioprocessingDatabase__publications, domain=None, range=Optional[Union[dict[Union[str, PublicationRecordUrl], Union[dict, PublicationRecord]], list[Union[dict, PublicationRecord]]]])

slots.lanthanideBioprocessingDatabase__datasets = Slot(uri=CMM.datasets, name="lanthanideBioprocessingDatabase__datasets", curie=CMM.curie('datasets'),
                   model_uri=CMM.lanthanideBioprocessingDatabase__datasets, domain=None, range=Optional[Union[dict[Union[str, DatasetRecordDatasetName], Union[dict, DatasetRecord]], list[Union[dict, DatasetRecord]]]])

slots.lanthanideBioprocessingDatabase__chemicals = Slot(uri=CMM.chemicals, name="lanthanideBioprocessingDatabase__chemicals", curie=CMM.curie('chemicals'),
                   model_uri=CMM.lanthanideBioprocessingDatabase__chemicals, domain=None, range=Optional[Union[dict[Union[str, ChemicalCompoundRecordChemicalId], Union[dict, ChemicalCompoundRecord]], list[Union[dict, ChemicalCompoundRecord]]]])

slots.lanthanideBioprocessingDatabase__assays = Slot(uri=CMM.assays, name="lanthanideBioprocessingDatabase__assays", curie=CMM.curie('assays'),
                   model_uri=CMM.lanthanideBioprocessingDatabase__assays, domain=None, range=Optional[Union[dict[Union[str, AssayMeasurementRecordAssayId], Union[dict, AssayMeasurementRecord]], list[Union[dict, AssayMeasurementRecord]]]])

slots.lanthanideBioprocessingDatabase__bioprocesses = Slot(uri=CMM.bioprocesses, name="lanthanideBioprocessingDatabase__bioprocesses", curie=CMM.curie('bioprocesses'),
                   model_uri=CMM.lanthanideBioprocessingDatabase__bioprocesses, domain=None, range=Optional[Union[dict[Union[str, BioprocessConditionsRecordProcessId], Union[dict, BioprocessConditionsRecord]], list[Union[dict, BioprocessConditionsRecord]]]])

slots.lanthanideBioprocessingDatabase__screening_results = Slot(uri=CMM.screening_results, name="lanthanideBioprocessingDatabase__screening_results", curie=CMM.curie('screening_results'),
                   model_uri=CMM.lanthanideBioprocessingDatabase__screening_results, domain=None, range=Optional[Union[dict[Union[str, ScreeningResultRecordExperimentId], Union[dict, ScreeningResultRecord]], list[Union[dict, ScreeningResultRecord]]]])

slots.lanthanideBioprocessingDatabase__protocols = Slot(uri=CMM.protocols, name="lanthanideBioprocessingDatabase__protocols", curie=CMM.curie('protocols'),
                   model_uri=CMM.lanthanideBioprocessingDatabase__protocols, domain=None, range=Optional[Union[dict[Union[str, ProtocolRecordProtocolId], Union[dict, ProtocolRecord]], list[Union[dict, ProtocolRecord]]]])

slots.GenomeRecord_scientific_name = Slot(uri=SCHEMA.scientificName, name="GenomeRecord_scientific_name", curie=SCHEMA.curie('scientificName'),
                   model_uri=CMM.GenomeRecord_scientific_name, domain=GenomeRecord, range=Union[str, GenomeRecordScientificName])

slots.GenomeRecord_ncbi_taxon_id = Slot(uri=NCBITAXON.id, name="GenomeRecord_ncbi_taxon_id", curie=NCBITAXON.curie('id'),
                   model_uri=CMM.GenomeRecord_ncbi_taxon_id, domain=GenomeRecord, range=Optional[int])

slots.GenomeRecord_genome_identifier = Slot(uri=CMM.genome_identifier, name="GenomeRecord_genome_identifier", curie=CMM.curie('genome_identifier'),
                   model_uri=CMM.GenomeRecord_genome_identifier, domain=GenomeRecord, range=Optional[str],
                   pattern=re.compile(r'^(GC[AF]_\d+\.\d+|\d+\.\d+)?$'))

slots.GenomeRecord_annotation_download_url = Slot(uri=CMM.annotation_download_url, name="GenomeRecord_annotation_download_url", curie=CMM.curie('annotation_download_url'),
                   model_uri=CMM.GenomeRecord_annotation_download_url, domain=GenomeRecord, range=Optional[Union[str, URI]])

slots.BiosampleRecord_sample_id = Slot(uri=CMM.sample_id, name="BiosampleRecord_sample_id", curie=CMM.curie('sample_id'),
                   model_uri=CMM.BiosampleRecord_sample_id, domain=BiosampleRecord, range=Union[str, BiosampleRecordSampleId],
                   pattern=re.compile(r'^SAM[NDE][A-Z]?\d+$'))

slots.BiosampleRecord_sample_name = Slot(uri=SCHEMA.name, name="BiosampleRecord_sample_name", curie=SCHEMA.curie('name'),
                   model_uri=CMM.BiosampleRecord_sample_name, domain=BiosampleRecord, range=Optional[str])

slots.BiosampleRecord_organism = Slot(uri=SCHEMA.organism, name="BiosampleRecord_organism", curie=SCHEMA.curie('organism'),
                   model_uri=CMM.BiosampleRecord_organism, domain=BiosampleRecord, range=Optional[str])

slots.BiosampleRecord_download_url = Slot(uri=SCHEMA.contentUrl, name="BiosampleRecord_download_url", curie=SCHEMA.curie('contentUrl'),
                   model_uri=CMM.BiosampleRecord_download_url, domain=BiosampleRecord, range=Optional[Union[str, URI]])

slots.PathwayRecord_pathway_id = Slot(uri=CMM.pathway_id, name="PathwayRecord_pathway_id", curie=CMM.curie('pathway_id'),
                   model_uri=CMM.PathwayRecord_pathway_id, domain=PathwayRecord, range=Union[str, PathwayRecordPathwayId],
                   pattern=re.compile(r'^(ko\d+|path:map\d+|PWY-\d+|PWY\d+|Custom_[A-Z0-9]+)$'))

slots.PathwayRecord_pathway_name = Slot(uri=SCHEMA.name, name="PathwayRecord_pathway_name", curie=SCHEMA.curie('name'),
                   model_uri=CMM.PathwayRecord_pathway_name, domain=PathwayRecord, range=str)

slots.PathwayRecord_organism = Slot(uri=SCHEMA.organism, name="PathwayRecord_organism", curie=SCHEMA.curie('organism'),
                   model_uri=CMM.PathwayRecord_organism, domain=PathwayRecord, range=Optional[str])

slots.PathwayRecord_genes = Slot(uri=CMM.genes, name="PathwayRecord_genes", curie=CMM.curie('genes'),
                   model_uri=CMM.PathwayRecord_genes, domain=PathwayRecord, range=Optional[Union[str, list[str]]])

slots.PathwayRecord_genes_kegg = Slot(uri=CMM.genes_kegg, name="PathwayRecord_genes_kegg", curie=CMM.curie('genes_kegg'),
                   model_uri=CMM.PathwayRecord_genes_kegg, domain=PathwayRecord, range=Optional[Union[str, list[str]]])

slots.PathwayRecord_download_url = Slot(uri=SCHEMA.contentUrl, name="PathwayRecord_download_url", curie=SCHEMA.curie('contentUrl'),
                   model_uri=CMM.PathwayRecord_download_url, domain=PathwayRecord, range=Optional[Union[str, URI]])

slots.GeneProteinRecord_gene_protein_id = Slot(uri=CMM.gene_protein_id, name="GeneProteinRecord_gene_protein_id", curie=CMM.curie('gene_protein_id'),
                   model_uri=CMM.GeneProteinRecord_gene_protein_id, domain=GeneProteinRecord, range=Union[str, GeneProteinRecordGeneProteinId],
                   pattern=re.compile(r'^(K\d+(_[A-Za-z0-9]+)?|[OPQ][0-9][A-Z0-9]{3}[0-9]|[A-NR-Z][0-9]([A-Z][A-Z0-9]{2}[0-9]){1,2}|custom_[\w]+)?$'))

slots.GeneProteinRecord_organism = Slot(uri=SCHEMA.organism, name="GeneProteinRecord_organism", curie=SCHEMA.curie('organism'),
                   model_uri=CMM.GeneProteinRecord_organism, domain=GeneProteinRecord, range=Optional[str])

slots.GeneProteinRecord_annotation = Slot(uri=SCHEMA.description, name="GeneProteinRecord_annotation", curie=SCHEMA.curie('description'),
                   model_uri=CMM.GeneProteinRecord_annotation, domain=GeneProteinRecord, range=str)

slots.GeneProteinRecord_ec_number = Slot(uri=CMM.ec_number, name="GeneProteinRecord_ec_number", curie=CMM.curie('ec_number'),
                   model_uri=CMM.GeneProteinRecord_ec_number, domain=GeneProteinRecord, range=Optional[str],
                   pattern=re.compile(r'^\d+\.\d+\.\d+\.\d+$'))

slots.GeneProteinRecord_go_terms = Slot(uri=CMM.go_terms, name="GeneProteinRecord_go_terms", curie=CMM.curie('go_terms'),
                   model_uri=CMM.GeneProteinRecord_go_terms, domain=GeneProteinRecord, range=Optional[Union[str, list[str]]],
                   pattern=re.compile(r'^GO:\d{7}'))

slots.GeneProteinRecord_chebi_terms = Slot(uri=CMM.chebi_terms, name="GeneProteinRecord_chebi_terms", curie=CMM.curie('chebi_terms'),
                   model_uri=CMM.GeneProteinRecord_chebi_terms, domain=GeneProteinRecord, range=Optional[Union[str, list[str]]],
                   pattern=re.compile(r'^CHEBI:\d+'))

slots.GeneProteinRecord_download_url = Slot(uri=SCHEMA.contentUrl, name="GeneProteinRecord_download_url", curie=SCHEMA.curie('contentUrl'),
                   model_uri=CMM.GeneProteinRecord_download_url, domain=GeneProteinRecord, range=Optional[Union[str, URI]])

slots.MacromolecularStructureRecord_structure_name = Slot(uri=SCHEMA.name, name="MacromolecularStructureRecord_structure_name", curie=SCHEMA.curie('name'),
                   model_uri=CMM.MacromolecularStructureRecord_structure_name, domain=MacromolecularStructureRecord, range=Union[str, MacromolecularStructureRecordStructureName])

slots.MacromolecularStructureRecord_organism = Slot(uri=SCHEMA.organism, name="MacromolecularStructureRecord_organism", curie=SCHEMA.curie('organism'),
                   model_uri=CMM.MacromolecularStructureRecord_organism, domain=MacromolecularStructureRecord, range=Optional[str])

slots.MacromolecularStructureRecord_components = Slot(uri=CMM.components, name="MacromolecularStructureRecord_components", curie=CMM.curie('components'),
                   model_uri=CMM.MacromolecularStructureRecord_components, domain=MacromolecularStructureRecord, range=Optional[str])

slots.MacromolecularStructureRecord_download_url = Slot(uri=SCHEMA.contentUrl, name="MacromolecularStructureRecord_download_url", curie=SCHEMA.curie('contentUrl'),
                   model_uri=CMM.MacromolecularStructureRecord_download_url, domain=MacromolecularStructureRecord, range=Optional[Union[str, URI]])

slots.MacromolecularStructureRecord_pdb_id = Slot(uri=CMM.pdb_id, name="MacromolecularStructureRecord_pdb_id", curie=CMM.curie('pdb_id'),
                   model_uri=CMM.MacromolecularStructureRecord_pdb_id, domain=MacromolecularStructureRecord, range=Optional[str])

slots.MacromolecularStructureRecord_resolution = Slot(uri=CMM.resolution, name="MacromolecularStructureRecord_resolution", curie=CMM.curie('resolution'),
                   model_uri=CMM.MacromolecularStructureRecord_resolution, domain=MacromolecularStructureRecord, range=Optional[str])

slots.MacromolecularStructureRecord_method = Slot(uri=CMM.method, name="MacromolecularStructureRecord_method", curie=CMM.curie('method'),
                   model_uri=CMM.MacromolecularStructureRecord_method, domain=MacromolecularStructureRecord, range=Optional[Union[str, "StructureMethodEnum"]])

slots.PublicationRecord_url = Slot(uri=SCHEMA.url, name="PublicationRecord_url", curie=SCHEMA.curie('url'),
                   model_uri=CMM.PublicationRecord_url, domain=PublicationRecord, range=Union[str, PublicationRecordUrl])

slots.PublicationRecord_title = Slot(uri=SCHEMA.headline, name="PublicationRecord_title", curie=SCHEMA.curie('headline'),
                   model_uri=CMM.PublicationRecord_title, domain=PublicationRecord, range=str)

slots.PublicationRecord_download_url = Slot(uri=SCHEMA.contentUrl, name="PublicationRecord_download_url", curie=SCHEMA.curie('contentUrl'),
                   model_uri=CMM.PublicationRecord_download_url, domain=PublicationRecord, range=Optional[Union[str, URI]])

slots.PublicationRecord_journal = Slot(uri=SCHEMA.publisher, name="PublicationRecord_journal", curie=SCHEMA.curie('publisher'),
                   model_uri=CMM.PublicationRecord_journal, domain=PublicationRecord, range=Optional[str])

slots.PublicationRecord_year = Slot(uri=SCHEMA.datePublished, name="PublicationRecord_year", curie=SCHEMA.curie('datePublished'),
                   model_uri=CMM.PublicationRecord_year, domain=PublicationRecord, range=Optional[int])

slots.PublicationRecord_authors = Slot(uri=SCHEMA.author, name="PublicationRecord_authors", curie=SCHEMA.curie('author'),
                   model_uri=CMM.PublicationRecord_authors, domain=PublicationRecord, range=Optional[str])

slots.DatasetRecord_dataset_name = Slot(uri=SCHEMA.name, name="DatasetRecord_dataset_name", curie=SCHEMA.curie('name'),
                   model_uri=CMM.DatasetRecord_dataset_name, domain=DatasetRecord, range=Union[str, DatasetRecordDatasetName])

slots.DatasetRecord_data_type = Slot(uri=CMM.data_type, name="DatasetRecord_data_type", curie=CMM.curie('data_type'),
                   model_uri=CMM.DatasetRecord_data_type, domain=DatasetRecord, range=Optional[Union[str, "DataTypeEnum"]])

slots.DatasetRecord_url = Slot(uri=SCHEMA.url, name="DatasetRecord_url", curie=SCHEMA.curie('url'),
                   model_uri=CMM.DatasetRecord_url, domain=DatasetRecord, range=Optional[Union[str, URI]])

slots.DatasetRecord_size = Slot(uri=CMM.size, name="DatasetRecord_size", curie=CMM.curie('size'),
                   model_uri=CMM.DatasetRecord_size, domain=DatasetRecord, range=Optional[str])

slots.DatasetRecord_publication = Slot(uri=CMM.publication, name="DatasetRecord_publication", curie=CMM.curie('publication'),
                   model_uri=CMM.DatasetRecord_publication, domain=DatasetRecord, range=Optional[str])

slots.DatasetRecord_license = Slot(uri=SCHEMA.license, name="DatasetRecord_license", curie=SCHEMA.curie('license'),
                   model_uri=CMM.DatasetRecord_license, domain=DatasetRecord, range=Optional[str])

slots.DatasetRecord_download_url = Slot(uri=SCHEMA.contentUrl, name="DatasetRecord_download_url", curie=SCHEMA.curie('contentUrl'),
                   model_uri=CMM.DatasetRecord_download_url, domain=DatasetRecord, range=Optional[Union[str, URI]])

slots.ChemicalCompoundRecord_chemical_id = Slot(uri=SCHEMA.identifier, name="ChemicalCompoundRecord_chemical_id", curie=SCHEMA.curie('identifier'),
                   model_uri=CMM.ChemicalCompoundRecord_chemical_id, domain=ChemicalCompoundRecord, range=Union[str, ChemicalCompoundRecordChemicalId])

slots.ChemicalCompoundRecord_chemical_name = Slot(uri=SCHEMA.name, name="ChemicalCompoundRecord_chemical_name", curie=SCHEMA.curie('name'),
                   model_uri=CMM.ChemicalCompoundRecord_chemical_name, domain=ChemicalCompoundRecord, range=str)

slots.ChemicalCompoundRecord_compound_type = Slot(uri=CMM.compound_type, name="ChemicalCompoundRecord_compound_type", curie=CMM.curie('compound_type'),
                   model_uri=CMM.ChemicalCompoundRecord_compound_type, domain=ChemicalCompoundRecord, range=Optional[Union[str, "CompoundTypeEnum"]])

slots.ChemicalCompoundRecord_molecular_formula = Slot(uri=CMM.molecular_formula, name="ChemicalCompoundRecord_molecular_formula", curie=CMM.curie('molecular_formula'),
                   model_uri=CMM.ChemicalCompoundRecord_molecular_formula, domain=ChemicalCompoundRecord, range=Optional[str])

slots.ChemicalCompoundRecord_molecular_weight = Slot(uri=CMM.molecular_weight, name="ChemicalCompoundRecord_molecular_weight", curie=CMM.curie('molecular_weight'),
                   model_uri=CMM.ChemicalCompoundRecord_molecular_weight, domain=ChemicalCompoundRecord, range=Optional[str])

slots.ChemicalCompoundRecord_role_in_bioprocess = Slot(uri=CMM.role_in_bioprocess, name="ChemicalCompoundRecord_role_in_bioprocess", curie=CMM.curie('role_in_bioprocess'),
                   model_uri=CMM.ChemicalCompoundRecord_role_in_bioprocess, domain=ChemicalCompoundRecord, range=Optional[str])

slots.ChemicalCompoundRecord_chebi_id = Slot(uri=CMM.chebi_id, name="ChemicalCompoundRecord_chebi_id", curie=CMM.curie('chebi_id'),
                   model_uri=CMM.ChemicalCompoundRecord_chebi_id, domain=ChemicalCompoundRecord, range=Optional[str],
                   pattern=re.compile(r'^CHEBI:\d+$'))

slots.ChemicalCompoundRecord_pubchem_id = Slot(uri=CMM.pubchem_id, name="ChemicalCompoundRecord_pubchem_id", curie=CMM.curie('pubchem_id'),
                   model_uri=CMM.ChemicalCompoundRecord_pubchem_id, domain=ChemicalCompoundRecord, range=Optional[int])

slots.ChemicalCompoundRecord_chembl_id = Slot(uri=CMM.chembl_id, name="ChemicalCompoundRecord_chembl_id", curie=CMM.curie('chembl_id'),
                   model_uri=CMM.ChemicalCompoundRecord_chembl_id, domain=ChemicalCompoundRecord, range=Optional[str],
                   pattern=re.compile(r'^CHEMBL\d+$'))

slots.ChemicalCompoundRecord_properties = Slot(uri=CMM.properties, name="ChemicalCompoundRecord_properties", curie=CMM.curie('properties'),
                   model_uri=CMM.ChemicalCompoundRecord_properties, domain=ChemicalCompoundRecord, range=Optional[str])

slots.ChemicalCompoundRecord_download_url = Slot(uri=SCHEMA.contentUrl, name="ChemicalCompoundRecord_download_url", curie=SCHEMA.curie('contentUrl'),
                   model_uri=CMM.ChemicalCompoundRecord_download_url, domain=ChemicalCompoundRecord, range=Optional[Union[str, URI]])

slots.AssayMeasurementRecord_assay_id = Slot(uri=SCHEMA.identifier, name="AssayMeasurementRecord_assay_id", curie=SCHEMA.curie('identifier'),
                   model_uri=CMM.AssayMeasurementRecord_assay_id, domain=AssayMeasurementRecord, range=Union[str, AssayMeasurementRecordAssayId])

slots.AssayMeasurementRecord_assay_name = Slot(uri=SCHEMA.name, name="AssayMeasurementRecord_assay_name", curie=SCHEMA.curie('name'),
                   model_uri=CMM.AssayMeasurementRecord_assay_name, domain=AssayMeasurementRecord, range=str)

slots.AssayMeasurementRecord_assay_type = Slot(uri=CMM.assay_type, name="AssayMeasurementRecord_assay_type", curie=CMM.curie('assay_type'),
                   model_uri=CMM.AssayMeasurementRecord_assay_type, domain=AssayMeasurementRecord, range=Optional[Union[str, "AssayTypeEnum"]])

slots.AssayMeasurementRecord_target_analytes = Slot(uri=CMM.target_analytes, name="AssayMeasurementRecord_target_analytes", curie=CMM.curie('target_analytes'),
                   model_uri=CMM.AssayMeasurementRecord_target_analytes, domain=AssayMeasurementRecord, range=Optional[Union[str, list[str]]])

slots.AssayMeasurementRecord_detection_method = Slot(uri=CMM.detection_method, name="AssayMeasurementRecord_detection_method", curie=CMM.curie('detection_method'),
                   model_uri=CMM.AssayMeasurementRecord_detection_method, domain=AssayMeasurementRecord, range=Optional[str])

slots.AssayMeasurementRecord_detection_limit = Slot(uri=CMM.detection_limit, name="AssayMeasurementRecord_detection_limit", curie=CMM.curie('detection_limit'),
                   model_uri=CMM.AssayMeasurementRecord_detection_limit, domain=AssayMeasurementRecord, range=Optional[str])

slots.AssayMeasurementRecord_dynamic_range = Slot(uri=CMM.dynamic_range, name="AssayMeasurementRecord_dynamic_range", curie=CMM.curie('dynamic_range'),
                   model_uri=CMM.AssayMeasurementRecord_dynamic_range, domain=AssayMeasurementRecord, range=Optional[str])

slots.AssayMeasurementRecord_protocol_reference = Slot(uri=CMM.protocol_reference, name="AssayMeasurementRecord_protocol_reference", curie=CMM.curie('protocol_reference'),
                   model_uri=CMM.AssayMeasurementRecord_protocol_reference, domain=AssayMeasurementRecord, range=Optional[str])

slots.AssayMeasurementRecord_equipment_required = Slot(uri=CMM.equipment_required, name="AssayMeasurementRecord_equipment_required", curie=CMM.curie('equipment_required'),
                   model_uri=CMM.AssayMeasurementRecord_equipment_required, domain=AssayMeasurementRecord, range=Optional[Union[str, list[str]]])

slots.AssayMeasurementRecord_sample_preparation = Slot(uri=CMM.sample_preparation, name="AssayMeasurementRecord_sample_preparation", curie=CMM.curie('sample_preparation'),
                   model_uri=CMM.AssayMeasurementRecord_sample_preparation, domain=AssayMeasurementRecord, range=Optional[str])

slots.AssayMeasurementRecord_data_output_format = Slot(uri=CMM.data_output_format, name="AssayMeasurementRecord_data_output_format", curie=CMM.curie('data_output_format'),
                   model_uri=CMM.AssayMeasurementRecord_data_output_format, domain=AssayMeasurementRecord, range=Optional[str])

slots.AssayMeasurementRecord_download_url = Slot(uri=SCHEMA.contentUrl, name="AssayMeasurementRecord_download_url", curie=SCHEMA.curie('contentUrl'),
                   model_uri=CMM.AssayMeasurementRecord_download_url, domain=AssayMeasurementRecord, range=Optional[Union[str, URI]])

slots.BioprocessConditionsRecord_process_id = Slot(uri=SCHEMA.identifier, name="BioprocessConditionsRecord_process_id", curie=SCHEMA.curie('identifier'),
                   model_uri=CMM.BioprocessConditionsRecord_process_id, domain=BioprocessConditionsRecord, range=Union[str, BioprocessConditionsRecordProcessId])

slots.BioprocessConditionsRecord_process_name = Slot(uri=SCHEMA.name, name="BioprocessConditionsRecord_process_name", curie=SCHEMA.curie('name'),
                   model_uri=CMM.BioprocessConditionsRecord_process_name, domain=BioprocessConditionsRecord, range=str)

slots.BioprocessConditionsRecord_process_type = Slot(uri=CMM.process_type, name="BioprocessConditionsRecord_process_type", curie=CMM.curie('process_type'),
                   model_uri=CMM.BioprocessConditionsRecord_process_type, domain=BioprocessConditionsRecord, range=Optional[Union[str, "ProcessTypeEnum"]])

slots.BioprocessConditionsRecord_strain_used = Slot(uri=CMM.strain_used, name="BioprocessConditionsRecord_strain_used", curie=CMM.curie('strain_used'),
                   model_uri=CMM.BioprocessConditionsRecord_strain_used, domain=BioprocessConditionsRecord, range=Optional[str])

slots.BioprocessConditionsRecord_organism_used = Slot(uri=CMM.organism_used, name="BioprocessConditionsRecord_organism_used", curie=CMM.curie('organism_used'),
                   model_uri=CMM.BioprocessConditionsRecord_organism_used, domain=BioprocessConditionsRecord, range=Optional[str])

slots.BioprocessConditionsRecord_growth_conditions = Slot(uri=CMM.growth_conditions, name="BioprocessConditionsRecord_growth_conditions", curie=CMM.curie('growth_conditions'),
                   model_uri=CMM.BioprocessConditionsRecord_growth_conditions, domain=BioprocessConditionsRecord, range=Optional[str])

slots.BioprocessConditionsRecord_ree_concentration = Slot(uri=CMM.ree_concentration, name="BioprocessConditionsRecord_ree_concentration", curie=CMM.curie('ree_concentration'),
                   model_uri=CMM.BioprocessConditionsRecord_ree_concentration, domain=BioprocessConditionsRecord, range=Optional[str])

slots.BioprocessConditionsRecord_contact_time = Slot(uri=CMM.contact_time, name="BioprocessConditionsRecord_contact_time", curie=CMM.curie('contact_time'),
                   model_uri=CMM.BioprocessConditionsRecord_contact_time, domain=BioprocessConditionsRecord, range=Optional[str])

slots.BioprocessConditionsRecord_pH = Slot(uri=CMM.pH, name="BioprocessConditionsRecord_pH", curie=CMM.curie('pH'),
                   model_uri=CMM.BioprocessConditionsRecord_pH, domain=BioprocessConditionsRecord, range=Optional[str])

slots.BioprocessConditionsRecord_temperature = Slot(uri=CMM.temperature, name="BioprocessConditionsRecord_temperature", curie=CMM.curie('temperature'),
                   model_uri=CMM.BioprocessConditionsRecord_temperature, domain=BioprocessConditionsRecord, range=Optional[str])

slots.BioprocessConditionsRecord_competing_ions = Slot(uri=CMM.competing_ions, name="BioprocessConditionsRecord_competing_ions", curie=CMM.curie('competing_ions'),
                   model_uri=CMM.BioprocessConditionsRecord_competing_ions, domain=BioprocessConditionsRecord, range=Optional[Union[str, list[str]]])

slots.BioprocessConditionsRecord_process_parameters = Slot(uri=CMM.process_parameters, name="BioprocessConditionsRecord_process_parameters", curie=CMM.curie('process_parameters'),
                   model_uri=CMM.BioprocessConditionsRecord_process_parameters, domain=BioprocessConditionsRecord, range=Optional[str])

slots.BioprocessConditionsRecord_optimization_history = Slot(uri=CMM.optimization_history, name="BioprocessConditionsRecord_optimization_history", curie=CMM.curie('optimization_history'),
                   model_uri=CMM.BioprocessConditionsRecord_optimization_history, domain=BioprocessConditionsRecord, range=Optional[str])

slots.BioprocessConditionsRecord_download_url = Slot(uri=SCHEMA.contentUrl, name="BioprocessConditionsRecord_download_url", curie=SCHEMA.curie('contentUrl'),
                   model_uri=CMM.BioprocessConditionsRecord_download_url, domain=BioprocessConditionsRecord, range=Optional[Union[str, URI]])

slots.ScreeningResultRecord_experiment_id = Slot(uri=SCHEMA.identifier, name="ScreeningResultRecord_experiment_id", curie=SCHEMA.curie('identifier'),
                   model_uri=CMM.ScreeningResultRecord_experiment_id, domain=ScreeningResultRecord, range=Union[str, ScreeningResultRecordExperimentId])

slots.ScreeningResultRecord_plate_coordinates = Slot(uri=CMM.plate_coordinates, name="ScreeningResultRecord_plate_coordinates", curie=CMM.curie('plate_coordinates'),
                   model_uri=CMM.ScreeningResultRecord_plate_coordinates, domain=ScreeningResultRecord, range=Optional[str])

slots.ScreeningResultRecord_strain_barcode = Slot(uri=CMM.strain_barcode, name="ScreeningResultRecord_strain_barcode", curie=CMM.curie('strain_barcode'),
                   model_uri=CMM.ScreeningResultRecord_strain_barcode, domain=ScreeningResultRecord, range=Optional[str])

slots.ScreeningResultRecord_screening_assay = Slot(uri=CMM.screening_assay, name="ScreeningResultRecord_screening_assay", curie=CMM.curie('screening_assay'),
                   model_uri=CMM.ScreeningResultRecord_screening_assay, domain=ScreeningResultRecord, range=Optional[str])

slots.ScreeningResultRecord_target_ree = Slot(uri=CMM.target_ree, name="ScreeningResultRecord_target_ree", curie=CMM.curie('target_ree'),
                   model_uri=CMM.ScreeningResultRecord_target_ree, domain=ScreeningResultRecord, range=Optional[Union[str, list[str]]])

slots.ScreeningResultRecord_measurement_values = Slot(uri=CMM.measurement_values, name="ScreeningResultRecord_measurement_values", curie=CMM.curie('measurement_values'),
                   model_uri=CMM.ScreeningResultRecord_measurement_values, domain=ScreeningResultRecord, range=Optional[str])

slots.ScreeningResultRecord_hit_classification = Slot(uri=CMM.hit_classification, name="ScreeningResultRecord_hit_classification", curie=CMM.curie('hit_classification'),
                   model_uri=CMM.ScreeningResultRecord_hit_classification, domain=ScreeningResultRecord, range=Optional[Union[str, "HitClassificationEnum"]])

slots.ScreeningResultRecord_validation_status = Slot(uri=CMM.validation_status, name="ScreeningResultRecord_validation_status", curie=CMM.curie('validation_status'),
                   model_uri=CMM.ScreeningResultRecord_validation_status, domain=ScreeningResultRecord, range=Optional[str])

slots.ScreeningResultRecord_follow_up_experiments = Slot(uri=CMM.follow_up_experiments, name="ScreeningResultRecord_follow_up_experiments", curie=CMM.curie('follow_up_experiments'),
                   model_uri=CMM.ScreeningResultRecord_follow_up_experiments, domain=ScreeningResultRecord, range=Optional[Union[str, list[str]]])

slots.ScreeningResultRecord_assay_reference = Slot(uri=CMM.assay_reference, name="ScreeningResultRecord_assay_reference", curie=CMM.curie('assay_reference'),
                   model_uri=CMM.ScreeningResultRecord_assay_reference, domain=ScreeningResultRecord, range=Optional[str])

slots.ScreeningResultRecord_download_url = Slot(uri=SCHEMA.contentUrl, name="ScreeningResultRecord_download_url", curie=SCHEMA.curie('contentUrl'),
                   model_uri=CMM.ScreeningResultRecord_download_url, domain=ScreeningResultRecord, range=Optional[Union[str, URI]])

slots.ProtocolRecord_protocol_id = Slot(uri=SCHEMA.identifier, name="ProtocolRecord_protocol_id", curie=SCHEMA.curie('identifier'),
                   model_uri=CMM.ProtocolRecord_protocol_id, domain=ProtocolRecord, range=Union[str, ProtocolRecordProtocolId])

slots.ProtocolRecord_protocol_name = Slot(uri=SCHEMA.name, name="ProtocolRecord_protocol_name", curie=SCHEMA.curie('name'),
                   model_uri=CMM.ProtocolRecord_protocol_name, domain=ProtocolRecord, range=str)

slots.ProtocolRecord_protocol_type = Slot(uri=CMM.protocol_type, name="ProtocolRecord_protocol_type", curie=CMM.curie('protocol_type'),
                   model_uri=CMM.ProtocolRecord_protocol_type, domain=ProtocolRecord, range=Optional[Union[str, "ProtocolTypeEnum"]])

slots.ProtocolRecord_protocol_version = Slot(uri=CMM.protocol_version, name="ProtocolRecord_protocol_version", curie=CMM.curie('protocol_version'),
                   model_uri=CMM.ProtocolRecord_protocol_version, domain=ProtocolRecord, range=Optional[str])

slots.ProtocolRecord_protocol_doi = Slot(uri=CMM.protocol_doi, name="ProtocolRecord_protocol_doi", curie=CMM.curie('protocol_doi'),
                   model_uri=CMM.ProtocolRecord_protocol_doi, domain=ProtocolRecord, range=Optional[str])

slots.ProtocolRecord_protocol_url = Slot(uri=CMM.protocol_url, name="ProtocolRecord_protocol_url", curie=CMM.curie('protocol_url'),
                   model_uri=CMM.ProtocolRecord_protocol_url, domain=ProtocolRecord, range=Optional[Union[str, URI]])

slots.ProtocolRecord_associated_assays = Slot(uri=CMM.associated_assays, name="ProtocolRecord_associated_assays", curie=CMM.curie('associated_assays'),
                   model_uri=CMM.ProtocolRecord_associated_assays, domain=ProtocolRecord, range=Optional[Union[str, list[str]]])

slots.ProtocolRecord_equipment_list = Slot(uri=CMM.equipment_list, name="ProtocolRecord_equipment_list", curie=CMM.curie('equipment_list'),
                   model_uri=CMM.ProtocolRecord_equipment_list, domain=ProtocolRecord, range=Optional[Union[str, list[str]]])

slots.ProtocolRecord_success_criteria = Slot(uri=CMM.success_criteria, name="ProtocolRecord_success_criteria", curie=CMM.curie('success_criteria'),
                   model_uri=CMM.ProtocolRecord_success_criteria, domain=ProtocolRecord, range=Optional[str])

slots.ProtocolRecord_quality_control = Slot(uri=CMM.quality_control, name="ProtocolRecord_quality_control", curie=CMM.curie('quality_control'),
                   model_uri=CMM.ProtocolRecord_quality_control, domain=ProtocolRecord, range=Optional[str])

slots.ProtocolRecord_dbtl_iteration = Slot(uri=CMM.dbtl_iteration, name="ProtocolRecord_dbtl_iteration", curie=CMM.curie('dbtl_iteration'),
                   model_uri=CMM.ProtocolRecord_dbtl_iteration, domain=ProtocolRecord, range=Optional[str])

slots.ProtocolRecord_validation_status = Slot(uri=CMM.validation_status, name="ProtocolRecord_validation_status", curie=CMM.curie('validation_status'),
                   model_uri=CMM.ProtocolRecord_validation_status, domain=ProtocolRecord, range=Optional[str])

slots.ProtocolRecord_user_notes = Slot(uri=CMM.user_notes, name="ProtocolRecord_user_notes", curie=CMM.curie('user_notes'),
                   model_uri=CMM.ProtocolRecord_user_notes, domain=ProtocolRecord, range=Optional[str])

slots.ProtocolRecord_download_url = Slot(uri=SCHEMA.contentUrl, name="ProtocolRecord_download_url", curie=SCHEMA.curie('contentUrl'),
                   model_uri=CMM.ProtocolRecord_download_url, domain=ProtocolRecord, range=Optional[Union[str, URI]])

