# PFAS-AI: Machine Learning-Enabled PFAS Biodegradation Pipeline

## 🔬 Project Overview

This project develops an automated, ML-enabled data pipeline for **PFAS biodegradation research**, focusing on the identification and characterization of microorganisms capable of degrading per- and polyfluoroalkyl substances (PFAS). The pipeline integrates multiple biological databases and machine learning approaches to design optimal microbial consortia for PFAS remediation.

### Scientific Focus: PFAS Biodegradation

PFAS ("forever chemicals") are persistent environmental contaminants characterized by strong C-F bonds that resist degradation. This project addresses PFAS contamination through:

- **C-F Bond Cleavage**: Identifying microbes with dehalogenases and defluorinases
- **Fluoride Resistance**: Characterizing fluoride export systems and resistance mechanisms
- **Hydrocarbon Degradation**: Finding microbes that can cleave PFAS carbon backbones
- **Microbial Consortia Design**: Using ML to design optimized 3-5 member consortia
- **Environmental Context**: AFFF-contaminated sites, groundwater, and wastewater systems

### Research Objectives

1. **ML-Powered Database**: Build a semantically-aware database using the KG-Microbe platform to identify putative PFAS biodegradation genes, pathways, taxa, environments, and microbial communities
2. **Intelligent Consortia Design**: Use graph learning and LLMs to design optimized microbial consortia (10-15 total, down-select to 5 best)
3. **Experimental Validation**: Test consortia for degradation of both perfluorinated (PFOA, PFOS) and polyfluorinated compounds

### Current Status: Initial Development

⚠️ **Important**: The current datasets represent **initial seed data** for pipeline development. This is transitioning from CMM-AI (lanthanide bioprocessing) to PFAS-AI with:
- **Initial seed data**: 6 microorganisms, 23 publications
- **Pipeline architecture**: Proven data extension workflows
- **ML integration**: KG-Microbe platform for intelligent feature extraction
- **Foundation for growth**: Automated extension to 100+ organisms and comprehensive datasets

## 🌟 Technical Features

- **📊 Automated Data Extension**: Transform small seed datasets into comprehensive research databases
- **🔗 Download URL Generation**: Direct links to NCBI, KEGG, UniProt, PDB, and other databases
- **🧬 Multi-Database Integration**: NCBI Assembly/BioSample, KEGG pathways, UniProt proteins, PDB structures
- **🤖 ML-Enabled Search**: KG-Microbe integration for intelligent feature identification
- **🔄 Pipeline Automation**: Complete Makefile workflow for reproducible research
- **📄 File Format Support**: Excel to TSV, Word/PDF to text conversion
- **✅ Data Validation**: LinkML schema validation and cross-sheet consistency checks

## 📋 Data Tables Structure

| Table | Initial Data | Description |
|-------|-------------|-------------|
| **Genomes** | 6 organisms | PFAS-degrading bacteria/archaea genomes with annotation URLs |
| **Biosamples** | (to extend) | Environmental samples from PFAS-contaminated sites |
| **Pathways** | (to extend) | KEGG and MetaCyc dehalogenation and fluoride metabolism pathways |
| **Genes/Proteins** | (to extend) | Dehalogenases, defluorinases, fluoride exporters from UniProt/KEGG |
| **Structures** | (to extend) | PDB crystal structures of dehalogenases and related enzymes |
| **Publications** | 23 papers | Peer-reviewed literature on PFAS biodegradation |
| **Datasets** | (to extend) | Research datasets from PFAS metagenomes and contaminated sites |
| **Chemicals** | (to extend) | PFAS compounds (PFOA, PFOS, precursors, metabolites) |
| **Assays** | (to extend) | Fluoride detection, PFAS quantification protocols |

## 🚀 Quick Start

### Prerequisites

