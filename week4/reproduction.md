# Week 4 Reproduction

## Inputs
- Accumulated data through Week 3: `initial_data/` plus `week1/results.json`, `week2/results.json`, and `week3/results.json`
- Raw candidate output file: `week4/candidates.json`
- Final submission file: `week4/inputs.json`

## Step 1: Generate raw candidates

```bash
/opt/anaconda3/bin/python scripts/generate_candidate_queries.py \
  --repo-root . \
  --through-week week3 \
  --output-file week4/candidates.json
```

## Step 2: Run the geometric sanity checks

```bash
/opt/anaconda3/bin/python scripts/sanity_check_candidates.py \
  --repo-root . \
  --through-week week3 \
  --candidate-file week4/candidates.json
```

## Step 3: Run the classifier region checks

```bash
/opt/anaconda3/bin/python scripts/classifier_region_check.py \
  --repo-root . \
  --through-week week3 \
  --candidate-file week4/candidates.json \
  --svm
```

## Step 4: Manually adjust the raw candidates into the final output
Use `week4/candidates.json` as the starting point, then apply this rule set:

1. Keep trust-region, nearest-neighbour, and boundary checks as the primary filters.
2. Use logistic-regression and SVM region checks as secondary evidence only.
3. Reject raw candidates that leave the validated basin, even if a classifier labels them as high-region.
4. Keep or lightly round raw candidates that stay local and are supported by both the geometric checks and strong nearby outcomes.
5. For momentum functions, continue exploiting locally but clip boundary-seeking proposals.

That rule set yields the following adjustments to produce `week4/inputs.json`:

- Function 1: raw candidate failed the primary geometric checks, so change `0.532723-0.778465` to the ultra-local point `0.732500-0.739500`
- Function 2: raw candidate failed the basin-locality rule, so change `0.709663-0.015135` to `0.702000-0.927500`
- Function 3: raw candidate failed both locality and boundary rules, so change `0.991962-0.937447-0.413796` to `0.496000-0.640000-0.334000`
- Function 4: classifiers looked more positive than the geometric checks, so follow the primary filters and reset from `0.398412-0.465551-0.390315-0.428857` to `0.577000-0.429000-0.426000-0.240000`
- Function 5: raw candidate was in the right region but violated the boundary rule, so clip `0.066447-0.972463-1.000000-1.000000` back to `0.140000-0.950000-0.950000-0.960000`
- Function 6: raw candidate passed the primary checks but was still more aggressive than necessary, so soften `0.541317-0.318594-0.248474-0.879926-0.037656` to `0.507000-0.323000-0.380000-0.892000-0.039000`
- Function 7: raw candidate stayed in the right basin but moved too far in `x2`, so smooth it into `0.050000-0.485000-0.238000-0.198000-0.290000-0.734000`
- Function 8: raw candidate largely satisfied the rule set, so keep the same local pattern and blend slightly toward the best historical point, yielding `0.086500-0.038500-0.056000-0.067500-0.575000-0.823000-0.045000-0.406500`

## Final Output
- Output file: `week4/inputs.json`
