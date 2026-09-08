# NASDAQ-100 Market Risk Analytics

An interactive Streamlit dashboard for examining historical NASDAQ-100 market
risk through returns, volatility, drawdowns, historical Value at Risk and
Expected Shortfall.

The project also documents a rejected directional-forecasting experiment. The
model was not deployed because it failed to outperform simple baselines on an
untouched test period.

## Business Question

How did the historical risk profile of the NASDAQ-100 change between July 2014
and July 2024, and what can drawdown, volatility and tail-loss measures reveal
that cumulative return alone does not?

The dashboard is designed for historical risk exploration. It does not predict
future prices, recommend trades or make portfolio-allocation decisions.

## Dataset

The repository contains 2,528 daily NASDAQ-100 index observations covering:

- July 8, 2014 through July 5, 2024
- Closing index level
- Opening index level
- Daily high
- Daily low

The records are complete, contain no duplicate dates and are sorted
chronologically during processing. The repository dataset is retained for
reproducibility. Its original source and licensing should be independently
verified before reuse outside this educational project.

## Dashboard Capabilities

Users can select a historical period and compare:

- Total and annualized return
- Annualized volatility
- Maximum drawdown and its date
- Historical Value at Risk at 95% or 99%
- Expected Shortfall at 95% or 99%
- Positive-session frequency
- Best and worst daily returns
- Sharpe ratio using a zero risk-free-rate assumption
- Rolling 20-, 60- and 252-session annualized volatility
- Sample-relative volatility regimes
- The ten largest historical one-session losses

## Verified Full-Period Results

For July 8, 2014 through July 5, 2024:

| Metric | Result |
|---|---:|
| Observations | 2,528 |
| Total return | 427.73% |
| Annualized return | 18.04% |
| Annualized volatility | 21.73% |
| Maximum drawdown | -35.56% |
| Maximum drawdown date | December 28, 2022 |
| Positive-day rate | 55.40% |
| Best daily return | 10.07% |
| Worst daily return | -12.19% |
| Sharpe ratio, zero risk-free rate | 0.87 |

### Historical Tail Risk

| Confidence level | Historical VaR | Expected Shortfall |
|---|---:|---:|
| 95% | 2.19% | 3.29% |
| 99% | 3.93% | 5.05% |

Historical VaR represents the observed daily-loss threshold at the selected
confidence level. Expected Shortfall is the average loss among sessions at or
beyond that threshold. Neither measure predicts the size or frequency of future
losses.

## Forecasting Experiment and Rejection Decision

A separate experiment tested whether lagged returns, moving-average gaps,
intraday range and rolling volatility could classify the next session as up or
down.

The experiment used:

1. Chronological 60% training, 20% validation and 20% test periods
2. Validation-only threshold selection
3. An untouched 494-observation test period
4. Five expanding-window time-series cross-validation folds
5. Majority-class and previous-direction baselines

### Untouched Test Results

| Model | Accuracy | Balanced accuracy | Precision | Recall | F1 | ROC-AUC |
|---|---:|---:|---:|---:|---:|---:|
| Majority baseline | 53.64% | 50.00% | 53.64% | 100.00% | 69.83% | — |
| Previous-direction baseline | 52.83% | 52.60% | 56.06% | 55.85% | 55.95% | — |
| Random forest | 46.36% | 49.76% | 50.00% | 3.02% | 5.69% | 0.4512 |

The random forest's mean time-series cross-validation ROC-AUC was `0.4920 ±
0.0263`, and its mean balanced accuracy was `0.4830 ± 0.0304`.

**Decision: reject the forecasting model.** It did not outperform the strongest
naive baseline and therefore is not used by the dashboard. This rejection is an
intentional model-governance outcome rather than a hidden unsuccessful result.

Detailed experiment outputs are retained under
`reports/forecasting_experiment/`.

## Methodology

### Annualized Return

Compound growth over the selected period is annualized using 252 trading
sessions per year.

### Annualized Volatility

The standard deviation of daily returns is multiplied by the square root of
252.

### Maximum Drawdown

Drawdown measures the percentage decline from the cumulative historical peak.
Maximum drawdown is the lowest observed value in that series.

### Historical VaR and Expected Shortfall

Historical VaR uses the empirical return distribution without assuming normal
returns. Expected Shortfall averages the returns in the corresponding loss
tail.

### Volatility Regimes

The dashboard classifies rolling 60-session annualized volatility using the
selected period's quartiles:

- Low: bottom quartile
- Normal: middle two quartiles
- High: top quartile

These are sample-relative analytical labels, not forecasts or trading signals.

## Repository Structure

```text
nasdaq-market-risk-dashboard/
├── app.py
├── risk_analysis.py
├── train_evaluate.py
├── data/
│   └── nasdaq_100_2014_2024.csv
├── reports/
│   └── forecasting_experiment/
│       ├── feature_importance.csv
│       ├── model_metadata.json
│       ├── model_results.csv
│       ├── test_predictions.csv
│       ├── time_series_cross_validation.csv
│       └── validation_thresholds.csv
├── tests/
│   └── test_risk_analysis.py
├── .streamlit/
│   └── config.toml
├── .gitignore
├── .python-version
├── Procfile
├── requirements.txt
├── requirements-dev.txt
└── README.md
```

## Installation

Clone and enter the repository:

```bash
git clone https://github.com/bofori20/nasdaq-market-risk-dashboard.git
cd nasdaq-market-risk-dashboard
```

Create and activate a Python 3.11 environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Install application dependencies:

```bash
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

For development and automated testing:

```bash
python -m pip install -r requirements-dev.txt
```

## Run the Dashboard

```bash
streamlit run app.py
```

Open `http://localhost:8501` if Streamlit does not open a browser automatically.

## Run Automated Tests

```bash
python -m pytest -q
```

The test suite validates data ordering, date filtering, return recalculation,
risk-metric boundaries, worst-session ordering and volatility-regime labels.

## Reproduce the Rejected Forecasting Experiment

```bash
python train_evaluate.py
```

This recreates the CSV and JSON evidence under
`reports/forecasting_experiment/`. It does not save or deploy a prediction
model.

## Production Command

The included `Procfile` runs the Streamlit application with the platform's
assigned port:

```text
web: streamlit run app.py --server.port=$PORT --server.address=0.0.0.0
```

## Limitations

- The dataset ends on July 5, 2024 and does not contain live prices.
- The dataset contains index-level OHLC data but no volume, constituents,
  macroeconomic variables or risk-free-rate series.
- Results are sensitive to the selected historical period.
- Historical VaR and Expected Shortfall may understate losses outside the
  observed sample.
- The Sharpe ratio assumes a zero risk-free rate.
- Volatility-regime thresholds are relative to the selected sample.
- Historical relationships may not persist in future market environments.
- The rejected forecasting experiment is not evidence of market predictability.

## Responsible-Use Statement

This is an educational portfolio project. Historical results do not predict
future performance. The dashboard is not investment advice and must not be used
as the sole basis for trading, investment or portfolio-allocation decisions.

## Author

**Bright Ofori**

Master's in Data Science with professional experience in banking, lending
operations and customer financial services.
