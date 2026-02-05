#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import random
from pathlib import Path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Generate placeholder pLDDT predictions for the manifest."
    )
    parser.add_argument(
        "--manifest",
        default="data/processed/manifest.csv",
        help="Path to the processed manifest CSV (default: data/processed/manifest.csv).",
    )
    parser.add_argument(
        "--output",
        default="predictions/predictions.csv",
        help="Path to write predictions (default: predictions/predictions.csv).",
    )
    parser.add_argument(
        "--seed",
        type=int,
        default=17,
        help="Random seed for deterministic placeholder predictions.",
    )
    parser.add_argument(
        "--noise",
        type=float,
        default=5.0,
        help="Noise scale applied to reference pLDDT (default: 5.0).",
    )
    return parser.parse_args()


def safe_float(value: str) -> float | None:
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def main() -> None:
    args = parse_args()
    manifest_path = Path(args.manifest)
    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    rng = random.Random(args.seed)

    with manifest_path.open("r", newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        rows = list(reader)

    with output_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        writer.writerow(["protein_id", "predicted_plddt"])
        for row in rows:
            reference = safe_float(row.get("reference_plddt", ""))
            if reference is None:
                prediction = 0.0
            else:
                prediction = max(0.0, min(100.0, reference + rng.uniform(-args.noise, args.noise)))
            writer.writerow([row.get("protein_id", "").strip(), f"{prediction:.2f}"])

    print(f"Wrote predictions to {output_path}")


if __name__ == "__main__":
    main()
