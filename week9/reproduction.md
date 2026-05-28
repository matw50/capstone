# Week 9 Reproduction

## Inputs
- Accumulated data through `week8`
- Week 8 diagnostics: `reports/week8_diagnostics/progress_diagnostics.md`
- Week 8 backtest: `reports/week8_backtest/state_policy_backtest.md`
- Raw candidate file: `week9/candidates.json`
- Final submitted inputs: `week9/inputs.json`

## Steps
1. Generate raw candidates:

```bash
/opt/anaconda3/bin/python scripts/generate_candidate_queries.py \
  --repo-root . \
  --through-week week8 \
  --output-file week9/candidates.json \
  --seed 42 \
  --policy-variant state
```

2. Run sanity checks on the raw candidates:

```bash
/opt/anaconda3/bin/python scripts/sanity_check_candidates.py \
  --repo-root . \
  --through-week week8 \
  --candidate-file week9/candidates.json
```

3. Run classifier and neural-network secondary checks on the raw candidates:

```bash
/opt/anaconda3/bin/python scripts/classifier_region_check.py \
  --repo-root . \
  --through-week week8 \
  --candidate-file week9/candidates.json \
  --svm

/opt/anaconda3/bin/python scripts/neural_net_surrogate_check.py \
  --repo-root . \
  --through-week week8 \
  --candidate-file week9/candidates.json
```

4. Apply the manual blending rule:
- momentum functions get smaller continuation moves
- stagnant functions may compare one bounded alternative against local refinement
- refine functions return toward the historical best
- recovery functions stay tightly anchored on the best observed basin
- classifier and neural-network checks do not override geometric and basin-aware checks

5. Save the final submission in `week9/inputs.json` and `week9/submission.txt`.

6. Run final checks on the submitted inputs:

```bash
/opt/anaconda3/bin/python scripts/sanity_check_candidates.py \
  --repo-root . \
  --through-week week8 \
  --candidate-file week9/inputs.json

/opt/anaconda3/bin/python scripts/classifier_region_check.py \
  --repo-root . \
  --through-week week8 \
  --candidate-file week9/inputs.json \
  --svm

/opt/anaconda3/bin/python scripts/neural_net_surrogate_check.py \
  --repo-root . \
  --through-week week8 \
  --candidate-file week9/inputs.json
```

7. After results return, record `outputs.json`, `results.json`, and appended `.npy` files.
