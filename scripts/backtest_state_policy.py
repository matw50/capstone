#!/usr/bin/env python3
"""Backtest the current state-policy generator against historical submissions.

This is a counterfactual report, not a portal evaluator. For each week boundary it:
- uses only data available through that week
- asks the current state-policy generator what it would submit next
- compares that counterfactual point with the actual next submission
- scores closeness to the prior best basin and the next week's submitted winner

Example:
    /opt/anaconda3/bin/python scripts/backtest_state_policy.py \
        --repo-root . \
        --from-week week1 \
        --through-week week7 \
        --output-dir reports/week7_backtest
"""

from __future__ import annotations

import argparse
import json
import sys
import warnings
from pathlib import Path

import numpy as np
from sklearn.exceptions import ConvergenceWarning


SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from generate_candidate_queries import (  # noqa: E402
    choose_policy_candidate,
    count_initial_observations,
    determine_policy_state,
    load_accumulated_data,
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Backtest current state-policy recommendations.")
    parser.add_argument(
        "--repo-root",
        type=Path,
        default=Path("."),
        help="Path to the repository root. Default: current directory.",
    )
    parser.add_argument(
        "--from-week",
        default="week1",
        help="First historical boundary to replay. Default: week1.",
    )
    parser.add_argument(
        "--through-week",
        required=True,
        help="Latest completed week, for example: week7.",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=None,
        help="Output directory. Default: reports/<through-week>_backtest.",
    )
    parser.add_argument(
        "--seed",
        type=int,
        default=42,
        help="Base random seed. Default: 42.",
    )
    return parser.parse_args()


def parse_week_number(week_name: str) -> int:
    if not week_name.startswith("week"):
        raise ValueError(f"Invalid week name: {week_name}")
    return int(week_name[4:])


def load_week_result(repo_root: Path, week: int, function_id: int) -> dict | None:
    path = repo_root / f"week{week}" / "results.json"
    if not path.exists():
        return None
    with path.open("r", encoding="utf-8") as fh:
        payload = json.load(fh)
    return payload.get("functions", {}).get(str(function_id))


def format_float(value: float) -> str:
    if abs(value) >= 1000 or (abs(value) > 0 and abs(value) < 1e-4):
        return f"{value:.6e}"
    return f"{value:.6f}"


def best_source(n_initial: int, best_index: int) -> str:
    if best_index < n_initial:
        return "initial"
    return f"week{best_index - n_initial + 1}"


def nearest_support(candidate: np.ndarray, x: np.ndarray, y: np.ndarray) -> float:
    k = min(3, len(y))
    distances = np.linalg.norm(x - candidate, axis=1)
    nearest_idx = np.argsort(distances)[:k]
    mean_output = float(np.mean(y[nearest_idx]))
    return float(np.mean(y <= mean_output))


def action_type(distance_to_best: float, dimension: int) -> str:
    normalized = distance_to_best / max(np.sqrt(dimension), 1.0)
    if normalized <= 0.015:
        return "micro-local"
    if normalized <= 0.04:
        return "local"
    if normalized <= 0.08:
        return "wide-local"
    return "broad"


def compare_boundary(
    repo_root: Path,
    boundary_week: int,
    next_week: int,
    function_id: int,
    seed: int,
) -> dict | None:
    actual_payload = load_week_result(repo_root, next_week, function_id)
    if actual_payload is None:
        return None

    through_week = f"week{boundary_week}"
    x, y, _latest_payload = load_accumulated_data(repo_root, through_week, function_id)
    n_initial = count_initial_observations(repo_root, function_id)
    state = determine_policy_state(y, n_initial)
    rng = np.random.default_rng(seed + boundary_week * 100 + function_id)

    candidate, metadata = choose_policy_candidate(x, y, n_initial, rng)
    actual_input = np.array(actual_payload["input"], dtype=float)
    actual_output = float(actual_payload["output"])

    best_idx = int(np.argmax(y))
    best_input = x[best_idx]
    best_output = float(y[best_idx])

    candidate_distance_to_prior_best = float(np.linalg.norm(candidate - best_input))
    actual_distance_to_prior_best = float(np.linalg.norm(actual_input - best_input))
    candidate_distance_to_actual = float(np.linalg.norm(candidate - actual_input))

    actual_improved = bool(actual_output >= best_output)
    candidate_more_local = candidate_distance_to_prior_best < actual_distance_to_prior_best
    candidate_support = nearest_support(candidate, x, y)
    actual_support = nearest_support(actual_input, x, y)

    return {
        "boundary_week": boundary_week,
        "next_week": next_week,
        "function": function_id,
        "state": state,
        "method": metadata["selected_method"],
        "prior_best_output": best_output,
        "prior_best_source": best_source(n_initial, best_idx),
        "actual_output": actual_output,
        "actual_improved_best": actual_improved,
        "policy_candidate": candidate.tolist(),
        "actual_input": actual_input.tolist(),
        "candidate_distance_to_prior_best": candidate_distance_to_prior_best,
        "actual_distance_to_prior_best": actual_distance_to_prior_best,
        "candidate_distance_to_actual": candidate_distance_to_actual,
        "candidate_action_type": action_type(candidate_distance_to_prior_best, candidate.shape[0]),
        "actual_action_type": action_type(actual_distance_to_prior_best, actual_input.shape[0]),
        "candidate_more_local_than_actual": candidate_more_local,
        "candidate_support_percentile": candidate_support,
        "actual_support_percentile": actual_support,
        "candidate_support_minus_actual": candidate_support - actual_support,
    }


def build_report(repo_root: Path, from_week: str, through_week: str, seed: int) -> dict:
    start = parse_week_number(from_week)
    end = parse_week_number(through_week)
    if start >= end:
        raise ValueError("--from-week must be earlier than --through-week")

    rows: list[dict] = []
    for boundary_week in range(start, end):
        for function_id in range(1, 9):
            row = compare_boundary(
                repo_root=repo_root,
                boundary_week=boundary_week,
                next_week=boundary_week + 1,
                function_id=function_id,
                seed=seed,
            )
            if row is not None:
                rows.append(row)

    by_function: dict[str, dict] = {}
    for function_id in range(1, 9):
        function_rows = [row for row in rows if row["function"] == function_id]
        if not function_rows:
            continue
        by_function[str(function_id)] = {
            "n_replays": len(function_rows),
            "candidate_more_local_rate": float(np.mean([row["candidate_more_local_than_actual"] for row in function_rows])),
            "mean_support_delta": float(np.mean([row["candidate_support_minus_actual"] for row in function_rows])),
            "actual_improvements": int(sum(row["actual_improved_best"] for row in function_rows)),
            "latest_state": function_rows[-1]["state"],
            "latest_candidate_action": function_rows[-1]["candidate_action_type"],
            "latest_actual_action": function_rows[-1]["actual_action_type"],
        }

    return {
        "from_week": from_week,
        "through_week": through_week,
        "seed": seed,
        "summary": {
            "n_replays": len(rows),
            "candidate_more_local_rate": float(np.mean([row["candidate_more_local_than_actual"] for row in rows])) if rows else None,
            "mean_support_delta": float(np.mean([row["candidate_support_minus_actual"] for row in rows])) if rows else None,
        },
        "by_function": by_function,
        "rows": rows,
    }


def markdown_table(rows: list[list[str]]) -> str:
    header = rows[0]
    lines = [
        "| " + " | ".join(header) + " |",
        "| " + " | ".join("---" for _ in header) + " |",
    ]
    lines.extend("| " + " | ".join(row) + " |" for row in rows[1:])
    return "\n".join(lines)


def write_markdown(report: dict, path: Path) -> None:
    summary_rows = [["Metric", "Value"]]
    summary_rows.append(["Replays", str(report["summary"]["n_replays"])])
    summary_rows.append([
        "Policy candidate more local than actual",
        f"{report['summary']['candidate_more_local_rate']:.2%}",
    ])
    summary_rows.append([
        "Mean nearest-neighbour support delta",
        f"{report['summary']['mean_support_delta']:.3f}",
    ])

    function_rows = [["Function", "Replays", "More Local Rate", "Support Delta", "Actual Improvements", "Latest State"]]
    for function_id, payload in report["by_function"].items():
        function_rows.append(
            [
                function_id,
                str(payload["n_replays"]),
                f"{payload['candidate_more_local_rate']:.2%}",
                f"{payload['mean_support_delta']:.3f}",
                str(payload["actual_improvements"]),
                payload["latest_state"],
            ]
        )

    recent_rows = [["Boundary", "Function", "State", "Actual Improved", "Policy Move", "Actual Move", "Support Delta"]]
    for row in report["rows"][-16:]:
        recent_rows.append(
            [
                f"week{row['boundary_week']} to week{row['next_week']}",
                str(row["function"]),
                row["state"],
                "yes" if row["actual_improved_best"] else "no",
                row["candidate_action_type"],
                row["actual_action_type"],
                f"{row['candidate_support_minus_actual']:.3f}",
            ]
        )

    content = [
        f"# State Policy Backtest Through {report['through_week'].title()}",
        "",
        "This report replays historical week boundaries without future data leakage. It compares the current state-policy recommendation with the actual next submission, using locality and nearest-neighbour support as proxy checks. It does not know the true output of unsubmitted counterfactual points.",
        "",
        "## Overall Summary",
        markdown_table(summary_rows),
        "",
        "## By Function",
        markdown_table(function_rows),
        "",
        "## Recent Replays",
        markdown_table(recent_rows),
        "",
        "## Interpretation",
        "- A positive support delta means the policy candidate sat nearer stronger historical neighbours than the actual submitted point.",
        "- A high more-local rate means the policy would have stayed closer to the best-known basin than the actual submission.",
        "- This backtest is best used as a guardrail against unnecessary basin jumps, not as proof that a counterfactual point would have produced a better portal output.",
        "",
    ]
    path.write_text("\n".join(content), encoding="utf-8")


def main() -> None:
    args = parse_args()
    warnings.filterwarnings("ignore", category=ConvergenceWarning)

    repo_root = args.repo_root.resolve()
    output_dir = (
        args.output_dir.resolve()
        if args.output_dir is not None
        else repo_root / "reports" / f"{args.through_week}_backtest"
    )
    output_dir.mkdir(parents=True, exist_ok=True)

    report = build_report(repo_root, args.from_week, args.through_week, args.seed)
    json_path = output_dir / "state_policy_backtest.json"
    markdown_path = output_dir / "state_policy_backtest.md"

    json_path.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    write_markdown(report, markdown_path)

    print(f"Wrote {json_path}")
    print(f"Wrote {markdown_path}")


if __name__ == "__main__":
    main()
