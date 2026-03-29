#!/usr/bin/env python3
"""Generate candidate queries for the next capstone round.

Trust-region strategy:
- Use Gaussian Process + UCB for lower-dimensional functions (dimension <= 4).
- Use local Random Forest search for higher-dimensional functions (dimension > 4).
- If the latest query improved the best score, shrink the search radius and exploit.
- If the latest query did not improve, search around the best historical point with a
  slightly wider radius and only a small amount of global coverage.

This is designed for the later capstone rounds where the remaining query budget is small
and sample efficiency matters more than broad exploration.

Example:
    python3 scripts/generate_candidate_queries.py \
        --repo-root . \
        --through-week week1 \
        --output-file week2/candidates.json
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.gaussian_process import GaussianProcessRegressor
from sklearn.gaussian_process.kernels import ConstantKernel, Matern, WhiteKernel


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Generate next-round candidate queries.")
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
        "--output-file",
        type=Path,
        default=None,
        help="Optional JSON file for saving generated candidates.",
    )
    parser.add_argument(
        "--seed",
        type=int,
        default=42,
        help="Random seed. Default: 42",
    )
    return parser.parse_args()


def parse_week_number(week_name: str) -> int:
    if not week_name.startswith("week"):
        raise ValueError(f"Invalid week name: {week_name}")
    return int(week_name[4:])


def load_accumulated_data(repo_root: Path, through_week: str, function_id: int) -> tuple[np.ndarray, np.ndarray, dict | None]:
    initial_dir = repo_root / "initial_data" / f"function_{function_id}"
    x = np.load(initial_dir / "initial_inputs.npy")
    y = np.load(initial_dir / "initial_outputs.npy")

    latest_payload = None
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
        x = np.vstack([x, np.array(payload["input"], dtype=float)])
        y = np.append(y, float(payload["output"]))
        latest_payload = payload

    return x, y, latest_payload


def latest_improved_best(y: np.ndarray) -> bool:
    if len(y) <= 1:
        return False
    return bool(y[-1] >= np.max(y[:-1]))


def trust_region_parameters(improved: bool, dimension: int) -> tuple[float, int, int]:
    if improved:
        radius = 0.04 if dimension <= 4 else 0.05
        local_count = 9000 if dimension <= 4 else 12000
        global_count = 250
    else:
        radius = 0.08 if dimension <= 4 else 0.10
        local_count = 7000 if dimension <= 4 else 9000
        global_count = 1000
    return radius, local_count, global_count


def build_candidate_pool(
    rng: np.random.Generator,
    center: np.ndarray,
    dimension: int,
    improved: bool,
) -> tuple[np.ndarray, float]:
    radius, local_count, global_count = trust_region_parameters(improved, dimension)
    local = np.clip(
        center + rng.normal(0.0, radius, size=(local_count, dimension)),
        0.0,
        1.0,
    )
    global_samples = rng.uniform(0.0, 1.0, size=(global_count, dimension))
    return np.vstack([local, global_samples]), radius


def suggest_with_gp(
    x: np.ndarray,
    y: np.ndarray,
    improved: bool,
    rng: np.random.Generator,
) -> tuple[np.ndarray, str, float]:
    dim = x.shape[1]
    center = x[int(np.argmax(y))]
    candidates, radius = build_candidate_pool(rng, center, dim, improved)

    kernel = ConstantKernel(1.0, (1e-3, 1e3)) * Matern(
        length_scale=np.ones(dim),
        length_scale_bounds=(1e-2, 1.5),
        nu=2.5,
    ) + WhiteKernel(noise_level=1e-5, noise_level_bounds=(1e-8, 1e-1))

    gp = GaussianProcessRegressor(
        kernel=kernel,
        normalize_y=True,
        n_restarts_optimizer=3,
        random_state=int(rng.integers(0, 1_000_000)),
    )
    gp.fit(x, y)

    mu, sigma = gp.predict(candidates, return_std=True)
    beta = 0.5 if improved else 1.2
    acquisition = mu + beta * sigma
    best_idx = int(np.argmax(acquisition))
    return candidates[best_idx], "gaussian_process_trust_region_ucb", radius


def suggest_with_rf(
    x: np.ndarray,
    y: np.ndarray,
    improved: bool,
    rng: np.random.Generator,
) -> tuple[np.ndarray, str, float]:
    dim = x.shape[1]
    center = x[int(np.argmax(y))]
    candidates, radius = build_candidate_pool(rng, center, dim, improved)

    model = RandomForestRegressor(
        n_estimators=500,
        random_state=int(rng.integers(0, 1_000_000)),
        n_jobs=-1,
        min_samples_leaf=1,
    )
    model.fit(x, y)
    predicted = model.predict(candidates)
    best_idx = int(np.argmax(predicted))
    return candidates[best_idx], "random_forest_trust_region", radius


def format_query(point: np.ndarray) -> str:
    return "-".join(f"{value:.6f}" for value in point)


def main() -> None:
    args = parse_args()
    repo_root = args.repo_root.resolve()
    rng = np.random.default_rng(args.seed)

    results = {
        "through_week": args.through_week,
        "strategy": "trust_region",
        "recommendations": {},
    }

    for function_id in range(1, 9):
        x, y, latest_payload = load_accumulated_data(repo_root, args.through_week, function_id)
        dim = x.shape[1]
        improved = latest_improved_best(y)

        if dim <= 4:
            candidate, method, radius = suggest_with_gp(x, y, improved, rng)
        else:
            candidate, method, radius = suggest_with_rf(x, y, improved, rng)

        results["recommendations"][str(function_id)] = {
            "dimension": dim,
            "method": method,
            "latest_query_improved_best": improved,
            "trust_region_radius": radius,
            "best_observed_output": float(np.max(y)),
            "best_observed_input": x[int(np.argmax(y))].tolist(),
            "candidate": candidate.tolist(),
            "portal": format_query(candidate),
            "latest_payload_present": latest_payload is not None,
        }

    output = json.dumps(results, indent=2) + "\n"
    print(output)

    if args.output_file is not None:
        output_path = args.output_file.resolve()
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(output, encoding="utf-8")


if __name__ == "__main__":
    main()
