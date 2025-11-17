"""Plotting and diagnostic helpers."""
from __future__ import annotations

from pathlib import Path
from typing import Tuple

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from sklearn.metrics import mean_absolute_error, r2_score

sns.set_context("talk")


def _base_plot(figsize=(6, 6)):
    fig, ax = plt.subplots(figsize=figsize)
    return fig, ax


def parity_plot(true, pred, path: Path, title: str, xlabel: str):
    fig, ax = _base_plot()
    sns.scatterplot(x=true, y=pred, ax=ax, color="#1f77b4")
    lims = [min(true.min(), pred.min()), max(true.max(), pred.max())]
    ax.plot(lims, lims, "--", color="black", label="Perfect fit")
    ax.set_title(title)
    ax.set_xlabel(f"True {xlabel}")
    ax.set_ylabel(f"Predicted {xlabel}")
    ax.legend()
    fig.tight_layout()
    fig.savefig(path, dpi=300)
    plt.close(fig)


def residual_plot(true, pred, path: Path, title: str, xlabel: str):
    fig, ax = _base_plot()
    residuals = pred - true
    sns.scatterplot(x=pred, y=residuals, ax=ax, color="#ff7f0e")
    ax.axhline(0, linestyle="--", color="black")
    ax.set_title(title)
    ax.set_xlabel(f"Predicted {xlabel}")
    ax.set_ylabel("Residual")
    fig.tight_layout()
    fig.savefig(path, dpi=300)
    plt.close(fig)


def summarize_predictions(predictions: pd.DataFrame, results_dir: Path) -> pd.DataFrame:
    """Create plots and a small metrics table for the test predictions."""

    results_dir.mkdir(parents=True, exist_ok=True)

    parity_plot(
        predictions["true_ugc"],
        predictions["pred_ugc_ridge"],
        results_dir / "parity_ridge_ugc.png",
        title="Ridge parity plot (usablegc)",
        xlabel="usablegc (wt. %)",
    )

    parity_plot(
        predictions["true_uvc"],
        predictions["pred_uvc_lasso"],
        results_dir / "parity_lasso_uvc.png",
        title="Lasso parity plot (usablevc)",
        xlabel="usablevc (kg/L)",
    )

    residual_plot(
        predictions["true_ugc"],
        predictions["pred_ugc_ridge"],
        results_dir / "residuals_ridge_ugc.png",
        title="Ridge residuals (usablegc)",
        xlabel="usablegc (wt. %)",
    )

    residual_plot(
        predictions["true_uvc"],
        predictions["pred_uvc_lasso"],
        results_dir / "residuals_lasso_uvc.png",
        title="Lasso residuals (usablevc)",
        xlabel="usablevc (kg/L)",
    )

    summary = pd.DataFrame(
        [
            {
                "model": "ridge",
                "target": "usablegc",
                "r2": r2_score(predictions["true_ugc"], predictions["pred_ugc_ridge"]),
                "mae": mean_absolute_error(
                    predictions["true_ugc"], predictions["pred_ugc_ridge"]
                ),
            },
            {
                "model": "lasso",
                "target": "usablevc",
                "r2": r2_score(predictions["true_uvc"], predictions["pred_uvc_lasso"]),
                "mae": mean_absolute_error(
                    predictions["true_uvc"], predictions["pred_uvc_lasso"]
                ),
            },
        ]
    )

    summary.to_csv(results_dir / "diagnostic_metrics.csv", index=False)
    return summary


__all__ = ["summarize_predictions"]
