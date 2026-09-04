"""Train and evaluate a leakage-aware NASDAQ-100 direction classifier."""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    accuracy_score,
    balanced_accuracy_score,
    confusion_matrix,
    f1_score,
    precision_score,
    recall_score,
    roc_auc_score,
)
from sklearn.model_selection import TimeSeriesSplit


DATA_PATH = Path("data/nasdaq_100_2014_2024.csv")
REPORT_DIRECTORY = Path("reports/forecasting_experiment")
RESULTS_PATH = REPORT_DIRECTORY / "model_results.csv"
PREDICTIONS_PATH = REPORT_DIRECTORY / "test_predictions.csv"
IMPORTANCE_PATH = REPORT_DIRECTORY / "feature_importance.csv"
METADATA_PATH = REPORT_DIRECTORY / "model_metadata.json"

RANDOM_STATE = 42
TRAIN_FRACTION = 0.60
VALIDATION_FRACTION = 0.20

FEATURES = [
    "return_1d",
    "return_2d",
    "return_5d",
    "return_10d",
    "return_20d",
    "intraday_range",
    "close_to_open",
    "ma_gap_5",
    "ma_gap_20",
    "ma_gap_50",
    "volatility_5",
    "volatility_20",
    "volatility_50",
]


def load_market_data(path: Path) -> pd.DataFrame:
    """Load, validate, and sort the source data chronologically."""
    data = pd.read_csv(path)

    required = {"Date", "Close/Last", "Open", "High", "Low"}
    missing = required.difference(data.columns)

    if missing:
        raise ValueError(
            "Dataset is missing required columns: "
            + ", ".join(sorted(missing))
        )

    data = data.rename(columns={"Close/Last": "Close"})
    data["Date"] = pd.to_datetime(
        data["Date"],
        format="%m/%d/%Y",
        errors="raise",
    )

    for column in ["Close", "Open", "High", "Low"]:
        data[column] = pd.to_numeric(data[column], errors="raise")

    data = (
        data.sort_values("Date")
        .drop_duplicates(subset="Date", keep="last")
        .reset_index(drop=True)
    )

    if data[["Close", "Open", "High", "Low"]].isna().any().any():
        raise ValueError("Price columns contain missing values.")

    if not data["Date"].is_monotonic_increasing:
        raise ValueError("Dates are not in ascending chronological order.")

    return data


def build_modeling_table(data: pd.DataFrame) -> pd.DataFrame:
    """Create past-and-present features for next-session direction."""
    table = data.copy()

    table["return_1d"] = table["Close"].pct_change(1)
    table["return_2d"] = table["Close"].pct_change(2)
    table["return_5d"] = table["Close"].pct_change(5)
    table["return_10d"] = table["Close"].pct_change(10)
    table["return_20d"] = table["Close"].pct_change(20)

    table["intraday_range"] = (
        (table["High"] - table["Low"]) / table["Open"]
    )
    table["close_to_open"] = (
        (table["Close"] - table["Open"]) / table["Open"]
    )

    daily_return = table["return_1d"]

    for window in [5, 20, 50]:
        moving_average = table["Close"].rolling(window=window).mean()
        table[f"ma_gap_{window}"] = table["Close"] / moving_average - 1
        table[f"volatility_{window}"] = daily_return.rolling(
            window=window
        ).std()

    table["target_date"] = table["Date"].shift(-1)
    table["next_close"] = table["Close"].shift(-1)
    table["next_return"] = table["next_close"] / table["Close"] - 1
    table["target_up"] = (table["next_return"] > 0).astype(int)

    table = table.dropna(
        subset=FEATURES + ["target_date", "next_return"]
    ).reset_index(drop=True)

    return table


def chronological_split(
    table: pd.DataFrame,
) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """Create contiguous train, validation, and untouched test sets."""
    train_end = int(len(table) * TRAIN_FRACTION)
    validation_end = int(
        len(table) * (TRAIN_FRACTION + VALIDATION_FRACTION)
    )

    train = table.iloc[:train_end].copy()
    validation = table.iloc[train_end:validation_end].copy()
    test = table.iloc[validation_end:].copy()

    if min(len(train), len(validation), len(test)) == 0:
        raise ValueError("A chronological split produced an empty dataset.")

    return train, validation, test


def build_model() -> RandomForestClassifier:
    """Return the fixed, reproducible model specification."""
    return RandomForestClassifier(
        n_estimators=500,
        max_depth=6,
        min_samples_leaf=15,
        max_features="sqrt",
        class_weight="balanced_subsample",
        random_state=RANDOM_STATE,
        n_jobs=-1,
    )


