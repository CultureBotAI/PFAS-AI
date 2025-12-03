#!/usr/bin/env python3
import gzip
import argparse
from pathlib import Path
import re
import csv

def parse_status_file(status_path: Path):
    """
    Parse status file. Supports two formats:
      - key/value blocks separated by blank lines (legacy)
      - tabular rows where one column contains a SAMNxxxxx sample id

    Returns dict keyed by sample id with a minimal dict value (parsed keys for block
    format, or 'columns' list + 'raw' for tabular rows).
    """
    records = {}
    with gzip.open(status_path, "rt", encoding="utf-8", errors="replace") as f:
        lines = f.read().splitlines()

    # Heuristic: if many non-empty lines contain tabs / multiple columns -> tabular file
    non_empty = [l for l in lines if l.strip()]
    n_tab_lines = sum(1 for l in non_empty if "\t" in l)
    if n_tab_lines >= max(3, int(0.05 * max(1, len(non_empty)))):
        # parse as table-like file
        for raw in non_empty:
            # use TSV splitting if present, else split on runs of whitespace
            cols = raw.split("\t") if "\t" in raw else re.split(r"\s+", raw)
            # find SAMN pattern in any column
            sid = None
            for c in cols:
                m = re.search(r"(SAMN\d+)", c)
                if m:
                    sid = m.group(1)
                    break
            # also accept "N:SID" first-col pattern like "2:SAMN123..."
            if sid is None and ":" in cols[0]:
                part = cols[0].split(":", 1)[1]
                if re.match(r"SAMN\d+", part):
                    sid = part
            if not sid:
                continue
            # store useful fields: keep columns and raw line for downstream logic
            records[sid] = {"columns": cols, "raw": raw}
        return records

    # Fallback: parse legacy key:value blocks (existing logic, more tolerant)
    current = {}

    def split_kv(line: str):
        # accept tab, colon, equals, or first whitespace as separator
        if "\t" in line:
            return line.split("\t", 1)
        if ":" in line:
            return line.split(":", 1)
        if "=" in line:
            return line.split("=", 1)
        parts = line.split(None, 1)
        if len(parts) == 2:
            return parts
        return (line, "")

    for i, raw in enumerate(lines):
        line = raw.strip()
        if not line:
            if current.get("sample"):
                sid = current["sample"].strip()
                records[sid] = current.copy()
            current = {}
            continue
        # skip lines that don't look like key/value after trying to split
        if not any(sep in raw for sep in ("\t", ":", "=", " ")):
            continue

        key, val = split_kv(raw)
        key = key.strip().lower()
        val = val.strip()

        # normalize key variants that refer to sample id
        if key in {"sample", "sample_id", "sampleid", "sample id"} or key.startswith("sample"):
            # flush previous if any
            if current.get("sample"):
                sid = current["sample"].strip()
                records[sid] = current.copy()
            current = {"sample": val}
        else:
            current[key] = val

    # final flush
    if current.get("sample"):
        sid = current["sample"].strip()
        records[sid] = current.copy()
    return records

def load_samples(fname: Path):
    samples = []
    for line in fname.read_text(encoding="utf-8", errors="replace").splitlines():
        s = line.strip()
        if not s or s.startswith("#"):
            continue
        samples.append(s)
    return samples

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--status-file", required=True)
    parser.add_argument("--samples", required=True)
    args = parser.parse_args()
    status_path = Path(args.status_file)
    if not status_path.exists():
        raise SystemExit(f"[ERROR] File not found: {status_path}")
    records = parse_status_file(status_path)
    print(f"[INFO] Parsed {len(records)} sample entries")
    print(f"[DEBUG] first 10 sample keys: {list(records.keys())[:10]}")
    sample_list = load_samples(Path(args.samples))
    print(f"[INFO] Loaded {len(sample_list)} requested sample IDs")

    missing = []
    found = []
    for s in sample_list:
        if s in records:
            found.append(s)
        else:
            missing.append(s)
    print(f"[RESULT] Found {len(found)}, missing {len(missing)}")
    if missing:
        print("[WARN] missing:", missing[:10])
    if found:
        print("[INFO] found samples:", found[:10])

if __name__ == "__main__":
    main()
