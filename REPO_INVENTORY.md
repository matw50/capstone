# Repository Inventory

## Purpose
This repository stores the capstone black-box optimisation data, weekly submissions, returned outputs, and helper scripts for maintaining the dataset over time.

## Environment
Install the core Python dependencies with:

```bash
python3 -m pip install -r requirements.txt
```

Current top-level dependencies:
- `numpy`
- `scikit-learn`
- `matplotlib`

## Current Structure
- `initial_data/function_<n>/initial_inputs.npy`: original input arrays for each function
- `initial_data/function_<n>/initial_outputs.npy`: original output arrays for each function
- `week1/` to `week6/`: completed rounds with recorded submissions, returned outputs, and appended `.npy` files
- `week7/` to `week13/`: standardized scaffold folders for future rounds
- `benchmarks/`: external benchmark runs used to sanity-check the policy outside the capstone portal
- `scripts/`: helper scripts for maintaining the weekly workflow
- `requirements.txt`: lightweight dependency file for reproducing the workflow

## Week Folder Contents
Each `weekN/` folder is intended to contain:
- `README.md`: short human-readable summary of the week folder
- `inputs.json`: submitted query point for each function
- `outputs.json`: returned output value for each function
- `results.json`: combined machine-readable input/output record
- `approach.md`: high-level strategy note for the round
- `notes.md`: round-specific reasoning and outcome notes
- `reproduction.md`: exact steps used to reproduce the submission
- `function_<n>/inputs.npy`: appended input array for that week when created
- `function_<n>/outputs.npy`: appended output array for that week when created

Optional files include:
- `candidates.json`: raw model-generated candidate points before manual blending
- plot folders such as `lower_dim/` or `convergence/`

## Scripts
### `scripts/scaffold_week_structure.py`
Creates or standardizes the core scaffold files for one or more future week folders.

Example:
```bash
python3 scripts/scaffold_week_structure.py --repo-root . --from-week 7 --to-week 13
```

### `scripts/fill_week_from_text.py`
Reads a pasted text block containing the weekly submitted inputs and returned outputs, then fills:
- `weekN/inputs.json`
- `weekN/outputs.json`
- `weekN/results.json`

Example:
```bash
python3 scripts/fill_week_from_text.py --repo-root . --week week2 --text-file /path/to/week2.txt
```

### `scripts/append_week_results.py`
Reads `initial_data` plus `weekN/results.json`, then writes appended `.npy` arrays to a chosen output directory.

Example:
```bash
python3 scripts/append_week_results.py --repo-root . --week week2 --output-dir updated_data/week2
```

### `scripts/generate_candidate_queries.py`
Generates candidate query points for the next round using a trust-region strategy.
- lower-dimensional functions use local Gaussian Process search
- higher-dimensional functions use local Random Forest search
- trust-region radius adapts depending on whether the latest query improved the best value

Example:
```bash
python3 scripts/generate_candidate_queries.py --repo-root . --through-week week1 --output-file week2/candidates.json
```

### `scripts/sanity_check_candidates.py`
Checks proposed candidate points against practical late-stage heuristics, including:
- distance to best historical point
- distance to latest query
- trust-region adherence
- nearest-neighbour outcomes
- boundary/extreme-value flags

### `scripts/run_coco_benchmark.py`
Runs the current capstone policy against the COCO/BBOB benchmark suite with a capstone-like evaluation budget and compares it against a random continuation baseline.

Example:
```bash
python3 scripts/sanity_check_candidates.py --repo-root . --through-week week1 --candidate-file week2/inputs.json
```

## Notes
- The repository now contains the core helper scripts needed for the current workflow.
- Week scaffolds are now standardized so future rounds start with the same core files.
- One possible future improvement would be to let `append_week_results.py` optionally write directly into `weekN/function_<n>/` so the generated `.npy` files land beside the JSON records without needing a separate output path.
- Another useful future improvement would be a script that combines all three steps: fill a week from pasted text, generate the appended `.npy` files for that week, and produce draft candidate queries for the next week.

## Current Recommendation
Keep the existing scripts as they are for now. They are small, clear, and already cover the main workflow:
1. Scaffold or standardize the target week folder.
2. Fill the weekly scaffold from text.
3. Generate appended `.npy` files for that week.
4. Generate and sanity-check next-round candidates.
5. Commit the updated week folder.
