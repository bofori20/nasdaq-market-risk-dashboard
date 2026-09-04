from pathlib import Path

import numpy as np
import pandas as pd
import pytest

from risk_analysis import (
    calculate_risk_metrics,
    classify_volatility_regimes,
    filter_period,
    load_market_data,
    worst_sessions,
)


def sample_csv(tmp_path: Path) -> Path:
    dates = pd.bdate_range("2023-01-02", periods=320)
    close = 100 * np.cumprod(1 + np.sin(np.arange(320) / 11) / 200)

    data = pd.DataFrame(
        {
            "Date": dates.strftime("%m/%d/%Y"),
            "Close/Last": close,
            "Open": close * 0.999,
            "High": close * 1.005,
            "Low": close * 0.995,
        }
    )
    data = data.iloc[::-1]
    path = tmp_path / "market.csv"
    data.to_csv(path, index=False)
    return path


def test_load_market_data_sorts_and_calculates_fields(tmp_path: Path) -> None:
    data = load_market_data(sample_csv(tmp_path))

    assert len(data) == 320
    assert data["Date"].is_monotonic_increasing
    assert {
        "Close",
        "Daily return",
        "Drawdown",
        "Volatility 60D",
    }.issubset(data.columns)
    assert data["Drawdown"].max() <= 0


def test_filter_period_is_inclusive_and_recalculates_returns(
    tmp_path: Path,
) -> None:
    data = load_market_data(sample_csv(tmp_path))
    start = data["Date"].iloc[50]
    end = data["Date"].iloc[100]

    period = filter_period(data, start, end)

    assert len(period) == 51
    assert period["Date"].iloc[0] == start
    assert period["Date"].iloc[-1] == end
    assert pd.isna(period["Daily return"].iloc[0])
    assert period["Drawdown"].max() <= 0


def test_filter_period_rejects_reversed_dates(tmp_path: Path) -> None:
    data = load_market_data(sample_csv(tmp_path))

    with pytest.raises(ValueError, match="Start date"):
        filter_period(
            data,
            data["Date"].iloc[100],
            data["Date"].iloc[50],
        )


def test_risk_metrics_have_expected_bounds(tmp_path: Path) -> None:
    data = load_market_data(sample_csv(tmp_path))
    metrics = calculate_risk_metrics(data, confidence_level=0.95)

    assert metrics["observations"] == 320
    assert metrics["annualized_volatility"] >= 0
    assert metrics["maximum_drawdown"] <= 0
    assert metrics["historical_var"] >= 0
    assert metrics["expected_shortfall"] >= metrics["historical_var"]
    assert 0 <= metrics["positive_day_rate"] <= 1


def test_worst_sessions_are_sorted_from_lowest_return(tmp_path: Path) -> None:
    data = load_market_data(sample_csv(tmp_path))
    worst = worst_sessions(data, count=5)

    assert len(worst) == 5
    assert worst["Daily return"].is_monotonic_increasing


def test_volatility_regimes_use_three_labels(tmp_path: Path) -> None:
    data = load_market_data(sample_csv(tmp_path))
    regimes = classify_volatility_regimes(data)

    assert not regimes.empty
    assert set(regimes["Risk regime"]).issubset(
        {"Low", "Normal", "High"}
    )
