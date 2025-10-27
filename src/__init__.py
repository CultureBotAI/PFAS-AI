"""PFAS-AI: ML-enabled AI tools for PFAS biodegradation research.

This package provides utilities for working with PFAS data, including:
- File parsing (Excel to TSV, Word/PDF to text)
- NCBI search for PFAS-relevant bacteria and archaea
- Data enhancement and merging capabilities
- ML-enabled feature extraction for microbial consortia design
"""

from .parsers import (
    xlsx_to_tsv,
    docx_to_text,
    pdf_to_text,
    parse_file
)
from .ncbi_search import (
    search_ncbi_assembly,
    search_ncbi_biosample,
    search_pfas_organisms,
    create_extended_tables
)

__version__ = "0.1.0"

__all__ = [
    "xlsx_to_tsv",
    "docx_to_text",
    "pdf_to_text",
    "parse_file",
    "search_ncbi_assembly",
    "search_ncbi_biosample",
    "search_pfas_organisms",
    "create_extended_tables"
]