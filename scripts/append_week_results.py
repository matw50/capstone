#!/usr/bin/env python3
"""Append weekly capstone results to the original .npy datasets.

This script reads:
- initial_data/function_<n>/initial_inputs.npy
- initial_data/function_<n>/initial_outputs.npy
- week<k>/results.json

It writes updated arrays to a separate output directory so the originals stay unchanged.

Example:
    python3 scripts/append_week_results.py \
        --repo-root . \
        --week week1 \
        --output-dir updated_data/week1
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Append weekly results onto the initial capstone datasets.")
    parser.add_argument(
        "--repo-root",
        type=Path,
        default=Path("."),
        help="Path to the repository root. Default: current directory.",
    )
    parser.add_argument(
        "--week",
        required=True,
        help="Week folder name, for example: week1",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        required=True,
        help="Directory where updated .npy files should be written.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    repo_root = args.repo_root.resolve()
    week_dir = repo_root / args.week
    results_path = week_dir / "results.json"

    if not results_path.exists():
        raise FileNotFoundError(f"Missing results file: {results_path}")

    with results_path.open("r", encoding="utf-8") as fh:
        results = json.load(fh)

    output_dir = args.output_dir.resolve()
    output_dir.mkdir(parents=True, exist_ok=True)

    functions = results["functions"]

    for function_id_str, payload in functions.items():
        function_id = int(function_id_str)
        initial_dir = repo_root / "initial_data" / f"function_{function_id}"
        inputs_path = initial_dir / "initial_inputs.npy"
        outputs_path = initial_dir / "initial_outputs.npy"

        if not inputs_path.exists() or not outputs_path.exists():
            raise FileNotFoundError(
                f"Missing initial data for function {function_id}: {inputs_path} / {outputs_path}"
            )

        inputs = np.load(inputs_path)
        outputs = np.load(outputs_path)

        new_input = np.array(payload["input"], dtype=float)
        new_output = float(payload["output"])

        if new_input.shape[0] != inputs.shape[1]:
            raise ValueError(
                f"Function {function_id} dimension mismatch: got {new_input.shape[0]}, expected {inputs.shape[1]}"
            )

        updated_inputs = np.vstack([inputs, new_input])
        updated_outputs = np.append(outputs, new_output)

        target_dir = output_dir / f"function_{function_id}"
        target_dir.mkdir(parents=True, exist_ok=True)

        np.save(target_dir / "inputs.npy", updated_inputs)
        np.save(target_dir / "outputs.npy", updated_outputs)

        print(
            f"Function {function_id}: wrote {target_dir / 'inputs.npy'} and {target_dir / 'outputs.npy'}"
        )


if __name__ == "__main__":
    main()
