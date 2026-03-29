#!/usr/bin/env python3
"""Sanity-check proposed capstone query points.

Checks performed:
- distance from best historical point
- distance from latest query
- nearest-neighbour outcome summary
- trust-region adherence relative to the best point
- boundary/extreme-value flags

Example:
    python3 scripts/sanity_check_candidates.py \
        --repo-root . \
        --through-week week1 \
        --candidate-file week2/inputs.json
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Sanity-check proposed weekly candidate queries.")
    parser.add_argument(
        "--repo-root",
        type=Path,
        default=Path("."),
        help="Path to the repository root. Default: current directory.",
    )
    parser.add_argument(
        "--through-week",
        required=True,
        help="Use results up to and including this week, for example: week1",
    )
    parser.add_argument(
        "--candidate-file",
        type=Path,
        required=True,
        help="JSON file containing proposed inputs, for example: week2/inputs.json",
    )
    return parser.parse_args()


def parse_week_number(week_name: str) -> int:
    if not week_name.startswith("week"):
        raise ValueError(f"Invalid week name: {week_name}")
    return int(week_name[4:])


def load_accumulated_data(repo_root: Path, through_week: str, function_id: int) -> tuple[np.ndarray, np.ndarray, np.ndarray | None]:
    initial_dir = repo_root / "initial_data" / f"function_{function_id}"
    x = np.load(initial_dir / "initial_inputs.npy")
    y = np.load(initial_dir / "initial_outputs.npy")

    latest_input = None
    max_week = parse_week_number(through_week)
    for week in range(1, max_week + 1):
        results_path = repo_root / f"week{week}" / "results.json"
        if not results_path.exists():
            continue
        with results_path.open("r", encoding="utf-8") as fh:
            results = json.load(fh)
        payload = results.get("functions", {}).get(str(function_id))
        if payload is None:
            continue
        latest_input = np.array(payload["input"], dtype=float)
        x = np.vstack([x, latest_input])
        y = np.append(y, float(payload["output"]))

    return x, y, latest_input


def euclidean_distances(point: np.ndarray, points: np.ndarray) -> np.ndarray:
    return np.sqrt(np.sum((points - point) ** 2, axis=1))


def neighbour_summary(candidate: np.ndarray, x: np.ndarray, y: np.ndarray, k: int = 3) -> dict:
    dists = euclidean_distances(candidate, x)
    idx = np.argsort(dists)[:k]
    return {
        "indices": idx.tolist(),
        "distances": dists[idx].round(6).tolist(),
        "outputs": y[idx].round(12).tolist(),
        "mean_output": float(np.mean(y[idx])),
        "max_output": float(np.max(y[idx])),
    }


def trust_radius(dimension: int, latest_improved_best: bool) -> float:
    if latest_improved_best:
        return 0.04 if dimension <= 4 else 0.05
    return 0.08 if dimension <= 4 else 0.10


def boundary_flags(candidate: np.ndarray) -> list[str]:
    flags = []
    for i, value in enumerate(candidate, start=1):
        if value <= 0.01:
            flags.append(f"x{i} near lower boundary")
        if value >= 0.99:
            flags.append(f"x{i} near upper boundary")
    return flags


def latest_improved_best(y: np.ndarray) -> bool:
    if len(y) <= 1:
        return False
    return bool(y[-1] >= np.max(y[:-1]))


def portal(point: np.ndarray) -> str:
    return "-".join(f"{value:.6f}" for value in point)


def main() -> None:
    args = parse_args()
    repo_root = args.repo_root.resolve()
    candidate_file = args.candidate_file.resolve()

    with candidate_file.open("r", encoding="utf-8") as fh:
        candidate_payload = json.load(fh)

    candidate_functions = candidate_payload["functions"]
    results = {
        "through_week": args.through_week,
        "candidate_file": str(candidate_file),
        "checks": {},
    }

    for function_id in range(1, 9):
        x, y, latest_input = load_accumulated_data(repo_root, args.through_week, function_id)
        candidate = np.array(candidate_functions[str(function_id)], dtype=float)
        best_idx = int(np.argmax(y))
        best_input = x[best_idx]
        improved = latest_improved_best(y)
        radius = trust_radius(x.shape[1], improved)

        dist_best = float(np.linalg.norm(candidate - best_input))
        dist_latest = None if latest_input is None else float(np.linalg.norm(candidate - latest_input))
        neighbours = neighbour_summary(candidate, x, y)
        flags = boundary_flags(candidate)

        results["checks"][str(function_id)] = {
            "portal": portal(candidate),
            "dimension": int(x.shape[1]),
            "latest_query_improved_best": improved,
            "best_observed_output": float(y[best_idx]),
            "best_observed_input": best_input.tolist(),
            "distance_to_best": dist_best,
            "distance_to_latest": dist_latest,
            "trust_region_radius": radius,
            "within_trust_region": bool(dist_best <= radius * np.sqrt(x.shape[1]) * 1.25),
            "nearest_neighbours": neighbours,
            "boundary_flags": flags,
        }

    print(json.dumps(results, indent=2) + "\n")


if __name__ == "__main__":
    main()
