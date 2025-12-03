#!/usr/bin/env python3
import argparse
import csv
import re
from pathlib import Path
from typing import List, Tuple

def load_species_calls(path: Path, sample_col: str = "sample_accession", species_col: str = "scientific_name") -> dict:
    """Robust loader: sniff delimiter, normalize header keys (case-insensitive, strip), handle BOM."""
    d = {}
    text = path.read_text(encoding="utf-8", errors="replace")
    if not text.strip():
        print(f"[WARN] species-calls file is empty: {path}")
        return d

    # Normalize common BOM
    if text.startswith("\ufeff"):
        text = text.lstrip("\ufeff")

    # sniff delimiter: prefer tab if present, else comma, else whitespace
    first_chunk = text.splitlines()[0] if text.splitlines() else ""
    if "\t" in first_chunk:
        delim = "\t"
    elif "," in first_chunk:
        delim = ","
    else:
        delim = None  # let csv.DictReader infer (whitespace-safe via split later)

    # use csv.DictReader; if delim is None use csv.Sniffer to guess
    from io import StringIO
    buf = StringIO(text)
    if delim is None:
        try:
            sniff = csv.Sniffer().sniff(first_chunk)
            delim = sniff.delimiter
        except Exception:
            delim = "\t"

    reader = csv.DictReader(buf, delimiter=delim)
    hdr = reader.fieldnames or []
    print(f"[DEBUG] detected delimiter={repr(delim)}, header columns={hdr[:10]}")

    # build case-insensitive map for header names
    lname_map = { (h.strip().lower() if h else ""): h for h in hdr }

    samp_key = lname_map.get(sample_col.lower(), None)
    sp_key = lname_map.get(species_col.lower(), None)

    # if user-provided names not found, try reasonable fallbacks
    if samp_key is None:
        for candidate in ("sample_accession","sample","sample_id","biosample","accession"):
            if candidate in lname_map:
                samp_key = lname_map[candidate]
                break
    if sp_key is None:
        for candidate in ("scientific_name","species","sylph_species","sylph_prediction","species_name"):
            if candidate in lname_map:
                sp_key = lname_map[candidate]
                break

    if samp_key is None or sp_key is None:
        print(f"[WARN] Could not find requested columns. resolved sample_col={samp_key}, species_col={sp_key}")
        # still attempt to iterate rows and pick first two columns as fallback
    count = 0
    for row in reader:
        # if DictReader failed to map keys properly, fall back to splitting line
        if samp_key and sp_key:
            sid = (row.get(samp_key) or "").strip()
            sp = (row.get(sp_key) or "").strip()
        else:
            # try fallback: take first two values of the row
            vals = [ (v or "").strip() for v in row.values() ]
            if len(vals) >= 2:
                sid, sp = vals[0], vals[1]
            elif len(vals) == 1:
                sid, sp = vals[0], ""
            else:
                continue
        if not sid:
            continue
        d[sid] = sp
        count += 1
    print(f"[INFO] loaded {count} rows from {path.name}")
    return d

def load_query_species(path: Path) -> List[str]:
    species_queries = []
    with path.open("r", encoding="utf-8", errors="replace") as f:
        for line in f:
            s = line.strip()
            if not s or s.startswith("#"):
                continue
            species_queries.append(s)
    return species_queries

def normalize_species(s: str) -> str:
    if s is None:
        return ""
    s = s.replace(".", " ").replace(",", " ")
    s = re.sub(r"\s+", " ", s).strip().lower()
    return s

def find_samples_by_species(species_calls: dict, query: str,
                            inclusive_words: int = 2, ignore_case: bool = True) -> List[Tuple[str, str]]:
    matches = []
    nq = normalize_species(query) if ignore_case else query
    # use first N words
    words = nq.split()
    if len(words) >= 1:
        prefix = " ".join(words[:inclusive_words])
    else:
        prefix = nq
    for sid, sp in species_calls.items():
        if not sp:
            continue
        target = normalize_species(sp) if ignore_case else sp
        # match prefix
        if prefix in target:
            matches.append((sid, sp))
    return matches

def write_matches(output_path: Path, matches: List[Tuple[str, str]], header: List[str]):
    with output_path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f, delimiter="\t", lineterminator="\n")
        writer.writerow(header)
        for row in matches:
            writer.writerow(row)

def main():
    parser = argparse.ArgumentParser(description="Match species queries (first two words) against Species_calls_sample file")
    parser.add_argument("--species-calls", required=True,
                        help="TSV file with Sample & Species columns")
    parser.add_argument("--query-species", required=True,
                        help="Text file with species names (one species per line)")
    parser.add_argument("--inclusive-words", type=int, default=2,
                        help="Take the first N words of the query species to match (default 2)")
    parser.add_argument("--output", required=True,
                        help="TSV file to write matching rows (Sample and Species)")
    parser.add_argument("--sample-col", default="sample_accession",
                        help="Column name for sample in species-calls file")
    parser.add_argument("--species-col", default="scientific_name",
                        help="Column name for species in species-calls file")
    args = parser.parse_args()

    species_calls = load_species_calls(Path(args.species_calls),
                                       sample_col=args.sample_col,
                                       species_col=args.species_col)
    species_queries = load_query_species(Path(args.query_species))
    print(f"[INFO] Loaded {len(species_calls)} sample→species entries")
    print(f"[INFO] Loaded {len(species_queries)} query species names")

    all_matches = []
    for q in species_queries:
        matches = find_samples_by_species(species_calls, q, inclusive_words=args.inclusive_words)
        print(f"[INFO] Query '{q}' → found {len(matches)} matches")
        all_matches.extend(matches)

    # Deduplicate (if same sample matched from multiple queries)
    unique = {}
    for sid, sp in all_matches:
        unique[sid] = sp
    match_list = list(unique.items())

    write_matches(Path(args.output), match_list, header=["Sample", "Species"])
    print(f"[DONE] Written {len(match_list)} unique matches to {args.output}")

if __name__ == "__main__":
    main()
