# Repository Inventory

## Purpose
This repository stores the capstone black-box optimisation data, weekly submissions, returned outputs, and helper scripts for maintaining the dataset over time.

## Current Structure
- `initial_data/function_<n>/initial_inputs.npy`: original input arrays for each function
- `initial_data/function_<n>/initial_outputs.npy`: original output arrays for each function
- `week1/`: completed week 1 records and appended `.npy` files
- `week2/` to `week13/`: scaffold folders for future rounds
- `scripts/`: helper scripts for maintaining the weekly workflow

## Week Folder Contents
Each `weekN/` folder is intended to contain:
- `README.md`: short human-readable summary of the week folder
- `inputs.json`: submitted query point for each function
- `outputs.json`: returned output value for each function
- `results.json`: combined machine-readable input/output record
- `function_<n>/inputs.npy`: appended input array for that week when created
- `function_<n>/outputs.npy`: appended output array for that week when created

## Scripts
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

## Notes
- The repository already contains the core helper scripts needed for the current workflow.
- No existing script is strictly required to change right now.
- One possible future improvement would be to let `append_week_results.py` optionally write directly into `weekN/function_<n>/` so the generated `.npy` files land beside the JSON records without needing a separate output path.
- Another useful future improvement would be a script that combines both steps: fill a week from pasted text, then automatically generate the appended `.npy` files for that same week.

## Current Recommendation
Keep the existing scripts as they are for now. They are small, clear, and already cover the main workflow:
1. Fill the weekly scaffold from text.
2. Generate appended `.npy` files for that week.
3. Commit the updated week folder.
