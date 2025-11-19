# Auto generated from pfas_biodegradation.yaml by pythongen.py version: 0.0.1
# Generation date: 2025-11-18T21:29:35
# Schema: pfas-biodegradation
#
# id: https://w3id.org/pfas-ai/pfas-biodegradation
# description: LinkML schema for modeling PFAS biodegradation research data including microorganisms, genes, pathways, structures, assays, and experimental conditions.
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

from linkml_runtime.linkml_model.types import Float, Integer, String, Uri
from linkml_runtime.utils.metamodelcore import URI

metamodel_version = "1.7.0"
version = None

# Namespaces
BAO = CurieNamespace('BAO', 'http://www.bioassayontology.org/bao#')
CHEBI = CurieNamespace('CHEBI', 'http://purl.obolibrary.org/obo/CHEBI_')
CHEMBL = CurieNamespace('ChEMBL', 'https://www.ebi.ac.uk/chembl/compound_report_card/')
DOI = CurieNamespace('DOI', 'https://doi.org/')
EC = CurieNamespace('EC', 'https://www.enzyme-database.org/query.php?ec=')
ENVO = CurieNamespace('ENVO', 'http://purl.obolibrary.org/obo/ENVO_')
GO = CurieNamespace('GO', 'http://purl.obolibrary.org/obo/GO_')
KEGG = CurieNamespace('KEGG', 'http://www.kegg.jp/entry/')
NCBI = CurieNamespace('NCBI', 'http://www.ncbi.nlm.nih.gov/gene/')
NCBITAXON = CurieNamespace('NCBITaxon', 'http://purl.obolibrary.org/obo/NCBITaxon_')
OBI = CurieNamespace('OBI', 'http://purl.obolibrary.org/obo/OBI_')
PDB = CurieNamespace('PDB', 'https://www.rcsb.org/structure/')
PMID = CurieNamespace('PMID', 'http://www.ncbi.nlm.nih.gov/pubmed/')
PUBCHEM = CurieNamespace('PubChem', 'https://pubchem.ncbi.nlm.nih.gov/compound/')
RHEA = CurieNamespace('RHEA', 'https://www.rhea-db.org/rhea/')
SRA = CurieNamespace('SRA', 'https://www.ncbi.nlm.nih.gov/sra/')
UNIPROTKB = CurieNamespace('UniProtKB', 'http://purl.uniprot.org/uniprot/')
LINKML = CurieNamespace('linkml', 'https://w3id.org/linkml/')
PFAS = CurieNamespace('pfas', 'https://w3id.org/pfas-ai/pfas-biodegradation/')
SCHEMA = CurieNamespace('schema', 'http://schema.org/')
DEFAULT_ = PFAS


# Types

# Class references
class GenomeRecordScientificName(extended_str):
    pass


class BiosampleRecordSampleId(extended_str):
    pass


class PathwayRecordPathwayId(extended_str):
    pass


class ReactionRecordReactionId(extended_str):
    pass


class GeneProteinRecordGeneProteinId(extended_str):
    pass


class MacromolecularStructureRecordPdbId(extended_str):
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


class TranscriptomicsRecordExperimentId(extended_str):
    pass


class StrainRecordStrainId(extended_str):
    pass


class GrowthMediaRecordMediaId(extended_str):
    pass


class MediaIngredientRecordIngredientId(extended_str):
    pass


