#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Analyze prediction errors and extract failure cases."
    )
    parser.add_argument(
        "--manifest",
        default="data/processed/manifest.csv",
        help="Path to the processed manifest CSV.",
    )
    parser.add_argument(
        "--predictions",
        default="predictions/predictions.csv",
        help="Path to the predictions CSV.",
    )
    parser.add_argument(
        "--threshold",
        type=float,
        default=10.0,
        help="Absolute error threshold for defining a failure case.",
    )
    parser.add_argument(
        "--summary",
        default="analysis/metrics/summary.json",
        help="Path to write the metrics summary JSON.",
    )
    parser.add_argument(
        "--failures",
        default="analysis/failure_cases/failures.csv",
        help="Path to write the failure cases CSV.",
    )
    return parser.parse_args()


def safe_float(value: str) -> float | None:
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def load_predictions(path: Path) -> dict[str, float]:
    with path.open("r", newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        return {
            row.get("protein_id", "").strip(): safe_float(row.get("predicted_plddt", ""))
            for row in reader
        }


def main() -> None:
    args = parse_args()
    predictions = load_predictions(Path(args.predictions))

    failures = []
    errors = []

    with Path(args.manifest).open("r", newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        for row in reader:
            protein_id = row.get("protein_id", "").strip()
            reference = safe_float(row.get("reference_plddt", ""))
            prediction = predictions.get(protein_id)
            if reference is None or prediction is None:
                continue
            error = prediction - reference
            errors.append(abs(error))
            if abs(error) >= args.threshold:
                failures.append(
                    {
                        "protein_id": protein_id,
                        "reference_plddt": f"{reference:.2f}",
                        "predicted_plddt": f"{prediction:.2f}",
                        "error": f"{error:.2f}",
                    }
                )

    summary = {
        "num_samples": len(errors),
        "num_failures": len(failures),
        "failure_rate": (len(failures) / len(errors)) if errors else 0.0,
        "mean_abs_error": (sum(errors) / len(errors)) if errors else 0.0,
        "threshold": args.threshold,
    }

    summary_path = Path(args.summary)
    summary_path.parent.mkdir(parents=True, exist_ok=True)
    summary_path.write_text(json.dumps(summary, indent=2), encoding="utf-8")

    failures_path = Path(args.failures)
    failures_path.parent.mkdir(parents=True, exist_ok=True)
    with failures_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(
            handle, fieldnames=["protein_id", "reference_plddt", "predicted_plddt", "error"]
        )
        writer.writeheader()
        writer.writerows(failures)

    print(f"Wrote summary to {summary_path}")
    print(f"Wrote {len(failures)} failure cases to {failures_path}")


if __name__ == "__main__":
    main()
