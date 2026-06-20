# Week 11 Reproduction

## Inputs
- Accumulated capstone data through `week10`
- Raw generated candidate file: `week11/candidates.json`
- Final manually blended submission: `week11/inputs.json`

## Generate Raw Candidates
Run:

```bash
/opt/anaconda3/bin/python scripts/generate_candidate_queries.py \
  --repo-root . \
  --through-week week10 \
  --output-file week11/candidates.json \
  --seed 42 \
  --policy-variant state
```

## Run Pre-Submission Checks
Run the checks on the raw candidates:

```bash
/opt/anaconda3/bin/python scripts/sanity_check_candidates.py \
  --repo-root . \
  --through-week week10 \
  --candidate-file week11/candidates.json
```

```bash
/opt/anaconda3/bin/python scripts/classifier_region_check.py \
  --repo-root . \
  --through-week week10 \
  --candidate-file week11/candidates.json \
  --svm
```

```bash
/opt/anaconda3/bin/python scripts/neural_net_surrogate_check.py \
  --repo-root . \
  --through-week week10 \
  --candidate-file week11/candidates.json
```

## Manual Blending Rules
Apply the Week 10 diagnostic state labels:
- Functions 1, 4, 5, 7, and 8: momentum, so use tiny local continuation moves.
- Function 2: recovery, so reset very close to the Week 6 best basin.
- Functions 3 and 6: refine, so return close to the Week 9 best basins.

Then clip the raw candidates manually because the Week 10 backtest showed the raw generator remained wider than the successful hand-blended submissions.

Final adjustments:
- Function 1: reject the wider GP jump and continue the tiny downward trend in both coordinates.
- Function 2: stay almost exactly on the Week 6 best basin.
- Function 3: stay close to the Week 9 best with a small `x2` up and `x3` down correction.
- Function 4: continue the smooth `x4` increase with very small supporting changes.
- Function 5: continue the low-`x1`, high-remaining-coordinate trend, but less aggressively than the raw boundary candidate.
- Function 6: stay almost exactly on the Week 9 best basin.
- Function 7: continue the repeated `x2` down, `x5` up trend.
- Function 8: stay extremely close to the Week 10 best basin.

Save the final values in `week11/inputs.json` and `week11/submission.txt`.

## Validate Final Submission
Run the same checks on the final submission:

```bash
/opt/anaconda3/bin/python scripts/sanity_check_candidates.py \
  --repo-root . \
  --through-week week10 \
  --candidate-file week11/inputs.json
```

```bash
/opt/anaconda3/bin/python scripts/classifier_region_check.py \
  --repo-root . \
  --through-week week10 \
  --candidate-file week11/inputs.json \
  --svm
```

```bash
/opt/anaconda3/bin/python scripts/neural_net_surrogate_check.py \
  --repo-root . \
  --through-week week10 \
  --candidate-file week11/inputs.json
```

## Record Returned Results
After portal results return, update `week11/outputs.json` and `week11/results.json`, then generate appended arrays:

```bash
/opt/anaconda3/bin/python scripts/append_week_results.py \
  --repo-root . \
  --week week11 \
  --output-dir week11
```

Generate follow-up diagnostics:

```bash
/opt/anaconda3/bin/python scripts/analyze_progress_diagnostics.py \
  --repo-root . \
  --through-week week11 \
  --output-dir reports/week11_diagnostics
```

```bash
/opt/anaconda3/bin/python scripts/backtest_state_policy.py \
  --repo-root . \
  --from-week week1 \
  --through-week week11 \
  --output-dir reports/week11_backtest
```
