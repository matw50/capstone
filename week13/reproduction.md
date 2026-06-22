# Week 13 Reproduction

## Generate Reference Candidates

```bash
/opt/anaconda3/bin/python scripts/generate_candidate_queries.py \
  --repo-root . \
  --through-week week12 \
  --output-file week13/candidates.json \
  --seed 42 \
  --policy-variant state
```

## Apply Final-Round Rules
- Continue the observed step trajectories for Functions 1, 4, 5, and 7.
- Fit a local quadratic through the Week 5 to Week 7 Function 2 points and query near its estimated peak.
- For Function 3, move just beyond the latest strong micro-local point because the recent path alternated between strong and weak outputs.
- For Function 6, use the coordinate-wise midpoint between the Week 9 best and Week 12 near-best alternative.
- For Function 8, apply a tiny sensitivity-guided move from the Week 12 best.

Save the selected values to `week13/inputs.json` and `week13/submission.txt`.

## Validate Final Submission

```bash
/opt/anaconda3/bin/python scripts/sanity_check_candidates.py \
  --repo-root . \
  --through-week week12 \
  --candidate-file week13/inputs.json
```

```bash
/opt/anaconda3/bin/python scripts/classifier_region_check.py \
  --repo-root . \
  --through-week week12 \
  --candidate-file week13/inputs.json \
  --svm
```

```bash
/opt/anaconda3/bin/python scripts/neural_net_surrogate_check.py \
  --repo-root . \
  --through-week week12 \
  --candidate-file week13/inputs.json
```