@dataclass(repr=False)
class Database(YAMLRoot):
    """
    Container for all PFAS biodegradation research data
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = PFAS["Database"]
    class_class_curie: ClassVar[str] = "pfas:Database"
    class_name: ClassVar[str] = "Database"
    class_model_uri: ClassVar[URIRef] = PFAS.Database

    genomes: Optional[Union[Union[str, GenomeRecordScientificName], list[Union[str, GenomeRecordScientificName]]]] = empty_list()
    biosamples: Optional[Union[Union[str, BiosampleRecordSampleId], list[Union[str, BiosampleRecordSampleId]]]] = empty_list()
    pathways: Optional[Union[Union[str, PathwayRecordPathwayId], list[Union[str, PathwayRecordPathwayId]]]] = empty_list()
    genes_proteins: Optional[Union[Union[str, GeneProteinRecordGeneProteinId], list[Union[str, GeneProteinRecordGeneProteinId]]]] = empty_list()
    structures: Optional[Union[Union[str, MacromolecularStructureRecordPdbId], list[Union[str, MacromolecularStructureRecordPdbId]]]] = empty_list()
    publications: Optional[Union[Union[str, PublicationRecordUrl], list[Union[str, PublicationRecordUrl]]]] = empty_list()
    datasets: Optional[Union[Union[str, DatasetRecordDatasetName], list[Union[str, DatasetRecordDatasetName]]]] = empty_list()
    chemicals: Optional[Union[Union[str, ChemicalCompoundRecordChemicalId], list[Union[str, ChemicalCompoundRecordChemicalId]]]] = empty_list()
    assays: Optional[Union[Union[str, AssayMeasurementRecordAssayId], list[Union[str, AssayMeasurementRecordAssayId]]]] = empty_list()
    bioprocesses: Optional[Union[Union[str, BioprocessConditionsRecordProcessId], list[Union[str, BioprocessConditionsRecordProcessId]]]] = empty_list()
    screening_results: Optional[Union[Union[str, ScreeningResultRecordExperimentId], list[Union[str, ScreeningResultRecordExperimentId]]]] = empty_list()
    protocols: Optional[Union[Union[str, ProtocolRecordProtocolId], list[Union[str, ProtocolRecordProtocolId]]]] = empty_list()
    reactions: Optional[Union[Union[str, ReactionRecordReactionId], list[Union[str, ReactionRecordReactionId]]]] = empty_list()
    transcriptomics: Optional[Union[Union[str, TranscriptomicsRecordExperimentId], list[Union[str, TranscriptomicsRecordExperimentId]]]] = empty_list()
    strains: Optional[Union[Union[str, StrainRecordStrainId], list[Union[str, StrainRecordStrainId]]]] = empty_list()
    growth_media: Optional[Union[Union[str, GrowthMediaRecordMediaId], list[Union[str, GrowthMediaRecordMediaId]]]] = empty_list()
    media_ingredients: Optional[Union[Union[str, MediaIngredientRecordIngredientId], list[Union[str, MediaIngredientRecordIngredientId]]]] = empty_list()

    def __post_init__(self, *_: str, **kwargs: Any):
        if not isinstance(self.genomes, list):
            self.genomes = [self.genomes] if self.genomes is not None else []
        self.genomes = [v if isinstance(v, GenomeRecordScientificName) else GenomeRecordScientificName(v) for v in self.genomes]

        if not isinstance(self.biosamples, list):
            self.biosamples = [self.biosamples] if self.biosamples is not None else []
        self.biosamples = [v if isinstance(v, BiosampleRecordSampleId) else BiosampleRecordSampleId(v) for v in self.biosamples]

        if not isinstance(self.pathways, list):
            self.pathways = [self.pathways] if self.pathways is not None else []
        self.pathways = [v if isinstance(v, PathwayRecordPathwayId) else PathwayRecordPathwayId(v) for v in self.pathways]

        if not isinstance(self.genes_proteins, list):
            self.genes_proteins = [self.genes_proteins] if self.genes_proteins is not None else []
        self.genes_proteins = [v if isinstance(v, GeneProteinRecordGeneProteinId) else GeneProteinRecordGeneProteinId(v) for v in self.genes_proteins]

        if not isinstance(self.structures, list):
            self.structures = [self.structures] if self.structures is not None else []
        self.structures = [v if isinstance(v, MacromolecularStructureRecordPdbId) else MacromolecularStructureRecordPdbId(v) for v in self.structures]

        if not isinstance(self.publications, list):
            self.publications = [self.publications] if self.publications is not None else []
        self.publications = [v if isinstance(v, PublicationRecordUrl) else PublicationRecordUrl(v) for v in self.publications]

        if not isinstance(self.datasets, list):
            self.datasets = [self.datasets] if self.datasets is not None else []
        self.datasets = [v if isinstance(v, DatasetRecordDatasetName) else DatasetRecordDatasetName(v) for v in self.datasets]

        if not isinstance(self.chemicals, list):
            self.chemicals = [self.chemicals] if self.chemicals is not None else []
        self.chemicals = [v if isinstance(v, ChemicalCompoundRecordChemicalId) else ChemicalCompoundRecordChemicalId(v) for v in self.chemicals]

        if not isinstance(self.assays, list):
            self.assays = [self.assays] if self.assays is not None else []
        self.assays = [v if isinstance(v, AssayMeasurementRecordAssayId) else AssayMeasurementRecordAssayId(v) for v in self.assays]

        if not isinstance(self.bioprocesses, list):
            self.bioprocesses = [self.bioprocesses] if self.bioprocesses is not None else []
        self.bioprocesses = [v if isinstance(v, BioprocessConditionsRecordProcessId) else BioprocessConditionsRecordProcessId(v) for v in self.bioprocesses]

        if not isinstance(self.screening_results, list):
            self.screening_results = [self.screening_results] if self.screening_results is not None else []
        self.screening_results = [v if isinstance(v, ScreeningResultRecordExperimentId) else ScreeningResultRecordExperimentId(v) for v in self.screening_results]

        if not isinstance(self.protocols, list):
            self.protocols = [self.protocols] if self.protocols is not None else []
        self.protocols = [v if isinstance(v, ProtocolRecordProtocolId) else ProtocolRecordProtocolId(v) for v in self.protocols]

        if not isinstance(self.reactions, list):
            self.reactions = [self.reactions] if self.reactions is not None else []
        self.reactions = [v if isinstance(v, ReactionRecordReactionId) else ReactionRecordReactionId(v) for v in self.reactions]

        if not isinstance(self.transcriptomics, list):
            self.transcriptomics = [self.transcriptomics] if self.transcriptomics is not None else []
        self.transcriptomics = [v if isinstance(v, TranscriptomicsRecordExperimentId) else TranscriptomicsRecordExperimentId(v) for v in self.transcriptomics]

        if not isinstance(self.strains, list):
            self.strains = [self.strains] if self.strains is not None else []
        self.strains = [v if isinstance(v, StrainRecordStrainId) else StrainRecordStrainId(v) for v in self.strains]

        if not isinstance(self.growth_media, list):
            self.growth_media = [self.growth_media] if self.growth_media is not None else []
        self.growth_media = [v if isinstance(v, GrowthMediaRecordMediaId) else GrowthMediaRecordMediaId(v) for v in self.growth_media]

        if not isinstance(self.media_ingredients, list):
            self.media_ingredients = [self.media_ingredients] if self.media_ingredients is not None else []
        self.media_ingredients = [v if isinstance(v, MediaIngredientRecordIngredientId) else MediaIngredientRecordIngredientId(v) for v in self.media_ingredients]

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class GenomeRecord(YAMLRoot):
    """
    Bacterial or archaeal genome with taxonomy and annotation information
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = PFAS["GenomeRecord"]
    class_class_curie: ClassVar[str] = "pfas:GenomeRecord"
    class_name: ClassVar[str] = "GenomeRecord"
    class_model_uri: ClassVar[URIRef] = PFAS.GenomeRecord

    scientific_name: Union[str, GenomeRecordScientificName] = None
    ncbi_taxon_id: Optional[str] = None
    genome_identifier: Optional[str] = None
    annotation_download_url: Optional[Union[str, URI]] = None
    source: Optional[str] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self._is_empty(self.scientific_name):
            self.MissingRequiredField("scientific_name")
        if not isinstance(self.scientific_name, GenomeRecordScientificName):
            self.scientific_name = GenomeRecordScientificName(self.scientific_name)

        if self.ncbi_taxon_id is not None and not isinstance(self.ncbi_taxon_id, str):
            self.ncbi_taxon_id = str(self.ncbi_taxon_id)

        if self.genome_identifier is not None and not isinstance(self.genome_identifier, str):
            self.genome_identifier = str(self.genome_identifier)

        if self.annotation_download_url is not None and not isinstance(self.annotation_download_url, URI):
            self.annotation_download_url = URI(self.annotation_download_url)

        if self.source is not None and not isinstance(self.source, str):
            self.source = str(self.source)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class BiosampleRecord(YAMLRoot):
    """
    Environmental or cultured biological sample
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = PFAS["BiosampleRecord"]
    class_class_curie: ClassVar[str] = "pfas:BiosampleRecord"
    class_name: ClassVar[str] = "BiosampleRecord"
    class_model_uri: ClassVar[URIRef] = PFAS.BiosampleRecord

    sample_id: Union[str, BiosampleRecordSampleId] = None
    sample_name: Optional[str] = None
    organism: Optional[str] = None
    download_url: Optional[Union[str, URI]] = None
    source: Optional[str] = None

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

        if self.source is not None and not isinstance(self.source, str):
            self.source = str(self.source)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class PathwayRecord(YAMLRoot):
    """
    Metabolic pathway relevant to PFAS biodegradation
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = PFAS["PathwayRecord"]
    class_class_curie: ClassVar[str] = "pfas:PathwayRecord"
    class_name: ClassVar[str] = "PathwayRecord"
    class_model_uri: ClassVar[URIRef] = PFAS.PathwayRecord

    pathway_id: Union[str, PathwayRecordPathwayId] = None
    pathway_name: str = None
    database: Optional[Union[str, "PathwayDatabaseEnum"]] = None
    url: Optional[Union[str, URI]] = None
    genes: Optional[Union[str, list[str]]] = empty_list()
    genes_kegg: Optional[Union[str, list[str]]] = empty_list()
    source: Optional[str] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self._is_empty(self.pathway_id):
            self.MissingRequiredField("pathway_id")
        if not isinstance(self.pathway_id, PathwayRecordPathwayId):
            self.pathway_id = PathwayRecordPathwayId(self.pathway_id)

        if self._is_empty(self.pathway_name):
            self.MissingRequiredField("pathway_name")
        if not isinstance(self.pathway_name, str):
            self.pathway_name = str(self.pathway_name)

        if self.database is not None and not isinstance(self.database, PathwayDatabaseEnum):
            self.database = PathwayDatabaseEnum(self.database)

        if self.url is not None and not isinstance(self.url, URI):
            self.url = URI(self.url)

        if not isinstance(self.genes, list):
            self.genes = [self.genes] if self.genes is not None else []
        self.genes = [v if isinstance(v, str) else str(v) for v in self.genes]

        if not isinstance(self.genes_kegg, list):
            self.genes_kegg = [self.genes_kegg] if self.genes_kegg is not None else []
        self.genes_kegg = [v if isinstance(v, str) else str(v) for v in self.genes_kegg]

        if self.source is not None and not isinstance(self.source, str):
            self.source = str(self.source)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class ReactionRecord(YAMLRoot):
    """
    Biochemical reaction relevant to PFAS biodegradation
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = PFAS["ReactionRecord"]
    class_class_curie: ClassVar[str] = "pfas:ReactionRecord"
    class_name: ClassVar[str] = "ReactionRecord"
    class_model_uri: ClassVar[URIRef] = PFAS.ReactionRecord

    reaction_id: Union[str, ReactionRecordReactionId] = None
    equation: str = None
    reaction_category: Union[str, "ReactionCategoryEnum"] = None
    reaction_name: Optional[str] = None
    enzyme_class: Optional[str] = None
    ec_number: Optional[Union[str, list[str]]] = empty_list()
    rhea_id: Optional[str] = None
    kegg_reaction_id: Optional[str] = None
    go_terms: Optional[Union[str, list[str]]] = empty_list()
    substrates: Optional[Union[str, list[str]]] = empty_list()
    products: Optional[Union[str, list[str]]] = empty_list()
    enzyme_genes: Optional[Union[str, list[str]]] = empty_list()
    pathway_id: Optional[str] = None
    note: Optional[str] = None
    url: Optional[Union[str, URI]] = None
    source: Optional[str] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self._is_empty(self.reaction_id):
            self.MissingRequiredField("reaction_id")
        if not isinstance(self.reaction_id, ReactionRecordReactionId):
            self.reaction_id = ReactionRecordReactionId(self.reaction_id)

        if self._is_empty(self.equation):
            self.MissingRequiredField("equation")
        if not isinstance(self.equation, str):
            self.equation = str(self.equation)

        if self._is_empty(self.reaction_category):
            self.MissingRequiredField("reaction_category")
        if not isinstance(self.reaction_category, ReactionCategoryEnum):
            self.reaction_category = ReactionCategoryEnum(self.reaction_category)

        if self.reaction_name is not None and not isinstance(self.reaction_name, str):
            self.reaction_name = str(self.reaction_name)

        if self.enzyme_class is not None and not isinstance(self.enzyme_class, str):
            self.enzyme_class = str(self.enzyme_class)

        if not isinstance(self.ec_number, list):
            self.ec_number = [self.ec_number] if self.ec_number is not None else []
        self.ec_number = [v if isinstance(v, str) else str(v) for v in self.ec_number]

        if self.rhea_id is not None and not isinstance(self.rhea_id, str):
            self.rhea_id = str(self.rhea_id)

        if self.kegg_reaction_id is not None and not isinstance(self.kegg_reaction_id, str):
            self.kegg_reaction_id = str(self.kegg_reaction_id)

        if not isinstance(self.go_terms, list):
            self.go_terms = [self.go_terms] if self.go_terms is not None else []
        self.go_terms = [v if isinstance(v, str) else str(v) for v in self.go_terms]

        if not isinstance(self.substrates, list):
            self.substrates = [self.substrates] if self.substrates is not None else []
        self.substrates = [v if isinstance(v, str) else str(v) for v in self.substrates]

        if not isinstance(self.products, list):
            self.products = [self.products] if self.products is not None else []
        self.products = [v if isinstance(v, str) else str(v) for v in self.products]

        if not isinstance(self.enzyme_genes, list):
            self.enzyme_genes = [self.enzyme_genes] if self.enzyme_genes is not None else []
        self.enzyme_genes = [v if isinstance(v, str) else str(v) for v in self.enzyme_genes]

        if self.pathway_id is not None and not isinstance(self.pathway_id, str):
            self.pathway_id = str(self.pathway_id)

        if self.note is not None and not isinstance(self.note, str):
            self.note = str(self.note)

        if self.url is not None and not isinstance(self.url, URI):
            self.url = URI(self.url)

        if self.source is not None and not isinstance(self.source, str):
            self.source = str(self.source)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class GeneProteinRecord(YAMLRoot):
    """
    Gene or protein with functional annotations
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = PFAS["GeneProteinRecord"]
    class_class_curie: ClassVar[str] = "pfas:GeneProteinRecord"
    class_name: ClassVar[str] = "GeneProteinRecord"
    class_model_uri: ClassVar[URIRef] = PFAS.GeneProteinRecord

    gene_protein_id: Union[str, GeneProteinRecordGeneProteinId] = None
    organism: Optional[str] = None
    annotation: Optional[str] = None
    ec_number: Optional[str] = None
    go_terms: Optional[Union[str, list[str]]] = empty_list()
    chebi_terms: Optional[Union[str, list[str]]] = empty_list()
    sequence_url: Optional[Union[str, URI]] = None
    source: Optional[str] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self._is_empty(self.gene_protein_id):
            self.MissingRequiredField("gene_protein_id")
        if not isinstance(self.gene_protein_id, GeneProteinRecordGeneProteinId):
            self.gene_protein_id = GeneProteinRecordGeneProteinId(self.gene_protein_id)

        if self.organism is not None and not isinstance(self.organism, str):
            self.organism = str(self.organism)

        if self.annotation is not None and not isinstance(self.annotation, str):
            self.annotation = str(self.annotation)

        if self.ec_number is not None and not isinstance(self.ec_number, str):
            self.ec_number = str(self.ec_number)

        if not isinstance(self.go_terms, list):
            self.go_terms = [self.go_terms] if self.go_terms is not None else []
        self.go_terms = [v if isinstance(v, str) else str(v) for v in self.go_terms]

        if not isinstance(self.chebi_terms, list):
            self.chebi_terms = [self.chebi_terms] if self.chebi_terms is not None else []
        self.chebi_terms = [v if isinstance(v, str) else str(v) for v in self.chebi_terms]

        if self.sequence_url is not None and not isinstance(self.sequence_url, URI):
            self.sequence_url = URI(self.sequence_url)

        if self.source is not None and not isinstance(self.source, str):
            self.source = str(self.source)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class MacromolecularStructureRecord(YAMLRoot):
    """
    3D structure of protein or complex
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = PFAS["MacromolecularStructureRecord"]
    class_class_curie: ClassVar[str] = "pfas:MacromolecularStructureRecord"
    class_name: ClassVar[str] = "MacromolecularStructureRecord"
    class_model_uri: ClassVar[URIRef] = PFAS.MacromolecularStructureRecord

    pdb_id: Union[str, MacromolecularStructureRecordPdbId] = None
    structure_name: Optional[str] = None
    components: Optional[str] = None
    method: Optional[Union[str, "StructureMethodEnum"]] = None
    resolution: Optional[float] = None
    organism: Optional[str] = None
    structure_url: Optional[Union[str, URI]] = None
    source: Optional[str] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self._is_empty(self.pdb_id):
            self.MissingRequiredField("pdb_id")
        if not isinstance(self.pdb_id, MacromolecularStructureRecordPdbId):
            self.pdb_id = MacromolecularStructureRecordPdbId(self.pdb_id)

        if self.structure_name is not None and not isinstance(self.structure_name, str):
            self.structure_name = str(self.structure_name)

        if self.components is not None and not isinstance(self.components, str):
            self.components = str(self.components)

        if self.method is not None and not isinstance(self.method, StructureMethodEnum):
            self.method = StructureMethodEnum(self.method)

        if self.resolution is not None and not isinstance(self.resolution, float):
            self.resolution = float(self.resolution)

        if self.organism is not None and not isinstance(self.organism, str):
            self.organism = str(self.organism)

        if self.structure_url is not None and not isinstance(self.structure_url, URI):
            self.structure_url = URI(self.structure_url)

        if self.source is not None and not isinstance(self.source, str):
            self.source = str(self.source)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class PublicationRecord(YAMLRoot):
    """
    Scientific publication
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = PFAS["PublicationRecord"]
    class_class_curie: ClassVar[str] = "pfas:PublicationRecord"
    class_name: ClassVar[str] = "PublicationRecord"
    class_model_uri: ClassVar[URIRef] = PFAS.PublicationRecord

    url: Union[str, PublicationRecordUrl] = None
    title: Optional[str] = None
    journal: Optional[str] = None
    year: Optional[int] = None
    authors: Optional[str] = None
    pmid: Optional[str] = None
    doi: Optional[str] = None
    source: Optional[str] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self._is_empty(self.url):
            self.MissingRequiredField("url")
        if not isinstance(self.url, PublicationRecordUrl):
            self.url = PublicationRecordUrl(self.url)

        if self.title is not None and not isinstance(self.title, str):
            self.title = str(self.title)

        if self.journal is not None and not isinstance(self.journal, str):
            self.journal = str(self.journal)

        if self.year is not None and not isinstance(self.year, int):
            self.year = int(self.year)

        if self.authors is not None and not isinstance(self.authors, str):
            self.authors = str(self.authors)

        if self.pmid is not None and not isinstance(self.pmid, str):
            self.pmid = str(self.pmid)

        if self.doi is not None and not isinstance(self.doi, str):
            self.doi = str(self.doi)

        if self.source is not None and not isinstance(self.source, str):
            self.source = str(self.source)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class DatasetRecord(YAMLRoot):
    """
    Research dataset from public repositories
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = PFAS["DatasetRecord"]
    class_class_curie: ClassVar[str] = "pfas:DatasetRecord"
    class_name: ClassVar[str] = "DatasetRecord"
    class_model_uri: ClassVar[URIRef] = PFAS.DatasetRecord

    dataset_name: Union[str, DatasetRecordDatasetName] = None
    data_type: Optional[Union[str, "DatasetTypeEnum"]] = None
    url: Optional[Union[str, URI]] = None
    accession: Optional[str] = None
    license: Optional[str] = None
    source: Optional[str] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self._is_empty(self.dataset_name):
            self.MissingRequiredField("dataset_name")
        if not isinstance(self.dataset_name, DatasetRecordDatasetName):
            self.dataset_name = DatasetRecordDatasetName(self.dataset_name)

        if self.data_type is not None and not isinstance(self.data_type, DatasetTypeEnum):
            self.data_type = DatasetTypeEnum(self.data_type)

        if self.url is not None and not isinstance(self.url, URI):
            self.url = URI(self.url)

        if self.accession is not None and not isinstance(self.accession, str):
            self.accession = str(self.accession)

        if self.license is not None and not isinstance(self.license, str):
            self.license = str(self.license)

        if self.source is not None and not isinstance(self.source, str):
            self.source = str(self.source)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class ChemicalCompoundRecord(YAMLRoot):
    """
    PFAS compounds and related chemicals
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = PFAS["ChemicalCompoundRecord"]
    class_class_curie: ClassVar[str] = "pfas:ChemicalCompoundRecord"
    class_name: ClassVar[str] = "ChemicalCompoundRecord"
    class_model_uri: ClassVar[URIRef] = PFAS.ChemicalCompoundRecord

    chemical_id: Union[str, ChemicalCompoundRecordChemicalId] = None
    chemical_name: str = None
    compound_type: Optional[Union[str, "CompoundTypeEnum"]] = None
    molecular_formula: Optional[str] = None
    molecular_weight: Optional[float] = None
    role_in_bioprocess: Optional[str] = None
    chebi_id: Optional[str] = None
    pubchem_id: Optional[str] = None
    chembl_id: Optional[str] = None
    properties: Optional[str] = None
    download_url: Optional[Union[str, URI]] = None
    source: Optional[str] = None

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

        if self.molecular_weight is not None and not isinstance(self.molecular_weight, float):
            self.molecular_weight = float(self.molecular_weight)

        if self.role_in_bioprocess is not None and not isinstance(self.role_in_bioprocess, str):
            self.role_in_bioprocess = str(self.role_in_bioprocess)

        if self.chebi_id is not None and not isinstance(self.chebi_id, str):
            self.chebi_id = str(self.chebi_id)

        if self.pubchem_id is not None and not isinstance(self.pubchem_id, str):
            self.pubchem_id = str(self.pubchem_id)

        if self.chembl_id is not None and not isinstance(self.chembl_id, str):
            self.chembl_id = str(self.chembl_id)

        if self.properties is not None and not isinstance(self.properties, str):
            self.properties = str(self.properties)

        if self.download_url is not None and not isinstance(self.download_url, URI):
            self.download_url = URI(self.download_url)

        if self.source is not None and not isinstance(self.source, str):
            self.source = str(self.source)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class AssayMeasurementRecord(YAMLRoot):
    """
    Analytical assay or measurement method
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = PFAS["AssayMeasurementRecord"]
    class_class_curie: ClassVar[str] = "pfas:AssayMeasurementRecord"
    class_name: ClassVar[str] = "AssayMeasurementRecord"
    class_model_uri: ClassVar[URIRef] = PFAS.AssayMeasurementRecord

    assay_id: Union[str, AssayMeasurementRecordAssayId] = None
    assay_name: str = None
    assay_type: Optional[Union[str, "AssayTypeEnum"]] = None
    target_analytes: Optional[str] = None
    detection_method: Optional[str] = None
    detection_limit: Optional[str] = None
    dynamic_range: Optional[str] = None
    protocol_reference: Optional[str] = None
    equipment_required: Optional[str] = None
    sample_preparation: Optional[str] = None
    data_output_format: Optional[str] = None
    download_url: Optional[Union[str, URI]] = None
    source: Optional[str] = None

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

        if self.target_analytes is not None and not isinstance(self.target_analytes, str):
            self.target_analytes = str(self.target_analytes)

        if self.detection_method is not None and not isinstance(self.detection_method, str):
            self.detection_method = str(self.detection_method)

        if self.detection_limit is not None and not isinstance(self.detection_limit, str):
            self.detection_limit = str(self.detection_limit)

        if self.dynamic_range is not None and not isinstance(self.dynamic_range, str):
            self.dynamic_range = str(self.dynamic_range)

        if self.protocol_reference is not None and not isinstance(self.protocol_reference, str):
            self.protocol_reference = str(self.protocol_reference)

        if self.equipment_required is not None and not isinstance(self.equipment_required, str):
            self.equipment_required = str(self.equipment_required)

        if self.sample_preparation is not None and not isinstance(self.sample_preparation, str):
            self.sample_preparation = str(self.sample_preparation)

        if self.data_output_format is not None and not isinstance(self.data_output_format, str):
            self.data_output_format = str(self.data_output_format)

        if self.download_url is not None and not isinstance(self.download_url, URI):
            self.download_url = URI(self.download_url)

        if self.source is not None and not isinstance(self.source, str):
            self.source = str(self.source)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class BioprocessConditionsRecord(YAMLRoot):
    """
    Experimental conditions for PFAS biodegradation
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = PFAS["BioprocessConditionsRecord"]
    class_class_curie: ClassVar[str] = "pfas:BioprocessConditionsRecord"
    class_name: ClassVar[str] = "BioprocessConditionsRecord"
    class_model_uri: ClassVar[URIRef] = PFAS.BioprocessConditionsRecord

    process_id: Union[str, BioprocessConditionsRecordProcessId] = None
    process_name: str = None
    process_type: Optional[Union[str, "ProcessTypeEnum"]] = None
    strain_used: Optional[str] = None
    ph: Optional[float] = None
    temperature: Optional[float] = None
    pfas_concentration: Optional[str] = None
    duration: Optional[str] = None
    oxygen_condition: Optional[str] = None
    medium_composition: Optional[str] = None
    degradation_percentage: Optional[float] = None
    fluoride_release: Optional[float] = None
    source: Optional[str] = None

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

        if self.ph is not None and not isinstance(self.ph, float):
            self.ph = float(self.ph)

        if self.temperature is not None and not isinstance(self.temperature, float):
            self.temperature = float(self.temperature)

        if self.pfas_concentration is not None and not isinstance(self.pfas_concentration, str):
            self.pfas_concentration = str(self.pfas_concentration)

        if self.duration is not None and not isinstance(self.duration, str):
            self.duration = str(self.duration)

        if self.oxygen_condition is not None and not isinstance(self.oxygen_condition, str):
            self.oxygen_condition = str(self.oxygen_condition)

        if self.medium_composition is not None and not isinstance(self.medium_composition, str):
            self.medium_composition = str(self.medium_composition)

        if self.degradation_percentage is not None and not isinstance(self.degradation_percentage, float):
            self.degradation_percentage = float(self.degradation_percentage)

        if self.fluoride_release is not None and not isinstance(self.fluoride_release, float):
            self.fluoride_release = float(self.fluoride_release)

        if self.source is not None and not isinstance(self.source, str):
            self.source = str(self.source)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class ScreeningResultRecord(YAMLRoot):
    """
    High-throughput screening result
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = PFAS["ScreeningResultRecord"]
    class_class_curie: ClassVar[str] = "pfas:ScreeningResultRecord"
    class_name: ClassVar[str] = "ScreeningResultRecord"
    class_model_uri: ClassVar[URIRef] = PFAS.ScreeningResultRecord

    experiment_id: Union[str, ScreeningResultRecordExperimentId] = None
    plate_coordinates: Optional[str] = None
    strain_barcode: Optional[str] = None
    screening_assay: Optional[str] = None
    measurement_values: Optional[str] = None
    hit_classification: Optional[Union[str, "HitClassificationEnum"]] = None
    source: Optional[str] = None

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

        if self.measurement_values is not None and not isinstance(self.measurement_values, str):
            self.measurement_values = str(self.measurement_values)

        if self.hit_classification is not None and not isinstance(self.hit_classification, HitClassificationEnum):
            self.hit_classification = HitClassificationEnum(self.hit_classification)

        if self.source is not None and not isinstance(self.source, str):
            self.source = str(self.source)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class ProtocolRecord(YAMLRoot):
    """
    Experimental protocol or SOP
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = PFAS["ProtocolRecord"]
    class_class_curie: ClassVar[str] = "pfas:ProtocolRecord"
    class_name: ClassVar[str] = "ProtocolRecord"
    class_model_uri: ClassVar[URIRef] = PFAS.ProtocolRecord

    protocol_id: Union[str, ProtocolRecordProtocolId] = None
    protocol_name: str = None
    protocol_type: Optional[Union[str, "ProtocolTypeEnum"]] = None
    protocol_version: Optional[str] = None
    protocol_doi: Optional[str] = None
    dbtl_iteration: Optional[int] = None
    source: Optional[str] = None

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

        if self.dbtl_iteration is not None and not isinstance(self.dbtl_iteration, int):
            self.dbtl_iteration = int(self.dbtl_iteration)

        if self.source is not None and not isinstance(self.source, str):
            self.source = str(self.source)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class TranscriptomicsRecord(YAMLRoot):
    """
    Transcriptomics experiment record from SRA, GEO, or ArrayExpress
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = PFAS["TranscriptomicsRecord"]
    class_class_curie: ClassVar[str] = "pfas:TranscriptomicsRecord"
    class_name: ClassVar[str] = "TranscriptomicsRecord"
    class_model_uri: ClassVar[URIRef] = PFAS.TranscriptomicsRecord

    experiment_id: Union[str, TranscriptomicsRecordExperimentId] = None
    organism: str = None
    study_id: Optional[str] = None
    sample_id: Optional[str] = None
    project_title: Optional[str] = None
    sample_description: Optional[str] = None
    condition: Optional[str] = None
    data_type: Optional[Union[str, "TranscriptomicsDataTypeEnum"]] = None
    sra_accession: Optional[str] = None
    geo_accession: Optional[str] = None
    arrayexpress_accession: Optional[str] = None
    size: Optional[str] = None
    publication: Optional[str] = None
    license: Optional[str] = None
    download_url: Optional[Union[str, URI]] = None
    source: Optional[str] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self._is_empty(self.experiment_id):
            self.MissingRequiredField("experiment_id")
        if not isinstance(self.experiment_id, TranscriptomicsRecordExperimentId):
            self.experiment_id = TranscriptomicsRecordExperimentId(self.experiment_id)

        if self._is_empty(self.organism):
            self.MissingRequiredField("organism")
        if not isinstance(self.organism, str):
            self.organism = str(self.organism)

        if self.study_id is not None and not isinstance(self.study_id, str):
            self.study_id = str(self.study_id)

        if self.sample_id is not None and not isinstance(self.sample_id, str):
            self.sample_id = str(self.sample_id)

        if self.project_title is not None and not isinstance(self.project_title, str):
            self.project_title = str(self.project_title)

        if self.sample_description is not None and not isinstance(self.sample_description, str):
            self.sample_description = str(self.sample_description)

        if self.condition is not None and not isinstance(self.condition, str):
            self.condition = str(self.condition)

        if self.data_type is not None and not isinstance(self.data_type, TranscriptomicsDataTypeEnum):
            self.data_type = TranscriptomicsDataTypeEnum(self.data_type)

        if self.sra_accession is not None and not isinstance(self.sra_accession, str):
            self.sra_accession = str(self.sra_accession)

        if self.geo_accession is not None and not isinstance(self.geo_accession, str):
            self.geo_accession = str(self.geo_accession)

        if self.arrayexpress_accession is not None and not isinstance(self.arrayexpress_accession, str):
            self.arrayexpress_accession = str(self.arrayexpress_accession)

        if self.size is not None and not isinstance(self.size, str):
            self.size = str(self.size)

        if self.publication is not None and not isinstance(self.publication, str):
            self.publication = str(self.publication)

        if self.license is not None and not isinstance(self.license, str):
            self.license = str(self.license)

        if self.download_url is not None and not isinstance(self.download_url, URI):
            self.download_url = URI(self.download_url)

        if self.source is not None and not isinstance(self.source, str):
            self.source = str(self.source)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class StrainRecord(YAMLRoot):
    """
    Microbial strain with standardized nomenclature and culture collection information
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = PFAS["StrainRecord"]
    class_class_curie: ClassVar[str] = "pfas:StrainRecord"
    class_name: ClassVar[str] = "StrainRecord"
    class_model_uri: ClassVar[URIRef] = PFAS.StrainRecord

    strain_id: Union[str, StrainRecordStrainId] = None
    scientific_name: str = None
    species_taxon_id: Optional[int] = None
    strain_designation: Optional[str] = None
    type_strain: Optional[Union[str, "TypeStrainEnum"]] = None
    culture_collection_ids: Optional[Union[str, list[str]]] = empty_list()
    procurement_urls: Optional[Union[Union[str, URI], list[Union[str, URI]]]] = empty_list()
    availability_status: Optional[Union[str, "AvailabilityStatusEnum"]] = None
    alternative_names: Optional[Union[str, list[str]]] = empty_list()
    biosafety_level: Optional[int] = None
    growth_requirements: Optional[str] = None
    kg_microbe_nodes: Optional[Union[str, list[str]]] = empty_list()
    notes: Optional[str] = None
    source: Optional[str] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self._is_empty(self.strain_id):
            self.MissingRequiredField("strain_id")
        if not isinstance(self.strain_id, StrainRecordStrainId):
            self.strain_id = StrainRecordStrainId(self.strain_id)

        if self._is_empty(self.scientific_name):
            self.MissingRequiredField("scientific_name")
        if not isinstance(self.scientific_name, str):
            self.scientific_name = str(self.scientific_name)

        if self.species_taxon_id is not None and not isinstance(self.species_taxon_id, int):
            self.species_taxon_id = int(self.species_taxon_id)

        if self.strain_designation is not None and not isinstance(self.strain_designation, str):
            self.strain_designation = str(self.strain_designation)

        if self.type_strain is not None and not isinstance(self.type_strain, TypeStrainEnum):
            self.type_strain = TypeStrainEnum(self.type_strain)

        if not isinstance(self.culture_collection_ids, list):
            self.culture_collection_ids = [self.culture_collection_ids] if self.culture_collection_ids is not None else []
        self.culture_collection_ids = [v if isinstance(v, str) else str(v) for v in self.culture_collection_ids]

        if not isinstance(self.procurement_urls, list):
            self.procurement_urls = [self.procurement_urls] if self.procurement_urls is not None else []
        self.procurement_urls = [v if isinstance(v, URI) else URI(v) for v in self.procurement_urls]

        if self.availability_status is not None and not isinstance(self.availability_status, AvailabilityStatusEnum):
            self.availability_status = AvailabilityStatusEnum(self.availability_status)

        if not isinstance(self.alternative_names, list):
            self.alternative_names = [self.alternative_names] if self.alternative_names is not None else []
        self.alternative_names = [v if isinstance(v, str) else str(v) for v in self.alternative_names]

        if self.biosafety_level is not None and not isinstance(self.biosafety_level, int):
            self.biosafety_level = int(self.biosafety_level)

        if self.growth_requirements is not None and not isinstance(self.growth_requirements, str):
            self.growth_requirements = str(self.growth_requirements)

        if not isinstance(self.kg_microbe_nodes, list):
            self.kg_microbe_nodes = [self.kg_microbe_nodes] if self.kg_microbe_nodes is not None else []
        self.kg_microbe_nodes = [v if isinstance(v, str) else str(v) for v in self.kg_microbe_nodes]

        if self.notes is not None and not isinstance(self.notes, str):
            self.notes = str(self.notes)

        if self.source is not None and not isinstance(self.source, str):
            self.source = str(self.source)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class GrowthMediaRecord(YAMLRoot):
    """
    Curated growth medium formulation for microbial cultivation with standardized nomenclature
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = PFAS["GrowthMediaRecord"]
    class_class_curie: ClassVar[str] = "pfas:GrowthMediaRecord"
    class_name: ClassVar[str] = "GrowthMediaRecord"
    class_model_uri: ClassVar[URIRef] = PFAS.GrowthMediaRecord

    media_id: Union[str, GrowthMediaRecordMediaId] = None
    media_name: str = None
    media_type: Optional[Union[str, "MediaTypeEnum"]] = None
    alternative_names: Optional[Union[str, list[str]]] = empty_list()
    description: Optional[str] = None
    target_organisms: Optional[str] = None
    ph: Optional[str] = None
    sterilization_method: Optional[str] = None
    references: Optional[Union[str, list[str]]] = empty_list()
    kg_microbe_nodes: Optional[Union[str, list[str]]] = empty_list()
    notes: Optional[str] = None
    source: Optional[str] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self._is_empty(self.media_id):
            self.MissingRequiredField("media_id")
        if not isinstance(self.media_id, GrowthMediaRecordMediaId):
            self.media_id = GrowthMediaRecordMediaId(self.media_id)

        if self._is_empty(self.media_name):
            self.MissingRequiredField("media_name")
        if not isinstance(self.media_name, str):
            self.media_name = str(self.media_name)

        if self.media_type is not None and not isinstance(self.media_type, MediaTypeEnum):
            self.media_type = MediaTypeEnum(self.media_type)

        if not isinstance(self.alternative_names, list):
            self.alternative_names = [self.alternative_names] if self.alternative_names is not None else []
        self.alternative_names = [v if isinstance(v, str) else str(v) for v in self.alternative_names]

        if self.description is not None and not isinstance(self.description, str):
            self.description = str(self.description)

        if self.target_organisms is not None and not isinstance(self.target_organisms, str):
            self.target_organisms = str(self.target_organisms)

        if self.ph is not None and not isinstance(self.ph, str):
            self.ph = str(self.ph)

        if self.sterilization_method is not None and not isinstance(self.sterilization_method, str):
            self.sterilization_method = str(self.sterilization_method)

        if not isinstance(self.references, list):
            self.references = [self.references] if self.references is not None else []
        self.references = [v if isinstance(v, str) else str(v) for v in self.references]

        if not isinstance(self.kg_microbe_nodes, list):
            self.kg_microbe_nodes = [self.kg_microbe_nodes] if self.kg_microbe_nodes is not None else []
        self.kg_microbe_nodes = [v if isinstance(v, str) else str(v) for v in self.kg_microbe_nodes]

        if self.notes is not None and not isinstance(self.notes, str):
            self.notes = str(self.notes)

        if self.source is not None and not isinstance(self.source, str):
            self.source = str(self.source)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class MediaIngredientRecord(YAMLRoot):
    """
    Individual ingredient in a growth medium with chemical details and concentration
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = PFAS["MediaIngredientRecord"]
    class_class_curie: ClassVar[str] = "pfas:MediaIngredientRecord"
    class_name: ClassVar[str] = "MediaIngredientRecord"
    class_model_uri: ClassVar[URIRef] = PFAS.MediaIngredientRecord

    ingredient_id: Union[str, MediaIngredientRecordIngredientId] = None
    ingredient_name: str = None
    media_id: str = None
    media_name: Optional[str] = None
    ontology_id: Optional[str] = None
    ontology_label: Optional[str] = None
    chemical_formula: Optional[str] = None
    concentration: Optional[float] = None
    unit: Optional[str] = None
    role: Optional[Union[str, "IngredientRoleEnum"]] = None
    kg_microbe_nodes: Optional[Union[str, list[str]]] = empty_list()
    notes: Optional[str] = None
    source: Optional[str] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self._is_empty(self.ingredient_id):
            self.MissingRequiredField("ingredient_id")
        if not isinstance(self.ingredient_id, MediaIngredientRecordIngredientId):
            self.ingredient_id = MediaIngredientRecordIngredientId(self.ingredient_id)

        if self._is_empty(self.ingredient_name):
            self.MissingRequiredField("ingredient_name")
        if not isinstance(self.ingredient_name, str):
            self.ingredient_name = str(self.ingredient_name)

        if self._is_empty(self.media_id):
            self.MissingRequiredField("media_id")
        if not isinstance(self.media_id, str):
            self.media_id = str(self.media_id)

        if self.media_name is not None and not isinstance(self.media_name, str):
            self.media_name = str(self.media_name)

        if self.ontology_id is not None and not isinstance(self.ontology_id, str):
            self.ontology_id = str(self.ontology_id)

        if self.ontology_label is not None and not isinstance(self.ontology_label, str):
            self.ontology_label = str(self.ontology_label)

        if self.chemical_formula is not None and not isinstance(self.chemical_formula, str):
            self.chemical_formula = str(self.chemical_formula)

        if self.concentration is not None and not isinstance(self.concentration, float):
            self.concentration = float(self.concentration)

        if self.unit is not None and not isinstance(self.unit, str):
            self.unit = str(self.unit)

        if self.role is not None and not isinstance(self.role, IngredientRoleEnum):
            self.role = IngredientRoleEnum(self.role)

        if not isinstance(self.kg_microbe_nodes, list):
            self.kg_microbe_nodes = [self.kg_microbe_nodes] if self.kg_microbe_nodes is not None else []
        self.kg_microbe_nodes = [v if isinstance(v, str) else str(v) for v in self.kg_microbe_nodes]

        if self.notes is not None and not isinstance(self.notes, str):
            self.notes = str(self.notes)

        if self.source is not None and not isinstance(self.source, str):
            self.source = str(self.source)

        super().__post_init__(**kwargs)


