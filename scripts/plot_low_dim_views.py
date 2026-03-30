#!/usr/bin/env python3
"""Generate low-dimensional exploratory visuals for Functions 1 to 4.

Outputs:
- Function 1: 2D scatter with output coloring
- Function 2: 2D scatter with output coloring
- Function 3: 3D scatter with output coloring
- Function 4: 4x4 pairwise scatter matrix with output coloring

Optional candidate inputs can be overlaid from a week inputs file or a generated
candidate file.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.mplot3d import Axes3D  # noqa: F401


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Generate low-dimensional capstone visuals.")
    parser.add_argument("--repo-root", type=Path, default=Path("."), help="Repository root.")
    parser.add_argument("--through-week", required=True, help="Use results up to and including this week.")
    parser.add_argument("--output-dir", type=Path, required=True, help="Directory for PNG outputs.")
    parser.add_argument(
        "--candidate-file",
        type=Path,
        default=None,
        help="Optional JSON file containing candidate inputs to overlay.",
    )
    return parser.parse_args()


def parse_week_number(week_name: str) -> int:
    if not week_name.startswith("week"):
        raise ValueError(f"Invalid week name: {week_name}")
    return int(week_name[4:])


def load_candidate_inputs(candidate_file: Path | None) -> dict[str, list[float]] | None:
    if candidate_file is None:
        return None
    with candidate_file.open("r", encoding="utf-8") as fh:
        payload = json.load(fh)
    if "functions" in payload:
        return payload["functions"]
    if "recommendations" in payload:
        return {key: value["candidate"] for key, value in payload["recommendations"].items()}
    raise KeyError("Candidate file must contain either 'functions' or 'recommendations'.")


def load_accumulated_data(repo_root: Path, through_week: str, function_id: int) -> tuple[np.ndarray, np.ndarray]:
    initial_dir = repo_root / "initial_data" / f"function_{function_id}"
    x = np.load(initial_dir / "initial_inputs.npy")
    y = np.load(initial_dir / "initial_outputs.npy")
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
    return x, y


def output_colors(y: np.ndarray) -> np.ndarray:
    # robust scaling for visibility with outliers/sparse values
    lo, hi = np.percentile(y, [5, 95])
    if hi <= lo:
        return y
    return np.clip((y - lo) / (hi - lo), 0.0, 1.0)


def add_candidate_2d(ax, candidate: np.ndarray | None) -> None:
    if candidate is None:
        return
    ax.scatter(candidate[0], candidate[1], marker="D", s=90, color="#7030A0", edgecolors="black", linewidths=0.8, zorder=5)
    ax.annotate("Candidate", (candidate[0], candidate[1]), textcoords="offset points", xytext=(6, 6), fontsize=8, color="#7030A0")


def plot_2d(x: np.ndarray, y: np.ndarray, function_id: int, output_path: Path, candidate: np.ndarray | None) -> None:
    c = output_colors(y)
    best_idx = int(np.argmax(y))
    fig, ax = plt.subplots(figsize=(6, 5))
    sc = ax.scatter(x[:, 0], x[:, 1], c=c, cmap="viridis", s=48, edgecolors="white", linewidths=0.4)
    ax.scatter(x[best_idx, 0], x[best_idx, 1], marker="*", s=140, color="#FFC000", edgecolors="black", linewidths=0.8, zorder=4)
    ax.annotate("Best", (x[best_idx, 0], x[best_idx, 1]), textcoords="offset points", xytext=(6, -10), fontsize=8, color="#7F6000")
    add_candidate_2d(ax, candidate)
    ax.set_xlabel("x1")
    ax.set_ylabel("x2")
    ax.set_title(f"Function {function_id} scatter through observations")
    ax.grid(alpha=0.25)
    fig.colorbar(sc, ax=ax, label="Scaled output")
    fig.tight_layout()
    fig.savefig(output_path, dpi=170)
    plt.close(fig)


def plot_3d(x: np.ndarray, y: np.ndarray, output_path: Path, candidate: np.ndarray | None) -> None:
    c = output_colors(y)
    best_idx = int(np.argmax(y))
    fig = plt.figure(figsize=(7, 5.5))
    ax = fig.add_subplot(111, projection="3d")
    sc = ax.scatter(x[:, 0], x[:, 1], x[:, 2], c=c, cmap="viridis", s=42, depthshade=True)
    ax.scatter(x[best_idx, 0], x[best_idx, 1], x[best_idx, 2], marker="*", s=170, color="#FFC000", edgecolors="black", linewidths=0.8)
    if candidate is not None:
        ax.scatter(candidate[0], candidate[1], candidate[2], marker="D", s=90, color="#7030A0", edgecolors="black", linewidths=0.8)
        ax.text(candidate[0], candidate[1], candidate[2], "Candidate", color="#7030A0", fontsize=8)
    ax.text(x[best_idx, 0], x[best_idx, 1], x[best_idx, 2], "Best", color="#7F6000", fontsize=8)
    ax.set_xlabel("x1")
    ax.set_ylabel("x2")
    ax.set_zlabel("x3")
    ax.set_title("Function 3 3D scatter")
    fig.colorbar(sc, ax=ax, shrink=0.75, pad=0.08, label="Scaled output")
    fig.tight_layout()
    fig.savefig(output_path, dpi=170)
    plt.close(fig)


def plot_pair_matrix(x: np.ndarray, y: np.ndarray, output_path: Path, candidate: np.ndarray | None) -> None:
    c = output_colors(y)
    best_idx = int(np.argmax(y))
    fig, axes = plt.subplots(4, 4, figsize=(10, 10))
    for i in range(4):
        for j in range(4):
            ax = axes[i, j]
            if i == j:
                ax.hist(x[:, i], bins=10, color="#D9E2F3", edgecolor="#4472C4")
                if candidate is not None:
                    ax.axvline(candidate[i], color="#7030A0", linestyle="--", linewidth=1.3)
                ax.axvline(x[best_idx, i], color="#C00000", linewidth=1.2)
            else:
                ax.scatter(x[:, j], x[:, i], c=c, cmap="viridis", s=20, edgecolors="none")
                ax.scatter(x[best_idx, j], x[best_idx, i], marker="*", s=70, color="#FFC000", edgecolors="black", linewidths=0.5, zorder=4)
                if candidate is not None:
                    ax.scatter(candidate[j], candidate[i], marker="D", s=34, color="#7030A0", edgecolors="black", linewidths=0.5, zorder=5)
            if i == 3:
                ax.set_xlabel(f"x{j+1}")
            else:
                ax.set_xticklabels([])
            if j == 0:
                ax.set_ylabel(f"x{i+1}")
            else:
                ax.set_yticklabels([])
            ax.grid(alpha=0.15)
    fig.suptitle("Function 4 pairwise scatter matrix", y=0.92)
    fig.tight_layout()
    fig.savefig(output_path, dpi=170)
    plt.close(fig)


def main() -> None:
    args = parse_args()
    repo_root = args.repo_root.resolve()
    output_dir = args.output_dir.resolve()
    output_dir.mkdir(parents=True, exist_ok=True)
    candidate_inputs = load_candidate_inputs(None if args.candidate_file is None else args.candidate_file.resolve())

    for function_id in range(1, 5):
        x, y = load_accumulated_data(repo_root, args.through_week, function_id)
        candidate = None
        if candidate_inputs is not None and str(function_id) in candidate_inputs:
            candidate = np.array(candidate_inputs[str(function_id)], dtype=float)
        if function_id in (1, 2):
            plot_2d(x, y, function_id, output_dir / f"function_{function_id}_scatter.png", candidate)
        elif function_id == 3:
            plot_3d(x, y, output_dir / "function_3_scatter.png", candidate)
        else:
            plot_pair_matrix(x, y, output_dir / "function_4_pairplot.png", candidate)


if __name__ == "__main__":
    main()
