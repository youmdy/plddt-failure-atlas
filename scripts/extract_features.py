#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
from pathlib import Path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Extract simple structural features from the manifest."
    )
    parser.add_argument(
        "--manifest",
        default="data/processed/manifest.csv",
        help="Path to the processed manifest CSV.",
    )
    parser.add_argument(
        "--output",
        default="analysis/features/features.csv",
        help="Path to write the extracted features.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with Path(args.manifest).open("r", newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        rows = list(reader)

    with output_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        writer.writerow(["protein_id", "sequence_length", "glycine_fraction", "has_cysteine"])
        for row in rows:
            sequence = (row.get("sequence") or "").strip()
            length = len(sequence)
            glycine_fraction = (sequence.count("G") / length) if length else 0.0
            has_cysteine = "yes" if "C" in sequence else "no"
            writer.writerow(
                [row.get("protein_id", "").strip(), length, f"{glycine_fraction:.3f}", has_cysteine]
            )

    print(f"Wrote features to {output_path}")


if __name__ == "__main__":
    main()