# Enumerations
class PathwayDatabaseEnum(EnumDefinitionImpl):

    KEGG = PermissibleValue(
        text="KEGG",
        description="Kyoto Encyclopedia of Genes and Genomes")
    MetaCyc = PermissibleValue(
        text="MetaCyc",
        description="Metabolic Pathway Database")
    BioCyc = PermissibleValue(
        text="BioCyc",
        description="Collection of Pathway/Genome Databases")
    RHEA = PermissibleValue(
        text="RHEA",
        description="Reaction database")

    _defn = EnumDefinition(
        name="PathwayDatabaseEnum",
    )

class ReactionCategoryEnum(EnumDefinitionImpl):

    dehalogenase = PermissibleValue(
        text="dehalogenase",
        description="Dehalogenase reactions for C-X bond cleavage")
    known_pfas_degraders = PermissibleValue(
        text="known_pfas_degraders",
        description="Reactions from known PFAS-degrading organisms")
    fluoride_resistance = PermissibleValue(
        text="fluoride_resistance",
        description="Fluoride resistance and transport reactions")
    hydrocarbon_degradation = PermissibleValue(
        text="hydrocarbon_degradation",
        description="Hydrocarbon degradation pathways")
    important_genes = PermissibleValue(
        text="important_genes",
        description="Important non-enzymatic genes (transporters, regulators)")
    oxygenase_cometabolism = PermissibleValue(
        text="oxygenase_cometabolism",
        description="Oxygenase and co-metabolism reactions")

    _defn = EnumDefinition(
        name="ReactionCategoryEnum",
    )

