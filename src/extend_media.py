#!/usr/bin/env python3
"""Script to create curated growth media and media ingredients tables.

This script generates standardized growth media formulations for methylotrophs
and related organisms, with detailed ingredient lists including CHEBI ontology IDs,
chemical formulas, and concentrations.
"""

import sys
from pathlib import Path

# Import the search module
from media_search import create_extended_media_tables


def main():
    """Main function to create media and media ingredients tables."""

    print("Creating curated growth media and ingredients tables...")
    print("Data sources: Curated formulations from ATCC, DSMZ, and literature")
    print()

    try:
        create_extended_media_tables(
            output_dir="data/txt/sheet"
        )
        print()
        print("Successfully created media tables!")
        return 0

    except Exception as e:
        print()
        print(f"Error creating media tables: {e}")
        print()
        print("This might be due to:")
        print("- File permission issues")
        print("- Missing dependencies")
        print()
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
