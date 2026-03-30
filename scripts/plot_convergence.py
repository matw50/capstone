#!/usr/bin/env python3
"""Plot convergence curves for the capstone functions.

The script loads the initial observations plus appended weekly results through a
chosen week, then writes one convergence plot per function showing:
- observed output by evaluation order
- best-so-far output by evaluation order
- markers for weekly submissions
- annotation for the current best observation
- optional marker for the next candidate submission
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Plot convergence curves for the capstone functions.")
    parser.add_argument(
        "--repo-root",
        type=Path,
        default=Path("."),
        help="Path to the repository root. Default: current directory.",
    )
    parser.add_argument(
        "--through-week",
        required=True,
        help="Use results up to and including this week, for example: week2",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        required=True,
        help="Directory where the plot PNGs should be written.",
    )
    parser.add_argument(
        "--candidate-file",
        type=Path,
        default=None,
        help="Optional JSON file containing next-round candidate inputs.",
    )
    return parser.parse_args()


def parse_week_number(week_name: str) -> int:
    if not week_name.startswith("week"):
        raise ValueError(f"Invalid week name: {week_name}")
    return int(week_name[4:])


def load_outputs(repo_root: Path, through_week: str, function_id: int) -> tuple[np.ndarray, list[tuple[int, int, float]]]:
    initial_dir = repo_root / "initial_data" / f"function_{function_id}"
    y = np.load(initial_dir / "initial_outputs.npy")
    submissions: list[tuple[int, int, float]] = []

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
        y = np.append(y, float(payload["output"]))
        submissions.append((week, len(y), float(payload["output"])))

    return y, submissions


def load_candidate_inputs(candidate_file: Path | None) -> dict[str, list[float]] | None:
    if candidate_file is None:
        return None
    with candidate_file.open("r", encoding="utf-8") as fh:
        payload = json.load(fh)
    if "functions" in payload:
        return payload["functions"]
    if "recommendations" in payload:
        return {
            key: value["candidate"]
            for key, value in payload["recommendations"].items()
        }
    raise KeyError("Candidate file must contain either 'functions' or 'recommendations'.")


def main() -> None:
    args = parse_args()
    repo_root = args.repo_root.resolve()
    output_dir = args.output_dir.resolve()
    output_dir.mkdir(parents=True, exist_ok=True)
    candidate_inputs = load_candidate_inputs(
        None if args.candidate_file is None else args.candidate_file.resolve()
    )

    all_outputs: list[tuple[int, np.ndarray, list[tuple[int, int, float]]]] = []
    for function_id in range(1, 9):
        y, submissions = load_outputs(repo_root, args.through_week, function_id)
        all_outputs.append((function_id, y, submissions))
        x = np.arange(1, len(y) + 1)
        best_so_far = np.maximum.accumulate(y)
        best_idx = int(np.argmax(y))
        best_eval = best_idx + 1
        best_val = float(y[best_idx])

        plt.figure(figsize=(8, 4.5))
        plt.plot(x, y, marker="o", linewidth=1.5, label="Observed output", color="#4472C4")
        plt.plot(x, best_so_far, linewidth=2.0, label="Best so far", color="#C00000")
        for week, eval_idx, output in submissions:
            plt.scatter(eval_idx, output, s=65, color="#70AD47", edgecolors="black", linewidths=0.6, zorder=4)
            plt.annotate(
                f"W{week}",
                (eval_idx, output),
                textcoords="offset points",
                xytext=(0, 8),
                ha="center",
                fontsize=8,
                color="#2F5597",
            )
        plt.scatter(best_eval, best_val, s=90, marker="*", color="#FFC000", edgecolors="black", linewidths=0.6, zorder=5)
        plt.annotate(
            f"Best ({best_eval})",
            (best_eval, best_val),
            textcoords="offset points",
            xytext=(8, -12),
            ha="left",
            fontsize=8,
            color="#7F6000",
        )
        if candidate_inputs is not None and str(function_id) in candidate_inputs:
            candidate_eval = len(y) + 1
            recent_window = y[-5:] if len(y) >= 5 else y
            candidate_y = float(np.median(recent_window))
            plt.scatter(
                candidate_eval,
                candidate_y,
                s=75,
                marker="D",
                color="#7030A0",
                edgecolors="black",
                linewidths=0.6,
                zorder=5,
            )
            plt.annotate(
                "Candidate",
                (candidate_eval, candidate_y),
                textcoords="offset points",
                xytext=(-4, 8),
                ha="right",
                fontsize=8,
                color="#7030A0",
            )
        plt.xlabel("Evaluation")
        plt.ylabel("Output")
        plt.title(f"Function {function_id} convergence through {args.through_week}")
        plt.grid(alpha=0.25)
        plt.legend()
        plt.tight_layout()
        plt.savefig(output_dir / f"function_{function_id}_convergence.png", dpi=160)
        plt.close()

    fig, axes = plt.subplots(2, 4, figsize=(16, 8))
    for ax, (function_id, y, submissions) in zip(axes.flat, all_outputs):
        x = np.arange(1, len(y) + 1)
        best_so_far = np.maximum.accumulate(y)
        best_idx = int(np.argmax(y))
        ax.plot(x, y, marker="o", linewidth=1.2, color="#4472C4")
        ax.plot(x, best_so_far, linewidth=1.8, color="#C00000")
        for week, eval_idx, output in submissions:
            ax.scatter(eval_idx, output, s=24, color="#70AD47", edgecolors="black", linewidths=0.4, zorder=4)
            ax.annotate(f"W{week}", (eval_idx, output), textcoords="offset points", xytext=(0, 5), ha="center", fontsize=6)
        ax.scatter(best_idx + 1, y[best_idx], s=40, marker="*", color="#FFC000", edgecolors="black", linewidths=0.4, zorder=5)
        if candidate_inputs is not None and str(function_id) in candidate_inputs:
            candidate_eval = len(y) + 1
            recent_window = y[-5:] if len(y) >= 5 else y
            candidate_y = float(np.median(recent_window))
            ax.scatter(candidate_eval, candidate_y, s=28, marker="D", color="#7030A0", edgecolors="black", linewidths=0.4, zorder=5)
            ax.annotate("C", (candidate_eval, candidate_y), textcoords="offset points", xytext=(0, 5), ha="center", fontsize=6, color="#7030A0")
        ax.set_title(f"Function {function_id}")
        ax.grid(alpha=0.25)
    fig.suptitle(f"Convergence through {args.through_week}")
    fig.tight_layout()
    fig.savefig(output_dir / "all_functions_convergence.png", dpi=180)
    plt.close(fig)


if __name__ == "__main__":
    main()
