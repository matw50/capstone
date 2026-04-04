# Week 2 Reproduction

## Inputs
- Accumulated data through Week 1: `initial_data/` plus `week1/results.json`
- Raw candidate output file: `week2/candidates.json`
- Final submission file: `week2/inputs.json`

## Step 1: Generate raw candidates

```bash
/opt/anaconda3/bin/python scripts/generate_candidate_queries.py \
  --repo-root . \
  --through-week week1 \
  --output-file week2/candidates.json
```

## Step 2: Run the baseline sanity check

```bash
/opt/anaconda3/bin/python scripts/sanity_check_candidates.py \
  --repo-root . \
  --through-week week1 \
  --candidate-file week2/candidates.json
```

## Step 3: Manually adjust the raw candidates into the final output
Use `week2/candidates.json` as the starting point, then apply this rule set:

1. If the raw candidate stays in the best historical basin and passes the trust-region check, keep it or round it lightly.
2. If the raw candidate jumps away from the best historical basin, replace it with a local point near the best known region.
3. If the raw candidate is in the right basin but pushes too hard toward a boundary, clip it back to a safer local point.
4. For higher-dimensional functions, keep raw trust-region suggestions only when they remain local and consistent with the strongest observed neighbourhood.

That rule set yields the following adjustments to produce `week2/inputs.json`:

- Function 1: raw candidate failed the basin-locality rule, so change `0.573381-0.209185` to the local recovery point `0.735000-0.770000`
- Function 2: raw candidate failed the basin-locality rule, so change `0.700124-0.303768` to the local basin point `0.700000-0.930000`
- Function 3: raw candidate failed the basin-locality rule, so change `0.983434-0.915074-0.398418` to `0.505000-0.715000-0.315000`
- Function 4: raw candidate was directionally plausible but still too far from the best basin, so reset and round from `0.416569-0.389804-0.365347-0.418554` to `0.574000-0.426000-0.415000-0.118000`
- Function 5: raw candidate stayed in the right basin but violated the boundary rule, so replace `0.146395-0.959380-0.979043-1.000000` with the safer local point `0.160000-0.930000-0.920000-0.940000`
- Function 6: raw candidate satisfied the locality rule, so keep it with rounding, yielding `0.517022-0.322479-0.379120-0.897885-0.041046`
- Function 7: raw candidate stayed near the correct basin but looked too aggressive, so smooth it into `0.040000-0.492000-0.225000-0.173000-0.148000-0.740000`
- Function 8: raw candidate satisfied the locality rule, so keep it with rounding, yielding `0.092062-0.042321-0.053471-0.065520-0.565106-0.833197-0.063626-0.409748`

## Final Output
- Output file: `week2/inputs.json`
