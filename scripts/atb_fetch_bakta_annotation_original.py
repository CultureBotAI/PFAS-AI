#!/usr/bin/env python3
import argparse
import csv
import gzip
import tarfile
import urllib.request
from pathlib import Path
from typing import Dict, Set, List
import pandas as pd

def download_file(url: str, dest: Path):
    dest.parent.mkdir(parents=True, exist_ok=True)
    if dest.exists():
        print(f"[INFO] {dest} exists, skipping")
        return
    print(f"[INFO] Downloading {url} -> {dest}")
    with urllib.request.urlopen(url) as r, open(dest, "wb") as f:
        while True:
            chunk = r.read(1024 * 1024)
            if not chunk:
                break
            f.write(chunk)

def parse_status_file(status_path: Path) -> Dict[str, Dict[str, str]]:
    """Parse status.tsv.gz where each line is one sample record (tab-separated)."""
    records: Dict[str, Dict[str, str]] = {}
    with gzip.open(status_path, "rt", encoding="utf-8", errors="replace") as f:
        header_line = f.readline().rstrip("\n")
        header = header_line.split("\t")
        try:
            idx_sample = header.index("sample")
        except ValueError:
            raise SystemExit(f"[ERROR] 'sample' column not found in header: {header}")
        for line in f:
            parts = line.rstrip("\n").split("\t")
            if len(parts) <= idx_sample:
                continue
            sid = parts[idx_sample].strip()
            if not sid:
                continue
            rec: Dict[str, str] = {}
            for i, col in enumerate(header):
                rec[col] = parts[i].strip() if i < len(parts) else ""
            records[sid] = rec
    return records

def load_id_list(path: Path) -> List[str]:
    ids = []
    with path.open("r", encoding="utf-8", errors="replace") as f:
        for line in f:
            s = line.strip()
            if not s or s.startswith("#"):
                continue
            ids.append(s)
    return ids

def extract_jsons_from_tar(tar_path: Path, json_names: Set[str], out_dir: Path) -> List[Path]:
    out_dir.mkdir(parents=True, exist_ok=True)
    extracted: List[Path] = []
    with tarfile.open(tar_path, mode="r:xz") as tar:
        members = {m.name: m for m in tar.getmembers()}
        for j in sorted(json_names):
            m = members.get(j)
            if not m:
                print(f"[WARN] {j} not found in {tar_path.name}")
                continue
            tar.extract(m, path=out_dir)
            extracted.append(out_dir / m.name)
    return extracted

def main():
    p = argparse.ArgumentParser(description="Fetch Bakta JSONs from AllTheBacteria using your all_atb_files.tsv")
    p.add_argument("--all-atb-tsv", default="all_atb_files.tsv",
                   help="Path to all_atb_files.tsv (local file you provided)")
    p.add_argument("--release", choices=["r0.2", "incr_release.202408"], default=None,
                   help="Pick a specific status file; if omitted, auto-pick first found")
    p.add_argument("--samples", required=True,
                   help="Text file with sample IDs (SAMN…); one per line")
    p.add_argument("--workdir", default="atb_work", help="Working directory")
    p.add_argument("--json-out", default="bakta_json", help="Where to put extracted *.bakta.json")
    args = p.parse_args()

    all_tsv = Path(args.all_atb_tsv)
    if not all_tsv.exists():
        raise SystemExit(f"[ERROR] {all_tsv} not found; point --all-atb-tsv to your local file")

    # Read your TSV
    df = pd.read_csv(all_tsv, sep="\t", dtype=str, encoding="utf-8", engine='python')

    # Find the status file row
    bakta_df = df[df["project"].str.contains("Annotation/Bakta", na=False)]
    status_rows = bakta_df[bakta_df["filename"].str.contains("status.tsv.gz", na=False)].copy()

    # Optionally filter by release
    if args.release:
        if args.release == "r0.2":
            status_rows = status_rows[status_rows["filename"].str.contains("r0.2", na=False)]
        elif args.release == "incr_release.202408":
            status_rows = status_rows[status_rows["filename"].str.contains("incr_release.202408", na=False)]

    if status_rows.empty:
        raise SystemExit("[ERROR] No Bakta status file matched in your all_atb_files.tsv")

    status_filename = status_rows.iloc[0]["filename"]
    status_url      = status_rows.iloc[0]["url"]
    print(f"[INFO] Using status file: {status_filename}")
    print(f"[INFO] URL: {status_url}")

    workdir = Path(args.workdir)
    workdir.mkdir(parents=True, exist_ok=True)
    status_local = workdir / Path(status_filename).name
    if not status_local.exists():
        download_file(status_url, status_local)

    # Parse status file → records keyed by sample
    records = parse_status_file(status_local)
    print(f"[INFO] Parsed {len(records)} sample records")

    # Load your sample list
    samples = load_id_list(Path(args.samples))
    print(f"[INFO] Loaded {len(samples)} requested samples")

    # Map sample → tar_xz & file_name
    tar_to_jsons: Dict[str, Set[str]] = {}
    missing, nonpass = [], []
    for sid in samples:
        rec = records.get(sid)
        if not rec:
            missing.append(sid)
            continue
        if rec.get("status") != "PASS":
            nonpass.append(sid)
            continue
        tar = rec.get("tar_xz")
        fname = rec.get("file_name")
        if tar and fname:
            tar_to_jsons.setdefault(tar, set()).add(fname)

    print(f"[INFO] Need {len(tar_to_jsons)} tarball(s)")
    if missing:
        print(f"[WARN] {len(missing)} samples missing from status: first few {missing[:5]}")
    if nonpass:
        print(f"[WARN] {len(nonpass)} samples with non-PASS status: first few {nonpass[:5]}")

    # Download required tarballs and extract requested JSONs
    tar_dir = workdir / "tarballs"
    tar_dir.mkdir(exist_ok=True)
    extracted: List[Path] = []

    for tar_name, jsonset in tar_to_jsons.items():
        match = bakta_df[bakta_df["filename"].str.endswith(tar_name)]
        if match.empty:
            print(f"[ERROR] Tarball URL not found for {tar_name} in your TSV; skipping")
            continue
        tar_url   = match.iloc[0]["url"]
        tar_local = tar_dir / tar_name
        if not tar_local.exists():
            download_file(tar_url, tar_local)
        extracted += extract_jsons_from_tar(tar_local, jsonset, Path(args.json_out))

    print(f"[DONE] Extracted {len(extracted)} JSON(s) to {args.json_out}")

if __name__ == "__main__":
    main()
