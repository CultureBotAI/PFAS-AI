#!/usr/bin/env python3
import argparse
import csv
import gzip
import tarfile
import urllib.request
import re
import hashlib
import time
from pathlib import Path
from typing import Dict, Set, List

import pandas as pd

def download_file(url: str, dest: Path, retries: int = 3, backoff: float = 1.0):
    dest.parent.mkdir(parents=True, exist_ok=True)
    if dest.exists():
        print(f"[INFO] {dest} exists, skipping")
        return
    tmp = dest.with_suffix(dest.suffix + ".part")
    headers = {"User-Agent": "atb-fetch/1.0 (+https://github.com/)"}
    for attempt in range(1, retries + 1):
        try:
            print(f"[INFO] Downloading {url} -> {tmp} (attempt {attempt})")
            req = urllib.request.Request(url, headers=headers)
            with urllib.request.urlopen(req, timeout=120) as r:
                cl = r.getheader("Content-Length")
                with open(tmp, "wb") as f:
                    while True:
                        chunk = r.read(1024 * 1024)
                        if not chunk:
                            break
                        f.write(chunk)
            # basic sanity checks
            if tmp.exists() and tmp.stat().st_size == 0:
                raise IOError("Downloaded file has size 0")
            # if Content-Length provided, check it
            if cl and tmp.exists():
                try:
                    expected = int(cl)
                    got = tmp.stat().st_size
                    if got != expected:
                        print(f"[WARN] size mismatch: expected {expected}, got {got}")
                except Exception:
                    pass
            tmp.replace(dest)
            print(f"[INFO] Saved {dest}")
            return
        except Exception as e:
            print(f"[WARN] download attempt {attempt} failed: {e}")
            if tmp.exists():
                try:
                    tmp.unlink()
                except Exception:
                    pass
            if attempt < retries:
                time.sleep(backoff * attempt)
            else:
                raise

def parse_status_file(status_path: Path) -> Dict[str, Dict[str, str]]:
    """Parse atb.bakta.*.status.tsv.gz.

    Supports two formats:
      - tabular rows where a column contains SAMNxxxxx, status, filename, tarball
      - legacy key/value blocks separated by blank lines (one sample per block)
    Returns records keyed by sample id with minimal fields: sample, status, file_name, tar_xz (when available).
    """
    records: Dict[str, Dict[str, str]] = {}
    with gzip.open(status_path, "rt", encoding="utf-8", errors="replace") as f:
        lines = [l.rstrip("\n") for l in f]

    non_empty = [l for l in lines if l.strip()]
    # Heuristic: treat as table if many lines have multiple whitespace-separated columns
    n_multi = sum(1 for l in non_empty if len(re.split(r"\s+", l.strip())) >= 3)
    if n_multi >= max(3, int(0.05 * max(1, len(non_empty)))):
        for raw in non_empty:
            cols = raw.split("\t") if "\t" in raw else re.split(r"\s+", raw.strip())
            # find SAMN pattern in any column (accept forms like "2:SAMN123...")
            sid = None
            for c in cols:
                m = re.search(r"(SAMN\d+)", c)
                if m:
                    sid = m.group(1)
                    break
            if sid is None and ":" in cols[0]:
                part = cols[0].split(":", 1)[1]
                if re.match(r"SAMN\d+", part):
                    sid = part
            if not sid:
                continue

            status = None
            fname = None
            tar = None
            for c in cols:
                uc = c.upper()
                if uc in {"PASS", "FAIL", "ERROR", "SKIP"}:
                    status = c
                if c.endswith(".bakta.json") or ".bakta.json" in c:
                    fname = c
                # accept common tar names / extensions
                if c.endswith(".tar.xz") or c.endswith(".tar.gz") or c.endswith(".tar"):
                    tar = c
            rec: Dict[str, str] = {"sample": sid}
            if status:
                rec["status"] = status
            if fname:
                rec["file_name"] = fname
            if tar:
                rec["tar_xz"] = tar
            records[sid] = rec
        return records

    # Fallback: legacy key:value blocks (one sample per block)
    current: Dict[str, str] = {}
    for line in non_empty:
        # lines expected like: key<TAB>value
        if "\t" not in line:
            continue
        key, val = line.split("\t", 1)
        key = key.strip()
        val = val.strip()
        if key.lower() in {"sample", "sample_id", "sampleid"} or key.lower().startswith("sample"):
            # flush previous block if present
            if current.get("sample"):
                records[current["sample"]] = dict(current)
            current = {"sample": val}
        else:
            current[key] = val
    if current.get("sample"):
        records[current["sample"]] = dict(current)
    return records

def load_id_list(path: Path) -> List[str]:
    ids = []
    with path.open() as f:
        for line in f:
            s = line.strip()
            if not s or s.startswith("#"):
                continue
            ids.append(s)
    return ids

