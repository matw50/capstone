#!/usr/bin/env python3
"""Generate candidate queries for the next capstone round.

State-machine trust-region strategy:
- `bootstrap`: no guided evaluations yet, start from the best observed basin.
- `momentum`: latest guided query improved the best score, exploit tightly nearby.
- `refine`: one non-improving round, return to the historical best and refine locally.
- `stagnant`: two non-improving rounds, test one bounded exploratory probe.
- `recovery`: after a failed exploratory probe, return to the best basin and stop jumping.

Modeling policy:
- Use Gaussian Process + UCB for lower-dimensional functions (dimension <= 4).
- Use local Random Forest search for higher-dimensional functions (dimension > 4).
- During stagnation, compare a local exploit candidate, a wider surrogate candidate, and
  a second-basin candidate when one exists.
- Apply simple guardrails on boundary chasing and candidate locality.

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


STATE_BOOTSTRAP = "bootstrap"
STATE_MOMENTUM = "momentum"
STATE_REFINE = "refine"
STATE_STAGNANT = "stagnant"
STATE_RECOVERY = "recovery"


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


def count_initial_observations(repo_root: Path, function_id: int) -> int:
    initial_dir = repo_root / "initial_data" / f"function_{function_id}"
    return int(np.load(initial_dir / "initial_outputs.npy").shape[0])


def last_improvement_index(y: np.ndarray, n_initial: int) -> int:
    if len(y) == 0:
        return -1

    running_best = float(np.max(y[:n_initial])) if n_initial else float("-inf")
    last_index = n_initial - 1 if n_initial else -1

    for idx in range(n_initial, len(y)):
        if y[idx] >= running_best:
            running_best = float(y[idx])
            last_index = idx

    return last_index


def non_improving_streak(y: np.ndarray, n_initial: int) -> int:
    if len(y) <= n_initial:
        return 0
    return (len(y) - 1) - last_improvement_index(y, n_initial)


def determine_policy_state(y: np.ndarray, n_initial: int) -> str:
    if len(y) <= n_initial:
        return STATE_BOOTSTRAP
    if latest_improved_best(y):
        return STATE_MOMENTUM

    streak = non_improving_streak(y, n_initial)
    if streak == 1:
        return STATE_REFINE
    if streak == 2:
        return STATE_STAGNANT
    return STATE_RECOVERY


def state_parameters(state: str, dimension: int) -> dict[str, float | int]:
    low_dim = dimension <= 4

    if state == STATE_BOOTSTRAP:
        return {
            "radius": 0.06 if low_dim else 0.08,
            "local_count": 800 if low_dim else 1000,
            "global_count": 100,
            "beta": 1.0,
        }
    if state == STATE_MOMENTUM:
        return {
            "radius": 0.04 if low_dim else 0.05,
            "local_count": 900 if low_dim else 1100,
            "global_count": 60,
            "beta": 0.35,
        }
    if state == STATE_REFINE:
        return {
            "radius": 0.06 if low_dim else 0.08,
            "local_count": 850 if low_dim else 1050,
            "global_count": 100,
            "beta": 0.9,
        }
    if state == STATE_STAGNANT:
        return {
            "radius": 0.10 if low_dim else 0.12,
            "local_count": 800 if low_dim else 1000,
            "global_count": 220,
            "beta": 1.4,
        }
    if state == STATE_RECOVERY:
        return {
            "radius": 0.06 if low_dim else 0.08,
            "local_count": 800 if low_dim else 1000,
            "global_count": 80,
            "beta": 0.7,
        }
    raise ValueError(f"Unknown state: {state}")


def boundary_flags(candidate: np.ndarray) -> list[tuple[int, str]]:
    flags: list[tuple[int, str]] = []
    for idx, value in enumerate(candidate):
        if value < 0.02:
            flags.append((idx, "low"))
        elif value > 0.98:
            flags.append((idx, "high"))
    return flags


def boundary_supported(candidate: np.ndarray, x: np.ndarray, y: np.ndarray, latest_improved: bool) -> bool:
    flags = boundary_flags(candidate)
    if not flags:
        return True
    if not latest_improved:
        return False

    good_count = min(len(y), max(3, len(y) // 4))
    good_idx = np.argsort(y)[-good_count:]
    distances = np.linalg.norm(x[good_idx] - candidate, axis=1)
    nearest_good = good_idx[np.argsort(distances)[: min(3, len(good_idx))]]

    for coord, side in flags:
        if side == "low":
            supported = np.sum(x[nearest_good, coord] <= 0.05) >= 2
        else:
            supported = np.sum(x[nearest_good, coord] >= 0.95) >= 2
        if not supported:
            return False
    return True


def project_to_radius(candidate: np.ndarray, center: np.ndarray, radius: float) -> np.ndarray:
    delta = candidate - center
    norm = float(np.linalg.norm(delta))
    if norm <= radius or norm == 0.0:
        return candidate
    return center + (delta / norm) * radius


def nearest_neighbor_support_percentile(candidate: np.ndarray, x: np.ndarray, y: np.ndarray) -> float:
    k = min(3, len(y))
    distances = np.linalg.norm(x - candidate, axis=1)
    nearest_idx = np.argsort(distances)[:k]
    support_mean = float(np.mean(y[nearest_idx]))
    return float(np.mean(y <= support_mean))


def choose_second_basin_center(x: np.ndarray, y: np.ndarray, main_anchor: np.ndarray, radius: float) -> np.ndarray | None:
    distances = np.linalg.norm(x - main_anchor, axis=1)
    min_distance = max(radius * 1.5, 0.08 if x.shape[1] <= 4 else 0.10)
    candidate_idx = np.where(distances > min_distance)[0]
    if len(candidate_idx) == 0:
        return None
    best_idx = candidate_idx[int(np.argmax(y[candidate_idx]))]
    return x[best_idx]


def build_candidate_pool(
    rng: np.random.Generator,
    center: np.ndarray,
    dimension: int,
    radius: float,
    local_count: int,
    global_count: int,
) -> tuple[np.ndarray, float]:
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
    center: np.ndarray,
    radius: float,
    beta: float,
    local_count: int,
    global_count: int,
    rng: np.random.Generator,
) -> tuple[np.ndarray, str, float]:
    dim = x.shape[1]
    candidates, radius = build_candidate_pool(rng, center, dim, radius, local_count, global_count)

    kernel = ConstantKernel(1.0, (1e-3, 1e3)) * Matern(
        length_scale=np.ones(dim),
        length_scale_bounds=(1e-2, 1.5),
        nu=2.5,
    ) + WhiteKernel(noise_level=1e-5, noise_level_bounds=(1e-8, 1e-1))

    gp = GaussianProcessRegressor(
        kernel=kernel,
        normalize_y=True,
        n_restarts_optimizer=0,
        random_state=int(rng.integers(0, 1_000_000)),
    )
    gp.fit(x, y)

    mu, sigma = gp.predict(candidates, return_std=True)
    acquisition = mu + beta * sigma
    best_idx = int(np.argmax(acquisition))
    return candidates[best_idx], "gaussian_process_state_ucb", float(acquisition[best_idx])


def suggest_with_rf(
    x: np.ndarray,
    y: np.ndarray,
    center: np.ndarray,
    radius: float,
    local_count: int,
    global_count: int,
    rng: np.random.Generator,
) -> tuple[np.ndarray, str, float]:
    dim = x.shape[1]
    candidates, radius = build_candidate_pool(rng, center, dim, radius, local_count, global_count)

    model = RandomForestRegressor(
        n_estimators=150,
        random_state=int(rng.integers(0, 1_000_000)),
        n_jobs=-1,
        min_samples_leaf=1,
    )
    model.fit(x, y)
    predicted = model.predict(candidates)
    best_idx = int(np.argmax(predicted))
    return candidates[best_idx], "random_forest_state_policy", float(predicted[best_idx])


def propose_candidate(
    x: np.ndarray,
    y: np.ndarray,
    center: np.ndarray,
    state: str,
    rng: np.random.Generator,
    radius_override: float | None = None,
    beta_override: float | None = None,
) -> tuple[np.ndarray, str, float, float]:
    dim = x.shape[1]
    params = state_parameters(state, dim)
    radius = float(radius_override if radius_override is not None else params["radius"])
    beta = float(beta_override if beta_override is not None else params["beta"])
    local_count = int(params["local_count"])
    global_count = int(params["global_count"])

    if dim <= 4:
        candidate, method, score = suggest_with_gp(
            x=x,
            y=y,
            center=center,
            radius=radius,
            beta=beta,
            local_count=local_count,
            global_count=global_count,
            rng=rng,
        )
    else:
        candidate, method, score = suggest_with_rf(
            x=x,
            y=y,
            center=center,
            radius=radius,
            local_count=local_count,
            global_count=global_count,
            rng=rng,
        )
    return candidate, method, radius, score


def choose_policy_candidate(
    x: np.ndarray,
    y: np.ndarray,
    n_initial: int,
    rng: np.random.Generator,
) -> tuple[np.ndarray, dict[str, object]]:
    state = determine_policy_state(y, n_initial)
    streak = non_improving_streak(y, n_initial)
    latest_improved = len(y) > n_initial and latest_improved_best(y)

    historical_best = x[int(np.argmax(y))]
    latest_point = x[-1]
    anchor = latest_point if state == STATE_MOMENTUM else historical_best
    anchor_type = "latest" if state == STATE_MOMENTUM else "historical_best"
    base_radius = float(state_parameters(state, x.shape[1])["radius"])

    candidates_to_compare: list[dict[str, object]] = []

    if state == STATE_STAGNANT:
        local_candidate, local_method, local_radius, local_score = propose_candidate(
            x=x,
            y=y,
            center=historical_best,
            state=STATE_REFINE,
            rng=rng,
            radius_override=0.04 if x.shape[1] <= 4 else 0.05,
            beta_override=0.6,
        )
        candidates_to_compare.append(
            {
                "candidate": local_candidate,
                "method": f"{local_method}_local_exploit",
                "radius": local_radius,
                "score": local_score,
            }
        )

        wide_candidate, wide_method, wide_radius, wide_score = propose_candidate(
            x=x,
            y=y,
            center=historical_best,
            state=STATE_STAGNANT,
            rng=rng,
        )
        candidates_to_compare.append(
            {
                "candidate": wide_candidate,
                "method": f"{wide_method}_wide_probe",
                "radius": wide_radius,
                "score": wide_score,
            }
        )

        second_center = choose_second_basin_center(x, y, historical_best, base_radius)
        if second_center is not None:
            basin_candidate, basin_method, basin_radius, basin_score = propose_candidate(
                x=x,
                y=y,
                center=second_center,
                state=STATE_REFINE,
                rng=rng,
                radius_override=0.06 if x.shape[1] <= 4 else 0.08,
                beta_override=0.8,
            )
            candidates_to_compare.append(
                {
                    "candidate": basin_candidate,
                    "method": f"{basin_method}_second_basin",
                    "radius": basin_radius,
                    "score": basin_score,
                }
            )
    else:
        candidate, method, radius, score = propose_candidate(
            x=x,
            y=y,
            center=anchor,
            state=state,
            rng=rng,
        )
        candidates_to_compare.append(
            {
                "candidate": candidate,
                "method": method,
                "radius": radius,
                "score": score,
            }
        )

    ranked: list[dict[str, object]] = []
    for option in candidates_to_compare:
        raw_candidate = np.array(option["candidate"], dtype=float)
        radius = float(option["radius"])
        candidate = np.clip(raw_candidate, 0.0, 1.0)
        candidate = project_to_radius(candidate, anchor, radius * 1.1)

        valid_boundary = boundary_supported(candidate, x, y, latest_improved)
        if not valid_boundary:
            candidate = np.clip(candidate, 0.02, 0.98)
            candidate = project_to_radius(candidate, anchor, radius)

        support_percentile = nearest_neighbor_support_percentile(candidate, x, y)
        ranked.append(
            {
                "candidate": candidate,
                "method": option["method"],
                "radius": radius,
                "score": float(option["score"]),
                "support_percentile": support_percentile,
                "boundary_ok": valid_boundary,
            }
        )

    ranked.sort(
        key=lambda item: (
            item["boundary_ok"],
            item["support_percentile"],
            item["score"],
        ),
        reverse=True,
    )
    selected = ranked[0]

    metadata = {
        "state": state,
        "non_improving_streak": streak,
        "anchor_type": anchor_type,
        "anchor": anchor.tolist(),
        "candidate_options": [
            {
                "method": item["method"],
                "radius": item["radius"],
                "support_percentile": item["support_percentile"],
                "boundary_ok": item["boundary_ok"],
            }
            for item in ranked
        ],
        "selected_method": selected["method"],
        "trust_region_radius": float(selected["radius"]),
    }
    return np.array(selected["candidate"], dtype=float), metadata


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
        n_initial = count_initial_observations(repo_root, function_id)
        dim = x.shape[1]
        improved = len(y) > n_initial and latest_improved_best(y)
        candidate, policy = choose_policy_candidate(x, y, n_initial, rng)

        results["recommendations"][str(function_id)] = {
            "dimension": dim,
            "method": policy["selected_method"],
            "state": policy["state"],
            "non_improving_streak": policy["non_improving_streak"],
            "anchor_type": policy["anchor_type"],
            "anchor": policy["anchor"],
            "latest_query_improved_best": improved,
            "trust_region_radius": policy["trust_region_radius"],
            "best_observed_output": float(np.max(y)),
            "best_observed_input": x[int(np.argmax(y))].tolist(),
            "candidate": candidate.tolist(),
            "portal": format_query(candidate),
            "latest_payload_present": latest_payload is not None,
            "candidate_options": policy["candidate_options"],
        }

    output = json.dumps(results, indent=2) + "\n"
    print(output)

    if args.output_file is not None:
        output_path = args.output_file.resolve()
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(output, encoding="utf-8")


if __name__ == "__main__":
    main()