- Python 3.9+
- [uv](https://docs.astral.sh/uv/) package manager
- Git

### Installation

```bash
# Clone the repository
git clone https://github.com/YourOrg/PFAS-AI.git
cd PFAS-AI

# Install dependencies
make install

# Convert PFAS Excel file to TSV
make convert-excel

# Run the full pipeline
make update-all
```

### Individual Pipeline Steps

```bash
# Update specific tables
make update-genomes      # Extend genomes with NCBI data (PFAS degraders)
make update-biosamples   # Extend biosamples with PFAS site data
make update-pathways     # Extend pathways with dehalogenation routes
make update-datasets     # Extend datasets with PFAS metagenomes
make update-genes        # Extend genes with dehalogenases, fluoride exporters
make update-structures   # Extend structures with dehalogenase PDB entries
make update-publications # Extend publications with PFAS literature

# Experimental data
make update-chemicals    # Extend PFAS compounds with PubChem/CHEBI
make update-assays       # Extend assays with fluoride/PFAS detection methods

# View pipeline status
make status
```

## 📁 Repository Structure

```
PFAS-AI/
├── 📂 src/                          # Python source code
│   ├── 🐍 parsers.py               # File conversion utilities
│   ├── 🐍 ncbi_search.py           # NCBI database integration (PFAS microbes)
│   ├── 🐍 pathway_search.py        # KEGG/MetaCyc pathway search (dehalogenation)
│   ├── 🐍 gene_search.py           # UniProt/KEGG gene search (dehalogenases)
│   ├── 🐍 structure_search.py      # PDB/AlphaFold structure search
│   ├── 🐍 dataset_search.py        # Multi-repository dataset search
│   ├── 🐍 publication_search.py    # PubMed/PMC literature search
│   ├── 🐍 chemical_search.py       # PFAS compound search
│   ├── 🐍 assay_search.py          # Assay protocol search
│   └── 🐍 extend_*.py              # Pipeline automation scripts
├── 📂 data/                         # Research data
│   ├── 📂 sheet/                   # Original Excel file (PFAS Data for AI.xlsx)
│   ├── 📂 txt/sheet/               # Converted TSV files + extensions
│   ├── 📂 publications/            # PDF research papers
│   └── 📂 proposal/                # Project documentation
├── 📂 schema/                       # LinkML schema definitions
│   └── 📄 pfas_biodegradation.yaml # PFAS data model (to be created)
├── ⚙️ Makefile                     # Pipeline automation
├── 📋 pyproject.toml               # Package configuration
└── 📚 CLAUDE.md                    # AI assistant guidance
```

## 🔗 Database Integrations

### NCBI APIs
- **Assembly Database**: Genome sequences with dehalogenase annotations
- **BioSample Database**: Environmental samples from PFAS-contaminated sites
- **PubMed/PMC**: Scientific literature on PFAS biodegradation

### Other APIs
- **KEGG REST**: Dehalogenation pathways and fluoride metabolism
- **UniProt REST**: Protein sequences (dehalogenases, fluoride exporters)
- **RCSB PDB**: Crystal structures of dehalogenase enzymes
- **AlphaFold**: Predicted structures for novel dehalogenases
- **PubChem/CHEBI**: PFAS compound structures and properties

## 📊 Data Pipeline Details

### Input Processing
1. **Excel Conversion**: Multi-sheet Excel file → Individual TSV files
2. **Document Parsing**: Word/PDF documents → Searchable text
3. **Filename Sanitization**: Spaces → underscores for consistency

### Data Extension Process
1. **NCBI Search**: Query Assembly/BioSample with PFAS-relevant terms
2. **Literature Mining**: PubMed searches for PFAS biodegradation papers
3. **Pathway Mapping**: KEGG/MetaCyc dehalogenation pathway identification
4. **Structure Discovery**: PDB searches for dehalogenase structures
5. **URL Generation**: Direct download links for all data sources

### Search Strategy

**PFAS-Specific Terms**:
- PFAS, perfluorinated, polyfluorinated, PFOA, PFOS, AFFF
- C-F bond, defluorination, dehalogenation, fluoride
- Forever chemicals, per- and polyfluoroalkyl substances

**Functional Terms**:
- Dehalogenase, defluorinase, fluoroacetate dehalogenase
- Fluoride exporter, fluoride resistance, CrcB, FEX
- Reductive dehalogenase (RdhA), haloalkane dehalogenase
- Hydrocarbon degradation, aromatic degradation

**Target Organisms**:
- Pseudomonas (known PFAS degraders)
- Hyphomicrobium (C1 metabolism)
- Acidimicrobium (acid-tolerant extremophile)
- Dechlorinating bacteria (Dehalococcoides, Desulfitobacterium)
- Hydrocarbon degraders (Rhodococcus, Mycobacterium)

### Quality Control
- **Rate Limiting**: Respects API usage guidelines (0.5-1.0 sec delays)
- **Duplicate Removal**: Based on unique identifiers
- **Error Handling**: Graceful degradation with informative messages
- **Validation**: Doctests, LinkML schema validation, cross-sheet consistency

## 🤖 Machine Learning Integration (KG-Microbe)

### Training Data Categories

1. **Known PFAS degraders**: Microbes with demonstrated PFAS biodegradation
2. **Dechlorinating microbes**: Organisms with dehalogenases (potential C-F bond cleavage)
3. **Fluoride-resistant microbes**: Organisms with fluoride exporters and resistance genes
4. **Hydrocarbon degraders**: Microbes for cleaving C-C bonds in PFAS backbones
5. **PFAS-contaminated site isolates**: Environmental microbes from AFFF sites
6. **Co-occurrence patterns**: Microbial associations in PFAS-contaminated environments
7. **Similar organisms**: High similarity to categories 1-6

### Negative Controls
- Pristine environment microbes (no PFAS exposure)
- Human pathogens (filter housekeeping genes)

### Feature Extraction
- Dehalogenase genes (RdhA, DehH, DhaA, etc.)
- Fluoride exporters (CrcB, FEX)
- Hydrocarbon degradation pathways
- Reactive oxygen species production
- Metabolic co-dependencies
- Environmental metadata (pH, temperature, salinity, PFAS concentration)

### Model Outputs
- PFAS biodegradation potential scores
- Community design recommendations (3-5 members per consortium)
- Stability predictions (microbe-microbe interactions)
- Pathway completeness assessment

## 🧪 Development

### Running Tests
```bash
# Run all tests
make test

# Run specific validation
python -m doctest src/parsers.py -v
python -m doctest src/ncbi_search.py -v

# Validate data schemas
make validate-schema
make validate-consistency
```

### Code Quality
```bash
# Check code formatting
uv run ruff check src/
uv run ruff format src/
```

## 📈 Expected Outcomes

### Phase 1: Database Construction
- Comprehensive PFAS biodegradation database with 100+ genomes
- Annotated dehalogenase and fluoride resistance gene catalog
- Environmental metadata from PFAS-contaminated sites

### Phase 2: ML Model Training
- Predictive models for PFAS biodegradation potential
- Community design algorithms for optimal consortia
- Feature importance rankings for experimental validation

### Phase 3: Experimental Validation
- 10-15 designed microbial consortia
- 5 top-performing consortia validated experimentally
- Degradation of PFOA, PFOS, and polyfluorinated precursors

## 🤝 Contributing

We welcome contributions! This project uses:
- **Python 3.9+** with type hints
- **uv** for dependency management
- **Make** for pipeline automation
- **Git** with conventional commits

### Development Setup
1. Fork the repository
2. Create a feature branch
3. Make changes with tests
4. Run `make test` to validate
5. Submit a pull request

## 📄 License

This project is licensed under the [MIT License](LICENSE).

## 🙏 Acknowledgments

- **NCBI** for comprehensive biological databases
- **KEGG** for metabolic pathway data
- **UniProt** for protein sequence databases
- **RCSB PDB** for structural biology data
- **KG-Microbe** for ML-enabled microbial feature extraction
- **Claude AI** for development assistance

## 📞 Support

- **Issues**: [GitHub Issues](https://github.com/YourOrg/PFAS-AI/issues)
- **Documentation**: See `CLAUDE.md` for detailed technical guidance
- **Discussions**: [GitHub Discussions](https://github.com/YourOrg/PFAS-AI/discussions)

## 📚 References

Key papers on PFAS biodegradation:
1. Wackett, L.P. (2021). Why is the biodegradation of polyfluorinated compounds so rare? mSphere 6, e0072121.
2. Zhang, C., et al. (2022). Biological Utility of Fluorinated Compounds: from Materials Design to Molecular Imaging, Therapeutics and Environmental Remediation. Chem. Rev. 122, 167–208.
3. Ochoa-Herrera, V., et al. (2009). Toxicity of fluoride to microorganisms in biological wastewater treatment systems. Water Res. 43, 3177–3186.

---

**🧪 Built for PFAS biodegradation research • 🤖 ML-enhanced discovery • 🌍 Environmental remediation**
