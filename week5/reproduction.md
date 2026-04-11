# Week 5 Reproduction

## Inputs
- Accumulated data through Week 4: `initial_data/` plus `week1/results.json`, `week2/results.json`, `week3/results.json`, and `week4/results.json`
- Raw candidate output file: `week5/candidates.json`
- Final submission file: `week5/inputs.json`

## Step 1: Generate raw candidates

```bash
/opt/anaconda3/bin/python scripts/generate_candidate_queries.py \
  --repo-root . \
  --through-week week4 \
  --output-file week5/candidates.json
```

## Step 2: Run the geometric sanity checks

```bash
/opt/anaconda3/bin/python scripts/sanity_check_candidates.py \
  --repo-root . \
  --through-week week4 \
  --candidate-file week5/candidates.json
```

## Step 3: Run the classifier region checks

```bash
/opt/anaconda3/bin/python scripts/classifier_region_check.py \
  --repo-root . \
  --through-week week4 \
  --candidate-file week5/candidates.json \
  --svm
```

## Step 4: Apply the Week 5 historical-best anchoring rule

Use `week5/candidates.json` as the starting point, then apply this rule set:

1. If Week 4 produced a new best, anchor on the Week 4 point and make a small local move.
2. If the historical best is still from initial data or an earlier week, anchor on that historical best rather than the latest point.
3. Use recent submissions as directional evidence, but do not let them become the centre of the search unless they are the best observed point.
4. Reject raw candidates that leave the validated basin.
5. Clip boundary-seeking raw candidates back into a local trust region.
6. Treat logistic regression and SVM outputs as secondary evidence only.

That rule set yields the following adjustments to produce `week5/inputs.json`:

- Function 1: raw `0.532264-0.951294` failed basin-locality, so use the ultra-local historical-best probe `0.731800-0.735000`
- Function 2: raw `0.791632-1.000000` pushed too far toward the boundary, so recenter near the best basin with `0.698000-0.932000`
- Function 3: raw `0.967842-0.357416-0.792961` failed locality and neighbour checks, so use `0.494000-0.625000-0.337000`
- Function 4: raw `0.398412-0.465551-0.390315-0.428857` failed basin-locality, so use `0.577500-0.428800-0.425900-0.247000`
- Function 5: raw `0.061447-0.977463-1.000000-1.000000` was in the right basin but boundary-seeking, so clip to `0.130000-0.955000-0.955000-0.965000`
- Function 6: raw `0.426288-0.310672-0.336922-0.875225-0.037359` passed trust-region checks but was more aggressive than needed, so soften to `0.495000-0.325000-0.388000-0.894000-0.038500`
- Function 7: raw `0.050023-0.379668-0.237448-0.200549-0.293792-0.727890` stayed in the right basin but drifted too much in `x2`, so smooth to `0.051000-0.478000-0.240000-0.200000-0.296000-0.732000`
- Function 8: raw `0.081089-0.034956-0.058262-0.069426-0.585510-0.812839-0.034003-0.403614` was well supported, but Week 2 is still best, so blend back toward the Week 2 best with `0.089300-0.040400-0.054700-0.066500-0.570000-0.828000-0.054000-0.408000`

## Final Output
- Output file: `week5/inputs.json`

## Optional Post-Blend Neural-Net Check

After `week5/inputs.json` has been created, run:

```bash
/opt/anaconda3/bin/python scripts/neural_net_surrogate_check.py \
  --repo-root . \
  --through-week week4 \
  --candidate-file week5/inputs.json
```

This is an experimental secondary check. It should not override the trust-region, neighbour, and boundary checks.
