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
Use `week4/candidates.json` as the starting point, then override as follows to produce `week4/inputs.json`:

- Function 1: change `0.532723-0.778465` to `0.732500-0.739500`
- Function 2: change `0.709663-0.015135` to `0.702000-0.927500`
- Function 3: change `0.991962-0.937447-0.413796` to `0.496000-0.640000-0.334000`
- Function 4: change `0.398412-0.465551-0.390315-0.428857` to `0.577000-0.429000-0.426000-0.240000`
- Function 5: change `0.066447-0.972463-1.000000-1.000000` to `0.140000-0.950000-0.950000-0.960000`
- Function 6: change `0.541317-0.318594-0.248474-0.879926-0.037656` to `0.507000-0.323000-0.380000-0.892000-0.039000`
- Function 7: change `0.049023-0.386668-0.235448-0.198549-0.287792-0.729890` to `0.050000-0.485000-0.238000-0.198000-0.290000-0.734000`
- Function 8: change `0.081089-0.034956-0.058262-0.069426-0.585510-0.812839-0.034003-0.403614` to `0.086500-0.038500-0.056000-0.067500-0.575000-0.823000-0.045000-0.406500`

## Final Output
- Output file: `week4/inputs.json`
