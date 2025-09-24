"""CMM-AI: AI tools for Culture Media Models.

This package provides utilities for working with CMM data, including:
- File parsing (Excel to TSV, Word/PDF to text)
- NCBI search for lanthanide-relevant bacteria and archaea
- Data enhancement and merging capabilities
"""

from cmm_ai.parsers import (
    xlsx_to_tsv,
    docx_to_text,
    pdf_to_text,
    parse_file
)
from cmm_ai.ncbi_search import (
    search_ncbi_assembly,
    search_ncbi_biosample,
    search_lanthanide_organisms,
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
    "search_lanthanide_organisms",
    "create_extended_tables"
]