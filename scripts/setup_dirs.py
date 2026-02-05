#!/usr/bin/env python3
from __future__ import annotations

import argparse
from pathlib import Path


DEFAULT_DIRS = [
    "data/raw",
    "data/processed",
    "predictions",
    "analysis/metrics",
    "analysis/failure_cases",
    "analysis/features",
    "reports/github_issues",
]


def create_directories(root: Path, paths: list[str]) -> None:
    for relative in paths:
        path = root / relative
        path.mkdir(parents=True, exist_ok=True)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Create the directory scaffold for the pLDDT failure atlas project."
    )
    parser.add_argument(
        "--root",
        default=".",
        help="Root directory for the project scaffold (default: current directory).",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    root = Path(args.root).resolve()
    create_directories(root, DEFAULT_DIRS)
    print(f"Created directory scaffold under {root}")


if __name__ == "__main__":
    main()