class StructureMethodEnum(EnumDefinitionImpl):

    _defn = EnumDefinition(
        name="StructureMethodEnum",
    )

    @classmethod
    def _addvals(cls):
        setattr(cls, "X-RAY DIFFRACTION",
            PermissibleValue(
                text="X-RAY DIFFRACTION",
                description="X-ray crystallography"))
        setattr(cls, "SOLUTION NMR",
            PermissibleValue(
                text="SOLUTION NMR",
                description="Nuclear magnetic resonance in solution"))
        setattr(cls, "ELECTRON MICROSCOPY",
            PermissibleValue(
                text="ELECTRON MICROSCOPY",
                description="Cryo-EM or electron microscopy"))
        setattr(cls, "SOLID-STATE NMR",
            PermissibleValue(
                text="SOLID-STATE NMR",
                description="Solid-state NMR"))
        setattr(cls, "THEORETICAL MODEL",
            PermissibleValue(
                text="THEORETICAL MODEL",
                description="Computational model (AlphaFold, etc.)"))

class DatasetTypeEnum(EnumDefinitionImpl):

    genomics = PermissibleValue(
        text="genomics",
        description="Genomic sequencing data")
    transcriptomics = PermissibleValue(
        text="transcriptomics",
        description="RNA-seq or microarray data")
    proteomics = PermissibleValue(
        text="proteomics",
        description="Protein expression data")
    metabolomics = PermissibleValue(
        text="metabolomics",
        description="Metabolite profiling data")
    metagenomics = PermissibleValue(
        text="metagenomics",
        description="Environmental metagenome data")
    other = PermissibleValue(
        text="other",
        description="Other data types")

    _defn = EnumDefinition(
        name="DatasetTypeEnum",
    )

class CompoundTypeEnum(EnumDefinitionImpl):

    perfluorinated = PermissibleValue(
        text="perfluorinated",
        description="Fully fluorinated PFAS (PFOA, PFOS)")
    polyfluorinated = PermissibleValue(
        text="polyfluorinated",
        description="Partially fluorinated PFAS (precursors)")
    fluoride = PermissibleValue(
        text="fluoride",
        description="Fluoride ion")
    metabolite = PermissibleValue(
        text="metabolite",
        description="PFAS degradation metabolite")
    degradation_product = PermissibleValue(
        text="degradation_product",
        description="Degradation product")
    fluorotelomer = PermissibleValue(
        text="fluorotelomer",
        description="Fluorotelomer alcohol")
    precursor = PermissibleValue(
        text="precursor",
        description="PFAS precursor compound")

    _defn = EnumDefinition(
        name="CompoundTypeEnum",
    )

class AssayTypeEnum(EnumDefinitionImpl):

    FACS = PermissibleValue(
        text="FACS",
        description="Fluorescence-activated cell sorting")

    _defn = EnumDefinition(
        name="AssayTypeEnum",
    )

    @classmethod
    def _addvals(cls):
        setattr(cls, "LC-MS/MS",
            PermissibleValue(
                text="LC-MS/MS",
                description="Liquid chromatography tandem mass spectrometry"))
        setattr(cls, "fluoride electrode",
            PermissibleValue(
                text="fluoride electrode",
                description="Ion-selective electrode"))
        setattr(cls, "ion chromatography",
            PermissibleValue(
                text="ion chromatography",
                description="Ion chromatography"))
        setattr(cls, "combustion IC",
            PermissibleValue(
                text="combustion IC",
                description="Combustion ion chromatography (TOF)"))
        setattr(cls, "growth assay",
            PermissibleValue(
                text="growth assay",
                description="Microbial growth assay"))
        setattr(cls, "ICP-MS",
            PermissibleValue(
                text="ICP-MS",
                description="Inductively coupled plasma mass spectrometry"))
        setattr(cls, "GC-MS",
            PermissibleValue(
                text="GC-MS",
                description="Gas chromatography mass spectrometry"))

class ProcessTypeEnum(EnumDefinitionImpl):

    aerobic_degradation = PermissibleValue(
        text="aerobic_degradation",
        description="Aerobic PFAS biodegradation")
    anaerobic_degradation = PermissibleValue(
        text="anaerobic_degradation",
        description="Anaerobic PFAS biodegradation")
    sequential_anaerobic_aerobic = PermissibleValue(
        text="sequential_anaerobic_aerobic",
        description="Sequential treatment")
    bioaugmentation = PermissibleValue(
        text="bioaugmentation",
        description="Bioaugmentation with degraders")
    consortia_based = PermissibleValue(
        text="consortia_based",
        description="Microbial consortia degradation")
    bioreactor = PermissibleValue(
        text="bioreactor",
        description="Bioreactor system")

    _defn = EnumDefinition(
        name="ProcessTypeEnum",
    )

class HitClassificationEnum(EnumDefinitionImpl):

    positive = PermissibleValue(
        text="positive",
        description="Positive hit")
    negative = PermissibleValue(
        text="negative",
        description="Negative hit")
    borderline = PermissibleValue(
        text="borderline",
        description="Borderline result")
    false_positive = PermissibleValue(
        text="false_positive",
        description="False positive")
    validated = PermissibleValue(
        text="validated",
        description="Validated hit")

    _defn = EnumDefinition(
        name="HitClassificationEnum",
    )

class ProtocolTypeEnum(EnumDefinitionImpl):

    assay_protocol = PermissibleValue(
        text="assay_protocol",
        description="Analytical assay protocol")
    cultivation_protocol = PermissibleValue(
        text="cultivation_protocol",
        description="Microbial cultivation protocol")
    extraction_protocol = PermissibleValue(
        text="extraction_protocol",
        description="Compound extraction protocol")
    transformation_protocol = PermissibleValue(
        text="transformation_protocol",
        description="Genetic transformation protocol")
    screening_protocol = PermissibleValue(
        text="screening_protocol",
        description="High-throughput screening protocol")
    degradation_protocol = PermissibleValue(
        text="degradation_protocol",
        description="PFAS degradation protocol")

    _defn = EnumDefinition(
        name="ProtocolTypeEnum",
    )

class TranscriptomicsDataTypeEnum(EnumDefinitionImpl):
    """
    Type of transcriptomics or gene expression data
    """
    microarray = PermissibleValue(
        text="microarray",
        description="Gene expression microarray")
    metatranscriptomics = PermissibleValue(
        text="metatranscriptomics",
        description="Community-level transcriptomics")

    _defn = EnumDefinition(
        name="TranscriptomicsDataTypeEnum",
        description="Type of transcriptomics or gene expression data",
    )

    @classmethod
    def _addvals(cls):
        setattr(cls, "RNA-Seq",
            PermissibleValue(
                text="RNA-Seq",
                description="RNA sequencing (Illumina, PacBio, Nanopore)"))
        setattr(cls, "single-cell RNA-seq",
            PermissibleValue(
                text="single-cell RNA-seq",
                description="Single-cell RNA sequencing"))
        setattr(cls, "differential expression",
            PermissibleValue(
                text="differential expression",
                description="Differential gene expression analysis"))
        setattr(cls, "time-course",
            PermissibleValue(
                text="time-course",
                description="Time-series transcriptomics"))
        setattr(cls, "dual RNA-seq",
            PermissibleValue(
                text="dual RNA-seq",
                description="Host-pathogen dual RNA-seq"))
        setattr(cls, "small RNA-seq",
            PermissibleValue(
                text="small RNA-seq",
                description="Small RNA or miRNA sequencing"))
        setattr(cls, "long-read RNA-seq",
            PermissibleValue(
                text="long-read RNA-seq",
                description="Long-read transcriptomics (PacBio, Nanopore)"))

class TypeStrainEnum(EnumDefinitionImpl):
    """
    Type strain designation
    """
    yes = PermissibleValue(
        text="yes",
        description="Nomenclatural type strain for the species")
    no = PermissibleValue(
        text="no",
        description="Not a type strain")
    unknown = PermissibleValue(
        text="unknown",
        description="Type strain status unknown")

    _defn = EnumDefinition(
        name="TypeStrainEnum",
        description="Type strain designation",
    )

class AvailabilityStatusEnum(EnumDefinitionImpl):
    """
    Culture collection availability status
    """
    available = PermissibleValue(
        text="available",
        description="Currently available for purchase/request")
    restricted = PermissibleValue(
        text="restricted",
        description="Available with restrictions (MTA, permits, etc.)")
    discontinued = PermissibleValue(
        text="discontinued",
        description="No longer maintained in collection")
    unknown = PermissibleValue(
        text="unknown",
        description="Availability status unknown")

    _defn = EnumDefinition(
        name="AvailabilityStatusEnum",
        description="Culture collection availability status",
    )

class MediaTypeEnum(EnumDefinitionImpl):
    """
    Type of growth medium
    """
    minimal = PermissibleValue(
        text="minimal",
        description="Minimal medium with defined chemical composition")
    complex = PermissibleValue(
        text="complex",
        description="Complex medium with undefined components (extracts, peptones)")
    selective = PermissibleValue(
        text="selective",
        description="Selective medium favoring specific organisms")
    differential = PermissibleValue(
        text="differential",
        description="Differential medium distinguishing organisms by visible changes")
    enrichment = PermissibleValue(
        text="enrichment",
        description="Enrichment medium promoting growth of target organisms")

    _defn = EnumDefinition(
        name="MediaTypeEnum",
        description="Type of growth medium",
    )

