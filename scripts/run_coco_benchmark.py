#!/usr/bin/env python3
"""Run a COCO/BBOB benchmark using the current capstone policy.

The benchmark mirrors the capstone structure:
- start from a small random initial design
- run a fixed number of sequential guided evaluations
- compare against a random-search continuation baseline

The capstone policy itself is imported from `generate_candidate_queries.py`:
- state-machine trust-region policy
- GP trust-region search for dimensions <= 4
- RF trust-region search for dimensions > 4
- one bounded stagnation probe before recovery

Example:
    /opt/anaconda3/bin/python scripts/run_coco_benchmark.py \
        --repo-root . \
        --initial-design 10 \
        --sequential-budget 13 \
        --dimensions 2,3,4,5,6,8 \
        --instances 1
"""

from __future__ import annotations

import argparse
import csv
import json
import time
import warnings
from pathlib import Path

import cocoex
import numpy as np
from sklearn.exceptions import ConvergenceWarning

from generate_candidate_queries import choose_policy_candidate


METHOD_CAPSTONE = "capstone_state_policy"
METHOD_RANDOM = "random_continuation"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run a COCO/BBOB benchmark for the capstone policy.")
    parser.add_argument(
        "--repo-root",
        type=Path,
        default=Path("."),
        help="Path to the repository root. Default: current directory.",
    )
    parser.add_argument(
        "--suite",
        default="bbob",
        help="COCO suite name. Default: bbob",
    )
    parser.add_argument(
        "--dimensions",
        default="2,3,4,5,6,8",
        help="Comma-separated list of dimensions. Default: 2,3,4,5,6,8",
    )
    parser.add_argument(
        "--instances",
        default="1",
        help="Comma-separated list of COCO instance indices. Default: 1",
    )
    parser.add_argument(
        "--initial-design",
        type=int,
        default=10,
        help="Number of random initial evaluations before guided search. Default: 10",
    )
    parser.add_argument(
        "--sequential-budget",
        type=int,
        default=13,
        help="Number of guided evaluations after the initial design. Default: 13",
    )
    parser.add_argument(
        "--seed",
        type=int,
        default=42,
        help="Base random seed. Default: 42",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=None,
        help="Optional output directory. Default: benchmarks/coco/week6_style_budget<budget>",
    )
    parser.add_argument(
        "--log-every",
        type=int,
        default=6,
        help="Print progress every N problems. Default: 6",
    )
    return parser.parse_args()


def parse_int_list(text: str) -> list[int]:
    return [int(part.strip()) for part in text.split(",") if part.strip()]


def suite_filter(dimensions: list[int], instances: list[int]) -> str:
    dim_text = ",".join(str(value) for value in dimensions)
    instance_text = ",".join(str(value) for value in instances)
    return f"dimensions: {dim_text} instance_indices: {instance_text}"


def to_domain(unit_point: np.ndarray, lower: np.ndarray, upper: np.ndarray) -> np.ndarray:
    return lower + unit_point * (upper - lower)


def evaluate_unit(problem: cocoex.Problem, unit_point: np.ndarray) -> float:
    x_domain = to_domain(unit_point, problem.lower_bounds, problem.upper_bounds)
    return float(problem(x_domain))


def initial_design(problem: cocoex.Problem, n_points: int, rng: np.random.Generator) -> tuple[np.ndarray, np.ndarray]:
    x_unit = rng.uniform(0.0, 1.0, size=(n_points, problem.dimension))
    y_reward = np.empty(n_points, dtype=float)
    for i in range(n_points):
        fval = evaluate_unit(problem, x_unit[i])
        y_reward[i] = -fval
    return x_unit, y_reward


def choose_capstone_candidate(
    x_unit: np.ndarray,
    y_reward: np.ndarray,
    n_initial: int,
    rng: np.random.Generator,
) -> tuple[np.ndarray, str]:
    candidate, metadata = choose_policy_candidate(x_unit, y_reward, n_initial, rng)
    method = str(metadata["selected_method"])
    return np.clip(candidate, 0.0, 1.0), method


def run_method(
    problem: cocoex.Problem,
    method_name: str,
    x_init: np.ndarray,
    y_init: np.ndarray,
    n_initial: int,
    sequential_budget: int,
    rng: np.random.Generator,
) -> dict:
    x_unit = np.array(x_init, copy=True)
    y_reward = np.array(y_init, copy=True)
    best_so_far_f = [float(np.min(-y_reward))]
    proposal_methods: list[str] = ["initial_design"] * len(y_reward)

    for _step in range(sequential_budget):
        if method_name == METHOD_CAPSTONE:
            candidate, proposal_method = choose_capstone_candidate(x_unit, y_reward, n_initial, rng)
        elif method_name == METHOD_RANDOM:
            candidate = rng.uniform(0.0, 1.0, size=problem.dimension)
            proposal_method = "random_uniform"
        else:
            raise ValueError(f"Unknown method: {method_name}")

        fval = evaluate_unit(problem, candidate)
        reward = -fval
        x_unit = np.vstack([x_unit, candidate])
        y_reward = np.append(y_reward, reward)
        best_so_far_f.append(float(np.min(-y_reward)))
        proposal_methods.append(proposal_method)

    return {
        "method": method_name,
        "best_f": float(np.min(-y_reward)),
        "best_reward": float(np.max(y_reward)),
        "final_target_hit": bool(problem.final_target_hit),
        "n_evaluations": int(problem.evaluations),
        "history_best_f": best_so_far_f,
        "proposal_methods": proposal_methods,
        "x_shape": list(x_unit.shape),
    }