def extract_jsons_from_tar(tar_path: Path, json_names: Set[str], out_dir: Path,
                           retry_download: bool = True) -> List[Path]:
    out_dir.mkdir(parents=True, exist_ok=True)
    extracted: List[Path] = []

    def _try_extract(path: Path) -> List[Path]:
        local_extracted: List[Path] = []
        try:
            with tarfile.open(path, mode="r:*") as tar:
                members = tar.getmembers()
                # maps for fast lookup
                full_map = {m.name: m for m in members}
                basename_map = {}
                for m in members:
                    b = Path(m.name).name
                    basename_map.setdefault(b, []).append(m)

                for j in sorted(json_names):
                    m = full_map.get(j)
                    if not m:
                        cands = basename_map.get(j)
                        if cands:
                            m = cands[0]
                    if not m:
                        sid_match = re.search(r"(SAMN\d+)", j)
                        if sid_match:
                            sid = sid_match.group(1)
                            for cand in members:
                                if sid in cand.name and (cand.name.endswith(".bakta.json") or cand.name.endswith(".bakta.json.gz") or cand.name.endswith(".json") or cand.name.endswith(".json.gz")):
                                    m = cand
                                    break
                    if not m:
                        print(f"[WARN] {j} not found in {tar_path.name}. Available members (sample of 20):")
                        for name in list(full_map.keys())[:20]:
                            print("  ", name)
                        continue

                    tar.extract(m, path=out_dir)
                    extracted_path = out_dir / m.name
                    if extracted_path.exists() and extracted_path.parent != out_dir:
                        target = out_dir / Path(m.name).name
                        try:
                            extracted_path.replace(target)
                            extracted_path = target
                        except Exception:
                            pass

                    if extracted_path.suffix == ".gz":
                        try:
                            import gzip as _gz
                            target_path = extracted_path.with_suffix("")  # remove .gz
                            with _gz.open(extracted_path, "rb") as fin, open(target_path, "wb") as fout:
                                fout.write(fin.read())
                            extracted_path.unlink(missing_ok=True)
                            extracted_path = target_path
                        except Exception as e:
                            print(f"[WARN] failed to decompress {extracted_path}: {e}")

                    local_extracted.append(extracted_path)
        except (tarfile.ReadError, EOFError) as e:
            raise e
        return local_extracted

    # attempt extraction, if tar is corrupt optionally try redownloading once
    try:
        extracted = _try_extract(tar_path)
        return extracted
    except (tarfile.ReadError, EOFError) as e:
        print(f"[ERROR] Tar read failed for {tar_path}: {e}")
        if retry_download:
            print(f"[INFO] Will attempt to re-download {tar_path.name} and retry extraction")
            # try to find tar URL from DataFrame context is not available here;
            # caller should re-download tar before calling again, but we attempt best-effort:
            # if tar_path has a .url companion (not implemented), skip automated re-download here.
            # For now, remove corrupt file and return empty so caller can re-download.
            try:
                tar_path.unlink(missing_ok=True)
            except Exception:
                pass
        return []
def main():
    p = argparse.ArgumentParser(description="Fetch Bakta JSONs from AllTheBacteria using your all_atb_files.tsv")
    p.add_argument("--all-atb-tsv", default="all_atb_files.tsv",
                   help="Path to all_atb_files.tsv (local file you provided)")
    p.add_argument("--release", choices=["r0.2","incr_release.202408"], default=None,
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
    df = pd.read_csv(all_tsv, sep="\t")

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

    # Choose the first match (there should be 1 for a specific release)
    status_filename = status_rows.iloc[0]["filename"]
    status_url = status_rows.iloc[0]["url"]
    print(f"[INFO] Using status file: {status_filename}")
    print(f"[INFO] URL: {status_url}")

    workdir = Path(args.workdir)
    workdir.mkdir(parents=True, exist_ok=True)
    status_local = workdir / Path(status_filename).name
    if not status_local.exists():
        download_file(status_url, status_local)

    # Parse status file -> records keyed by sample
    records = parse_status_file(status_local)
    print(f"[INFO] Parsed {len(records)} sample records")

    # Load your sample list
    samples = load_id_list(Path(args.samples))
    print(f"[INFO] Loaded {len(samples)} requested samples")

    # Map sample -> tar_xz & file_name
    tar_to_jsons: Dict[str, Set[str]] = {}
    missing, nonpass = [], []
    for sid in samples:
        rec = records.get(sid)
        if not rec:
            missing.append(sid); continue
        if rec.get("status") != "PASS":
            nonpass.append(sid); continue
        tar = rec.get("tar_xz"); fname = rec.get("file_name")
        if tar and fname:
            tar_to_jsons.setdefault(tar, set()).add(fname)

    print(f"[INFO] Need {len(tar_to_jsons)} tarball(s)")
    if missing:
        print(f"[WARN] {len(missing)} samples missing from status: first few {missing[:5]}")
    if nonpass:
        print(f"[WARN] {len(nonpass)} samples with non-PASS status: first few {nonpass[:5]}")

    # Download required tarballs and extract requested JSONs
    tar_dir = workdir / "tarballs"; tar_dir.mkdir(exist_ok=True)
    extracted: List[Path] = []

    for tar_name, jsonset in tar_to_jsons.items():
        # find URL for this tarball in all_atb_files.tsv
        match = bakta_df[bakta_df["filename"].str.endswith(tar_name)]
        if match.empty:
            print(f"[ERROR] Tarball URL not found for {tar_name} in your TSV; skipping")
            continue
        tar_url = match.iloc[0]["url"]
        tar_local = tar_dir / tar_name
        if not tar_local.exists():
            download_file(tar_url, tar_local)
        extracted += extract_jsons_from_tar(tar_local, jsonset, Path(args.json_out))

    print(f"[DONE] Extracted {len(extracted)} JSON(s) to {args.json_out}")

if __name__ == "__main__":
    main()