class IngredientRoleEnum(EnumDefinitionImpl):
    """
    Function of ingredient in growth medium
    """
    mineral = PermissibleValue(
        text="mineral",
        description="Essential mineral (Mg, Ca, etc.)")
    buffer = PermissibleValue(
        text="buffer",
        description="pH buffer (phosphate, HEPES, etc.)")
    salt = PermissibleValue(
        text="salt",
        description="Osmotic support or ionic strength")
    vitamin = PermissibleValue(
        text="vitamin",
        description="Vitamin or growth factor")
    indicator = PermissibleValue(
        text="indicator",
        description="pH or metabolic indicator")

    _defn = EnumDefinition(
        name="IngredientRoleEnum",
        description="Function of ingredient in growth medium",
    )

    @classmethod
    def _addvals(cls):
        setattr(cls, "carbon source",
            PermissibleValue(
                text="carbon source",
                description="Primary carbon source for growth"))
        setattr(cls, "nitrogen source",
            PermissibleValue(
                text="nitrogen source",
                description="Nitrogen source (nitrate, ammonium, amino acids)"))
        setattr(cls, "trace element",
            PermissibleValue(
                text="trace element",
                description="Micronutrient or trace element mix"))
        setattr(cls, "solidifying agent",
            PermissibleValue(
                text="solidifying agent",
                description="Agar or gellan gum for solid media"))
        setattr(cls, "protein source",
            PermissibleValue(
                text="protein source",
                description="Peptone, tryptone, or protein hydrolysate"))
        setattr(cls, "vitamin source",
            PermissibleValue(
                text="vitamin source",
                description="Yeast extract or vitamin mix"))
        setattr(cls, "amino acid source",
            PermissibleValue(
                text="amino acid source",
                description="Casamino acids or amino acid mix"))

# Slots
class slots:
    pass

slots.database__genomes = Slot(uri=PFAS.genomes, name="database__genomes", curie=PFAS.curie('genomes'),
                   model_uri=PFAS.database__genomes, domain=None, range=Optional[Union[Union[str, GenomeRecordScientificName], list[Union[str, GenomeRecordScientificName]]]])

slots.database__biosamples = Slot(uri=PFAS.biosamples, name="database__biosamples", curie=PFAS.curie('biosamples'),
                   model_uri=PFAS.database__biosamples, domain=None, range=Optional[Union[Union[str, BiosampleRecordSampleId], list[Union[str, BiosampleRecordSampleId]]]])

slots.database__pathways = Slot(uri=PFAS.pathways, name="database__pathways", curie=PFAS.curie('pathways'),
                   model_uri=PFAS.database__pathways, domain=None, range=Optional[Union[Union[str, PathwayRecordPathwayId], list[Union[str, PathwayRecordPathwayId]]]])

slots.database__genes_proteins = Slot(uri=PFAS.genes_proteins, name="database__genes_proteins", curie=PFAS.curie('genes_proteins'),
                   model_uri=PFAS.database__genes_proteins, domain=None, range=Optional[Union[Union[str, GeneProteinRecordGeneProteinId], list[Union[str, GeneProteinRecordGeneProteinId]]]])

slots.database__structures = Slot(uri=PFAS.structures, name="database__structures", curie=PFAS.curie('structures'),
                   model_uri=PFAS.database__structures, domain=None, range=Optional[Union[Union[str, MacromolecularStructureRecordPdbId], list[Union[str, MacromolecularStructureRecordPdbId]]]])

slots.database__publications = Slot(uri=PFAS.publications, name="database__publications", curie=PFAS.curie('publications'),
                   model_uri=PFAS.database__publications, domain=None, range=Optional[Union[Union[str, PublicationRecordUrl], list[Union[str, PublicationRecordUrl]]]])

slots.database__datasets = Slot(uri=PFAS.datasets, name="database__datasets", curie=PFAS.curie('datasets'),
                   model_uri=PFAS.database__datasets, domain=None, range=Optional[Union[Union[str, DatasetRecordDatasetName], list[Union[str, DatasetRecordDatasetName]]]])

slots.database__chemicals = Slot(uri=PFAS.chemicals, name="database__chemicals", curie=PFAS.curie('chemicals'),
                   model_uri=PFAS.database__chemicals, domain=None, range=Optional[Union[Union[str, ChemicalCompoundRecordChemicalId], list[Union[str, ChemicalCompoundRecordChemicalId]]]])

slots.database__assays = Slot(uri=PFAS.assays, name="database__assays", curie=PFAS.curie('assays'),
                   model_uri=PFAS.database__assays, domain=None, range=Optional[Union[Union[str, AssayMeasurementRecordAssayId], list[Union[str, AssayMeasurementRecordAssayId]]]])

slots.database__bioprocesses = Slot(uri=PFAS.bioprocesses, name="database__bioprocesses", curie=PFAS.curie('bioprocesses'),
                   model_uri=PFAS.database__bioprocesses, domain=None, range=Optional[Union[Union[str, BioprocessConditionsRecordProcessId], list[Union[str, BioprocessConditionsRecordProcessId]]]])

slots.database__screening_results = Slot(uri=PFAS.screening_results, name="database__screening_results", curie=PFAS.curie('screening_results'),
                   model_uri=PFAS.database__screening_results, domain=None, range=Optional[Union[Union[str, ScreeningResultRecordExperimentId], list[Union[str, ScreeningResultRecordExperimentId]]]])

slots.database__protocols = Slot(uri=PFAS.protocols, name="database__protocols", curie=PFAS.curie('protocols'),
                   model_uri=PFAS.database__protocols, domain=None, range=Optional[Union[Union[str, ProtocolRecordProtocolId], list[Union[str, ProtocolRecordProtocolId]]]])

slots.database__reactions = Slot(uri=PFAS.reactions, name="database__reactions", curie=PFAS.curie('reactions'),
                   model_uri=PFAS.database__reactions, domain=None, range=Optional[Union[Union[str, ReactionRecordReactionId], list[Union[str, ReactionRecordReactionId]]]])

slots.database__transcriptomics = Slot(uri=PFAS.transcriptomics, name="database__transcriptomics", curie=PFAS.curie('transcriptomics'),
                   model_uri=PFAS.database__transcriptomics, domain=None, range=Optional[Union[Union[str, TranscriptomicsRecordExperimentId], list[Union[str, TranscriptomicsRecordExperimentId]]]])

slots.database__strains = Slot(uri=PFAS.strains, name="database__strains", curie=PFAS.curie('strains'),
                   model_uri=PFAS.database__strains, domain=None, range=Optional[Union[Union[str, StrainRecordStrainId], list[Union[str, StrainRecordStrainId]]]])

slots.database__growth_media = Slot(uri=PFAS.growth_media, name="database__growth_media", curie=PFAS.curie('growth_media'),
                   model_uri=PFAS.database__growth_media, domain=None, range=Optional[Union[Union[str, GrowthMediaRecordMediaId], list[Union[str, GrowthMediaRecordMediaId]]]])

slots.database__media_ingredients = Slot(uri=PFAS.media_ingredients, name="database__media_ingredients", curie=PFAS.curie('media_ingredients'),
                   model_uri=PFAS.database__media_ingredients, domain=None, range=Optional[Union[Union[str, MediaIngredientRecordIngredientId], list[Union[str, MediaIngredientRecordIngredientId]]]])

slots.genomeRecord__scientific_name = Slot(uri=PFAS.scientific_name, name="genomeRecord__scientific_name", curie=PFAS.curie('scientific_name'),
                   model_uri=PFAS.genomeRecord__scientific_name, domain=None, range=URIRef)

slots.genomeRecord__ncbi_taxon_id = Slot(uri=PFAS.ncbi_taxon_id, name="genomeRecord__ncbi_taxon_id", curie=PFAS.curie('ncbi_taxon_id'),
                   model_uri=PFAS.genomeRecord__ncbi_taxon_id, domain=None, range=Optional[str],
                   pattern=re.compile(r'^\d+$'))

slots.genomeRecord__genome_identifier = Slot(uri=PFAS.genome_identifier, name="genomeRecord__genome_identifier", curie=PFAS.curie('genome_identifier'),
                   model_uri=PFAS.genomeRecord__genome_identifier, domain=None, range=Optional[str],
                   pattern=re.compile(r'^(GCF_|GCA_|\d+).*'))

slots.genomeRecord__annotation_download_url = Slot(uri=PFAS.annotation_download_url, name="genomeRecord__annotation_download_url", curie=PFAS.curie('annotation_download_url'),
                   model_uri=PFAS.genomeRecord__annotation_download_url, domain=None, range=Optional[Union[str, URI]])

slots.genomeRecord__source = Slot(uri=PFAS.source, name="genomeRecord__source", curie=PFAS.curie('source'),
                   model_uri=PFAS.genomeRecord__source, domain=None, range=Optional[str])

slots.biosampleRecord__sample_id = Slot(uri=PFAS.sample_id, name="biosampleRecord__sample_id", curie=PFAS.curie('sample_id'),
                   model_uri=PFAS.biosampleRecord__sample_id, domain=None, range=URIRef,
                   pattern=re.compile(r'^SAMN\d+$'))

slots.biosampleRecord__sample_name = Slot(uri=PFAS.sample_name, name="biosampleRecord__sample_name", curie=PFAS.curie('sample_name'),
                   model_uri=PFAS.biosampleRecord__sample_name, domain=None, range=Optional[str])

slots.biosampleRecord__organism = Slot(uri=PFAS.organism, name="biosampleRecord__organism", curie=PFAS.curie('organism'),
                   model_uri=PFAS.biosampleRecord__organism, domain=None, range=Optional[str])

slots.biosampleRecord__download_url = Slot(uri=PFAS.download_url, name="biosampleRecord__download_url", curie=PFAS.curie('download_url'),
                   model_uri=PFAS.biosampleRecord__download_url, domain=None, range=Optional[Union[str, URI]])

slots.biosampleRecord__source = Slot(uri=PFAS.source, name="biosampleRecord__source", curie=PFAS.curie('source'),
                   model_uri=PFAS.biosampleRecord__source, domain=None, range=Optional[str])

slots.pathwayRecord__pathway_id = Slot(uri=PFAS.pathway_id, name="pathwayRecord__pathway_id", curie=PFAS.curie('pathway_id'),
                   model_uri=PFAS.pathwayRecord__pathway_id, domain=None, range=URIRef)

slots.pathwayRecord__pathway_name = Slot(uri=PFAS.pathway_name, name="pathwayRecord__pathway_name", curie=PFAS.curie('pathway_name'),
                   model_uri=PFAS.pathwayRecord__pathway_name, domain=None, range=str)

slots.pathwayRecord__database = Slot(uri=PFAS.database, name="pathwayRecord__database", curie=PFAS.curie('database'),
                   model_uri=PFAS.pathwayRecord__database, domain=None, range=Optional[Union[str, "PathwayDatabaseEnum"]])

slots.pathwayRecord__url = Slot(uri=PFAS.url, name="pathwayRecord__url", curie=PFAS.curie('url'),
                   model_uri=PFAS.pathwayRecord__url, domain=None, range=Optional[Union[str, URI]])

slots.pathwayRecord__genes = Slot(uri=PFAS.genes, name="pathwayRecord__genes", curie=PFAS.curie('genes'),
                   model_uri=PFAS.pathwayRecord__genes, domain=None, range=Optional[Union[str, list[str]]])

slots.pathwayRecord__genes_kegg = Slot(uri=PFAS.genes_kegg, name="pathwayRecord__genes_kegg", curie=PFAS.curie('genes_kegg'),
                   model_uri=PFAS.pathwayRecord__genes_kegg, domain=None, range=Optional[Union[str, list[str]]],
                   pattern=re.compile(r'^K\d{5}$'))

slots.pathwayRecord__source = Slot(uri=PFAS.source, name="pathwayRecord__source", curie=PFAS.curie('source'),
                   model_uri=PFAS.pathwayRecord__source, domain=None, range=Optional[str])

slots.reactionRecord__reaction_id = Slot(uri=PFAS.reaction_id, name="reactionRecord__reaction_id", curie=PFAS.curie('reaction_id'),
                   model_uri=PFAS.reactionRecord__reaction_id, domain=None, range=URIRef)

slots.reactionRecord__reaction_name = Slot(uri=PFAS.reaction_name, name="reactionRecord__reaction_name", curie=PFAS.curie('reaction_name'),
                   model_uri=PFAS.reactionRecord__reaction_name, domain=None, range=Optional[str])

slots.reactionRecord__equation = Slot(uri=PFAS.equation, name="reactionRecord__equation", curie=PFAS.curie('equation'),
                   model_uri=PFAS.reactionRecord__equation, domain=None, range=str)

slots.reactionRecord__reaction_category = Slot(uri=PFAS.reaction_category, name="reactionRecord__reaction_category", curie=PFAS.curie('reaction_category'),
                   model_uri=PFAS.reactionRecord__reaction_category, domain=None, range=Union[str, "ReactionCategoryEnum"])

slots.reactionRecord__enzyme_class = Slot(uri=PFAS.enzyme_class, name="reactionRecord__enzyme_class", curie=PFAS.curie('enzyme_class'),
                   model_uri=PFAS.reactionRecord__enzyme_class, domain=None, range=Optional[str])

slots.reactionRecord__ec_number = Slot(uri=PFAS.ec_number, name="reactionRecord__ec_number", curie=PFAS.curie('ec_number'),
                   model_uri=PFAS.reactionRecord__ec_number, domain=None, range=Optional[Union[str, list[str]]],
                   pattern=re.compile(r'^EC:\d+\.\d+\.\d+\.\d+$|^EC:\d+\.\d+\.\d+\.-$'))