def summarize_pairwise(rows: list[dict]) -> dict:
    paired: dict[str, dict[str, dict]] = {}
    for row in rows:
        paired.setdefault(row["problem_id"], {})[row["method"]] = row

    wins = 0
    losses = 0
    ties = 0
    by_dimension: dict[int, dict[str, int]] = {}

    for problem_id, methods in paired.items():
        if METHOD_CAPSTONE not in methods or METHOD_RANDOM not in methods:
            continue
        cap = methods[METHOD_CAPSTONE]
        rnd = methods[METHOD_RANDOM]
        dim = int(cap["dimension"])
        by_dimension.setdefault(dim, {"wins": 0, "losses": 0, "ties": 0})

        cap_best_f = float(cap["best_f"])
        rnd_best_f = float(rnd["best_f"])

        if cap_best_f < rnd_best_f:
            wins += 1
            by_dimension[dim]["wins"] += 1
        elif cap_best_f > rnd_best_f:
            losses += 1
            by_dimension[dim]["losses"] += 1
        else:
            ties += 1
            by_dimension[dim]["ties"] += 1

    total = wins + losses + ties
    return {
        "wins": wins,
        "losses": losses,
        "ties": ties,
        "total_compared": total,
        "win_rate": (wins / total) if total else None,
        "by_dimension": by_dimension,
    }


def main() -> None:
    args = parse_args()
    repo_root = args.repo_root.resolve()
    dimensions = parse_int_list(args.dimensions)
    instances = parse_int_list(args.instances)

    warnings.filterwarnings("ignore", category=ConvergenceWarning)

    if args.output_dir is None:
        output_dir = repo_root / "benchmarks" / "coco" / f"week6_style_budget{args.sequential_budget}"
    else:
        output_dir = args.output_dir.resolve()
    output_dir.mkdir(parents=True, exist_ok=True)

    suite = cocoex.Suite(args.suite, "", suite_filter(dimensions, instances))
    suite_random = cocoex.Suite(args.suite, "", suite_filter(dimensions, instances))
    total_problems = len(suite)
    rows: list[dict] = []
    histories: dict[str, dict[str, list[float] | list[str]]] = {}
    start_time = time.time()

    for suite_position, problem in enumerate(suite):
        problem_key = problem.id
        init_rng = np.random.default_rng(args.seed + 10_000 + problem.index)
        cap_rng = np.random.default_rng(args.seed + 20_000 + problem.index)
        rnd_rng = np.random.default_rng(args.seed + 30_000 + problem.index)

        x_init, y_init = initial_design(problem, args.initial_design, init_rng)
        initial_best_f = float(np.min(-y_init))

        capstone_result = run_method(
            problem=problem,
            method_name=METHOD_CAPSTONE,
            x_init=x_init,
            y_init=y_init,
            n_initial=args.initial_design,
            sequential_budget=args.sequential_budget,
            rng=cap_rng,
        )

        problem_random = suite_random.get_problem(suite_position)
        x_init_random, y_init_random = initial_design(problem_random, args.initial_design, np.random.default_rng(args.seed + 10_000 + problem.index))
        random_result = run_method(
            problem=problem_random,
            method_name=METHOD_RANDOM,
            x_init=x_init_random,
            y_init=y_init_random,
            n_initial=args.initial_design,
            sequential_budget=args.sequential_budget,
            rng=rnd_rng,
        )

        for result in (capstone_result, random_result):
            row = {
                "suite": args.suite,
                "problem_id": problem_key,
                "problem_name": problem.name,
                "dimension": int(problem.dimension),
                "initial_design": args.initial_design,
                "sequential_budget": args.sequential_budget,
                "method": result["method"],
                "initial_best_f": initial_best_f,
                "best_f": result["best_f"],
                "best_reward": result["best_reward"],
                "final_target_hit": result["final_target_hit"],
                "n_evaluations": result["n_evaluations"],
            }
            rows.append(row)
            histories.setdefault(problem_key, {})[result["method"]] = {
                "history_best_f": result["history_best_f"],
                "proposal_methods": result["proposal_methods"],
            }

        if hasattr(problem, "free"):
            problem.free()
        if hasattr(problem_random, "free"):
            problem_random.free()

        if (
            (suite_position + 1) % args.log_every == 0
            or suite_position + 1 == total_problems
        ):
            elapsed = time.time() - start_time
            completed = suite_position + 1
            per_problem = elapsed / completed
            remaining = total_problems - completed
            eta_seconds = per_problem * remaining
            print(
                f"[progress] completed {completed}/{total_problems} problems "
                f"in {elapsed:.1f}s, eta {eta_seconds:.1f}s",
                flush=True,
            )

    pairwise = summarize_pairwise(rows)
    summary = {
        "suite": args.suite,
        "requested_dimensions": dimensions,
        "instances": instances,
        "initial_design": args.initial_design,
        "sequential_budget": args.sequential_budget,
        "seed": args.seed,
        "n_problems": len({row["problem_id"] for row in rows}),
        "actual_dimensions": sorted({int(row["dimension"]) for row in rows}),
        "methods": [METHOD_CAPSTONE, METHOD_RANDOM],
        "pairwise_vs_random": pairwise,
    }

    csv_path = output_dir / "results.csv"
    with csv_path.open("w", encoding="utf-8", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)

    summary_path = output_dir / "summary.json"
    summary_path.write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")

    histories_path = output_dir / "histories.json"
    histories_path.write_text(json.dumps(histories, indent=2) + "\n", encoding="utf-8")

    print(json.dumps(summary, indent=2))
    print(f"Wrote {csv_path}")
    print(f"Wrote {summary_path}")
    print(f"Wrote {histories_path}")


if __name__ == "__main__":
    main()
