"""UniProt REST API client for programmatic access to protein knowledge.

This module provides a comprehensive client for the UniProt REST API with support for:
- Protein search and retrieval
- ID mapping between databases
- GO, EC, CHEBI, Rhea, pathway, and publication extraction
- Rate limiting and retry logic
- Batch operations

API Documentation: https://www.uniprot.org/help/api
Return Fields: https://www.uniprot.org/help/return_fields
"""

import time
import requests
from typing import Dict, List, Optional, Set, Tuple, Iterator, Any
from dataclasses import dataclass
from functools import wraps
import json
from pathlib import Path


# UniProt REST API base URLs
UNIPROT_BASE_URL = "https://rest.uniprot.org"
UNIPROT_SEARCH_URL = f"{UNIPROT_BASE_URL}/uniprotkb/search"
UNIPROT_ENTRY_URL = f"{UNIPROT_BASE_URL}/uniprotkb"
UNIPROT_ID_MAPPING_URL = f"{UNIPROT_BASE_URL}/idmapping"


# Comprehensive field mappings for UniProt API
UNIPROT_FIELDS = {
    'basic': [
        'accession', 'id', 'gene_names', 'gene_primary', 'gene_synonym',
        'protein_name', 'organism_name', 'organism_id', 'reviewed'
    ],
    'function': [
        'cc_function', 'cc_catalytic_activity', 'cc_pathway',
        'ec', 'rhea', 'keyword'
    ],
    'ontology': [
        'go_p', 'go_c', 'go_f', 'go_id', 'go'
    ],
    'chemistry': [
        'cc_cofactor', 'chebi', 'ft_binding', 'ft_active_site'
    ],
    'pathways': [
        'xref_reactome', 'xref_unipathway', 'xref_kegg',
        'xref_biocyc', 'xref_brenda'
    ],
    'references': [
        'lit_pubmed_id', 'lit_doi', 'date_created', 'date_modified'
    ],
    'structure': [
        'xref_pdb', 'xref_alphafolddb', 'structure_3d'
    ],
    'sequence': [
        'sequence', 'length', 'mass', 'ft_domain', 'ft_region'
    ],
    'taxonomy': [
        'lineage', 'lineage_ids'
    ]
}


def rate_limited(min_interval: float = 0.5):
    """Decorator to enforce minimum time between API calls.

    Args:
        min_interval: Minimum seconds between calls (default 0.5)
    """
    last_call = {'time': 0}

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            elapsed = time.time() - last_call['time']
            if elapsed < min_interval:
                time.sleep(min_interval - elapsed)
            result = func(*args, **kwargs)
            last_call['time'] = time.time()
            return result
        return wrapper
    return decorator


@dataclass
class UniProtSearchResult:
    """Container for UniProt search results."""
    accession: str
    gene_names: str = ""
    protein_name: str = ""
    organism: str = ""
    ec: str = ""
    go_terms: str = ""
    rhea: str = ""
    reviewed: bool = False
    raw_data: Dict = None