slots.reactionRecord__rhea_id = Slot(uri=PFAS.rhea_id, name="reactionRecord__rhea_id", curie=PFAS.curie('rhea_id'),
                   model_uri=PFAS.reactionRecord__rhea_id, domain=None, range=Optional[str],
                   pattern=re.compile(r'^RHEA:\d+$'))

slots.reactionRecord__kegg_reaction_id = Slot(uri=PFAS.kegg_reaction_id, name="reactionRecord__kegg_reaction_id", curie=PFAS.curie('kegg_reaction_id'),
                   model_uri=PFAS.reactionRecord__kegg_reaction_id, domain=None, range=Optional[str],
                   pattern=re.compile(r'^R\d{5}$'))

slots.reactionRecord__go_terms = Slot(uri=PFAS.go_terms, name="reactionRecord__go_terms", curie=PFAS.curie('go_terms'),
                   model_uri=PFAS.reactionRecord__go_terms, domain=None, range=Optional[Union[str, list[str]]],
                   pattern=re.compile(r'^GO:\d{7}$'))

slots.reactionRecord__substrates = Slot(uri=PFAS.substrates, name="reactionRecord__substrates", curie=PFAS.curie('substrates'),
                   model_uri=PFAS.reactionRecord__substrates, domain=None, range=Optional[Union[str, list[str]]])

slots.reactionRecord__products = Slot(uri=PFAS.products, name="reactionRecord__products", curie=PFAS.curie('products'),
                   model_uri=PFAS.reactionRecord__products, domain=None, range=Optional[Union[str, list[str]]])

slots.reactionRecord__enzyme_genes = Slot(uri=PFAS.enzyme_genes, name="reactionRecord__enzyme_genes", curie=PFAS.curie('enzyme_genes'),
                   model_uri=PFAS.reactionRecord__enzyme_genes, domain=None, range=Optional[Union[str, list[str]]])

slots.reactionRecord__pathway_id = Slot(uri=PFAS.pathway_id, name="reactionRecord__pathway_id", curie=PFAS.curie('pathway_id'),
                   model_uri=PFAS.reactionRecord__pathway_id, domain=None, range=Optional[str])

slots.reactionRecord__note = Slot(uri=PFAS.note, name="reactionRecord__note", curie=PFAS.curie('note'),
                   model_uri=PFAS.reactionRecord__note, domain=None, range=Optional[str])

slots.reactionRecord__url = Slot(uri=PFAS.url, name="reactionRecord__url", curie=PFAS.curie('url'),
                   model_uri=PFAS.reactionRecord__url, domain=None, range=Optional[Union[str, URI]])

slots.reactionRecord__source = Slot(uri=PFAS.source, name="reactionRecord__source", curie=PFAS.curie('source'),
                   model_uri=PFAS.reactionRecord__source, domain=None, range=Optional[str])

slots.geneProteinRecord__gene_protein_id = Slot(uri=PFAS.gene_protein_id, name="geneProteinRecord__gene_protein_id", curie=PFAS.curie('gene_protein_id'),
                   model_uri=PFAS.geneProteinRecord__gene_protein_id, domain=None, range=URIRef)

slots.geneProteinRecord__organism = Slot(uri=PFAS.organism, name="geneProteinRecord__organism", curie=PFAS.curie('organism'),
                   model_uri=PFAS.geneProteinRecord__organism, domain=None, range=Optional[str])

slots.geneProteinRecord__annotation = Slot(uri=PFAS.annotation, name="geneProteinRecord__annotation", curie=PFAS.curie('annotation'),
                   model_uri=PFAS.geneProteinRecord__annotation, domain=None, range=Optional[str])

slots.geneProteinRecord__ec_number = Slot(uri=PFAS.ec_number, name="geneProteinRecord__ec_number", curie=PFAS.curie('ec_number'),
                   model_uri=PFAS.geneProteinRecord__ec_number, domain=None, range=Optional[str],
                   pattern=re.compile(r'^\d+\.\d+\.\d+\.\d+$|^\d+\.\d+\.\d+\.-$'))

slots.geneProteinRecord__go_terms = Slot(uri=PFAS.go_terms, name="geneProteinRecord__go_terms", curie=PFAS.curie('go_terms'),
                   model_uri=PFAS.geneProteinRecord__go_terms, domain=None, range=Optional[Union[str, list[str]]],
                   pattern=re.compile(r'^GO:\d{7}$'))

slots.geneProteinRecord__chebi_terms = Slot(uri=PFAS.chebi_terms, name="geneProteinRecord__chebi_terms", curie=PFAS.curie('chebi_terms'),
                   model_uri=PFAS.geneProteinRecord__chebi_terms, domain=None, range=Optional[Union[str, list[str]]],
                   pattern=re.compile(r'^CHEBI:\d+$'))

slots.geneProteinRecord__sequence_url = Slot(uri=PFAS.sequence_url, name="geneProteinRecord__sequence_url", curie=PFAS.curie('sequence_url'),
                   model_uri=PFAS.geneProteinRecord__sequence_url, domain=None, range=Optional[Union[str, URI]])

slots.geneProteinRecord__source = Slot(uri=PFAS.source, name="geneProteinRecord__source", curie=PFAS.curie('source'),
                   model_uri=PFAS.geneProteinRecord__source, domain=None, range=Optional[str])

slots.macromolecularStructureRecord__pdb_id = Slot(uri=PFAS.pdb_id, name="macromolecularStructureRecord__pdb_id", curie=PFAS.curie('pdb_id'),
                   model_uri=PFAS.macromolecularStructureRecord__pdb_id, domain=None, range=URIRef,
                   pattern=re.compile(r'^[0-9][A-Za-z0-9]{3}$'))

slots.macromolecularStructureRecord__structure_name = Slot(uri=PFAS.structure_name, name="macromolecularStructureRecord__structure_name", curie=PFAS.curie('structure_name'),
                   model_uri=PFAS.macromolecularStructureRecord__structure_name, domain=None, range=Optional[str])

slots.macromolecularStructureRecord__components = Slot(uri=PFAS.components, name="macromolecularStructureRecord__components", curie=PFAS.curie('components'),
                   model_uri=PFAS.macromolecularStructureRecord__components, domain=None, range=Optional[str])

slots.macromolecularStructureRecord__method = Slot(uri=PFAS.method, name="macromolecularStructureRecord__method", curie=PFAS.curie('method'),
                   model_uri=PFAS.macromolecularStructureRecord__method, domain=None, range=Optional[Union[str, "StructureMethodEnum"]])

slots.macromolecularStructureRecord__resolution = Slot(uri=PFAS.resolution, name="macromolecularStructureRecord__resolution", curie=PFAS.curie('resolution'),
                   model_uri=PFAS.macromolecularStructureRecord__resolution, domain=None, range=Optional[float])

slots.macromolecularStructureRecord__organism = Slot(uri=PFAS.organism, name="macromolecularStructureRecord__organism", curie=PFAS.curie('organism'),
                   model_uri=PFAS.macromolecularStructureRecord__organism, domain=None, range=Optional[str])

slots.macromolecularStructureRecord__structure_url = Slot(uri=PFAS.structure_url, name="macromolecularStructureRecord__structure_url", curie=PFAS.curie('structure_url'),
                   model_uri=PFAS.macromolecularStructureRecord__structure_url, domain=None, range=Optional[Union[str, URI]])

slots.macromolecularStructureRecord__source = Slot(uri=PFAS.source, name="macromolecularStructureRecord__source", curie=PFAS.curie('source'),
                   model_uri=PFAS.macromolecularStructureRecord__source, domain=None, range=Optional[str])

slots.publicationRecord__url = Slot(uri=PFAS.url, name="publicationRecord__url", curie=PFAS.curie('url'),
                   model_uri=PFAS.publicationRecord__url, domain=None, range=URIRef)

slots.publicationRecord__title = Slot(uri=PFAS.title, name="publicationRecord__title", curie=PFAS.curie('title'),
                   model_uri=PFAS.publicationRecord__title, domain=None, range=Optional[str])

slots.publicationRecord__journal = Slot(uri=PFAS.journal, name="publicationRecord__journal", curie=PFAS.curie('journal'),
                   model_uri=PFAS.publicationRecord__journal, domain=None, range=Optional[str])

slots.publicationRecord__year = Slot(uri=PFAS.year, name="publicationRecord__year", curie=PFAS.curie('year'),
                   model_uri=PFAS.publicationRecord__year, domain=None, range=Optional[int])

slots.publicationRecord__authors = Slot(uri=PFAS.authors, name="publicationRecord__authors", curie=PFAS.curie('authors'),
                   model_uri=PFAS.publicationRecord__authors, domain=None, range=Optional[str])

slots.publicationRecord__pmid = Slot(uri=PFAS.pmid, name="publicationRecord__pmid", curie=PFAS.curie('pmid'),
                   model_uri=PFAS.publicationRecord__pmid, domain=None, range=Optional[str],
                   pattern=re.compile(r'^\d+$'))

slots.publicationRecord__doi = Slot(uri=PFAS.doi, name="publicationRecord__doi", curie=PFAS.curie('doi'),
                   model_uri=PFAS.publicationRecord__doi, domain=None, range=Optional[str],
                   pattern=re.compile(r'^10\.\d+/.*$'))

slots.publicationRecord__source = Slot(uri=PFAS.source, name="publicationRecord__source", curie=PFAS.curie('source'),
                   model_uri=PFAS.publicationRecord__source, domain=None, range=Optional[str])

slots.datasetRecord__dataset_name = Slot(uri=PFAS.dataset_name, name="datasetRecord__dataset_name", curie=PFAS.curie('dataset_name'),
                   model_uri=PFAS.datasetRecord__dataset_name, domain=None, range=URIRef)

slots.datasetRecord__data_type = Slot(uri=PFAS.data_type, name="datasetRecord__data_type", curie=PFAS.curie('data_type'),
                   model_uri=PFAS.datasetRecord__data_type, domain=None, range=Optional[Union[str, "DatasetTypeEnum"]])

slots.datasetRecord__url = Slot(uri=PFAS.url, name="datasetRecord__url", curie=PFAS.curie('url'),
                   model_uri=PFAS.datasetRecord__url, domain=None, range=Optional[Union[str, URI]])

slots.datasetRecord__accession = Slot(uri=PFAS.accession, name="datasetRecord__accession", curie=PFAS.curie('accession'),
                   model_uri=PFAS.datasetRecord__accession, domain=None, range=Optional[str])

slots.datasetRecord__license = Slot(uri=PFAS.license, name="datasetRecord__license", curie=PFAS.curie('license'),
                   model_uri=PFAS.datasetRecord__license, domain=None, range=Optional[str])

slots.datasetRecord__source = Slot(uri=PFAS.source, name="datasetRecord__source", curie=PFAS.curie('source'),
                   model_uri=PFAS.datasetRecord__source, domain=None, range=Optional[str])

slots.chemicalCompoundRecord__chemical_id = Slot(uri=PFAS.chemical_id, name="chemicalCompoundRecord__chemical_id", curie=PFAS.curie('chemical_id'),
                   model_uri=PFAS.chemicalCompoundRecord__chemical_id, domain=None, range=URIRef)

slots.chemicalCompoundRecord__chemical_name = Slot(uri=PFAS.chemical_name, name="chemicalCompoundRecord__chemical_name", curie=PFAS.curie('chemical_name'),
                   model_uri=PFAS.chemicalCompoundRecord__chemical_name, domain=None, range=str)

slots.chemicalCompoundRecord__compound_type = Slot(uri=PFAS.compound_type, name="chemicalCompoundRecord__compound_type", curie=PFAS.curie('compound_type'),
                   model_uri=PFAS.chemicalCompoundRecord__compound_type, domain=None, range=Optional[Union[str, "CompoundTypeEnum"]])

slots.chemicalCompoundRecord__molecular_formula = Slot(uri=PFAS.molecular_formula, name="chemicalCompoundRecord__molecular_formula", curie=PFAS.curie('molecular_formula'),
                   model_uri=PFAS.chemicalCompoundRecord__molecular_formula, domain=None, range=Optional[str])

slots.chemicalCompoundRecord__molecular_weight = Slot(uri=PFAS.molecular_weight, name="chemicalCompoundRecord__molecular_weight", curie=PFAS.curie('molecular_weight'),
                   model_uri=PFAS.chemicalCompoundRecord__molecular_weight, domain=None, range=Optional[float])

slots.chemicalCompoundRecord__role_in_bioprocess = Slot(uri=PFAS.role_in_bioprocess, name="chemicalCompoundRecord__role_in_bioprocess", curie=PFAS.curie('role_in_bioprocess'),
                   model_uri=PFAS.chemicalCompoundRecord__role_in_bioprocess, domain=None, range=Optional[str])

slots.chemicalCompoundRecord__chebi_id = Slot(uri=PFAS.chebi_id, name="chemicalCompoundRecord__chebi_id", curie=PFAS.curie('chebi_id'),
                   model_uri=PFAS.chemicalCompoundRecord__chebi_id, domain=None, range=Optional[str],
                   pattern=re.compile(r'^CHEBI:\d+$'))

slots.chemicalCompoundRecord__pubchem_id = Slot(uri=PFAS.pubchem_id, name="chemicalCompoundRecord__pubchem_id", curie=PFAS.curie('pubchem_id'),
                   model_uri=PFAS.chemicalCompoundRecord__pubchem_id, domain=None, range=Optional[str],
                   pattern=re.compile(r'^\d+$'))

slots.chemicalCompoundRecord__chembl_id = Slot(uri=PFAS.chembl_id, name="chemicalCompoundRecord__chembl_id", curie=PFAS.curie('chembl_id'),
                   model_uri=PFAS.chemicalCompoundRecord__chembl_id, domain=None, range=Optional[str])

slots.chemicalCompoundRecord__properties = Slot(uri=PFAS.properties, name="chemicalCompoundRecord__properties", curie=PFAS.curie('properties'),
                   model_uri=PFAS.chemicalCompoundRecord__properties, domain=None, range=Optional[str])

