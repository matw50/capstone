#!/usr/bin/env python3
"""Classifier-based region checks for proposed capstone candidates.

This script turns each function into a temporary binary classification problem by
labelling the top fraction of observed outputs as "high-performing". It then
scores proposed candidates using:
- logistic regression probability of belonging to the high-performing region
- optional RBF-kernel SVM classification

This is intended as a secondary sanity check, not a primary optimiser.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVC


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Classifier-based region checks for capstone candidates.")
    parser.add_argument(
        "--repo-root",
        type=Path,
        default=Path("."),
        help="Path to the repository root. Default: current directory.",
    )
    parser.add_argument(
        "--through-week",
        required=True,
        help="Use results up to and including this week, for example: week3",
    )
    parser.add_argument(
        "--candidate-file",
        type=Path,
        required=True,
        help="JSON file containing proposed inputs or generated candidates.",
    )
    parser.add_argument(
        "--top-fraction",
        type=float,
        default=0.25,
        help="Fraction of observed points to label as high-performing. Default: 0.25",
    )
    parser.add_argument(
        "--svm",
        action="store_true",
        help="Also run an RBF-kernel SVM region classifier.",
    )
    return parser.parse_args()


def parse_week_number(week_name: str) -> int:
    if not week_name.startswith("week"):
        raise ValueError(f"Invalid week name: {week_name}")
    return int(week_name[4:])


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


def load_candidates(candidate_file: Path) -> dict[str, list[float]]:
    with candidate_file.open("r", encoding="utf-8") as fh:
        payload = json.load(fh)
    if "functions" in payload:
        return payload["functions"]
    if "recommendations" in payload:
        return {key: value["candidate"] for key, value in payload["recommendations"].items()}
    raise KeyError("Candidate file must contain either 'functions' or 'recommendations'.")


def make_labels(y: np.ndarray, top_fraction: float) -> np.ndarray:
    n_pos = max(2, int(np.ceil(len(y) * top_fraction)))
    idx = np.argsort(y)[-n_pos:]
    labels = np.zeros(len(y), dtype=int)
    labels[idx] = 1
    return labels


def main() -> None:
    args = parse_args()
    repo_root = args.repo_root.resolve()
    candidate_file = args.candidate_file.resolve()
    candidates = load_candidates(candidate_file)

    results: dict[str, object] = {
        "through_week": args.through_week,
        "candidate_file": str(candidate_file),
        "top_fraction": args.top_fraction,
        "checks": {},
    }

    for function_id in range(1, 9):
        x, y = load_accumulated_data(repo_root, args.through_week, function_id)
        candidate = np.array(candidates[str(function_id)], dtype=float).reshape(1, -1)
        labels = make_labels(y, args.top_fraction)

        positive_count = int(labels.sum())
        negative_count = int(len(labels) - positive_count)
        if positive_count < 2 or negative_count < 2:
            results["checks"][str(function_id)] = {
                "status": "insufficient_class_balance",
                "positives": positive_count,
                "negatives": negative_count,
            }
            continue

        logistic = make_pipeline(
            StandardScaler(),
            LogisticRegression(max_iter=5000, class_weight="balanced"),
        )
        logistic.fit(x, labels)
        logistic_prob = float(logistic.predict_proba(candidate)[0, 1])
        logistic_pred = int(logistic.predict(candidate)[0])

        check: dict[str, object] = {
            "positives": positive_count,
            "negatives": negative_count,
            "logistic_high_region_probability": logistic_prob,
            "logistic_predicted_high_region": bool(logistic_pred),
        }

        if args.svm:
            svm = make_pipeline(
                StandardScaler(),
                SVC(kernel="rbf", class_weight="balanced", probability=True),
            )
            svm.fit(x, labels)
            svm_prob = float(svm.predict_proba(candidate)[0, 1])
            svm_pred = int(svm.predict(candidate)[0])
            check["svm_high_region_probability"] = svm_prob
            check["svm_predicted_high_region"] = bool(svm_pred)

        results["checks"][str(function_id)] = check

    print(json.dumps(results, indent=2) + "\n")


if __name__ == "__main__":
    main()
