"""
Tiny baseline forecaster utilities.

NOTE: These are intentionally simple demos (e.g., linear trend) to keep the
focus on the dashboard. Replace with proper models if needed.
"""

from __future__ import annotations

import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression


def linear_trend(df: pd.DataFrame, ticker: str, horizon: int = 10) -> pd.DataFrame:
    """
    Fit a linear model close ~ time and predict the next `horizon` business days.

    Parameters
    ----------
    df
        Tidy frame with at least [date, ticker, close].
    ticker
        Ticker to model.
    horizon
        Number of future business days to predict.

    Returns
    -------
    pd.DataFrame
        Columns: [date, ticker, close_pred]
    """
    sub = df[df["ticker"] == ticker].dropna(subset=["close"]).copy()
    sub = sub.sort_values("date")
    if sub.empty:
        return pd.DataFrame(columns=["date", "ticker", "close_pred"])

    # time index feature
    sub["t"] = np.arange(len(sub), dtype=float)
    X = sub["t"].to_numpy().reshape(-1, 1)
    y = sub["close"].to_numpy()

    model = LinearRegression().fit(X, y)

    last_t = sub["t"].iloc[-1]
    fut_t = np.arange(last_t + 1, last_t + 1 + horizon, dtype=float).reshape(-1, 1)
    preds = model.predict(fut_t)

    fut_dates = pd.bdate_range(sub["date"].iloc[-1], periods=horizon + 1, closed="right")
    out = pd.DataFrame({"date": fut_dates, "ticker": ticker, "close_pred": preds})
    return out