def metric_row(
    name: str,
    y_true: pd.Series | np.ndarray,
    predictions: np.ndarray,
    probabilities: np.ndarray | None = None,
) -> dict[str, float | str | int]:
    """Calculate consistent binary-classification metrics."""
    tn, fp, fn, tp = confusion_matrix(
        y_true,
        predictions,
        labels=[0, 1],
    ).ravel()

    row: dict[str, float | str | int] = {
        "model": name,
        "accuracy": accuracy_score(y_true, predictions),
        "balanced_accuracy": balanced_accuracy_score(y_true, predictions),
        "precision": precision_score(
            y_true,
            predictions,
            zero_division=0,
        ),
        "recall": recall_score(
            y_true,
            predictions,
            zero_division=0,
        ),
        "f1": f1_score(
            y_true,
            predictions,
            zero_division=0,
        ),
        "true_negatives": int(tn),
        "false_positives": int(fp),
        "false_negatives": int(fn),
        "true_positives": int(tp),
    }

    row["roc_auc"] = (
        roc_auc_score(y_true, probabilities)
        if probabilities is not None
        else np.nan
    )

    return row


def select_threshold(
    y_true: pd.Series,
    probabilities: np.ndarray,
) -> tuple[float, pd.DataFrame]:
    """Select a threshold using validation balanced accuracy only."""
    rows = []

    for threshold in np.arange(0.35, 0.651, 0.01):
        predictions = (probabilities >= threshold).astype(int)
        rows.append(
            {
                "threshold": round(float(threshold), 2),
                "balanced_accuracy": balanced_accuracy_score(
                    y_true,
                    predictions,
                ),
                "f1": f1_score(
                    y_true,
                    predictions,
                    zero_division=0,
                ),
            }
        )

    results = pd.DataFrame(rows)
    results["distance_from_0_5"] = (
        results["threshold"] - 0.50
    ).abs()

    best = results.sort_values(
        ["balanced_accuracy", "distance_from_0_5"],
        ascending=[False, True],
    ).iloc[0]

    return float(best["threshold"]), results.drop(
        columns="distance_from_0_5"
    )


def time_series_cross_validation(
    development: pd.DataFrame,
) -> pd.DataFrame:
    """Evaluate temporal stability with expanding-window splits."""
    splitter = TimeSeriesSplit(n_splits=5)
    rows = []

    X = development[FEATURES]
    y = development["target_up"]

    for fold, (train_indices, validation_indices) in enumerate(
        splitter.split(X),
        start=1,
    ):
        model = build_model()
        model.fit(X.iloc[train_indices], y.iloc[train_indices])

        probabilities = model.predict_proba(
            X.iloc[validation_indices]
        )[:, 1]
        predictions = (probabilities >= 0.50).astype(int)

        row = metric_row(
            f"time_series_fold_{fold}",
            y.iloc[validation_indices],
            predictions,
            probabilities,
        )
        row["fold"] = fold
        row["train_end"] = development.iloc[train_indices]["Date"].max()
        row["validation_start"] = development.iloc[
            validation_indices
        ]["Date"].min()
        row["validation_end"] = development.iloc[
            validation_indices
        ]["Date"].max()
        rows.append(row)

    return pd.DataFrame(rows)


