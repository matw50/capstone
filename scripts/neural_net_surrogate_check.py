#!/usr/bin/env python3
"""Experimental neural-network surrogate check for proposed candidates.

This script fits a small bootstrap ensemble of MLP regressors for each
black-box function and scores proposed candidates. It is intentionally a
secondary check, not the primary optimiser, because the observed datasets are
small and neural networks can overfit or extrapolate too confidently.
"""

from __future__ import annotations

import argparse
import json
import warnings
from pathlib import Path

import numpy as np
from sklearn.exceptions import ConvergenceWarning
from sklearn.neural_network import MLPRegressor
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Experimental neural-net surrogate check for capstone candidates.")
    parser.add_argument(
        "--repo-root",
        type=Path,
        default=Path("."),
        help="Path to the repository root. Default: current directory.",
    )
    parser.add_argument(
        "--through-week",
        required=True,
        help="Use results up to and including this week, for example: week4",
    )
    parser.add_argument(
        "--candidate-file",
        type=Path,
        required=True,
        help="JSON file containing proposed inputs or generated candidates.",
    )
    parser.add_argument(
        "--ensemble-size",
        type=int,
        default=25,
        help="Number of bootstrap MLP models to fit per function. Default: 25",
    )
    parser.add_argument(
        "--hidden-units",
        type=int,
        default=8,
        help="Hidden units in the single hidden layer. Default: 8",
    )
    parser.add_argument(
        "--alpha",
        type=float,
        default=0.1,
        help="L2 regularisation strength for the MLP. Default: 0.1",
    )
    parser.add_argument(
        "--random-seed",
        type=int,
        default=42,
        help="Base random seed. Default: 42",
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
    if all(str(function_id) in payload for function_id in range(1, 9)):
        return payload
    raise KeyError("Candidate file must contain 'functions', 'recommendations', or top-level function IDs.")


def portal(point: np.ndarray) -> str:
    return "-".join(f"{value:.6f}" for value in point)


def fit_predict_ensemble(
    x: np.ndarray,
    y: np.ndarray,
    candidate: np.ndarray,
    ensemble_size: int,
    hidden_units: int,
    alpha: float,
    random_seed: int,
) -> np.ndarray:
    rng = np.random.default_rng(random_seed)
    y_mean = float(np.mean(y))
    y_std = float(np.std(y))
    if y_std <= 1e-12:
        y_std = 1.0
    y_scaled = (y - y_mean) / y_std

    predictions: list[float] = []
    n = len(y)
    for model_idx in range(ensemble_size):
        bootstrap_idx = rng.integers(0, n, size=n)
        model = make_pipeline(
            StandardScaler(),
            MLPRegressor(
                hidden_layer_sizes=(hidden_units,),
                activation="tanh",
                solver="lbfgs",
                alpha=alpha,
                max_iter=2000,
                random_state=random_seed + model_idx,
            ),
        )
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", ConvergenceWarning)
            model.fit(x[bootstrap_idx], y_scaled[bootstrap_idx])
        pred_scaled = float(model.predict(candidate.reshape(1, -1))[0])
        predictions.append((pred_scaled * y_std) + y_mean)

    return np.array(predictions, dtype=float)


def main() -> None:
    args = parse_args()
    repo_root = args.repo_root.resolve()
    candidate_file = args.candidate_file.resolve()
    candidates = load_candidates(candidate_file)

    results: dict[str, object] = {
        "through_week": args.through_week,
        "candidate_file": str(candidate_file),
        "status": "experimental_secondary_check",
        "ensemble_size": args.ensemble_size,
        "hidden_units": args.hidden_units,
        "alpha": args.alpha,
        "checks": {},
    }

    for function_id in range(1, 9):
        x, y = load_accumulated_data(repo_root, args.through_week, function_id)
        candidate = np.array(candidates[str(function_id)], dtype=float)
        best_idx = int(np.argmax(y))
        predictions = fit_predict_ensemble(
            x=x,
            y=y,
            candidate=candidate,
            ensemble_size=args.ensemble_size,
            hidden_units=args.hidden_units,
            alpha=args.alpha,
            random_seed=args.random_seed + (function_id * 1000),
        )
        pred_mean = float(np.mean(predictions))
        pred_std = float(np.std(predictions))
        percentile = float(np.mean(y <= pred_mean))
        results["checks"][str(function_id)] = {
            "portal": portal(candidate),
            "dimension": int(x.shape[1]),
            "observations": int(len(y)),
            "best_observed_output": float(y[best_idx]),
            "best_observed_input": x[best_idx].tolist(),
            "nn_predicted_output_mean": pred_mean,
            "nn_predicted_output_std": pred_std,
            "predicted_percentile_vs_observed": percentile,
            "predicts_above_best": bool(pred_mean > float(y[best_idx])),
        }

    print(json.dumps(results, indent=2) + "\n")


if __name__ == "__main__":
    main()
