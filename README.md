# plddt-failure-atlas
Mining failure modes in pLDDT prediction and reporting reproducible breakcases to upstream developers

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
