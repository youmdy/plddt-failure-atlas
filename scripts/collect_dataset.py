#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
from pathlib import Path


DEFAULT_HEADERS = ["protein_id", "sequence", "reference_plddt"]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Prepare a normalized manifest for pLDDT comparison."
    )
    parser.add_argument(
        "--input-manifest",
        default="data/raw/manifest.csv",
        help="Path to the raw manifest CSV (default: data/raw/manifest.csv).",
    )
    parser.add_argument(
        "--output-manifest",
        default="data/processed/manifest.csv",
        help="Path to write the normalized manifest (default: data/processed/manifest.csv).",
    )
    return parser.parse_args()


def ensure_manifest(path: Path) -> None:
    if path.exists():
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        writer.writerow(DEFAULT_HEADERS)
        writer.writerow(["example_protein", "MSEQVENCE", "85.0"])


def normalize_manifest(input_path: Path, output_path: Path) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with input_path.open("r", newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        rows = list(reader)

    with output_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=DEFAULT_HEADERS)
        writer.writeheader()
        for row in rows:
            normalized = {header: row.get(header, "").strip() for header in DEFAULT_HEADERS}
            writer.writerow(normalized)


def main() -> None:
    args = parse_args()
    input_path = Path(args.input_manifest)
    output_path = Path(args.output_manifest)
    ensure_manifest(input_path)
    normalize_manifest(input_path, output_path)
    print(f"Wrote normalized manifest to {output_path}")


if __name__ == "__main__":
    main()
