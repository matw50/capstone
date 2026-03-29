#!/usr/bin/env python3
"""Fill a week scaffold from pasted capstone input/output text.

The input text should look like:

This week's input values:
Function 1: [0.1, 0.2]
...
This week's output values:
Function 1: 0.5
...

Example:
    python3 scripts/fill_week_from_text.py \
        --repo-root . \
        --week week2 \
        --text-file /path/to/week2.txt
"""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path


INPUT_HEADER = "This week's input values:"
OUTPUT_HEADER = "This week's output values:"
LINE_RE = re.compile(r"Function\s+(\d+):\s*(.+)")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Populate a week scaffold from pasted text.")
    parser.add_argument(
        "--repo-root",
        type=Path,
        default=Path("."),
        help="Path to the repository root. Default: current directory.",
    )
    parser.add_argument(
        "--week",
        required=True,
        help="Week folder name, for example: week2",
    )
    parser.add_argument(
        "--text-file",
        type=Path,
        required=True,
        help="Path to a text file containing the pasted week input/output block.",
    )
    return parser.parse_args()


def parse_week_number(week_name: str) -> int:
    match = re.fullmatch(r"week(\d+)", week_name.strip())
    if not match:
        raise ValueError(f"Invalid week name: {week_name}")
    return int(match.group(1))


def parse_text(text: str) -> tuple[dict[str, list[float]], dict[str, float]]:
    lines = [line.strip() for line in text.splitlines() if line.strip()]

    try:
        input_start = lines.index(INPUT_HEADER)
        output_start = lines.index(OUTPUT_HEADER)
    except ValueError as exc:
        raise ValueError("Text must contain both input and output headers.") from exc

    input_lines = lines[input_start + 1 : output_start]
    output_lines = lines[output_start + 1 :]

    inputs: dict[str, list[float]] = {}
    outputs: dict[str, float] = {}

    for line in input_lines:
        match = LINE_RE.fullmatch(line)
        if not match:
            continue
        function_id, value = match.groups()
        inputs[function_id] = json.loads(value)

    for line in output_lines:
        match = LINE_RE.fullmatch(line)
        if not match:
            continue
        function_id, value = match.groups()
        outputs[function_id] = float(value)

    if not inputs:
        raise ValueError("No input values found.")
    if not outputs:
        raise ValueError("No output values found.")

    return inputs, outputs


def write_json(path: Path, payload: dict) -> None:
    path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")


def main() -> None:
    args = parse_args()
    repo_root = args.repo_root.resolve()
    week_dir = repo_root / args.week
    week_number = parse_week_number(args.week)

    if not week_dir.exists():
        raise FileNotFoundError(f"Week folder does not exist: {week_dir}")

    text = args.text_file.read_text(encoding="utf-8")
    inputs, outputs = parse_text(text)

    results = {
        "week": week_number,
        "functions": {
            function_id: {
                "input": inputs[function_id],
                "output": outputs[function_id],
            }
            for function_id in sorted(inputs.keys(), key=int)
        },
    }

    write_json(week_dir / "inputs.json", {"week": week_number, "functions": inputs})
    write_json(week_dir / "outputs.json", {"week": week_number, "functions": outputs})
    write_json(week_dir / "results.json", results)

    print(f"Updated {week_dir / 'inputs.json'}")
    print(f"Updated {week_dir / 'outputs.json'}")
    print(f"Updated {week_dir / 'results.json'}")


if __name__ == "__main__":
    main()
