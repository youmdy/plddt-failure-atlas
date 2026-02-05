#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
from pathlib import Path


ISSUE_TEMPLATE = """## Summary
High-error pLDDT prediction for `{protein_id}`.

## Evidence
- Reference pLDDT: {reference_plddt}
- Predicted pLDDT: {predicted_plddt}
- Error: {error}

## Observed features
- Sequence length: {sequence_length}
- Glycine fraction: {glycine_fraction}
- Contains cysteine: {has_cysteine}

## Reproduction
1. Use the manifest entry for `{protein_id}` from `data/processed/manifest.csv`.
2. Run the prediction and analysis pipeline.
3. Confirm the error exceeds the failure threshold.
"""


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Generate GitHub issue drafts for failure cases."
    )
    parser.add_argument(
        "--failures",
        default="analysis/failure_cases/failures.csv",
        help="Path to the failure cases CSV.",
    )
    parser.add_argument(
        "--features",
        default="analysis/features/features.csv",
        help="Path to the extracted features CSV.",
    )
    parser.add_argument(
        "--output-dir",
        default="reports/github_issues",
        help="Directory to write markdown issue drafts.",
    )
    return parser.parse_args()


def load_features(path: Path) -> dict[str, dict[str, str]]:
    with path.open("r", newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        return {row["protein_id"]: row for row in reader}


def main() -> None:
    args = parse_args()
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    features = load_features(Path(args.features))

    with Path(args.failures).open("r", newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        for row in reader:
            protein_id = row["protein_id"]
            feature_row = features.get(
                protein_id,
                {
                    "sequence_length": "unknown",
                    "glycine_fraction": "unknown",
                    "has_cysteine": "unknown",
                },
            )
            body = ISSUE_TEMPLATE.format(**row, **feature_row)
            issue_path = output_dir / f"{protein_id}.md"
            issue_path.write_text(body, encoding="utf-8")

    print(f"Wrote issue drafts to {output_dir}")


if __name__ == "__main__":
    main()
