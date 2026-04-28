# Week 8 Reproduction

## Inputs
- Accumulated data through `week7`
- Week 7 progress diagnostic: `reports/week7_diagnostics/progress_diagnostics.md`
- Week 7 state-policy backtest: `reports/week7_backtest/state_policy_backtest.md`
- Raw candidate file: `week8/candidates.json`
- Final blended submission: `week8/inputs.json`

## Steps
1. Generate raw candidates using the state-policy generator:

```bash
/opt/anaconda3/bin/python scripts/generate_candidate_queries.py \
  --repo-root . \
  --through-week week7 \
  --output-file week8/candidates.json \
  --seed 42 \
  --policy-variant state
```

2. Run the historical backtest to decide how much to trust raw generated coordinates:

```bash
/opt/anaconda3/bin/python scripts/backtest_state_policy.py \
  --repo-root . \
  --from-week week1 \
  --through-week week7 \
  --output-dir reports/week7_backtest
```

3. Run sanity checks on the raw candidates:

```bash
/opt/anaconda3/bin/python scripts/sanity_check_candidates.py \
  --repo-root . \
  --through-week week7 \
  --candidate-file week8/candidates.json
```

4. Run classifier and neural-network secondary checks on the raw candidates:

```bash
/opt/anaconda3/bin/python scripts/classifier_region_check.py \
  --repo-root . \
  --through-week week7 \
  --candidate-file week8/candidates.json \
  --svm

/opt/anaconda3/bin/python scripts/neural_net_surrogate_check.py \
  --repo-root . \
  --through-week week7 \
  --candidate-file week8/candidates.json
```

5. Apply the systematic manual blending rule:
- keep state labels from the generator
- if latest query improved, continue with a smaller move along the proven trajectory
- if latest query did not improve, anchor on the historical best and make a very small corrective move
- if the raw candidate makes a wider move than recent successful submissions, clip it back toward the proven basin
- do not let classifier or neural-network checks override geometric and basin-aware checks

6. Save the final blended submission in `week8/inputs.json` and `week8/submission.txt`.

7. Run final checks on `week8/inputs.json`:

```bash
/opt/anaconda3/bin/python scripts/sanity_check_candidates.py \
  --repo-root . \
  --through-week week7 \
  --candidate-file week8/inputs.json

/opt/anaconda3/bin/python scripts/classifier_region_check.py \
  --repo-root . \
  --through-week week7 \
  --candidate-file week8/inputs.json \
  --svm

/opt/anaconda3/bin/python scripts/neural_net_surrogate_check.py \
  --repo-root . \
  --through-week week7 \
  --candidate-file week8/inputs.json
```

8. After results return, record `outputs.json`, `results.json`, and appended `.npy` files.
