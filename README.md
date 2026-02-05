# plddt-failure-atlas
Mining failure modes in pLDDT prediction and reporting reproducible breakcases to upstream developers.

## Project goals
- Predict known pLDDT values and compare them to model outputs to collect failure cases.
- Identify shared characteristics among structures that the model frequently misses to surface weaknesses.
- Package reproducible failures and report them to upstream developers via GitHub issues.

## Draft plan
1. **Dataset collection**: Gather public pLDDT labels and structure data.
2. **Model prediction**: Predict pLDDT on the same inputs and compare against reference values.
3. **Error analysis**: Analyze error distributions and cluster failure cases.
4. **Feature extraction**: Summarize traits such as secondary structure, length, domain splits, and multichain status.
5. **Reporting**: Share reproducible cases and analysis summaries through GitHub issues.

## Implementation scaffold
The repository includes lightweight scripts to stand up the analysis flow end-to-end:

```bash
python scripts/setup_dirs.py
python scripts/collect_dataset.py
python scripts/predict_plddt.py
python scripts/analyze_errors.py
python scripts/extract_features.py
python scripts/generate_issue_reports.py
```

### Inputs
- `data/raw/manifest.csv` contains `protein_id`, `sequence`, and `reference_plddt`.
- `scripts/collect_dataset.py` will create a starter manifest if none exists.

### Outputs
- `predictions/predictions.csv` contains placeholder pLDDT predictions.
- `analysis/metrics/summary.json` stores basic error metrics.
- `analysis/failure_cases/failures.csv` lists high-error samples.
- `analysis/features/features.csv` stores derived features.
- `reports/github_issues/` contains draft GitHub issue markdown files.
