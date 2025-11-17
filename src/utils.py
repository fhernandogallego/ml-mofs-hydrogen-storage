"""Utility functions for loading data and preparing splits.
"""
from __future__ import annotations

from pathlib import Path
from typing import Tuple

import pandas as pd
from sklearn.model_selection import train_test_split

DATA_PATH = Path(__file__).resolve().parent.parent / "data" / "structuralparameters-vs-capacities-h2.dat"

FEATURE_COLUMNS = ["density", "porosity", "Ri", "SSA", "SPV"]
TARGET_COLUMNS = ["usablegc", "usablevc"]


def load_dataset(path: Path | str = DATA_PATH) -> pd.DataFrame:
    """Load the MOF dataset with cleaned column names.

    The raw file contains a short header (four rows) with units. These rows are
    skipped and the remaining rows are parsed as whitespace-delimited values.
    """

    df = pd.read_csv(
        path,
        delim_whitespace=True,
        skiprows=4,
        names=["name", *TARGET_COLUMNS, *FEATURE_COLUMNS],
    )

    # Ensure correct dtypes
    for col in TARGET_COLUMNS + FEATURE_COLUMNS:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    df = df.dropna(subset=TARGET_COLUMNS + FEATURE_COLUMNS)
    return df.reset_index(drop=True)


def build_stratification_labels(df: pd.DataFrame, n_bins: int = 5) -> pd.Series:
    """Create stratification labels by combining quantile bins of both targets.

    This preserves marginal distributions of usable gravimetric and volumetric
    capacities simultaneously when splitting into train and test sets.
    """

    bins_gc = pd.qcut(df["usablegc"], q=n_bins, duplicates="drop")
    bins_vc = pd.qcut(df["usablevc"], q=n_bins, duplicates="drop")
    return bins_gc.astype(str) + "__" + bins_vc.astype(str)


def make_train_test_split(
    df: pd.DataFrame,
    test_size: float = 0.3,
    random_state: int = 42,
    n_bins: int = 5,
) -> Tuple[pd.DataFrame, pd.DataFrame]:
    """Split the dataframe into train and test subsets using stratification.

    Stratification is based on quantile bins of both usable capacities to keep
    their distributions balanced across splits.
    """

    strat_labels = None
    # Try to build stratification labels; if any bin is underpopulated (<2),
    # progressively reduce the number of bins. If no valid stratification is
    # possible, fall back to an unstratified split to avoid runtime errors on
    # small datasets.
    for bins in range(n_bins, 1, -1):
        labels = build_stratification_labels(df, n_bins=bins)
        if labels.value_counts().min() >= 2:
            strat_labels = labels
            break

    train_df, test_df = train_test_split(
        df,
        test_size=test_size,
        random_state=random_state,
        stratify=strat_labels,
    )
    return train_df.reset_index(drop=True), test_df.reset_index(drop=True)


def get_features_and_targets(df: pd.DataFrame) -> Tuple[pd.DataFrame, pd.Series, pd.Series]:
    """Return feature matrix and both target vectors."""

    X = df[FEATURE_COLUMNS]
    y_gc = df["usablegc"]
    y_vc = df["usablevc"]
    return X, y_gc, y_vc


__all__ = [
    "load_dataset",
    "make_train_test_split",
    "get_features_and_targets",
    "FEATURE_COLUMNS",
    "TARGET_COLUMNS",
]
