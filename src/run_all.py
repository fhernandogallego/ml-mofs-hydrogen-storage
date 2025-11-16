"""End-to-end entry point to reproduce the SI results.

Running this script trains all models, computes diagnostics, and stores
artifacts (models, plots, metrics) in the ``results/`` directory.
"""
from __future__ import annotations

import json
from pathlib import Path

import pandas as pd

from .bootstrap_confidence_intervals import bootstrap_scores, summarize_ci
from .diagnostics import summarize_predictions
from .run_regression import train_models
from .utils import get_features_and_targets, load_dataset, make_train_test_split

RESULTS_DIR = Path(__file__).resolve().parent.parent / "results"


def main():
    RESULTS_DIR.mkdir(exist_ok=True)

    df = load_dataset()
    train_df, test_df = make_train_test_split(df)

    models, predictions = train_models(train_df, test_df, results_dir=RESULTS_DIR)

    # Diagnostics and plots
    diag_summary = summarize_predictions(predictions, results_dir=RESULTS_DIR)
    diag_summary.to_csv(RESULTS_DIR / "summary_from_predictions.csv", index=False)

    # Bootstrap CIs on the held-out test set
    X_train, y_train_gc, y_train_vc = get_features_and_targets(train_df)
    X_test, y_test_gc, y_test_vc = get_features_and_targets(test_df)

    bootstrap_outputs = {}
    for key, (model, X, y) in {
        "ridge": (models["ridge"].best_estimator_, X_test, y_test_gc),
        "lasso": (models["lasso"].best_estimator_, X_test, y_test_vc),
    }.items():
        scores = bootstrap_scores(model, X, y)
        scores.to_csv(RESULTS_DIR / f"bootstrap_{key}.csv", index=False)
        bootstrap_outputs[key] = summarize_ci(scores)

    with open(RESULTS_DIR / "bootstrap_intervals.json", "w", encoding="utf-8") as f:
        json.dump(bootstrap_outputs, f, indent=2)

    print("All artifacts written to", RESULTS_DIR)


if __name__ == "__main__":
    main()
