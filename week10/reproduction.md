# Week 10 Reproduction

## Inputs
- Accumulated data through `week9`
- Week 9 diagnostics: `reports/week9_diagnostics/progress_diagnostics.md`
- Week 9 backtest: `reports/week9_backtest/state_policy_backtest.md`
- Raw candidate file: `week10/candidates.json`
- Final submitted inputs: `week10/inputs.json`

## Steps
1. Generate raw candidates:

```bash
/opt/anaconda3/bin/python scripts/generate_candidate_queries.py \
  --repo-root . \
  --through-week week9 \
  --output-file week10/candidates.json \
  --seed 42 \
  --policy-variant state
```

2. Run checks on raw candidates:

```bash
/opt/anaconda3/bin/python scripts/sanity_check_candidates.py \
  --repo-root . \
  --through-week week9 \
  --candidate-file week10/candidates.json

/opt/anaconda3/bin/python scripts/classifier_region_check.py \
  --repo-root . \
  --through-week week9 \
  --candidate-file week10/candidates.json \
  --svm

/opt/anaconda3/bin/python scripts/neural_net_surrogate_check.py \
  --repo-root . \
  --through-week week9 \
  --candidate-file week10/candidates.json
```

3. Apply the manual blending rule:
- momentum functions get smaller continuation moves
- recovery functions reset toward the historical best basin
- raw candidates are treated as signals, not automatic submissions
- classifier and neural-network checks do not override geometric and basin-aware checks

4. Save final submission in `week10/inputs.json` and `week10/submission.txt`.

5. Run final checks on the submitted inputs:

```bash
/opt/anaconda3/bin/python scripts/sanity_check_candidates.py \
  --repo-root . \
  --through-week week9 \
  --candidate-file week10/inputs.json

/opt/anaconda3/bin/python scripts/classifier_region_check.py \
  --repo-root . \
  --through-week week9 \
  --candidate-file week10/inputs.json \
  --svm

/opt/anaconda3/bin/python scripts/neural_net_surrogate_check.py \
  --repo-root . \
  --through-week week9 \
  --candidate-file week10/inputs.json
```

6. After results return, record `outputs.json`, `results.json`, and appended `.npy` files.
