"""Streamlit interface for historical NASDAQ-100 market-risk analysis."""

from pathlib import Path

import pandas as pd
import streamlit as st

from risk_analysis import (
    calculate_risk_metrics,
    classify_volatility_regimes,
    filter_period,
    load_market_data,
    worst_sessions,
)


DATA_PATH = Path("data/nasdaq_100_2014_2024.csv")

st.set_page_config(
    page_title="NASDAQ-100 Market Risk Analytics",
    page_icon="📉",
    layout="wide",
)

st.markdown(
    """
    <style>
    .block-container {max-width: 1200px; padding-top: 2rem;}
    [data-testid="stMetric"] {
        background: #f7f9fc;
        border: 1px solid #e3e8f0;
        border-radius: 0.75rem;
        padding: 1rem;
    }

    [data-testid="stMetricLabel"],
    [data-testid="stMetricValue"],
    [data-testid="stMetricDelta"] {
        color: #172033 !important;
}
    </style>
    """,
    unsafe_allow_html=True,
)


@st.cache_data
def get_data() -> pd.DataFrame:
    return load_market_data(DATA_PATH)


def percent(value: float) -> str:
    return f"{value:.2%}"


try:
    market = get_data()
except (FileNotFoundError, ValueError) as error:
    st.error(f"Unable to load the market dataset: {error}")
    st.stop()

st.title("NASDAQ-100 Market Risk Analytics")
st.caption(
    "Historical risk analysis of daily NASDAQ-100 index observations "
    "from July 2014 through July 2024."
)

with st.sidebar:
    st.header("Analysis controls")

    start_date = st.date_input(
        "Start date",
        value=market["Date"].min().date(),
        min_value=market["Date"].min().date(),
        max_value=market["Date"].max().date(),
    )
    end_date = st.date_input(
        "End date",
        value=market["Date"].max().date(),
        min_value=market["Date"].min().date(),
        max_value=market["Date"].max().date(),
    )
    confidence_label = st.selectbox(
        "Historical loss confidence",
        options=["95%", "99%"],
        index=0,
    )
    confidence_level = 0.95 if confidence_label == "95%" else 0.99

    st.divider()
    st.caption(
        "The dataset is fixed for reproducibility and does not contain "
        "live market prices."
    )

try:
    period = filter_period(market, start_date, end_date)
    metrics = calculate_risk_metrics(period, confidence_level)
except ValueError as error:
    st.warning(str(error))
    st.stop()

st.subheader("Selected-period summary")
st.write(
    f"{metrics['observations']:,} trading sessions from "
    f"{metrics['start_date']:%B %d, %Y} through "
    f"{metrics['end_date']:%B %d, %Y}."
)

row_one = st.columns(4)
row_one[0].metric("Total return", percent(metrics["total_return"]))
row_one[1].metric(
    "Annualized return",
    percent(metrics["annualized_return"]),
)
row_one[2].metric(
    "Annualized volatility",
    percent(metrics["annualized_volatility"]),
)
row_one[3].metric(
    "Maximum drawdown",
    percent(metrics["maximum_drawdown"]),
)

row_two = st.columns(4)
row_two[0].metric(
    f"Historical VaR ({confidence_label})",
    percent(metrics["historical_var"]),
)
row_two[1].metric(
    f"Expected shortfall ({confidence_label})",
    percent(metrics["expected_shortfall"]),
)
row_two[2].metric(
    "Positive-day rate",
    percent(metrics["positive_day_rate"]),
)
row_two[3].metric(
    "Sharpe ratio",
    f"{metrics['sharpe_ratio_zero_rf']:.2f}",
    help="Annualized using a zero risk-free-rate assumption.",
)

st.divider()
st.subheader("Index level and drawdown")

price_chart = period.set_index("Date")[["Close"]]
st.line_chart(price_chart, y="Close", y_label="Index level")

drawdown_chart = period.set_index("Date")[["Drawdown"]]
st.area_chart(drawdown_chart, y="Drawdown", y_label="Drawdown")

st.info(
    "Maximum drawdown reached "
    f"{percent(metrics['maximum_drawdown'])} on "
    f"{metrics['maximum_drawdown_date']:%B %d, %Y}."
)

st.divider()
st.subheader("Rolling annualized volatility")

volatility_columns = [
    "Volatility 20D",
    "Volatility 60D",
    "Volatility 252D",
]
volatility_chart = period.set_index("Date")[volatility_columns]
st.line_chart(volatility_chart, y=volatility_columns, y_label="Volatility")

regimes = classify_volatility_regimes(period)

if not regimes.empty:
    regime_summary = (
        regimes.groupby("Risk regime", as_index=False)
        .agg(
            Sessions=("Date", "size"),
            Average_volatility=("Volatility 60D", "mean"),
            Average_daily_return=("Daily return", "mean"),
        )
    )
    regime_summary["Average volatility"] = regime_summary[
        "Average_volatility"
    ].map(percent)
    regime_summary["Average daily return"] = regime_summary[
        "Average_daily_return"
    ].map(percent)
    regime_summary = regime_summary.drop(
        columns=["Average_volatility", "Average_daily_return"]
    )

    st.markdown("#### Sample-relative volatility regimes")
    st.dataframe(
        regime_summary,
        hide_index=True,
        use_container_width=True,
    )
    st.caption(
        "Low and high regimes represent the bottom and top quartiles of "
        "60-session annualized volatility within the selected period."
    )

st.divider()
st.subheader("Largest historical one-session losses")

worst = worst_sessions(period, count=10)
worst["Date"] = worst["Date"].dt.strftime("%Y-%m-%d")
worst["Close"] = worst["Close"].map(lambda value: f"{value:,.2f}")
worst["Daily return"] = worst["Daily return"].map(percent)
worst["Drawdown"] = worst["Drawdown"].map(percent)

st.dataframe(worst, hide_index=True, use_container_width=True)

with st.expander("Methodology and interpretation"):
    st.markdown(
        f"""
        - **Annualized return:** Compound growth over the selected period,
          annualized using 252 trading sessions per year.
        - **Annualized volatility:** Standard deviation of daily returns,
          multiplied by the square root of 252.
        - **Maximum drawdown:** Largest decline from a prior cumulative peak.
        - **Historical VaR ({confidence_label}):** Observed daily-loss threshold
          at the selected confidence level.
        - **Expected shortfall ({confidence_label}):** Average loss on days at
          or beyond the historical VaR threshold.
        - **Sharpe ratio:** Annualized mean daily excess return using a zero
          risk-free-rate assumption.
        """
    )

st.warning(
    "Educational portfolio project only. Historical risk does not predict "
    "future performance. This dashboard is not investment advice and should "
    "not be used to make trading or portfolio-allocation decisions."
)
