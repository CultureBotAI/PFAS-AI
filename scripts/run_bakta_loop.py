#!/usr/bin/env python3
import argparse
import subprocess
from pathlib import Path

def load_samples_list(path: Path) -> set:
    """Load a set of sample IDs (one per line) from a text file."""
    sids = set()
    with path.open("r", encoding="utf-8", errors="replace") as f:
        for line in f:
            sid = line.strip()
            if not sid or sid.startswith("#"):
                continue
            sids.add(sid)
    return sids

def main():
    parser = argparse.ArgumentParser(
        description="Run bakta_io only on selected samples listed in a query file")
    parser.add_argument("--samples-file", required=True,
                        help="Text file containing sample IDs (one per line) to process")
    parser.add_argument("--json-dir", required=True,
                        help="Directory where *.bakta.json files live")
    parser.add_argument("--output-base", required=True,
                        help="Base directory where each sample’s output dir will go")
    parser.add_argument("--prefix-ext", default=".bakta",
                        help="Suffix to append to sample ID for prefix (default: .bakta)")
    parser.add_argument("--bakta-cmd", default="bakta_io",
                        help="Command to run bakta_io (path or command name)")
    parser.add_argument("--force", action="store_true",
                        help="If set, pass --force to bakta_io to overwrite existing output dirs")
    args = parser.parse_args()

    samples_to_run = load_samples_list(Path(args.samples_file))
    print(f"[INFO] Loaded {len(samples_to_run)} sample IDs to process")

    json_dir    = Path(args.json_dir)
    output_base = Path(args.output_base)
    prefix_ext  = args.prefix_ext
    bakta_cmd   = args.bakta_cmd
    do_force    = args.force

    if not json_dir.is_dir():
        raise SystemExit(f"[ERROR] JSON directory not found: {json_dir}")

    # For each sample in the list, check if JSON exists and run
    for sid in sorted(samples_to_run):
        json_path = json_dir / f"{sid}{prefix_ext}.json"
        if not json_path.exists():
            print(f"[WARN] JSON not found for sample {sid} → {json_path}")
            continue

        output_dir = output_base / sid
        output_dir.mkdir(parents=True, exist_ok=True)

        prefix = f"{sid}{prefix_ext}"
        cmd = [bakta_cmd, "--output", str(output_dir), "--prefix", prefix]
        if do_force:
            cmd.append("--force")
        cmd.append(str(json_path))

        print(f"[INFO] Running: {' '.join(cmd)}")
        try:
            subprocess.run(cmd, check=True)
            print(f"[SUCCESS] Completed sample {sid}")
        except subprocess.CalledProcessError as e:
            print(f"[ERROR] Failed sample {sid}: {e}")

    print("[DONE] All done.")

if __name__ == "__main__":
    main()
