# Week 3 Reproduction

## Inputs
- Accumulated data through Week 2: `initial_data/` plus `week1/results.json` and `week2/results.json`
- Raw candidate output file: `week3/candidates.json`
- Final submission file: `week3/inputs.json`

## Step 1: Generate raw candidates

```bash
/opt/anaconda3/bin/python scripts/generate_candidate_queries.py \
  --repo-root . \
  --through-week week2 \
  --output-file week3/candidates.json
```

## Step 2: Run the baseline sanity check

```bash
/opt/anaconda3/bin/python scripts/sanity_check_candidates.py \
  --repo-root . \
  --through-week week2 \
  --candidate-file week3/candidates.json
```

## Step 3: Review convergence and low-dimensional plots

```bash
/opt/anaconda3/bin/python scripts/plot_convergence.py \
  --repo-root . \
  --through-week week2 \
  --output-dir week3/convergence

/opt/anaconda3/bin/python scripts/plot_low_dim_views.py \
  --repo-root . \
  --through-week week2 \
  --output-dir week3/lower_dim
```

## Step 4: Manually adjust the raw candidates into the final output
Use `week3/candidates.json` as the starting point, then apply this rule set:

1. Reject raw candidates that fail the trust-region check and jump away from the best historical basin.
2. Keep or lightly round raw candidates that remain local and are supported by nearby strong observations.
3. For recovery functions, reset toward the best historical basin rather than continuing in a weak direction.
4. For momentum functions, keep exploiting locally but clip edge-seeking proposals back inside the local neighbourhood.

That rule set yields the following adjustments to produce `week3/inputs.json`:

- Function 1: raw candidate failed the locality rule, so change `0.573381-0.209185` to the tighter local point `0.733000-0.748000`
- Function 2: raw candidate failed the locality rule, so change `0.709663-0.015135` to `0.701500-0.928000`
- Function 3: raw candidate failed the locality rule, so change `0.991962-0.937447-0.413796` to `0.498000-0.665000-0.328000`
- Function 4: this was a recovery function, so reset from `0.416569-0.389804-0.365347-0.418554` to `0.576000-0.429000-0.426000-0.225000`
- Function 5: this was a momentum function with an edge-seeking raw proposal, so clip `0.090024-0.988172-1.000000-0.975024` back to `0.145000-0.945000-0.945000-0.955000`
- Function 6: this was a recovery function, so soften the raw move from `0.541317-0.318594-0.248474-0.879926-0.037656` to `0.505000-0.323000-0.372000-0.890000-0.039000`
- Function 7: raw candidate was in the right basin but too aggressive, so smooth it into `0.049000-0.492000-0.236000-0.196000-0.284000-0.736000`
- Function 8: raw candidate satisfied the locality rule, so keep it with rounding, yielding `0.076137-0.036885-0.051524-0.069041-0.640532-0.823614-0.026805-0.370276`

## Final Output
- Output file: `week3/inputs.json`
