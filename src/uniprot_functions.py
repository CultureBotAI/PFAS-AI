"""Extract biological functions from UniProt for comparative genomics analysis.

This module creates a comprehensive functions table from UniProt annotations,
including enzymes (EC), GO processes, reactions (Rhea), pathways, and chemicals (CHEBI).
"""

import pandas as pd
from pathlib import Path
from typing import List, Dict, Set, Tuple, Optional
from collections import defaultdict
import time

try:
    from src.apis.uniprot_client import UniProtClient
except ImportError:
    from apis.uniprot_client import UniProtClient


def extract_functions_from_uniprot(
    query_terms: List[str],
    organisms: List[str],
    size_per_query: int = 100
) -> Dict[str, List[Dict]]:
    """Extract comprehensive function data from UniProt.

    Args:
        query_terms: Search terms for UniProt queries
        organisms: List of organism names to filter
        size_per_query: Maximum results per query

    Returns:
        Dictionary with function types as keys:
        - 'enzymes': EC numbers with enzyme names
        - 'go_processes': GO biological processes
        - 'reactions': Rhea reactions
        - 'pathways': KEGG/Reactome/UniPathway
        - 'chemicals': CHEBI cofactors and substrates

    Examples:
        >>> functions = extract_functions_from_uniprot(
        ...     query_terms=["methanol dehydrogenase"],
        ...     organisms=["Methylobacterium"],
        ...     size_per_query=10
        ... )
        >>> isinstance(functions, dict)
        True
    """
    client = UniProtClient()

    # Track unique functions with associated proteins
    enzymes = defaultdict(lambda: {
        'function_id': '',
        'function_name': '',
        'function_type': 'enzyme',
        'proteins': set(),
        'organisms': set()
    })

    go_processes = defaultdict(lambda: {
        'function_id': '',
        'function_name': '',
        'function_type': 'go_process',
        'proteins': set(),
        'organisms': set()
    })

    reactions = defaultdict(lambda: {
        'function_id': '',
        'function_name': '',
        'function_type': 'reaction',
        'proteins': set(),
        'organisms': set()
    })

    pathways = defaultdict(lambda: {
        'function_id': '',
        'function_name': '',
        'function_type': 'pathway',
        'database': '',
        'proteins': set(),
        'organisms': set()
    })

    chemicals = defaultdict(lambda: {
        'function_id': '',
        'function_name': '',
        'function_type': 'chemical',
        'role': '',
        'proteins': set(),
        'organisms': set()
    })

    # Search UniProt for each query term
    print(f"Searching UniProt for {len(query_terms)} query terms across {len(organisms)} organisms...")

    all_proteins = []
    for query_term in query_terms:
        for organism in organisms:
            query = f"{query_term} AND organism_name:\"{organism}\""
            print(f"  Querying: {query}")

            try:
                results = client.search_proteins(
                    query=query,
                    fields='all',
                    size=size_per_query,
                    format='tsv'
                )

                if results:
                    all_proteins.extend(results)
                    print(f"    Found {len(results)} proteins")

                time.sleep(0.5)  # Rate limiting

            except Exception as e:
                print(f"    Error searching: {e}")
                continue

    # Deduplicate proteins by accession
    unique_proteins = {}
    for protein in all_proteins:
        accession = protein.get('accession', '')
        if accession and accession not in unique_proteins:
            unique_proteins[accession] = protein

    print(f"\nProcessing {len(unique_proteins)} unique proteins...")

    # Extract functions from each protein
    for accession, protein_data in unique_proteins.items():
        organism = protein_data.get('organism', 'Unknown')

        # Get detailed entry for comprehensive extraction
        try:
            entry = client.get_protein_entry(accession, format='json')
            if not entry:
                continue

            # Extract EC numbers
            ec_data = client.extract_ec_numbers(entry)
            for ec_id, ec_name in ec_data:
                enzymes[ec_id]['function_id'] = ec_id
                enzymes[ec_id]['function_name'] = ec_name
                enzymes[ec_id]['proteins'].add(accession)
                enzymes[ec_id]['organisms'].add(organism)

            # Extract GO biological processes only
            go_data = client.extract_go_terms(entry)
            for go_id, go_name, evidence in go_data:
                if go_id.startswith('GO:') and 'P:' in evidence:  # P = biological process
                    go_processes[go_id]['function_id'] = go_id
                    go_processes[go_id]['function_name'] = go_name
                    go_processes[go_id]['proteins'].add(accession)
                    go_processes[go_id]['organisms'].add(organism)

            # Extract Rhea reactions
            rhea_data = client.extract_rhea_reactions(entry)
            for rhea_id, rhea_name in rhea_data:
                reactions[rhea_id]['function_id'] = rhea_id
                reactions[rhea_id]['function_name'] = rhea_name
                reactions[rhea_id]['proteins'].add(accession)
                reactions[rhea_id]['organisms'].add(organism)

            # Extract pathways
            pathway_data = client.extract_pathways(entry)
            for db_name, pathway_ids in pathway_data.items():
                for pathway_id in pathway_ids:
                    key = f"{db_name}:{pathway_id}"
                    pathways[key]['function_id'] = pathway_id
                    pathways[key]['function_name'] = f"{db_name} pathway"
                    pathways[key]['database'] = db_name
                    pathways[key]['proteins'].add(accession)
                    pathways[key]['organisms'].add(organism)

            # Extract CHEBI chemicals (cofactors)
            chebi_data = client.extract_chebi_terms(entry)
            for chebi_id, chebi_name, role in chebi_data:
                chemicals[chebi_id]['function_id'] = chebi_id
                chemicals[chebi_id]['function_name'] = chebi_name
                chemicals[chebi_id]['role'] = role
                chemicals[chebi_id]['proteins'].add(accession)
                chemicals[chebi_id]['organisms'].add(organism)

            time.sleep(0.5)  # Rate limiting

        except Exception as e:
            print(f"  Error processing {accession}: {e}")
            continue

    # Convert to list format
    def convert_to_list(func_dict):
        result = []
        for func_data in func_dict.values():
            # Convert sets to sorted lists
            func_data['proteins'] = sorted(list(func_data['proteins']))
            func_data['organisms'] = sorted(list(func_data['organisms']))
            result.append(func_data)
        return result

    return {
        'enzymes': convert_to_list(enzymes),
        'go_processes': convert_to_list(go_processes),
        'reactions': convert_to_list(reactions),
        'pathways': convert_to_list(pathways),
        'chemicals': convert_to_list(chemicals)
    }