slots.chemicalCompoundRecord__download_url = Slot(uri=PFAS.download_url, name="chemicalCompoundRecord__download_url", curie=PFAS.curie('download_url'),
                   model_uri=PFAS.chemicalCompoundRecord__download_url, domain=None, range=Optional[Union[str, URI]])

slots.chemicalCompoundRecord__source = Slot(uri=PFAS.source, name="chemicalCompoundRecord__source", curie=PFAS.curie('source'),
                   model_uri=PFAS.chemicalCompoundRecord__source, domain=None, range=Optional[str])

slots.assayMeasurementRecord__assay_id = Slot(uri=PFAS.assay_id, name="assayMeasurementRecord__assay_id", curie=PFAS.curie('assay_id'),
                   model_uri=PFAS.assayMeasurementRecord__assay_id, domain=None, range=URIRef)

slots.assayMeasurementRecord__assay_name = Slot(uri=PFAS.assay_name, name="assayMeasurementRecord__assay_name", curie=PFAS.curie('assay_name'),
                   model_uri=PFAS.assayMeasurementRecord__assay_name, domain=None, range=str)

slots.assayMeasurementRecord__assay_type = Slot(uri=PFAS.assay_type, name="assayMeasurementRecord__assay_type", curie=PFAS.curie('assay_type'),
                   model_uri=PFAS.assayMeasurementRecord__assay_type, domain=None, range=Optional[Union[str, "AssayTypeEnum"]])

slots.assayMeasurementRecord__target_analytes = Slot(uri=PFAS.target_analytes, name="assayMeasurementRecord__target_analytes", curie=PFAS.curie('target_analytes'),
                   model_uri=PFAS.assayMeasurementRecord__target_analytes, domain=None, range=Optional[str])

slots.assayMeasurementRecord__detection_method = Slot(uri=PFAS.detection_method, name="assayMeasurementRecord__detection_method", curie=PFAS.curie('detection_method'),
                   model_uri=PFAS.assayMeasurementRecord__detection_method, domain=None, range=Optional[str])

slots.assayMeasurementRecord__detection_limit = Slot(uri=PFAS.detection_limit, name="assayMeasurementRecord__detection_limit", curie=PFAS.curie('detection_limit'),
                   model_uri=PFAS.assayMeasurementRecord__detection_limit, domain=None, range=Optional[str])

slots.assayMeasurementRecord__dynamic_range = Slot(uri=PFAS.dynamic_range, name="assayMeasurementRecord__dynamic_range", curie=PFAS.curie('dynamic_range'),
                   model_uri=PFAS.assayMeasurementRecord__dynamic_range, domain=None, range=Optional[str])

slots.assayMeasurementRecord__protocol_reference = Slot(uri=PFAS.protocol_reference, name="assayMeasurementRecord__protocol_reference", curie=PFAS.curie('protocol_reference'),
                   model_uri=PFAS.assayMeasurementRecord__protocol_reference, domain=None, range=Optional[str])

slots.assayMeasurementRecord__equipment_required = Slot(uri=PFAS.equipment_required, name="assayMeasurementRecord__equipment_required", curie=PFAS.curie('equipment_required'),
                   model_uri=PFAS.assayMeasurementRecord__equipment_required, domain=None, range=Optional[str])

slots.assayMeasurementRecord__sample_preparation = Slot(uri=PFAS.sample_preparation, name="assayMeasurementRecord__sample_preparation", curie=PFAS.curie('sample_preparation'),
                   model_uri=PFAS.assayMeasurementRecord__sample_preparation, domain=None, range=Optional[str])

slots.assayMeasurementRecord__data_output_format = Slot(uri=PFAS.data_output_format, name="assayMeasurementRecord__data_output_format", curie=PFAS.curie('data_output_format'),
                   model_uri=PFAS.assayMeasurementRecord__data_output_format, domain=None, range=Optional[str])

slots.assayMeasurementRecord__download_url = Slot(uri=PFAS.download_url, name="assayMeasurementRecord__download_url", curie=PFAS.curie('download_url'),
                   model_uri=PFAS.assayMeasurementRecord__download_url, domain=None, range=Optional[Union[str, URI]])

slots.assayMeasurementRecord__source = Slot(uri=PFAS.source, name="assayMeasurementRecord__source", curie=PFAS.curie('source'),
                   model_uri=PFAS.assayMeasurementRecord__source, domain=None, range=Optional[str])

slots.bioprocessConditionsRecord__process_id = Slot(uri=PFAS.process_id, name="bioprocessConditionsRecord__process_id", curie=PFAS.curie('process_id'),
                   model_uri=PFAS.bioprocessConditionsRecord__process_id, domain=None, range=URIRef)

slots.bioprocessConditionsRecord__process_name = Slot(uri=PFAS.process_name, name="bioprocessConditionsRecord__process_name", curie=PFAS.curie('process_name'),
                   model_uri=PFAS.bioprocessConditionsRecord__process_name, domain=None, range=str)

slots.bioprocessConditionsRecord__process_type = Slot(uri=PFAS.process_type, name="bioprocessConditionsRecord__process_type", curie=PFAS.curie('process_type'),
                   model_uri=PFAS.bioprocessConditionsRecord__process_type, domain=None, range=Optional[Union[str, "ProcessTypeEnum"]])

slots.bioprocessConditionsRecord__strain_used = Slot(uri=PFAS.strain_used, name="bioprocessConditionsRecord__strain_used", curie=PFAS.curie('strain_used'),
                   model_uri=PFAS.bioprocessConditionsRecord__strain_used, domain=None, range=Optional[str])

slots.bioprocessConditionsRecord__ph = Slot(uri=PFAS.ph, name="bioprocessConditionsRecord__ph", curie=PFAS.curie('ph'),
                   model_uri=PFAS.bioprocessConditionsRecord__ph, domain=None, range=Optional[float])

slots.bioprocessConditionsRecord__temperature = Slot(uri=PFAS.temperature, name="bioprocessConditionsRecord__temperature", curie=PFAS.curie('temperature'),
                   model_uri=PFAS.bioprocessConditionsRecord__temperature, domain=None, range=Optional[float])

slots.bioprocessConditionsRecord__pfas_concentration = Slot(uri=PFAS.pfas_concentration, name="bioprocessConditionsRecord__pfas_concentration", curie=PFAS.curie('pfas_concentration'),
                   model_uri=PFAS.bioprocessConditionsRecord__pfas_concentration, domain=None, range=Optional[str])

slots.bioprocessConditionsRecord__duration = Slot(uri=PFAS.duration, name="bioprocessConditionsRecord__duration", curie=PFAS.curie('duration'),
                   model_uri=PFAS.bioprocessConditionsRecord__duration, domain=None, range=Optional[str])

slots.bioprocessConditionsRecord__oxygen_condition = Slot(uri=PFAS.oxygen_condition, name="bioprocessConditionsRecord__oxygen_condition", curie=PFAS.curie('oxygen_condition'),
                   model_uri=PFAS.bioprocessConditionsRecord__oxygen_condition, domain=None, range=Optional[str])

slots.bioprocessConditionsRecord__medium_composition = Slot(uri=PFAS.medium_composition, name="bioprocessConditionsRecord__medium_composition", curie=PFAS.curie('medium_composition'),
                   model_uri=PFAS.bioprocessConditionsRecord__medium_composition, domain=None, range=Optional[str])

slots.bioprocessConditionsRecord__degradation_percentage = Slot(uri=PFAS.degradation_percentage, name="bioprocessConditionsRecord__degradation_percentage", curie=PFAS.curie('degradation_percentage'),
                   model_uri=PFAS.bioprocessConditionsRecord__degradation_percentage, domain=None, range=Optional[float])

slots.bioprocessConditionsRecord__fluoride_release = Slot(uri=PFAS.fluoride_release, name="bioprocessConditionsRecord__fluoride_release", curie=PFAS.curie('fluoride_release'),
                   model_uri=PFAS.bioprocessConditionsRecord__fluoride_release, domain=None, range=Optional[float])

slots.bioprocessConditionsRecord__source = Slot(uri=PFAS.source, name="bioprocessConditionsRecord__source", curie=PFAS.curie('source'),
                   model_uri=PFAS.bioprocessConditionsRecord__source, domain=None, range=Optional[str])

slots.screeningResultRecord__experiment_id = Slot(uri=PFAS.experiment_id, name="screeningResultRecord__experiment_id", curie=PFAS.curie('experiment_id'),
                   model_uri=PFAS.screeningResultRecord__experiment_id, domain=None, range=URIRef)

slots.screeningResultRecord__plate_coordinates = Slot(uri=PFAS.plate_coordinates, name="screeningResultRecord__plate_coordinates", curie=PFAS.curie('plate_coordinates'),
                   model_uri=PFAS.screeningResultRecord__plate_coordinates, domain=None, range=Optional[str])

slots.screeningResultRecord__strain_barcode = Slot(uri=PFAS.strain_barcode, name="screeningResultRecord__strain_barcode", curie=PFAS.curie('strain_barcode'),
                   model_uri=PFAS.screeningResultRecord__strain_barcode, domain=None, range=Optional[str])

slots.screeningResultRecord__screening_assay = Slot(uri=PFAS.screening_assay, name="screeningResultRecord__screening_assay", curie=PFAS.curie('screening_assay'),
                   model_uri=PFAS.screeningResultRecord__screening_assay, domain=None, range=Optional[str])

slots.screeningResultRecord__measurement_values = Slot(uri=PFAS.measurement_values, name="screeningResultRecord__measurement_values", curie=PFAS.curie('measurement_values'),
                   model_uri=PFAS.screeningResultRecord__measurement_values, domain=None, range=Optional[str])

slots.screeningResultRecord__hit_classification = Slot(uri=PFAS.hit_classification, name="screeningResultRecord__hit_classification", curie=PFAS.curie('hit_classification'),
                   model_uri=PFAS.screeningResultRecord__hit_classification, domain=None, range=Optional[Union[str, "HitClassificationEnum"]])

slots.screeningResultRecord__source = Slot(uri=PFAS.source, name="screeningResultRecord__source", curie=PFAS.curie('source'),
                   model_uri=PFAS.screeningResultRecord__source, domain=None, range=Optional[str])

slots.protocolRecord__protocol_id = Slot(uri=PFAS.protocol_id, name="protocolRecord__protocol_id", curie=PFAS.curie('protocol_id'),
                   model_uri=PFAS.protocolRecord__protocol_id, domain=None, range=URIRef)

slots.protocolRecord__protocol_name = Slot(uri=PFAS.protocol_name, name="protocolRecord__protocol_name", curie=PFAS.curie('protocol_name'),
                   model_uri=PFAS.protocolRecord__protocol_name, domain=None, range=str)

slots.protocolRecord__protocol_type = Slot(uri=PFAS.protocol_type, name="protocolRecord__protocol_type", curie=PFAS.curie('protocol_type'),
                   model_uri=PFAS.protocolRecord__protocol_type, domain=None, range=Optional[Union[str, "ProtocolTypeEnum"]])

slots.protocolRecord__protocol_version = Slot(uri=PFAS.protocol_version, name="protocolRecord__protocol_version", curie=PFAS.curie('protocol_version'),
                   model_uri=PFAS.protocolRecord__protocol_version, domain=None, range=Optional[str])

slots.protocolRecord__protocol_doi = Slot(uri=PFAS.protocol_doi, name="protocolRecord__protocol_doi", curie=PFAS.curie('protocol_doi'),
                   model_uri=PFAS.protocolRecord__protocol_doi, domain=None, range=Optional[str])

slots.protocolRecord__dbtl_iteration = Slot(uri=PFAS.dbtl_iteration, name="protocolRecord__dbtl_iteration", curie=PFAS.curie('dbtl_iteration'),
                   model_uri=PFAS.protocolRecord__dbtl_iteration, domain=None, range=Optional[int])

slots.protocolRecord__source = Slot(uri=PFAS.source, name="protocolRecord__source", curie=PFAS.curie('source'),
                   model_uri=PFAS.protocolRecord__source, domain=None, range=Optional[str])

slots.transcriptomicsRecord__experiment_id = Slot(uri=PFAS.experiment_id, name="transcriptomicsRecord__experiment_id", curie=PFAS.curie('experiment_id'),
                   model_uri=PFAS.transcriptomicsRecord__experiment_id, domain=None, range=URIRef,
                   pattern=re.compile(r'^([SED]RX\d+|GSE\d+|E-[A-Z]+-\d+)$'))

slots.transcriptomicsRecord__study_id = Slot(uri=PFAS.study_id, name="transcriptomicsRecord__study_id", curie=PFAS.curie('study_id'),
                   model_uri=PFAS.transcriptomicsRecord__study_id, domain=None, range=Optional[str],
                   pattern=re.compile(r'^([SED]RP\d+|GSE\d+|E-[A-Z]+-\d+)?$'))

slots.transcriptomicsRecord__sample_id = Slot(uri=PFAS.sample_id, name="transcriptomicsRecord__sample_id", curie=PFAS.curie('sample_id'),
                   model_uri=PFAS.transcriptomicsRecord__sample_id, domain=None, range=Optional[str],
                   pattern=re.compile(r'^(SAM[NED]\d+|GSM\d+)?$'))

slots.transcriptomicsRecord__organism = Slot(uri=PFAS.organism, name="transcriptomicsRecord__organism", curie=PFAS.curie('organism'),
                   model_uri=PFAS.transcriptomicsRecord__organism, domain=None, range=str)

slots.transcriptomicsRecord__project_title = Slot(uri=PFAS.project_title, name="transcriptomicsRecord__project_title", curie=PFAS.curie('project_title'),
                   model_uri=PFAS.transcriptomicsRecord__project_title, domain=None, range=Optional[str])

slots.transcriptomicsRecord__sample_description = Slot(uri=PFAS.sample_description, name="transcriptomicsRecord__sample_description", curie=PFAS.curie('sample_description'),
                   model_uri=PFAS.transcriptomicsRecord__sample_description, domain=None, range=Optional[str])

