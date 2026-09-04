"""Reusable calculations for the NASDAQ-100 market-risk dashboard."""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd


TRADING_DAYS = 252


def load_market_data(path: str | Path) -> pd.DataFrame:
    """Load and validate daily NASDAQ-100 OHLC observations."""
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
        data["Date"], format="%m/%d/%Y", errors="raise"
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

    data["Daily return"] = data["Close"].pct_change()
    data["Cumulative peak"] = data["Close"].cummax()
    data["Drawdown"] = data["Close"] / data["Cumulative peak"] - 1

    for window in [20, 60, 252]:
        data[f"Volatility {window}D"] = (
            data["Daily return"].rolling(window).std()
            * np.sqrt(TRADING_DAYS)
        )

    return data


def filter_period(
    data: pd.DataFrame,
    start_date: object,
    end_date: object,
) -> pd.DataFrame:
    """Return an inclusive date window and recalculate path-dependent fields."""
    start = pd.Timestamp(start_date)
    end = pd.Timestamp(end_date)

    if start > end:
        raise ValueError("Start date must be on or before end date.")

    period = data.loc[data["Date"].between(start, end)].copy()

    if len(period) < 2:
        raise ValueError("Select a period containing at least two observations.")

    period["Daily return"] = period["Close"].pct_change()
    period["Cumulative peak"] = period["Close"].cummax()
    period["Drawdown"] = period["Close"] / period["Cumulative peak"] - 1

    for window in [20, 60, 252]:
        period[f"Volatility {window}D"] = (
            period["Daily return"].rolling(window).std()
            * np.sqrt(TRADING_DAYS)
        )

    return period


def calculate_risk_metrics(
    period: pd.DataFrame,
    confidence_level: float = 0.95,
) -> dict[str, float | int | pd.Timestamp]:
    """Calculate historical return, volatility, drawdown, VaR, and ES metrics."""
    if not 0 < confidence_level < 1:
        raise ValueError("Confidence level must be between 0 and 1.")

    returns = period["Daily return"].dropna()

    if returns.empty:
        raise ValueError("The selected period has no calculable daily returns.")

    years = len(returns) / TRADING_DAYS
    annualized_return = (
        (period["Close"].iloc[-1] / period["Close"].iloc[0])
        ** (1 / years)
        - 1
        if years > 0
        else np.nan
    )
    annualized_volatility = returns.std(ddof=1) * np.sqrt(TRADING_DAYS)
    sharpe_ratio = (
        returns.mean() / returns.std(ddof=1) * np.sqrt(TRADING_DAYS)
        if returns.std(ddof=1) > 0
        else np.nan
    )

    loss_quantile = returns.quantile(1 - confidence_level)
    tail_returns = returns.loc[returns <= loss_quantile]

    max_drawdown_index = period["Drawdown"].idxmin()

    return {
        "observations": len(period),
        "start_date": period["Date"].iloc[0],
        "end_date": period["Date"].iloc[-1],
        "total_return": period["Close"].iloc[-1] / period["Close"].iloc[0] - 1,
        "annualized_return": annualized_return,
        "annualized_volatility": annualized_volatility,
        "sharpe_ratio_zero_rf": sharpe_ratio,
        "maximum_drawdown": period["Drawdown"].min(),
        "maximum_drawdown_date": period.loc[max_drawdown_index, "Date"],
        "historical_var": -loss_quantile,
        "expected_shortfall": -tail_returns.mean(),
        "positive_day_rate": (returns > 0).mean(),
        "best_day": returns.max(),
        "worst_day": returns.min(),
    }


def worst_sessions(period: pd.DataFrame, count: int = 10) -> pd.DataFrame:
    """Return the sessions with the lowest daily returns."""
    return (
        period.dropna(subset=["Daily return"])
        .nsmallest(count, "Daily return")
        .loc[:, ["Date", "Close", "Daily return", "Drawdown"]]
        .reset_index(drop=True)
    )


def classify_volatility_regimes(period: pd.DataFrame) -> pd.DataFrame:
    """Classify 60-day volatility into sample-relative low, normal, and high regimes."""
    output = period.dropna(subset=["Volatility 60D"]).copy()

    if output.empty:
        output["Risk regime"] = pd.Series(dtype="object")
        return output

    low_threshold = output["Volatility 60D"].quantile(0.25)
    high_threshold = output["Volatility 60D"].quantile(0.75)

    output["Risk regime"] = np.select(
        [
            output["Volatility 60D"] <= low_threshold,
            output["Volatility 60D"] >= high_threshold,
        ],
        ["Low", "High"],
        default="Normal",
    )

    return output