def create_functions_table(
    query_terms: Optional[List[str]] = None,
    organisms: Optional[List[str]] = None,
    output_dir: str = "data/txt/sheet",
    source_label: str = "uniprot_api"
) -> None:
    """Create comprehensive biological functions table from UniProt.

    Creates a TSV table with all biological functions found in UniProt,
    including enzymes, GO processes, reactions, pathways, and chemicals.

    Args:
        query_terms: Search terms (default: lanthanide-relevant terms)
        organisms: Organism names (default: methylotroph genera)
        output_dir: Directory to save output file
        source_label: Source provenance label

    Examples:
        >>> # Create table with defaults
        >>> create_functions_table()  # doctest: +SKIP
    """
    # Default search terms
    if query_terms is None:
        query_terms = [
            "methanol dehydrogenase",
            "XoxF",
            "MxaF",
            "ExaF",
            "alcohol dehydrogenase",
            "lanthanide",
            "lanthanophore",
            "lanmodulin",
            "methylotroph"
        ]

    if organisms is None:
        organisms = [
            "Methylobacterium",
            "Methylorubrum",
            "Methylosinus",
            "Paracoccus"
        ]

    print("Extracting biological functions from UniProt...")
    functions_data = extract_functions_from_uniprot(
        query_terms=query_terms,
        organisms=organisms,
        size_per_query=100
    )

    # Combine all function types into single table
    all_functions = []

    for func_type, func_list in functions_data.items():
        print(f"\n{func_type.capitalize()}: {len(func_list)} unique functions")
        for func in func_list:
            row = {
                'function_id': func['function_id'],
                'function_name': func['function_name'],
                'function_type': func['function_type'],
                'associated_proteins': '; '.join(func['proteins'][:10]),  # Limit to 10 for readability
                'protein_count': len(func['proteins']),
                'organisms': '; '.join(func['organisms'][:5]),  # Limit to 5
                'organism_count': len(func['organisms']),
                'database': func.get('database', ''),
                'role': func.get('role', ''),
                'source': source_label
            }
            all_functions.append(row)

    # Create DataFrame
    functions_df = pd.DataFrame(all_functions)

    # Sort by function type and then by protein count (most common first)
    functions_df = functions_df.sort_values(
        by=['function_type', 'protein_count'],
        ascending=[True, False]
    )

    # Save to TSV
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    output_file = output_dir / "BER_CMM_Data_for_AI_biological_functions.tsv"
    functions_df.to_csv(output_file, sep='\t', index=False)

    print(f"\nBiological functions table saved: {output_file}")
    print(f"  Total functions: {len(functions_df)}")
    print(f"  Enzymes (EC): {len(functions_df[functions_df['function_type'] == 'enzyme'])}")
    print(f"  GO Processes: {len(functions_df[functions_df['function_type'] == 'go_process'])}")
    print(f"  Reactions (Rhea): {len(functions_df[functions_df['function_type'] == 'reaction'])}")
    print(f"  Pathways: {len(functions_df[functions_df['function_type'] == 'pathway'])}")
    print(f"  Chemicals (CHEBI): {len(functions_df[functions_df['function_type'] == 'chemical'])}")


def extend_existing_functions_table(
    input_file: str,
    query_terms: Optional[List[str]] = None,
    organisms: Optional[List[str]] = None,
    output_dir: str = "data/txt/sheet"
) -> None:
    """Extend existing functions table with UniProt data.

    Args:
        input_file: Path to existing functions TSV file
        query_terms: Search terms (default: lanthanide-relevant terms)
        organisms: Organism names (default: methylotroph genera)
        output_dir: Directory to save extended table
    """
    print("Reading existing functions table...")
    try:
        existing_df = pd.read_csv(input_file, sep='\t')
        print(f"  Loaded {len(existing_df)} existing functions")
    except FileNotFoundError:
        print(f"  File not found: {input_file}")
        print("  Creating new functions table instead...")
        create_functions_table(query_terms, organisms, output_dir)
        return

    # Create new functions table
    create_functions_table(query_terms, organisms, output_dir)

    # Read newly created table
    new_file = Path(output_dir) / "BER_CMM_Data_for_AI_biological_functions.tsv"
    new_df = pd.read_csv(new_file, sep='\t')

    # Merge with existing data
    print("\nMerging with existing data...")
    combined_df = pd.concat([existing_df, new_df], ignore_index=True)

    # Remove duplicates based on function_id
    combined_df = combined_df.drop_duplicates(subset=['function_id'], keep='first')

    # Save extended table
    output_file = Path(output_dir) / "BER_CMM_Data_for_AI_biological_functions_extended.tsv"
    combined_df.to_csv(output_file, sep='\t', index=False)

    print(f"\nExtended functions table saved: {output_file}")
    print(f"  Original: {len(existing_df)}, New: {len(new_df)}, Combined: {len(combined_df)}")
    print(f"  Added {len(combined_df) - len(existing_df)} new functions")


if __name__ == "__main__":
    # Example usage
    create_functions_table()
