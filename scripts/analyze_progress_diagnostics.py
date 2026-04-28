#!/usr/bin/env python3
"""Analyze capstone progress before choosing the next BBO submission.

The report focuses on two practical questions:
- Which coordinates appear sensitive in recent successful or failed moves?
- Which functions are in momentum, refine, or recovery mode based on history?

Example:
    /opt/anaconda3/bin/python scripts/analyze_progress_diagnostics.py \
        --repo-root . \
        --through-week week7 \
        --output-dir reports/week7_diagnostics
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Create capstone progress diagnostics.")
    parser.add_argument(
        "--repo-root",
        type=Path,
        default=Path("."),
        help="Path to the repository root. Default: current directory.",
    )
    parser.add_argument(
        "--through-week",
        required=True,
        help="Use results up to and including this week, for example: week7.",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=None,
        help="Directory for report files. Default: reports/<through-week>_diagnostics.",
    )
    parser.add_argument(
        "--recent-moves",
        type=int,
        default=5,
        help="Number of recent guided moves to use for sensitivity. Default: 5.",
    )
    return parser.parse_args()


def parse_week_number(week_name: str) -> int:
    if not week_name.startswith("week"):
        raise ValueError(f"Invalid week name: {week_name}")
    return int(week_name[4:])


def load_history(repo_root: Path, through_week: str, function_id: int) -> dict:
    initial_dir = repo_root / "initial_data" / f"function_{function_id}"
    x_initial = np.load(initial_dir / "initial_inputs.npy")
    y_initial = np.load(initial_dir / "initial_outputs.npy").astype(float)

    weekly: list[dict] = []
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
        weekly.append(
            {
                "week": week,
                "input": np.array(payload["input"], dtype=float),
                "output": float(payload["output"]),
            }
        )

    x_weekly = np.vstack([item["input"] for item in weekly]) if weekly else np.empty((0, x_initial.shape[1]))
    y_weekly = np.array([item["output"] for item in weekly], dtype=float)

    return {
        "x_initial": x_initial,
        "y_initial": y_initial,
        "weekly": weekly,
        "x_all": np.vstack([x_initial, x_weekly]),
        "y_all": np.append(y_initial, y_weekly),
        "n_initial": int(len(y_initial)),
    }


def best_source(n_initial: int, best_index: int) -> str:
    if best_index < n_initial:
        return "initial"
    return f"week{best_index - n_initial + 1}"


def latest_state(y_all: np.ndarray, n_initial: int) -> tuple[str, int]:
    if len(y_all) <= n_initial:
        return "bootstrap", 0

    weekly_outputs = y_all[n_initial:]
    best_before_weekly = float(np.max(y_all[:n_initial]))
    last_improvement_week_index = -1
    running_best = best_before_weekly

    for idx, output in enumerate(weekly_outputs):
        if output >= running_best:
            running_best = float(output)
            last_improvement_week_index = idx

    streak = len(weekly_outputs) - 1 - last_improvement_week_index
    if weekly_outputs[-1] >= np.max(y_all[:-1]):
        return "momentum", 0
    if streak == 1:
        return "refine", streak
    if streak == 2:
        return "stagnant", streak
    return "recovery", streak


def classify_action(distance_to_best: float, dimension: int) -> str:
    scale = max(np.sqrt(dimension), 1.0)
    normalized = distance_to_best / scale
    if normalized <= 0.015:
        return "micro-local"
    if normalized <= 0.04:
        return "local"
    if normalized <= 0.08:
        return "wide-local"
    return "broad"


def week_outcomes(history: dict) -> list[dict]:
    x_seen = history["x_initial"].copy()
    y_seen = history["y_initial"].copy()
    rows: list[dict] = []

    for item in history["weekly"]:
        point = item["input"]
        output = item["output"]
        best_idx = int(np.argmax(y_seen))
        best_input = x_seen[best_idx]
        latest_input = x_seen[-1]
        best_before = float(y_seen[best_idx])
        improved = bool(output >= best_before)

        rows.append(
            {
                "week": item["week"],
                "output": output,
                "best_before": best_before,
                "improved_best": improved,
                "distance_to_prior_best": float(np.linalg.norm(point - best_input)),
                "distance_to_latest": float(np.linalg.norm(point - latest_input)),
                "action_type": classify_action(float(np.linalg.norm(point - best_input)), point.shape[0]),
            }
        )

        x_seen = np.vstack([x_seen, point])
        y_seen = np.append(y_seen, output)

    return rows


def sensitivity(history: dict, recent_moves: int) -> dict:
    weekly = history["weekly"]
    dim = history["x_initial"].shape[1]
    if len(weekly) < 2:
        return {
            "status": "insufficient_weekly_moves",
            "scores": [0.0] * dim,
            "top_coordinates": [],
        }

    points = np.vstack([item["input"] for item in weekly])
    outputs = np.array([item["output"] for item in weekly], dtype=float)

    dx = np.diff(points, axis=0)
    dy = np.diff(outputs)
    if recent_moves > 0:
        dx = dx[-recent_moves:]
        dy = dy[-recent_moves:]

    y_scale = float(np.ptp(outputs))
    if y_scale <= 1e-12:
        y_scale = max(float(np.max(np.abs(outputs))), 1.0)

    scores = []
    for coord in range(dim):
        denom = float(np.sum(np.abs(dx[:, coord]))) + 1e-12
        score = float(np.sum(dx[:, coord] * (dy / y_scale)) / denom)
        scores.append(score)

    top = sorted(
        [
            {
                "coordinate": idx + 1,
                "score": score,
                "direction": "increase" if score > 0 else "decrease" if score < 0 else "flat",
                "strength": abs(score),
            }
            for idx, score in enumerate(scores)
        ],
        key=lambda item: item["strength"],
        reverse=True,
    )

    return {
        "status": "ok",
        "scores": scores,
        "top_coordinates": top[: min(3, dim)],
    }


def next_read(state: str, sensitivity_payload: dict, latest_improved: bool) -> str:
    top = sensitivity_payload.get("top_coordinates", [])
    if top:
        coord_text = ", ".join(
            f"x{item['coordinate']} {item['direction']}" for item in top[:2]
        )
    else:
        coord_text = "no strong coordinate signal"

    if state == "momentum":
        return f"Exploit locally; consider moving mainly along {coord_text}."
    if state == "refine":
        return f"Return toward historical best; use {coord_text} cautiously."
    if state == "stagnant":
        return f"Compare a local point against one bounded alternative; sensitivity says {coord_text}."
    if state == "recovery":
        return f"Reset to best basin before exploring; sensitivity says {coord_text}."
    return "Bootstrap from best observed basin."


def markdown_table(rows: list[list[str]]) -> str:
    if not rows:
        return ""
    header = rows[0]
    body = rows[1:]
    lines = [
        "| " + " | ".join(header) + " |",
        "| " + " | ".join("---" for _ in header) + " |",
    ]
    lines.extend("| " + " | ".join(row) + " |" for row in body)
    return "\n".join(lines)


def format_float(value: float) -> str:
    if abs(value) >= 1000 or (abs(value) > 0 and abs(value) < 1e-4):
        return f"{value:.6e}"
    return f"{value:.6f}"


def build_report(repo_root: Path, through_week: str, recent_moves: int) -> dict:
    functions: dict[str, dict] = {}

    for function_id in range(1, 9):
        history = load_history(repo_root, through_week, function_id)
        y_all = history["y_all"]
        x_all = history["x_all"]
        n_initial = history["n_initial"]
        best_idx = int(np.argmax(y_all))
        state, streak = latest_state(y_all, n_initial)
        weekly_rows = week_outcomes(history)
        latest_improved = bool(weekly_rows[-1]["improved_best"]) if weekly_rows else False
        sensitivity_payload = sensitivity(history, recent_moves)

        functions[str(function_id)] = {
            "dimension": int(x_all.shape[1]),
            "observations": int(len(y_all)),
            "best_output": float(y_all[best_idx]),
            "best_input": x_all[best_idx].tolist(),
            "best_source": best_source(n_initial, best_idx),
            "latest_output": float(y_all[-1]),
            "latest_state": state,
            "non_improving_streak": streak,
            "week_outcomes": weekly_rows,
            "sensitivity": sensitivity_payload,
            "next_read": next_read(state, sensitivity_payload, latest_improved),
        }

    return {
        "through_week": through_week,
        "recent_moves": recent_moves,
        "functions": functions,
    }


def write_markdown(report: dict, path: Path) -> None:
    rows = [["Function", "Best", "Source", "Latest", "State", "Read"]]
    sensitivity_rows = [["Function", "Top Coordinate Signals"]]

    for function_id, payload in report["functions"].items():
        rows.append(
            [
                function_id,
                format_float(payload["best_output"]),
                payload["best_source"],
                format_float(payload["latest_output"]),
                f"{payload['latest_state']} ({payload['non_improving_streak']})",
                payload["next_read"],
            ]
        )

        top = payload["sensitivity"].get("top_coordinates", [])
        if top:
            signal = ", ".join(
                f"x{item['coordinate']} {item['direction']} ({item['strength']:.3f})"
                for item in top
            )
        else:
            signal = payload["sensitivity"]["status"]
        sensitivity_rows.append([function_id, signal])

    content = [
        f"# Progress Diagnostics Through {report['through_week'].title()}",
        "",
        "This report is a lightweight pre-submission diagnostic. It does not choose queries directly; it highlights function state, recent coordinate sensitivity, and where the next round should be cautious.",
        "",
        "## Function Summary",
        markdown_table(rows),
        "",
        "## Coordinate Sensitivity",
        markdown_table(sensitivity_rows),
        "",
        "## Notes",
        "- `State` follows the current capstone policy language: momentum, refine, stagnant, or recovery.",
        "- Coordinate signals are estimated from recent weekly moves only, so they should guide manual review rather than override observed best basins.",
        "- A positive coordinate score means recent increases in that coordinate tended to align with better outputs; a negative score means decreases tended to align with better outputs.",
        "",
    ]
    path.write_text("\n".join(content), encoding="utf-8")


def main() -> None:
    args = parse_args()
    repo_root = args.repo_root.resolve()
    output_dir = (
        args.output_dir.resolve()
        if args.output_dir is not None
        else repo_root / "reports" / f"{args.through_week}_diagnostics"
    )
    output_dir.mkdir(parents=True, exist_ok=True)

    report = build_report(repo_root, args.through_week, args.recent_moves)
    json_path = output_dir / "progress_diagnostics.json"
    markdown_path = output_dir / "progress_diagnostics.md"

    json_path.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    write_markdown(report, markdown_path)

    print(f"Wrote {json_path}")
    print(f"Wrote {markdown_path}")


if __name__ == "__main__":
    main()
