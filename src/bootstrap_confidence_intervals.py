"""Bootstrap confidence intervals for model performance."""
from __future__ import annotations

from pathlib import Path
from typing import Dict, Tuple

import numpy as np
import pandas as pd
from sklearn.metrics import mean_absolute_error, r2_score
from sklearn.model_selection import ShuffleSplit
from sklearn.pipeline import Pipeline


def bootstrap_scores(
    model: Pipeline,
    X,
    y,
    n_bootstrap: int = 1000,
    random_state: int = 42,
) -> pd.DataFrame:
    rng = np.random.default_rng(random_state)
    scores = []
    for _ in range(n_bootstrap):
        indices = rng.integers(0, len(y), len(y))
        X_resampled = X.iloc[indices]
        y_resampled = y.iloc[indices]
        preds = model.predict(X_resampled)
        scores.append(
            {
                "r2": r2_score(y_resampled, preds),
                "mae": mean_absolute_error(y_resampled, preds),
            }
        )
    return pd.DataFrame(scores)


def summarize_ci(scores: pd.DataFrame, alpha: float = 0.05) -> Dict[str, Tuple[float, float]]:
    lower = scores.quantile(alpha / 2)
    upper = scores.quantile(1 - alpha / 2)
    return {metric: (lower[metric], upper[metric]) for metric in scores.columns}


__all__ = ["bootstrap_scores", "summarize_ci"]
