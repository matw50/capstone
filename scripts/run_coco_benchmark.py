#!/usr/bin/env python3
"""Run a COCO/BBOB benchmark using the current capstone policy.

The benchmark mirrors the capstone structure:
- start from a small random initial design
- run a fixed number of sequential guided evaluations
- compare against a random-search continuation baseline

The capstone policy itself is imported from `generate_candidate_queries.py`:
- state-machine trust-region policy
- ranked three-candidate selection layer
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

from generate_candidate_queries import choose_policy_candidate, choose_ranked_policy_candidate


METHOD_STATE = "capstone_state_policy"
METHOD_RANKED = "capstone_ranked_policy"
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
        help="Optional output directory. Default: benchmarks/coco/policy_comparison_budget<budget>",
    )
    parser.add_argument(
        "--log-every",
        type=int,
        default=6,
        help="Print progress every N problems. Default: 6",
    )
    parser.add_argument(
        "--methods",
        default="state,ranked,random",
        help="Comma-separated benchmark methods. Choices: state, ranked, random. Default: state,ranked,random",
    )
    return parser.parse_args()


def parse_int_list(text: str) -> list[int]:
    return [int(part.strip()) for part in text.split(",") if part.strip()]


def parse_method_list(text: str) -> list[str]:
    mapping = {
        "state": METHOD_STATE,
        "ranked": METHOD_RANKED,
        "random": METHOD_RANDOM,
    }
    methods: list[str] = []
    for part in text.split(","):
        key = part.strip().lower()
        if not key:
            continue
        if key not in mapping:
            raise ValueError(f"Unknown benchmark method: {part}")
        methods.append(mapping[key])
    if not methods:
        raise ValueError("At least one benchmark method must be specified.")
    return methods


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
    return x_unit, evaluate_design(problem, x_unit)


def evaluate_design(problem: cocoex.Problem, x_unit: np.ndarray) -> np.ndarray:
    y_reward = np.empty(x_unit.shape[0], dtype=float)
    for i in range(x_unit.shape[0]):
        fval = evaluate_unit(problem, x_unit[i])
        y_reward[i] = -fval
    return y_reward


def choose_capstone_candidate(
    x_unit: np.ndarray,
    y_reward: np.ndarray,
    n_initial: int,
    rng: np.random.Generator,
    method_name: str,
) -> tuple[np.ndarray, str]:
    if method_name == METHOD_STATE:
        candidate, metadata = choose_policy_candidate(x_unit, y_reward, n_initial, rng)
    elif method_name == METHOD_RANKED:
        candidate, metadata = choose_ranked_policy_candidate(x_unit, y_reward, n_initial, rng)
    else:
        raise ValueError(f"Unknown capstone method: {method_name}")
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
        if method_name in {METHOD_STATE, METHOD_RANKED}:
            candidate, proposal_method = choose_capstone_candidate(
                x_unit,
                y_reward,
                n_initial,
                rng,
                method_name,
            )
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


def summarize_pairwise(rows: list[dict], lhs_method: str, rhs_method: str) -> dict:
    paired: dict[str, dict[str, dict]] = {}
    for row in rows:
        paired.setdefault(row["problem_id"], {})[row["method"]] = row

    wins = 0
    losses = 0
    ties = 0
    by_dimension: dict[int, dict[str, int]] = {}

    for problem_id, methods in paired.items():
        if lhs_method not in methods or rhs_method not in methods:
            continue
        lhs = methods[lhs_method]
        rhs = methods[rhs_method]
        dim = int(lhs["dimension"])
        by_dimension.setdefault(dim, {"wins": 0, "losses": 0, "ties": 0})

        lhs_best_f = float(lhs["best_f"])
        rhs_best_f = float(rhs["best_f"])

        if lhs_best_f < rhs_best_f:
            wins += 1
            by_dimension[dim]["wins"] += 1
        elif lhs_best_f > rhs_best_f:
            losses += 1
            by_dimension[dim]["losses"] += 1
        else:
            ties += 1
            by_dimension[dim]["ties"] += 1

    total = wins + losses + ties
    return {
        "lhs_method": lhs_method,
        "rhs_method": rhs_method,
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
    methods = parse_method_list(args.methods)

    warnings.filterwarnings("ignore", category=ConvergenceWarning)

    if args.output_dir is None:
        output_dir = repo_root / "benchmarks" / "coco" / f"policy_comparison_budget{args.sequential_budget}"
    else:
        output_dir = args.output_dir.resolve()
    output_dir.mkdir(parents=True, exist_ok=True)

    primary_method = methods[0]
    primary_suite = cocoex.Suite(args.suite, "", suite_filter(dimensions, instances))
    secondary_suites = {
        method: cocoex.Suite(args.suite, "", suite_filter(dimensions, instances))
        for method in methods[1:]
    }
    total_problems = len(primary_suite)
    rows: list[dict] = []
    histories: dict[str, dict[str, list[float] | list[str]]] = {}
    start_time = time.time()

    for suite_position, primary_problem in enumerate(primary_suite):
        problem_key = primary_problem.id
        init_rng = np.random.default_rng(args.seed + 10_000 + primary_problem.index)
        x_init_unit = init_rng.uniform(0.0, 1.0, size=(args.initial_design, primary_problem.dimension))

        method_results: list[tuple[cocoex.Problem, dict]] = []
        initial_best_f: float | None = None

        for method_offset, method_name in enumerate(methods):
            if method_name == primary_method:
                problem = primary_problem
            else:
                problem = secondary_suites[method_name].get_problem(suite_position)

            y_init = evaluate_design(problem, x_init_unit)
            if initial_best_f is None:
                initial_best_f = float(np.min(-y_init))
            method_rng = np.random.default_rng(args.seed + (20_000 * (method_offset + 1)) + primary_problem.index)
            result = run_method(
                problem=problem,
                method_name=method_name,
                x_init=x_init_unit,
                y_init=y_init,
                n_initial=args.initial_design,
                sequential_budget=args.sequential_budget,
                rng=method_rng,
            )
            method_results.append((problem, result))

        for problem, result in method_results:
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

        for problem, _result in method_results:
            if hasattr(problem, "free"):
                problem.free()

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

    pairwise: dict[str, dict] = {}
    if METHOD_RANKED in methods and METHOD_STATE in methods:
        pairwise["ranked_vs_state"] = summarize_pairwise(rows, METHOD_RANKED, METHOD_STATE)
    if METHOD_RANKED in methods and METHOD_RANDOM in methods:
        pairwise["ranked_vs_random"] = summarize_pairwise(rows, METHOD_RANKED, METHOD_RANDOM)
    if METHOD_STATE in methods and METHOD_RANDOM in methods:
        pairwise["state_vs_random"] = summarize_pairwise(rows, METHOD_STATE, METHOD_RANDOM)

    summary = {
        "suite": args.suite,
        "requested_dimensions": dimensions,
        "instances": instances,
        "initial_design": args.initial_design,
        "sequential_budget": args.sequential_budget,
        "seed": args.seed,
        "n_problems": len({row["problem_id"] for row in rows}),
        "actual_dimensions": sorted({int(row["dimension"]) for row in rows}),
        "methods": methods,
        "pairwise": pairwise,
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
