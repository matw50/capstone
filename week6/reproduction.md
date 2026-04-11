# Week 6 Reproduction

## Inputs
- Accumulated data through Week 5: `initial_data/` plus `week1/results.json` through `week5/results.json`
- Raw candidate output file: `week6/candidates.json`
- Final submission file: `week6/inputs.json`

## Step 1: Generate raw candidates

```bash
/opt/anaconda3/bin/python scripts/generate_candidate_queries.py \
  --repo-root . \
  --through-week week5 \
  --output-file week6/candidates.json
```

## Step 2: Run the geometric sanity checks

```bash
/opt/anaconda3/bin/python scripts/sanity_check_candidates.py \
  --repo-root . \
  --through-week week5 \
  --candidate-file week6/candidates.json
```

## Step 3: Run classifier and neural-net checks

```bash
/opt/anaconda3/bin/python scripts/classifier_region_check.py \
  --repo-root . \
  --through-week week5 \
  --candidate-file week6/candidates.json \
  --svm

/opt/anaconda3/bin/python scripts/neural_net_surrogate_check.py \
  --repo-root . \
  --through-week week5 \
  --candidate-file week6/candidates.json
```

## Step 4: Apply the Week 6 rule set

Use `week6/candidates.json` as the starting point, then apply this rule set:

1. Anchor on the historical best unless Week 5 created a new best.
2. For Week 5 new bests, take a small continuation step only.
3. Reject GP candidates that jump away from the validated basin.
4. Clip boundary-seeking candidates back inside a local trust region.
5. Treat Function 6 as a correction case: keep `x4` high and `x5` low, but deliberately probe lower `x2` and lower `x3`.

That rule set yields the following adjustments:

- Function 1: raw `0.529307-0.727222` failed locality, so use `0.730500-0.731500`
- Function 2: raw `0.684955-0.738726` moved away from the Week 5 best, so use `0.696000-0.934000`
- Function 3: raw `0.945253-0.929213-0.399431` failed locality, so use `0.492000-0.604000-0.343000`
- Function 4: raw `0.390832-0.457585-0.383826-0.377659` failed locality, so use `0.578000-0.428800-0.425800-0.251000`
- Function 5: raw `0.000558-0.941226-1.000000-1.000000` was boundary-seeking, so use `0.120000-0.960000-0.960000-0.970000`
- Function 6: raw `0.479957-0.287967-0.398944-0.881792-0.034367` was plausible but did not match the deliberate correction, so use `0.500000-0.300000-0.365000-0.900000-0.030000`
- Function 7: raw `0.045987-0.405307-0.233941-0.194971-0.282582-0.735056` moved too much in `x2`, so use `0.052000-0.471000-0.242000-0.202000-0.302000-0.730000`
- Function 8: raw `0.083333-0.000000-0.057705-0.067658-0.636816-0.829837-0.061050-0.619546` had a boundary flag and moved too far in `x8`, so use `0.091000-0.041500-0.053900-0.065900-0.567000-0.831000-0.060000-0.409000`

## Final Output
- Output file: `week6/inputs.json`
