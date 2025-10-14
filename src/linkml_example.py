"""Example usage of LinkML models for lanthanide bioprocessing data.

This module demonstrates how to use the generated LinkML dataclasses to create,
validate, and serialize lanthanide bioprocessing research data.
"""

from linkml_models import (
    LanthanideBioprocessingDatabase,
    GenomeRecord,
    BiosampleRecord,
    PathwayRecord,
    GeneProteinRecord,
    MacromolecularStructureRecord,
    PublicationRecord,
    DatasetRecord,
    StructureMethodEnum,
    DataTypeEnum,
)
from linkml_runtime.dumpers import yaml_dumper, json_dumper
from linkml_runtime.loaders import yaml_loader, json_loader


def create_example_database() -> LanthanideBioprocessingDatabase:
    """Create an example database with sample records.

    Returns:
        LanthanideBioprocessingDatabase instance with example data

    Examples:
        >>> db = create_example_database()
        >>> len(db.genomes)
        2
        >>> db.genomes[0].scientific_name
        'Methylobacterium aquaticum'
    """
    # Create genome records
    genome1 = GenomeRecord(
        scientific_name="Methylobacterium aquaticum",
        ncbi_taxon_id=270351,
        genome_identifier="GCF_050408745.1",
        annotation_download_url="ftp://ftp.ncbi.nlm.nih.gov/genomes/all/GCF/050/408/745/GCF_050408745.1_*_genomic.gff.gz"
    )

    genome2 = GenomeRecord(
        scientific_name="Methylorubrum extorquens",
        ncbi_taxon_id=408,
        genome_identifier="GCF_051522905.1",
        annotation_download_url="ftp://ftp.ncbi.nlm.nih.gov/genomes/all/GCF/051/522/905/GCF_051522905.1_*_genomic.gff.gz"
    )

    # Create biosample record
    biosample1 = BiosampleRecord(
        sample_id="SAMN44800722",
        sample_name="203a",
        organism="Methylobacterium aquaticum strain: LEGMi203a",
        download_url="https://www.ncbi.nlm.nih.gov/biosample/SAMN44800722"
    )

    # Create pathway record
    pathway1 = PathwayRecord(
        pathway_id="ko00680",
        pathway_name="Methane metabolism",
        organism="Methylotrophic bacteria (Methylobacterium, Methylorubrum, Paracoccus)",
        genes=["xoxF", "mxaF", "exaF", "mxbD", "fae1", "fae2"],
        genes_kegg=["K23995", "K14028"],
        download_url="https://www.kegg.jp/entry/path:map00680"
    )

    # Create gene/protein record
    gene1 = GeneProteinRecord(
        gene_protein_id="K23995",
        organism="Methylobacterium species",
        annotation="PQQ-dependent methanol dehydrogenase, lanthanide-dependent (XoxF)",
        ec_number="1.1.2.7",
        go_terms=["GO:0018525"],  # methanol metabolic process
        chebi_terms=["CHEBI:17790"],  # methanol
        download_url="https://www.kegg.jp/entry/K23995"
    )

    # Create structure record
    structure1 = MacromolecularStructureRecord(
        structure_name="PQQ-dependent methanol dehydrogenase with Ce3+",
        organism="Methylobacterium extorquens",
        components="XoxF subunit, PQQ cofactor, Ce3+ ion, cytochrome c",
        pdb_id="4MAE",
        resolution="1.6 Å",
        method=StructureMethodEnum("X-ray crystallography"),
        download_url="https://www.rcsb.org/structure/4MAE"
    )

    # Create publication record
    pub1 = PublicationRecord(
        url="https://doi.org/10.1038/nature16174",
        title="Rare earth elements are essential for methanotrophic life in volcanic mudpots",
        journal="Nature",
        year=2016,
        authors="Pol A, et al.",
        download_url="https://doi.org/10.1038/nature16174"
    )

    # Create dataset record
    dataset1 = DatasetRecord(
        dataset_name="Methylobacterium genome sequencing projects",
        data_type=DataTypeEnum("genomic DNA sequencing"),
        url="https://www.ncbi.nlm.nih.gov/sra/?term=Methylobacterium",
        size="Multiple projects",
        publication="Various publications",
        license="NCBI SRA",
        download_url="https://www.ncbi.nlm.nih.gov/sra/?term=Methylobacterium"
    )

    # Create database container
    database = LanthanideBioprocessingDatabase(
        genomes=[genome1, genome2],
        biosamples=[biosample1],
        pathways=[pathway1],
        genes_proteins=[gene1],
        structures=[structure1],
        publications=[pub1],
        datasets=[dataset1]
    )

    return database


def save_to_yaml(database: LanthanideBioprocessingDatabase, output_path: str) -> None:
    """Save database to YAML file.

    Args:
        database: Database instance to save
        output_path: Path to output YAML file
    """
    yaml_dumper.dump(database, output_path)
    print(f"Database saved to {output_path}")


def save_to_json(database: LanthanideBioprocessingDatabase, output_path: str) -> None:
    """Save database to JSON file.

    Args:
        database: Database instance to save
        output_path: Path to output JSON file
    """
    json_dumper.dump(database, output_path)
    print(f"Database saved to {output_path}")


def load_from_yaml(input_path: str) -> LanthanideBioprocessingDatabase:
    """Load database from YAML file.

    Args:
        input_path: Path to input YAML file

    Returns:
        LanthanideBioprocessingDatabase instance
    """
    database = yaml_loader.load(input_path, target_class=LanthanideBioprocessingDatabase)
    print(f"Database loaded from {input_path}")
    return database


def load_from_json(input_path: str) -> LanthanideBioprocessingDatabase:
    """Load database from JSON file.

    Args:
        input_path: Path to input JSON file

    Returns:
        LanthanideBioprocessingDatabase instance
    """
    database = json_loader.load(input_path, target_class=LanthanideBioprocessingDatabase)
    print(f"Database loaded from {input_path}")
    return database


def main():
    """Demonstrate LinkML model usage."""
    # Create example database
    print("Creating example database...")
    db = create_example_database()

    # Print statistics
    print(f"\nDatabase statistics:")
    print(f"  Genomes: {len(db.genomes)}")
    print(f"  Biosamples: {len(db.biosamples)}")
    print(f"  Pathways: {len(db.pathways)}")
    print(f"  Genes/Proteins: {len(db.genes_proteins)}")
    print(f"  Structures: {len(db.structures)}")
    print(f"  Publications: {len(db.publications)}")
    print(f"  Datasets: {len(db.datasets)}")

    # Example: Access genome data
    print(f"\nFirst genome:")
    print(f"  Name: {db.genomes[0].scientific_name}")
    print(f"  NCBI Taxon: {db.genomes[0].ncbi_taxon_id}")
    print(f"  Accession: {db.genomes[0].genome_identifier}")

    # Example: Access pathway data
    print(f"\nFirst pathway:")
    print(f"  Name: {db.pathways[0].pathway_name}")
    print(f"  ID: {db.pathways[0].pathway_id}")
    print(f"  Genes: {', '.join(db.pathways[0].genes or [])}")

    # Save to files
    # save_to_yaml(db, "example_database.yaml")
    # save_to_json(db, "example_database.json")

    print("\nExample completed successfully!")


if __name__ == "__main__":
    main()
