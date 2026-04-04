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
Use `week2/candidates.json` as the starting point, then override as follows to produce `week2/inputs.json`:

- Function 1: change `0.573381-0.209185` to `0.735000-0.770000`
- Function 2: change `0.700124-0.303768` to `0.700000-0.930000`
- Function 3: change `0.983434-0.915074-0.398418` to `0.505000-0.715000-0.315000`
- Function 4: round and reset toward the best basin from `0.416569-0.389804-0.365347-0.418554` to `0.574000-0.426000-0.415000-0.118000`
- Function 5: replace `0.146395-0.959380-0.979043-1.000000` with the safer local point `0.160000-0.930000-0.920000-0.940000`
- Function 6: keep the raw candidate with rounding, yielding `0.517022-0.322479-0.379120-0.897885-0.041046`
- Function 7: replace `0.000000-0.484896-0.224957-0.172504-0.148439-0.739898` with `0.040000-0.492000-0.225000-0.173000-0.148000-0.740000`
- Function 8: keep the raw candidate with rounding, yielding `0.092062-0.042321-0.053471-0.065520-0.565106-0.833197-0.063626-0.409748`

## Final Output
- Output file: `week2/inputs.json`