slots.transcriptomicsRecord__condition = Slot(uri=PFAS.condition, name="transcriptomicsRecord__condition", curie=PFAS.curie('condition'),
                   model_uri=PFAS.transcriptomicsRecord__condition, domain=None, range=Optional[str])

slots.transcriptomicsRecord__data_type = Slot(uri=PFAS.data_type, name="transcriptomicsRecord__data_type", curie=PFAS.curie('data_type'),
                   model_uri=PFAS.transcriptomicsRecord__data_type, domain=None, range=Optional[Union[str, "TranscriptomicsDataTypeEnum"]])

slots.transcriptomicsRecord__sra_accession = Slot(uri=PFAS.sra_accession, name="transcriptomicsRecord__sra_accession", curie=PFAS.curie('sra_accession'),
                   model_uri=PFAS.transcriptomicsRecord__sra_accession, domain=None, range=Optional[str],
                   pattern=re.compile(r'^[SED]RX\d*$'))

slots.transcriptomicsRecord__geo_accession = Slot(uri=PFAS.geo_accession, name="transcriptomicsRecord__geo_accession", curie=PFAS.curie('geo_accession'),
                   model_uri=PFAS.transcriptomicsRecord__geo_accession, domain=None, range=Optional[str],
                   pattern=re.compile(r'^(GSE|GSM)\d*$'))

slots.transcriptomicsRecord__arrayexpress_accession = Slot(uri=PFAS.arrayexpress_accession, name="transcriptomicsRecord__arrayexpress_accession", curie=PFAS.curie('arrayexpress_accession'),
                   model_uri=PFAS.transcriptomicsRecord__arrayexpress_accession, domain=None, range=Optional[str],
                   pattern=re.compile(r'^E-[A-Z]+-\d*$'))

slots.transcriptomicsRecord__size = Slot(uri=PFAS.size, name="transcriptomicsRecord__size", curie=PFAS.curie('size'),
                   model_uri=PFAS.transcriptomicsRecord__size, domain=None, range=Optional[str])

slots.transcriptomicsRecord__publication = Slot(uri=PFAS.publication, name="transcriptomicsRecord__publication", curie=PFAS.curie('publication'),
                   model_uri=PFAS.transcriptomicsRecord__publication, domain=None, range=Optional[str])

slots.transcriptomicsRecord__license = Slot(uri=PFAS.license, name="transcriptomicsRecord__license", curie=PFAS.curie('license'),
                   model_uri=PFAS.transcriptomicsRecord__license, domain=None, range=Optional[str])

slots.transcriptomicsRecord__download_url = Slot(uri=PFAS.download_url, name="transcriptomicsRecord__download_url", curie=PFAS.curie('download_url'),
                   model_uri=PFAS.transcriptomicsRecord__download_url, domain=None, range=Optional[Union[str, URI]])

slots.transcriptomicsRecord__source = Slot(uri=PFAS.source, name="transcriptomicsRecord__source", curie=PFAS.curie('source'),
                   model_uri=PFAS.transcriptomicsRecord__source, domain=None, range=Optional[str])

slots.strainRecord__strain_id = Slot(uri=PFAS.strain_id, name="strainRecord__strain_id", curie=PFAS.curie('strain_id'),
                   model_uri=PFAS.strainRecord__strain_id, domain=None, range=URIRef,
                   pattern=re.compile(r'^([A-Z]{2,10}:\d+|STRAIN_\d+)$'))

slots.strainRecord__species_taxon_id = Slot(uri=PFAS.species_taxon_id, name="strainRecord__species_taxon_id", curie=PFAS.curie('species_taxon_id'),
                   model_uri=PFAS.strainRecord__species_taxon_id, domain=None, range=Optional[int])

slots.strainRecord__scientific_name = Slot(uri=PFAS.scientific_name, name="strainRecord__scientific_name", curie=PFAS.curie('scientific_name'),
                   model_uri=PFAS.strainRecord__scientific_name, domain=None, range=str)

slots.strainRecord__strain_designation = Slot(uri=PFAS.strain_designation, name="strainRecord__strain_designation", curie=PFAS.curie('strain_designation'),
                   model_uri=PFAS.strainRecord__strain_designation, domain=None, range=Optional[str])

slots.strainRecord__type_strain = Slot(uri=PFAS.type_strain, name="strainRecord__type_strain", curie=PFAS.curie('type_strain'),
                   model_uri=PFAS.strainRecord__type_strain, domain=None, range=Optional[Union[str, "TypeStrainEnum"]])

slots.strainRecord__culture_collection_ids = Slot(uri=PFAS.culture_collection_ids, name="strainRecord__culture_collection_ids", curie=PFAS.curie('culture_collection_ids'),
                   model_uri=PFAS.strainRecord__culture_collection_ids, domain=None, range=Optional[Union[str, list[str]]])

slots.strainRecord__procurement_urls = Slot(uri=PFAS.procurement_urls, name="strainRecord__procurement_urls", curie=PFAS.curie('procurement_urls'),
                   model_uri=PFAS.strainRecord__procurement_urls, domain=None, range=Optional[Union[Union[str, URI], list[Union[str, URI]]]])

slots.strainRecord__availability_status = Slot(uri=PFAS.availability_status, name="strainRecord__availability_status", curie=PFAS.curie('availability_status'),
                   model_uri=PFAS.strainRecord__availability_status, domain=None, range=Optional[Union[str, "AvailabilityStatusEnum"]])

slots.strainRecord__alternative_names = Slot(uri=PFAS.alternative_names, name="strainRecord__alternative_names", curie=PFAS.curie('alternative_names'),
                   model_uri=PFAS.strainRecord__alternative_names, domain=None, range=Optional[Union[str, list[str]]])

slots.strainRecord__biosafety_level = Slot(uri=PFAS.biosafety_level, name="strainRecord__biosafety_level", curie=PFAS.curie('biosafety_level'),
                   model_uri=PFAS.strainRecord__biosafety_level, domain=None, range=Optional[int])

slots.strainRecord__growth_requirements = Slot(uri=PFAS.growth_requirements, name="strainRecord__growth_requirements", curie=PFAS.curie('growth_requirements'),
                   model_uri=PFAS.strainRecord__growth_requirements, domain=None, range=Optional[str])

slots.strainRecord__kg_microbe_nodes = Slot(uri=PFAS.kg_microbe_nodes, name="strainRecord__kg_microbe_nodes", curie=PFAS.curie('kg_microbe_nodes'),
                   model_uri=PFAS.strainRecord__kg_microbe_nodes, domain=None, range=Optional[Union[str, list[str]]])

slots.strainRecord__notes = Slot(uri=PFAS.notes, name="strainRecord__notes", curie=PFAS.curie('notes'),
                   model_uri=PFAS.strainRecord__notes, domain=None, range=Optional[str])

slots.strainRecord__source = Slot(uri=PFAS.source, name="strainRecord__source", curie=PFAS.curie('source'),
                   model_uri=PFAS.strainRecord__source, domain=None, range=Optional[str])

slots.growthMediaRecord__media_id = Slot(uri=PFAS.media_id, name="growthMediaRecord__media_id", curie=PFAS.curie('media_id'),
                   model_uri=PFAS.growthMediaRecord__media_id, domain=None, range=URIRef,
                   pattern=re.compile(r'^([A-Z]+:\d+|[A-Z0-9]+)$'))

slots.growthMediaRecord__media_name = Slot(uri=PFAS.media_name, name="growthMediaRecord__media_name", curie=PFAS.curie('media_name'),
                   model_uri=PFAS.growthMediaRecord__media_name, domain=None, range=str)

slots.growthMediaRecord__media_type = Slot(uri=PFAS.media_type, name="growthMediaRecord__media_type", curie=PFAS.curie('media_type'),
                   model_uri=PFAS.growthMediaRecord__media_type, domain=None, range=Optional[Union[str, "MediaTypeEnum"]])

slots.growthMediaRecord__alternative_names = Slot(uri=PFAS.alternative_names, name="growthMediaRecord__alternative_names", curie=PFAS.curie('alternative_names'),
                   model_uri=PFAS.growthMediaRecord__alternative_names, domain=None, range=Optional[Union[str, list[str]]])

slots.growthMediaRecord__description = Slot(uri=PFAS.description, name="growthMediaRecord__description", curie=PFAS.curie('description'),
                   model_uri=PFAS.growthMediaRecord__description, domain=None, range=Optional[str])

slots.growthMediaRecord__target_organisms = Slot(uri=PFAS.target_organisms, name="growthMediaRecord__target_organisms", curie=PFAS.curie('target_organisms'),
                   model_uri=PFAS.growthMediaRecord__target_organisms, domain=None, range=Optional[str])

slots.growthMediaRecord__ph = Slot(uri=PFAS.ph, name="growthMediaRecord__ph", curie=PFAS.curie('ph'),
                   model_uri=PFAS.growthMediaRecord__ph, domain=None, range=Optional[str])

slots.growthMediaRecord__sterilization_method = Slot(uri=PFAS.sterilization_method, name="growthMediaRecord__sterilization_method", curie=PFAS.curie('sterilization_method'),
                   model_uri=PFAS.growthMediaRecord__sterilization_method, domain=None, range=Optional[str])

slots.growthMediaRecord__references = Slot(uri=PFAS.references, name="growthMediaRecord__references", curie=PFAS.curie('references'),
                   model_uri=PFAS.growthMediaRecord__references, domain=None, range=Optional[Union[str, list[str]]])

slots.growthMediaRecord__kg_microbe_nodes = Slot(uri=PFAS.kg_microbe_nodes, name="growthMediaRecord__kg_microbe_nodes", curie=PFAS.curie('kg_microbe_nodes'),
                   model_uri=PFAS.growthMediaRecord__kg_microbe_nodes, domain=None, range=Optional[Union[str, list[str]]])

slots.growthMediaRecord__notes = Slot(uri=PFAS.notes, name="growthMediaRecord__notes", curie=PFAS.curie('notes'),
                   model_uri=PFAS.growthMediaRecord__notes, domain=None, range=Optional[str])

slots.growthMediaRecord__source = Slot(uri=PFAS.source, name="growthMediaRecord__source", curie=PFAS.curie('source'),
                   model_uri=PFAS.growthMediaRecord__source, domain=None, range=Optional[str])

slots.mediaIngredientRecord__ingredient_id = Slot(uri=PFAS.ingredient_id, name="mediaIngredientRecord__ingredient_id", curie=PFAS.curie('ingredient_id'),
                   model_uri=PFAS.mediaIngredientRecord__ingredient_id, domain=None, range=URIRef,
                   pattern=re.compile(r'^[A-Z0-9_:]+_ING_\d+$'))

slots.mediaIngredientRecord__ingredient_name = Slot(uri=PFAS.ingredient_name, name="mediaIngredientRecord__ingredient_name", curie=PFAS.curie('ingredient_name'),
                   model_uri=PFAS.mediaIngredientRecord__ingredient_name, domain=None, range=str)

slots.mediaIngredientRecord__media_id = Slot(uri=PFAS.media_id, name="mediaIngredientRecord__media_id", curie=PFAS.curie('media_id'),
                   model_uri=PFAS.mediaIngredientRecord__media_id, domain=None, range=str)

slots.mediaIngredientRecord__media_name = Slot(uri=PFAS.media_name, name="mediaIngredientRecord__media_name", curie=PFAS.curie('media_name'),
                   model_uri=PFAS.mediaIngredientRecord__media_name, domain=None, range=Optional[str])

slots.mediaIngredientRecord__ontology_id = Slot(uri=PFAS.ontology_id, name="mediaIngredientRecord__ontology_id", curie=PFAS.curie('ontology_id'),
                   model_uri=PFAS.mediaIngredientRecord__ontology_id, domain=None, range=Optional[str],
                   pattern=re.compile(r'^(CHEBI:\d+|PUBCHEM:\d+|)$'))

slots.mediaIngredientRecord__ontology_label = Slot(uri=PFAS.ontology_label, name="mediaIngredientRecord__ontology_label", curie=PFAS.curie('ontology_label'),
                   model_uri=PFAS.mediaIngredientRecord__ontology_label, domain=None, range=Optional[str])

slots.mediaIngredientRecord__chemical_formula = Slot(uri=PFAS.chemical_formula, name="mediaIngredientRecord__chemical_formula", curie=PFAS.curie('chemical_formula'),
                   model_uri=PFAS.mediaIngredientRecord__chemical_formula, domain=None, range=Optional[str])

slots.mediaIngredientRecord__concentration = Slot(uri=PFAS.concentration, name="mediaIngredientRecord__concentration", curie=PFAS.curie('concentration'),
                   model_uri=PFAS.mediaIngredientRecord__concentration, domain=None, range=Optional[float])

slots.mediaIngredientRecord__unit = Slot(uri=PFAS.unit, name="mediaIngredientRecord__unit", curie=PFAS.curie('unit'),
                   model_uri=PFAS.mediaIngredientRecord__unit, domain=None, range=Optional[str])

slots.mediaIngredientRecord__role = Slot(uri=PFAS.role, name="mediaIngredientRecord__role", curie=PFAS.curie('role'),
                   model_uri=PFAS.mediaIngredientRecord__role, domain=None, range=Optional[Union[str, "IngredientRoleEnum"]])

slots.mediaIngredientRecord__kg_microbe_nodes = Slot(uri=PFAS.kg_microbe_nodes, name="mediaIngredientRecord__kg_microbe_nodes", curie=PFAS.curie('kg_microbe_nodes'),
                   model_uri=PFAS.mediaIngredientRecord__kg_microbe_nodes, domain=None, range=Optional[Union[str, list[str]]])

slots.mediaIngredientRecord__notes = Slot(uri=PFAS.notes, name="mediaIngredientRecord__notes", curie=PFAS.curie('notes'),
                   model_uri=PFAS.mediaIngredientRecord__notes, domain=None, range=Optional[str])

slots.mediaIngredientRecord__source = Slot(uri=PFAS.source, name="mediaIngredientRecord__source", curie=PFAS.curie('source'),
                   model_uri=PFAS.mediaIngredientRecord__source, domain=None, range=Optional[str])

