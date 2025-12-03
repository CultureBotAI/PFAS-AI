#!/usr/bin/env python3
import argparse
import csv
from pathlib import Path

def load_species_calls(path: Path, sample_col: str = "Sample", species_col: str = "Species") -> dict:
    d = {}
    with path.open("r", encoding="utf-8", errors="replace") as f:
        reader = csv.DictReader(f, delimiter="\t")
        for row in reader:
            sid = row.get(sample_col)
            sp = row.get(species_col)
            if sid is None or sp is None:
                continue
            d[sid.strip()] = sp.strip()
    return d

def write_unique_by_species(species_calls: dict, output_path: Path):
    seen = {}
    for sid, sp in species_calls.items():
        # only keep first seen sample for each species
        if sp not in seen:
            seen[sp] = sid
    # now output species + sample
    with output_path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f, delimiter="\t", lineterminator="\n")
        writer.writerow(["Species", "Sample"])
        for sp, sid in seen.items():
            writer.writerow([sp, sid])

def main():
    parser = argparse.ArgumentParser(description="Export one sample per unique species from species calls file")
    parser.add_argument("--species-calls", required=True, help="TSV file with Sample & Species columns")
    parser.add_argument("--sample-col", default="Sample", help="Column name for sample in species-calls file")
    parser.add_argument("--species-col", default="Species", help="Column name for species in species-calls file")
    parser.add_argument("--output", required=True, help="Output TSV listing unique species + sample")
    args = parser.parse_args()

    species_calls = load_species_calls(Path(args.species_calls), sample_col=args.sample_col, species_col=args.species_col)
    print(f"[INFO] Loaded {len(species_calls)} sample→species entries")
    write_unique_by_species(species_calls, Path(args.output))
    print(f"[DONE] Written {args.output} containing {len(set(species_calls.values()))} unique species.")

if __name__ == "__main__":
    main()
