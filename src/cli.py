"""Command-line interface for CMM-AI file parsers."""

import argparse
import sys
from pathlib import Path
from typing import Optional

from .parsers import parse_file, xlsx_to_tsv, docx_to_text, pdf_to_text, sanitize_filename


def main(argv: Optional[list] = None) -> int:
    """Main CLI entry point.
    
    Args:
        argv: Command line arguments (for testing)
        
    Returns:
        Exit code (0 for success, non-zero for error)
    """
    parser = argparse.ArgumentParser(
        description="Convert various file formats to text/TSV",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Convert Excel to TSV
  python -m cmm_ai.cli data.xlsx -o data.tsv
  
  # Convert specific sheet
  python -m cmm_ai.cli data.xlsx -o data.tsv --sheet "Sheet2"
  
  # Convert Word doc to text
  python -m cmm_ai.cli document.docx -o document.txt
  
  # Convert PDF to text (specific pages)
  python -m cmm_ai.cli document.pdf -o document.txt --pages 1 2 3
  
  # Print to stdout
  python -m cmm_ai.cli data.xlsx
"""
    )
    
    parser.add_argument(
        "input",
        type=Path,
        help="Input file (xlsx, xls, docx, or pdf)"
    )
    
    parser.add_argument(
        "-o", "--output",
        type=Path,
        help="Output file path. If not specified, prints to stdout"
    )
    
    # Excel-specific options
    parser.add_argument(
        "--sheet",
        help="Sheet name or index for Excel files (default: first sheet)"
    )
    
    # PDF-specific options
    parser.add_argument(
        "--pages",
        nargs="+",
        type=int,
        help="Page numbers to extract from PDF (1-indexed)"
    )
    
    args = parser.parse_args(argv)
    
    # Check input file exists
    if not args.input.exists():
        print(f"Error: Input file not found: {args.input}", file=sys.stderr)
        return 1
    
    try:
        extension = args.input.suffix.lower()
        
        # Sanitize output path if provided
        output_path = args.output
        if output_path:
            sanitized_name = sanitize_filename(output_path.name)
            output_path = output_path.parent / sanitized_name
        
        if extension in ['.xlsx', '.xls']:
            # Handle Excel files
            sheet = args.sheet
            if sheet and sheet.isdigit():
                sheet = int(sheet)
            content = xlsx_to_tsv(args.input, output_path, sheet_name=sheet)
            
        elif extension == '.docx':
            # Handle Word docs
            content = docx_to_text(args.input, output_path)
            
        elif extension == '.pdf':
            # Handle PDFs
            pages = None
            if args.pages:
                # Convert 1-indexed to 0-indexed
                pages = [p - 1 for p in args.pages]
            content = pdf_to_text(args.input, output_path, page_numbers=pages)
            
        else:
            # Use generic parser
            content = parse_file(args.input, output_path)
        
        # Print to stdout if no output file specified
        if not args.output and content:
            print(content)
            
        return 0
        
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())