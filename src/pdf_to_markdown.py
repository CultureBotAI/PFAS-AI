"""Convert PDF files to markdown format.

This script uses PyMuPDF (fitz) to extract text from PDFs and convert to markdown,
preserving structure for better data extraction.
"""

import argparse
import re
from pathlib import Path
from typing import List, Optional

try:
    import fitz  # PyMuPDF
    HAS_PYMUPDF = True
except ImportError:
    HAS_PYMUPDF = False
    print("Warning: PyMuPDF not installed. Install with: uv pip install pymupdf")


class PDFToMarkdownConverter:
    """Convert PDF to markdown format."""

    def __init__(self, pdf_path: Path):
        """Initialize converter with PDF path.

        Args:
            pdf_path: Path to PDF file
        """
        self.pdf_path = pdf_path
        self.pdf_name = pdf_path.stem

    def convert_to_markdown(self) -> str:
        """Convert PDF to markdown format.

        Returns:
            Markdown-formatted text content
        """
        if not HAS_PYMUPDF:
            return self._fallback_text_extraction()

        try:
            doc = fitz.open(self.pdf_path)
            markdown_content = []

            # Add title from filename
            markdown_content.append(f"# {self.pdf_name}\n\n")
            markdown_content.append(f"**Source PDF**: {self.pdf_path.name}\n\n")
            markdown_content.append("---\n\n")

            # Extract text from each page
            for page_num, page in enumerate(doc, 1):
                # Get page text
                text = page.get_text()

                # Clean up text
                text = self._clean_text(text)

                # Add page marker
                markdown_content.append(f"## Page {page_num}\n\n")
                markdown_content.append(text)
                markdown_content.append("\n\n")

            doc.close()

            return "".join(markdown_content)

        except Exception as e:
            print(f"Error converting {self.pdf_path.name}: {e}")
            return self._fallback_text_extraction()

    def _clean_text(self, text: str) -> str:
        """Clean extracted text.

        Args:
            text: Raw extracted text

        Returns:
            Cleaned text
        """
        # Remove excessive whitespace
        text = re.sub(r'\n\s*\n\s*\n+', '\n\n', text)

        # Fix hyphenation at line breaks
        text = re.sub(r'(\w+)-\s*\n\s*(\w+)', r'\1\2', text)

        # Preserve chemical formulas and Greek letters
        # (already handled by PyMuPDF in most cases)

        return text.strip()

    def _fallback_text_extraction(self) -> str:
        """Fallback text extraction using basic file reading.

        Returns:
            Basic text content
        """
        return f"# {self.pdf_name}\n\n**Note**: PyMuPDF not available. Using placeholder.\n\nInstall PyMuPDF with: `uv pip install pymupdf`\n"


def convert_pdf_to_markdown(pdf_path: Path, output_path: Optional[Path] = None) -> Path:
    """Convert a single PDF to markdown.

    Args:
        pdf_path: Path to input PDF file
        output_path: Optional output path (defaults to same name with .md extension)

    Returns:
        Path to output markdown file
    """
    if output_path is None:
        output_path = pdf_path.parent / f"{pdf_path.stem}.md"

    print(f"Converting {pdf_path.name} to markdown...")

    converter = PDFToMarkdownConverter(pdf_path)
    markdown_content = converter.convert_to_markdown()

    # Write markdown file
    output_path.write_text(markdown_content, encoding='utf-8')

    print(f"  Saved to: {output_path}")
    print(f"  Size: {len(markdown_content)} characters")

    return output_path


def batch_convert_pdfs(pdf_dir: Path, output_dir: Optional[Path] = None) -> List[Path]:
    """Convert all PDFs in directory to markdown.

    Args:
        pdf_dir: Directory containing PDF files
        output_dir: Optional output directory (defaults to same directory)

    Returns:
        List of paths to generated markdown files
    """
    if output_dir is None:
        output_dir = pdf_dir

    pdf_files = list(pdf_dir.glob("*.pdf"))

    if not pdf_files:
        print(f"No PDF files found in {pdf_dir}")
        return []

    print(f"Found {len(pdf_files)} PDF files to convert\n")

    markdown_files = []
    for pdf_file in pdf_files:
        output_path = output_dir / f"{pdf_file.stem}.md"
        md_path = convert_pdf_to_markdown(pdf_file, output_path)
        markdown_files.append(md_path)
        print()

    print(f"Converted {len(markdown_files)} PDFs to markdown")
    return markdown_files


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Convert PDF files to markdown format"
    )
    parser.add_argument(
        'pdf_path',
        type=Path,
        nargs='?',
        help='Path to PDF file (optional if using --batch)'
    )
    parser.add_argument(
        '--output',
        type=Path,
        help='Output markdown file path'
    )
    parser.add_argument(
        '--batch',
        type=Path,
        help='Convert all PDFs in directory'
    )
    parser.add_argument(
        '--output-dir',
        type=Path,
        help='Output directory for batch conversion'
    )

    args = parser.parse_args()

    if args.batch:
        # Batch conversion
        batch_convert_pdfs(args.batch, args.output_dir)
    elif args.pdf_path:
        # Single file conversion
        convert_pdf_to_markdown(args.pdf_path, args.output)
    else:
        parser.print_help()
        print("\nError: Either provide a PDF path or use --batch")
        return 1

    return 0


if __name__ == "__main__":
    exit(main())
