# Week 1 Reproduction

Week 1 predates the query-generation scripts, so there is no raw `candidates.json` file to replay. Reproducing Week 1 is therefore a manual baseline exercise driven by the original input-output data and the low-dimensional plots.

## Inputs
- Source data: `initial_data/function_<n>/initial_inputs.npy`
- Source outputs: `initial_data/function_<n>/initial_outputs.npy`
- Visual aid command:

```bash
/opt/anaconda3/bin/python scripts/plot_low_dim_views.py \
  --repo-root . \
  --through-week week1 \
  --output-dir week1/lower_dim
```

## Procedure
1. Load the original `.npy` arrays from `initial_data/`.
2. Generate the low-dimensional views with the command above.
3. Select the Week 1 submission manually using the Week 1 heuristic:
   - Functions 1 to 4: local visual reasoning around the best observed basin
   - Functions 5 to 8: surrogate-style reasoning based on the strongest observed region
4. Write the final portal-ready values to `week1/inputs.json`.

## Final Output
- Output file: `week1/inputs.json`

The final Week 1 submission set in that file is the canonical output for this round.
