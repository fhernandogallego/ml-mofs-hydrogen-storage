"""Training routines for the regression models used in the paper.
"""
from __future__ import annotations

import json
from pathlib import Path
from typing import Dict, Tuple

import joblib
import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import Lasso, Ridge
from sklearn.metrics import mean_absolute_error, r2_score
from sklearn.model_selection import GridSearchCV
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import MinMaxScaler, PolynomialFeatures

from .utils import FEATURE_COLUMNS, get_features_and_targets


def _make_preprocessor() -> ColumnTransformer:
    return ColumnTransformer(
        transformers=[
            (
                "numeric",
                Pipeline(
                    steps=[
                        ("poly", PolynomialFeatures(degree=2, include_bias=False)),
                        ("scaler", MinMaxScaler()),
                    ]
                ),
                FEATURE_COLUMNS,
            )
        ],
        remainder="drop",
    )


def _fit_model(
    estimator,
    param_grid: Dict,
    X_train: pd.DataFrame,
    y_train: pd.Series,
    scoring: str = "r2",
) -> GridSearchCV:
    preprocessor = _make_preprocessor()
    pipe = Pipeline([("preprocess", preprocessor), ("model", estimator)])
    search = GridSearchCV(
        pipe,
        param_grid=param_grid,
        cv=5,
        scoring=scoring,
        n_jobs=-1,
    )
    search.fit(X_train, y_train)
    return search


def train_models(
    train_df: pd.DataFrame,
    test_df: pd.DataFrame,
    results_dir: Path,
) -> Tuple[Dict[str, GridSearchCV], pd.DataFrame]:
    """Train Ridge, Lasso and Random Forest regressors.

    Returns a dictionary of fitted search objects and a dataframe with
    predictions on the held-out test set.
    """

    results_dir.mkdir(parents=True, exist_ok=True)

    X_train, y_train_gc, y_train_vc = get_features_and_targets(train_df)
    X_test, y_test_gc, y_test_vc = get_features_and_targets(test_df)

    ridge_grid = {"model__alpha": [0.01, 0.1, 1.0, 10.0]}
    lasso_grid = {"model__alpha": [0.0001, 0.001, 0.01, 0.1], "model__max_iter": [5000]}
    rf_grid = {
        "model__n_estimators": [300],
        "model__max_depth": [None, 8, 12],
        "model__min_samples_leaf": [1, 3],
        "model__random_state": [42],
    }

    ridge_search = _fit_model(Ridge(random_state=42), ridge_grid, X_train, y_train_gc)
    lasso_search = _fit_model(Lasso(random_state=42), lasso_grid, X_train, y_train_vc)
    rf_search = _fit_model(RandomForestRegressor(), rf_grid, X_train, y_train_gc)

    models = {"ridge": ridge_search, "lasso": lasso_search, "rf": rf_search}

    y_pred_ridge = ridge_search.predict(X_test)
    y_pred_lasso = lasso_search.predict(X_test)
    y_pred_rf = rf_search.predict(X_test)

    metrics = {
        "ridge": {
            "r2": r2_score(y_test_gc, y_pred_ridge),
            "mae": mean_absolute_error(y_test_gc, y_pred_ridge),
            "best_params": ridge_search.best_params_,
        },
        "lasso": {
            "r2": r2_score(y_test_vc, y_pred_lasso),
            "mae": mean_absolute_error(y_test_vc, y_pred_lasso),
            "best_params": lasso_search.best_params_,
        },
        "rf": {
            "r2": r2_score(y_test_gc, y_pred_rf),
            "mae": mean_absolute_error(y_test_gc, y_pred_rf),
            "best_params": rf_search.best_params_,
        },
    }

    with open(results_dir / "metrics.json", "w", encoding="utf-8") as f:
        json.dump(metrics, f, indent=2)

    joblib.dump(ridge_search.best_estimator_, results_dir / "ridge_model.joblib")
    joblib.dump(lasso_search.best_estimator_, results_dir / "lasso_model.joblib")
    joblib.dump(rf_search.best_estimator_, results_dir / "rf_model.joblib")

    predictions = pd.DataFrame(
        {
            "name": test_df["name"],
            "true_ugc": y_test_gc,
            "pred_ugc_ridge": y_pred_ridge,
            "pred_ugc_rf": y_pred_rf,
            "true_uvc": y_test_vc,
            "pred_uvc_lasso": y_pred_lasso,
        }
    )
    predictions.to_csv(results_dir / "test_predictions.csv", index=False)

    feature_importances = pd.DataFrame(
        {
            "feature": ridge_search.best_estimator_["preprocess"]
            .transformers_[0][1]["poly"]
            .get_feature_names_out(FEATURE_COLUMNS),
            "ridge_coef": ridge_search.best_estimator_["model"].coef_,
        }
    )
    feature_importances.to_csv(results_dir / "ridge_coefficients.csv", index=False)

    rf_importances = pd.DataFrame(
        {
            "feature": ridge_search.best_estimator_["preprocess"]
            .transformers_[0][1]["poly"]
            .get_feature_names_out(FEATURE_COLUMNS),
            "importance": rf_search.best_estimator_["model"].feature_importances_,
        }
    )
    rf_importances.to_csv(results_dir / "rf_feature_importances.csv", index=False)

    return models, predictions


__all__ = ["train_models"]
