# Week 12 Reproduction

## Inputs
- Accumulated capstone data through `week11`
- Raw generated candidate file: `week12/candidates.json`
- Final manually blended submission: `week12/inputs.json`

## Generate Raw Candidates
Run:

```bash
/opt/anaconda3/bin/python scripts/generate_candidate_queries.py \
  --repo-root . \
  --through-week week11 \
  --output-file week12/candidates.json \
  --seed 42 \
  --policy-variant state
```

## Run Pre-Submission Checks
Run:

```bash
/opt/anaconda3/bin/python scripts/sanity_check_candidates.py \
  --repo-root . \
  --through-week week11 \
  --candidate-file week12/candidates.json
```

```bash
/opt/anaconda3/bin/python scripts/classifier_region_check.py \
  --repo-root . \
  --through-week week11 \
  --candidate-file week12/candidates.json \
  --svm
```

```bash
/opt/anaconda3/bin/python scripts/neural_net_surrogate_check.py \
  --repo-root . \
  --through-week week11 \
  --candidate-file week12/candidates.json
```

## Apply Endgame Manual Blending
Use the final-two-submissions rule:
- Preserve momentum functions with tiny local moves.
- Keep near-miss functions very close to their best basins.
- Allow one bounded alternative for repeated recovery failures.

Manual adjustments:
- Functions 1, 4, 5, and 7 are clipped back to tiny continuation moves.
- Function 3 is kept close to the Week 9 best and Week 11 near miss.
- Function 8 is returned close to the Week 10 best after a tiny Week 11 miss.
- Function 2 receives a bounded alternative: `x1` up and `x2` down from the Week 6 best.
- Function 6 receives a bounded alternative: `x2` and `x3` up while preserving high `x4` and low `x5`.

Save the final values in `week12/inputs.json` and `week12/submission.txt`.

## Validate Final Submission
Run:

```bash
/opt/anaconda3/bin/python scripts/sanity_check_candidates.py \
  --repo-root . \
  --through-week week11 \
  --candidate-file week12/inputs.json
```

```bash
/opt/anaconda3/bin/python scripts/classifier_region_check.py \
  --repo-root . \
  --through-week week11 \
  --candidate-file week12/inputs.json \
  --svm
```

```bash
/opt/anaconda3/bin/python scripts/neural_net_surrogate_check.py \
  --repo-root . \
  --through-week week11 \
  --candidate-file week12/inputs.json
```