def main() -> None:
    REPORT_DIRECTORY.mkdir(parents=True, exist_ok=True)

    raw = load_market_data(DATA_PATH)
    table = build_modeling_table(raw)
    train, validation, test = chronological_split(table)

    X_train = train[FEATURES]
    y_train = train["target_up"]
    X_validation = validation[FEATURES]
    y_validation = validation["target_up"]
    X_test = test[FEATURES]
    y_test = test["target_up"]

    threshold_model = build_model()
    threshold_model.fit(X_train, y_train)
    validation_probabilities = threshold_model.predict_proba(
        X_validation
    )[:, 1]

    threshold, threshold_results = select_threshold(
        y_validation,
        validation_probabilities,
    )

    development = pd.concat([train, validation], ignore_index=True)
    cross_validation = time_series_cross_validation(development)

    final_model = build_model()
    final_model.fit(
        development[FEATURES],
        development["target_up"],
    )

    test_probabilities = final_model.predict_proba(X_test)[:, 1]
    model_predictions = (test_probabilities >= threshold).astype(int)

    majority_class = int(development["target_up"].mode().iloc[0])
    majority_predictions = np.full(len(test), majority_class)
    momentum_predictions = (test["return_1d"] > 0).astype(int).to_numpy()

    results = pd.DataFrame(
        [
            metric_row(
                "majority_baseline",
                y_test,
                majority_predictions,
            ),
            metric_row(
                "previous_direction_baseline",
                y_test,
                momentum_predictions,
            ),
            metric_row(
                "random_forest",
                y_test,
                model_predictions,
                test_probabilities,
            ),
        ]
    )
    results.insert(1, "evaluation_set", "untouched_test")
    results["decision_threshold"] = [np.nan, np.nan, threshold]
    results.to_csv(RESULTS_PATH, index=False)

    predictions = test[
        [
            "Date",
            "target_date",
            "Close",
            "next_close",
            "next_return",
            "target_up",
        ]
    ].copy()
    predictions["probability_up"] = test_probabilities
    predictions["predicted_up"] = model_predictions
    predictions.to_csv(PREDICTIONS_PATH, index=False)

    importance = pd.DataFrame(
        {
            "feature": FEATURES,
            "importance": final_model.feature_importances_,
        }
    ).sort_values("importance", ascending=False)
    importance.to_csv(IMPORTANCE_PATH, index=False)

    threshold_results.to_csv(
        REPORT_DIRECTORY / "validation_thresholds.csv",
        index=False,
    )
    cross_validation.to_csv(
        REPORT_DIRECTORY / "time_series_cross_validation.csv",
        index=False,
    )

    model_balanced_accuracy = float(
        results.loc[
            results["model"] == "random_forest",
            "balanced_accuracy",
        ].iloc[0]
    )
    best_baseline_balanced_accuracy = float(
        results.loc[
            results["model"] != "random_forest",
            "balanced_accuracy",
        ].max()
    )
    deployment_decision = (
        "reject"
        if model_balanced_accuracy <= best_baseline_balanced_accuracy
        else "candidate_for_additional_validation"
    )

    metadata = {
        "project": "NASDAQ-100 next-session directional forecasting",
        "target": "1 when next session closes above current close, else 0",
        "forecast_horizon": "next trading session",
        "features": FEATURES,
        "selected_threshold": threshold,
        "threshold_selection_set": "validation",
        "data_start": raw["Date"].min().date().isoformat(),
        "data_end": raw["Date"].max().date().isoformat(),
        "modeling_rows": len(table),
        "train_rows": len(train),
        "validation_rows": len(validation),
        "test_rows": len(test),
        "train_start": train["Date"].min().date().isoformat(),
        "train_end": train["Date"].max().date().isoformat(),
        "validation_start": validation["Date"].min().date().isoformat(),
        "validation_end": validation["Date"].max().date().isoformat(),
        "test_start": test["Date"].min().date().isoformat(),
        "test_end": test["Date"].max().date().isoformat(),
        "random_state": RANDOM_STATE,
        "deployment_decision": deployment_decision,
        "decision_reason": (
            "Model must outperform the strongest naive baseline on "
            "untouched-test balanced accuracy before deployment."
        ),
    }
    METADATA_PATH.write_text(json.dumps(metadata, indent=2) + "\n")

    print("Dataset and split summary")
    print("-------------------------")
    print(f"Raw rows: {len(raw):,}")
    print(f"Modeling rows: {len(table):,}")
    print(f"Train rows: {len(train):,}")
    print(f"Validation rows: {len(validation):,}")
    print(f"Test rows: {len(test):,}")
    print(f"Selected validation threshold: {threshold:.2f}")

    print("\nUntouched test results")
    print("----------------------")
    display_columns = [
        "model",
        "accuracy",
        "balanced_accuracy",
        "precision",
        "recall",
        "f1",
        "roc_auc",
    ]
    print(results[display_columns].to_string(index=False, float_format="%.4f"))

    print("\nTime-series cross-validation: random forest at 0.50")
    print("---------------------------------------------------")
    for metric in ["balanced_accuracy", "precision", "recall", "f1", "roc_auc"]:
        print(
            f"{metric}: "
            f"{cross_validation[metric].mean():.4f} "
            f"+/- {cross_validation[metric].std(ddof=1):.4f}"
        )

    print("\nSaved outputs")
    print("-------------")
    for path in [
        RESULTS_PATH,
        PREDICTIONS_PATH,
        IMPORTANCE_PATH,
        METADATA_PATH,
        REPORT_DIRECTORY / "validation_thresholds.csv",
        REPORT_DIRECTORY / "time_series_cross_validation.csv",
    ]:
        print(path)

    print("\nDeployment decision")
    print("-------------------")
    print(deployment_decision.upper())


if __name__ == "__main__":
    main()
