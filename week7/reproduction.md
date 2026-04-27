# Week 7 Reproduction

## Inputs
- Accumulated data through Week 6: `initial_data/` plus `week1/results.json` through `week6/results.json`
- Raw state-policy candidate file: `week7/candidates.json`
- Final submission file: `week7/inputs.json`

## Step 1: Generate raw state-policy candidates

```bash
/opt/anaconda3/bin/python scripts/generate_candidate_queries.py \
  --repo-root . \
  --through-week week6 \
  --output-file week7/candidates.json
```

## Step 2: Run geometric sanity checks

```bash
/opt/anaconda3/bin/python scripts/sanity_check_candidates.py \
  --repo-root . \
  --through-week week6 \
  --candidate-file week7/candidates.json
```

## Step 3: Run classifier and neural-net checks

```bash
/opt/anaconda3/bin/python scripts/classifier_region_check.py \
  --repo-root . \
  --through-week week6 \
  --candidate-file week7/candidates.json \
  --svm

/opt/anaconda3/bin/python scripts/neural_net_surrogate_check.py \
  --repo-root . \
  --through-week week6 \
  --candidate-file week7/candidates.json
```

## Step 4: Apply the Week 7 rule set

Use `week7/candidates.json` as the starting point, then apply this rule set:

1. Keep the new state-policy as the default generator.
2. For `momentum` functions, continue the local improving direction only if the raw move stays consistent with recent basin geometry.
3. For `refine` or `recovery` functions, anchor back on the historical best basin.
4. Reject raw candidates that break sparse-peak logic, reverse a clearly successful trend, or make a large jump in a function with a known narrow basin.
5. Prefer small hand-smoothed continuation steps over large raw surrogate jumps.

That rule set yields the following adjustments:

- Function 1: raw `0.698492-0.756814` overreached, so use `0.729800-0.729800`
- Function 2: raw `0.688668-0.908232` reversed the improving direction, so use `0.694000-0.936000`
- Function 3: raw `0.480636-0.561951-0.349225` moved too far in `x2`, so use `0.491000-0.594000-0.346000`
- Function 4: raw `0.544388-0.442764-0.439301-0.271712` left the validated basin, so use `0.578300-0.428800-0.425800-0.253000`
- Function 5: raw `0.089436-0.979773-0.979773-0.984829` was clipped to `0.110000-0.965000-0.965000-0.975000`
- Function 6: raw `0.531818-0.327337-0.457703-0.877102-0.043070` did not match the recovery reset, so use `0.500300-0.325000-0.386000-0.893000-0.039000`
- Function 7: raw `0.050400-0.451878-0.239475-0.252691-0.310372-0.726723` was smoothed to `0.053000-0.464000-0.244000-0.204000-0.308000-0.728000`
- Function 8: raw `0.083832-0.048337-0.020000-0.057516-0.567401-0.820099-0.075850-0.385018` was blended back to `0.091500-0.041900-0.053700-0.065700-0.566100-0.832100-0.061800-0.409400`

## Final Output
- Output file: `week7/inputs.json`