class UniProtClient:
    """Client for UniProt REST API with comprehensive protein data access.

    Examples:
        >>> client = UniProtClient()
        >>> results = client.search_proteins("lanM AND organism_name:Methylobacterium")
        >>> protein = client.get_protein_entry("C5B164")
        >>> mapped_ids = client.map_ids(["K23995"], from_db="KEGG", to_db="UniProtKB")
    """

    def __init__(self, timeout: int = 30, max_retries: int = 3):
        """Initialize UniProt client.

        Args:
            timeout: Request timeout in seconds
            max_retries: Maximum number of retry attempts
        """
        self.timeout = timeout
        self.max_retries = max_retries
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'CMM-AI/1.0 (https://github.com/yourusername/CMM-AI)'
        })

    @rate_limited(0.5)
    def _make_request(self, url: str, params: Dict = None, method: str = 'GET') -> requests.Response:
        """Make HTTP request with retry logic.

        Args:
            url: Request URL
            params: Query parameters
            method: HTTP method (GET, POST)

        Returns:
            Response object

        Raises:
            requests.RequestException: If request fails after retries
        """
        for attempt in range(self.max_retries):
            try:
                if method == 'GET':
                    response = self.session.get(url, params=params, timeout=self.timeout)
                else:
                    response = self.session.post(url, data=params, timeout=self.timeout)

                response.raise_for_status()
                return response

            except requests.exceptions.RequestException as e:
                if attempt == self.max_retries - 1:
                    raise
                wait_time = 2 ** attempt  # Exponential backoff
                print(f"Request failed, retrying in {wait_time}s... ({e})")
                time.sleep(wait_time)

        raise requests.RequestException("Max retries exceeded")

    def get_all_fields(self, categories: List[str] = None) -> str:
        """Get comma-separated field list for API requests.

        Args:
            categories: List of field categories to include (e.g., ['basic', 'function'])
                       If None, includes all categories

        Returns:
            Comma-separated field string
        """
        if categories is None:
            categories = list(UNIPROT_FIELDS.keys())

        fields = []
        for category in categories:
            if category in UNIPROT_FIELDS:
                fields.extend(UNIPROT_FIELDS[category])

        return ','.join(fields)

    def search_proteins(
        self,
        query: str,
        fields: List[str] = None,
        size: int = 500,
        format: str = 'tsv'
    ) -> List[Dict[str, str]]:
        """Search UniProtKB and return results.

        Args:
            query: UniProt query string (e.g., "lanM AND organism_id:83618")
            fields: List of return fields. If None, uses comprehensive default set
            size: Maximum number of results (default 500)
            format: Return format ('tsv' or 'json')

        Returns:
            List of protein records as dictionaries

        Examples:
            >>> client = UniProtClient()
            >>> results = client.search_proteins(
            ...     "gene:xoxF AND organism_name:Methylobacterium",
            ...     size=10
            ... )
            >>> len(results) > 0
            True
        """
        if fields is None:
            fields_str = self.get_all_fields(['basic', 'function', 'ontology', 'chemistry', 'pathways', 'references'])
        else:
            fields_str = ','.join(fields)

        params = {
            'query': query,
            'format': format,
            'fields': fields_str,
            'size': str(size)
        }

        try:
            response = self._make_request(UNIPROT_SEARCH_URL, params)

            if format == 'tsv':
                return self._parse_tsv_response(response.text)
            elif format == 'json':
                return response.json().get('results', [])
            else:
                return []

        except Exception as e:
            print(f"Error searching UniProt: {e}")
            return []

    def _parse_tsv_response(self, tsv_text: str) -> List[Dict[str, str]]:
        """Parse TSV response into list of dictionaries.

        Args:
            tsv_text: TSV formatted text

        Returns:
            List of dictionaries with column headers as keys
        """
        lines = tsv_text.strip().split('\n')
        if len(lines) < 2:
            return []

        headers = lines[0].split('\t')
        records = []

        for line in lines[1:]:
            if not line.strip():
                continue
            values = line.split('\t')
            # Pad with empty strings if needed
            values += [''] * (len(headers) - len(values))
            record = dict(zip(headers, values))
            records.append(record)

        return records

    def get_protein_entry(self, accession: str, format: str = 'json') -> Optional[Dict]:
        """Retrieve complete protein entry by accession.

        Args:
            accession: UniProt accession (e.g., "C5B164")
            format: Return format ('json', 'txt', 'xml', 'fasta')

        Returns:
            Protein entry as dictionary (for JSON) or string (for other formats)

        Examples:
            >>> client = UniProtClient()
            >>> entry = client.get_protein_entry("P0A0H3")
            >>> 'primaryAccession' in entry if entry else False
            True
        """
        url = f"{UNIPROT_ENTRY_URL}/{accession}.{format}"

        try:
            response = self._make_request(url)

            if format == 'json':
                return response.json()
            else:
                return response.text

        except Exception as e:
            print(f"Error retrieving entry {accession}: {e}")
            return None

    def get_proteins_batch(
        self,
        accessions: List[str],
        fields: List[str] = None
    ) -> List[Dict[str, str]]:
        """Retrieve multiple protein entries in batch.

        Args:
            accessions: List of UniProt accessions
            fields: Fields to retrieve

        Returns:
            List of protein records
        """
        if not accessions:
            return []

        # Batch by 100 to avoid URL length limits
        batch_size = 100
        all_records = []

        for i in range(0, len(accessions), batch_size):
            batch = accessions[i:i+batch_size]
            query = f"accession:({' OR '.join(batch)})"
            records = self.search_proteins(query, fields=fields, size=batch_size)
            all_records.extend(records)

        return all_records

    def stream_search_results(
        self,
        query: str,
        fields: List[str] = None,
        batch_size: int = 500
    ) -> Iterator[Dict[str, str]]:
        """Stream search results for large queries using pagination.

        Args:
            query: UniProt query string
            fields: Fields to retrieve
            batch_size: Number of results per request

        Yields:
            Individual protein records
        """
        cursor = "*"

        while cursor:
            params = {
                'query': query,
                'format': 'json',
                'fields': ','.join(fields) if fields else self.get_all_fields(),
                'size': str(batch_size),
                'cursor': cursor
            }

            try:
                response = self._make_request(UNIPROT_SEARCH_URL, params)
                data = response.json()

                for result in data.get('results', []):
                    yield result

                # Get next cursor for pagination
                cursor = data.get('nextCursor')

                if not cursor:
                    break

            except Exception as e:
                print(f"Error streaming results: {e}")
                break

    def map_ids(
        self,
        ids: List[str],
        from_db: str,
        to_db: str = "UniProtKB"
    ) -> Dict[str, List[str]]:
        """Map identifiers between databases using UniProt ID mapping service.

        Args:
            ids: List of identifiers to map
            from_db: Source database (e.g., 'KEGG', 'Gene_Name', 'RefSeq_Protein')
            to_db: Target database (default 'UniProtKB')

        Returns:
            Dictionary mapping source IDs to list of target IDs

        Supported databases:
            - Gene_Name, Gene_Synonym
            - KEGG, EMBL-GenBank-DDBJ, RefSeq_Protein
            - PDB, AlphaFoldDB
            - GO, EC, Rhea
            - And many more: https://www.uniprot.org/help/id_mapping

        Examples:
            >>> client = UniProtClient()
            >>> mapped = client.map_ids(["K23995"], from_db="KEGG", to_db="UniProtKB")
            >>> type(mapped) == dict
            True
        """
        if not ids:
            return {}

        # Submit ID mapping job
        submit_url = f"{UNIPROT_ID_MAPPING_URL}/run"
        params = {
            'from': from_db,
            'to': to_db,
            'ids': ','.join(ids)
        }

        try:
            # Submit job
            response = self._make_request(submit_url, params, method='POST')
            job_id = response.json()['jobId']

            # Poll for results
            status_url = f"{UNIPROT_ID_MAPPING_URL}/status/{job_id}"
            max_polls = 20

            for _ in range(max_polls):
                time.sleep(1)  # Wait between polls
                response = self._make_request(status_url)
                status = response.json()

                if 'results' in status or 'failedIds' in status:
                    # Job complete, get results
                    results_url = f"{UNIPROT_ID_MAPPING_URL}/results/{job_id}"
                    response = self._make_request(results_url, params={'format': 'json'})
                    results_data = response.json()

                    # Parse results into dict
                    mapping = {}
                    for result in results_data.get('results', []):
                        from_id = result.get('from')
                        to_id = result.get('to', {}).get('primaryAccession', '')
                        if from_id and to_id:
                            if from_id not in mapping:
                                mapping[from_id] = []
                            mapping[from_id].append(to_id)

                    return mapping

            print(f"ID mapping timed out for job {job_id}")
            return {}

        except Exception as e:
            print(f"Error mapping IDs: {e}")
            return {}

    def extract_go_terms(self, entry: Dict) -> List[Tuple[str, str, str]]:
        """Extract GO terms from protein entry with evidence codes.

        Args:
            entry: UniProt entry (JSON format)

        Returns:
            List of (GO_ID, term_name, evidence_code) tuples
        """
        go_terms = []

        for go_annotation in entry.get('uniProtKBCrossReferences', []):
            if go_annotation.get('database') == 'GO':
                go_id = go_annotation.get('id', '')
                properties = {p['key']: p['value'] for p in go_annotation.get('properties', [])}
                term = properties.get('GoTerm', '')
                evidence = properties.get('GoEvidenceType', '')

                if go_id and term:
                    go_terms.append((go_id, term, evidence))

        return go_terms

    def extract_ec_numbers(self, entry: Dict) -> List[Tuple[str, str]]:
        """Extract EC numbers with catalytic activities.

        Args:
            entry: UniProt entry (JSON format)

        Returns:
            List of (EC_number, activity_description) tuples
        """
        ec_numbers = []

        # From protein description
        protein_desc = entry.get('proteinDescription', {})
        for rec_name in protein_desc.get('recommendedName', {}).get('ecNumbers', []):
            ec_numbers.append((rec_name.get('value', ''), ''))

        # From comments (catalytic activity)
        for comment in entry.get('comments', []):
            if comment.get('commentType') == 'CATALYTIC ACTIVITY':
                reaction = comment.get('reaction', {})
                ec = reaction.get('ecNumber', '')
                name = reaction.get('name', '')
                if ec:
                    ec_numbers.append((ec, name))

        return ec_numbers

    def extract_rhea_reactions(self, entry: Dict) -> List[Tuple[str, str]]:
        """Extract Rhea reaction IDs.

        Args:
            entry: UniProt entry (JSON format)

        Returns:
            List of (Rhea_ID, reaction_description) tuples
        """
        rhea_reactions = []

        for comment in entry.get('comments', []):
            if comment.get('commentType') == 'CATALYTIC ACTIVITY':
                reaction = comment.get('reaction', {})

                # Rhea cross-references
                for xref in reaction.get('reactionCrossReferences', []):
                    if xref.get('database') == 'Rhea':
                        rhea_id = xref.get('id', '')
                        name = reaction.get('name', '')
                        if rhea_id:
                            rhea_reactions.append((f"RHEA:{rhea_id}", name))

        return rhea_reactions

    def extract_chebi_terms(self, entry: Dict) -> List[Tuple[str, str, str]]:
        """Extract CHEBI terms from cofactors and catalytic activities.

        Args:
            entry: UniProt entry (JSON format)

        Returns:
            List of (CHEBI_ID, chemical_name, role) tuples
        """
        chebi_terms = []

        # From cofactor comments
        for comment in entry.get('comments', []):
            if comment.get('commentType') == 'COFACTOR':
                for cofactor in comment.get('cofactors', []):
                    name = cofactor.get('name', '')
                    # cofactorCrossReference is a dict, not a list
                    xref = cofactor.get('cofactorCrossReference', {})
                    if isinstance(xref, dict) and xref.get('database') == 'ChEBI':
                        chebi_id = xref.get('id', '')
                        if chebi_id:
                            chebi_terms.append((f"CHEBI:{chebi_id}", name, 'cofactor'))

            # From catalytic activity
            if comment.get('commentType') == 'CATALYTIC ACTIVITY':
                reaction = comment.get('reaction', {})
                # reactionCrossReferences might be a list
                xrefs = reaction.get('reactionCrossReferences', [])
                if isinstance(xrefs, list):
                    for xref in xrefs:
                        if isinstance(xref, dict) and xref.get('database') == 'ChEBI':
                            chebi_id = xref.get('id', '')
                            if chebi_id:
                                chebi_terms.append((f"CHEBI:{chebi_id}", '', 'substrate_or_product'))

        return chebi_terms

    def extract_pathways(self, entry: Dict) -> Dict[str, List[str]]:
        """Extract pathway associations from various databases.

        Args:
            entry: UniProt entry (JSON format)

        Returns:
            Dictionary with pathway database as key, list of pathway IDs as values
        """
        pathways = {
            'KEGG': [],
            'Reactome': [],
            'UniPathway': [],
            'BioCyc': []
        }

        for xref in entry.get('uniProtKBCrossReferences', []):
            db = xref.get('database', '')
            pathway_id = xref.get('id', '')

            if db == 'KEGG' and pathway_id:
                pathways['KEGG'].append(pathway_id)
            elif db == 'Reactome' and pathway_id:
                pathways['Reactome'].append(pathway_id)
            elif db == 'UniPathway' and pathway_id:
                pathways['UniPathway'].append(pathway_id)
            elif db == 'BioCyc' and pathway_id:
                pathways['BioCyc'].append(pathway_id)

        # Also check pathway comments
        for comment in entry.get('comments', []):
            if comment.get('commentType') == 'PATHWAY':
                # Pathway text description available in comment['texts']
                pass

        return pathways

    def extract_publications(self, entry: Dict) -> List[Tuple[str, str, str]]:
        """Extract publication references (PubMed IDs and DOIs).

        Args:
            entry: UniProt entry (JSON format)

        Returns:
            List of (PubMed_ID, DOI, title) tuples
        """
        publications = []

        for reference in entry.get('references', []):
            citation = reference.get('citation', {})

            pubmed_id = ''
            doi = ''
            title = citation.get('title', '')

            for xref in citation.get('citationCrossReferences', []):
                if xref.get('database') == 'PubMed':
                    pubmed_id = xref.get('id', '')
                elif xref.get('database') == 'DOI':
                    doi = xref.get('id', '')

            if pubmed_id or doi:
                publications.append((pubmed_id, doi, title))

        return publications


if __name__ == "__main__":
    import doctest
    doctest.testmod()
