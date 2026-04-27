#!/usr/bin/env python3
"""Create or standardize week folder scaffolds for the capstone repo.

This script creates the core files expected in each `weekN/` folder:
- README.md
- approach.md
- notes.md
- reproduction.md
- inputs.json
- outputs.json
- results.json

Existing files are preserved unless `--overwrite` is passed.

Example:
    python3 scripts/scaffold_week_structure.py \
        --repo-root . \
        --from-week 7 \
        --to-week 13
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Create or standardize week folder scaffolds.")
    parser.add_argument(
        "--repo-root",
        type=Path,
        default=Path("."),
        help="Path to the repository root. Default: current directory.",
    )
    parser.add_argument(
        "--from-week",
        type=int,
        required=True,
        help="First week number to scaffold.",
    )
    parser.add_argument(
        "--to-week",
        type=int,
        required=True,
        help="Last week number to scaffold.",
    )
    parser.add_argument(
        "--overwrite",
        action="store_true",
        help="Overwrite existing scaffold files.",
    )
    return parser.parse_args()


def write_if_missing(path: Path, content: str, overwrite: bool) -> bool:
    if path.exists() and not overwrite:
        return False
    path.write_text(content, encoding="utf-8")
    return True


def json_stub(week_number: int) -> str:
    return json.dumps({"week": week_number, "functions": {}}, indent=2) + "\n"


def readme_stub(week_number: int) -> str:
    return f"""# Week {week_number}

This folder stores the working files for week {week_number} of the capstone black-box optimisation challenge.

Core files:
- `inputs.json`: submitted query point for each function
- `outputs.json`: returned output value for each function
- `results.json`: combined machine-readable input/output record
- `approach.md`: high-level strategy for the round
- `notes.md`: round-specific observations and decisions
- `reproduction.md`: exact steps used to reproduce the submission

Optional files:
- `candidates.json`: raw model-generated candidate queries before manual review
- `function_<n>/inputs.npy` and `function_<n>/outputs.npy`: accumulated arrays after the round is recorded
- plot folders such as `lower_dim/` or `convergence/`
"""


def approach_stub(week_number: int) -> str:
    return f"""# Week {week_number} Approach

Status: scaffold placeholder

Use this file to describe the main optimisation logic for the round, including:
- whether the round is mainly exploratory or exploitative
- which functions are treated as momentum, recovery, or reset cases
- which model signals are trusted most strongly
"""


def notes_stub(week_number: int) -> str:
    return f"""# Week {week_number} Notes

Status: scaffold placeholder

Use this file to capture:
- what the previous round taught us
- what the raw candidate generation suggested
- what was accepted, rejected, or manually adjusted
- what the returned outputs mean once the round is completed
"""


def reproduction_stub(week_number: int) -> str:
    previous_week = week_number - 1
    if previous_week >= 1:
        through_week_line = f"`week{previous_week}`"
    else:
        through_week_line = "the initial data only"

    return f"""# Week {week_number} Reproduction

## Inputs
- Accumulated data through {through_week_line}
- Candidate file for this round, if generated
- Final `inputs.json` used for submission

## Steps
1. Record the prior available data used to generate this round.
2. Generate raw candidates if a modelling step is used.
3. Run sanity checks and any supporting model checks.
4. Apply any manual blending or trust-region rules.
5. Save the final submission in `inputs.json`.
6. After results return, record `outputs.json`, `results.json`, and appended `.npy` files.
"""


def scaffold_week(repo_root: Path, week_number: int, overwrite: bool) -> list[Path]:
    week_dir = repo_root / f"week{week_number}"
    week_dir.mkdir(parents=True, exist_ok=True)

    files = {
        week_dir / "README.md": readme_stub(week_number),
        week_dir / "approach.md": approach_stub(week_number),
        week_dir / "notes.md": notes_stub(week_number),
        week_dir / "reproduction.md": reproduction_stub(week_number),
        week_dir / "inputs.json": json_stub(week_number),
        week_dir / "outputs.json": json_stub(week_number),
        week_dir / "results.json": json_stub(week_number),
    }

    updated: list[Path] = []
    for path, content in files.items():
        if write_if_missing(path, content, overwrite):
            updated.append(path)

    return updated


def main() -> None:
    args = parse_args()
    repo_root = args.repo_root.resolve()

    if args.from_week > args.to_week:
        raise ValueError("--from-week must be less than or equal to --to-week")

    all_updated: list[Path] = []
    for week_number in range(args.from_week, args.to_week + 1):
        all_updated.extend(scaffold_week(repo_root, week_number, args.overwrite))

    if all_updated:
        for path in all_updated:
            print(f"Updated {path}")
    else:
        print("No scaffold changes were needed.")


if __name__ == "__main__":
    main()
