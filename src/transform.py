"""
Core transforms on tidy market data.

Expected input shape (tidy/long):
    [date, ticker, open, high, low, close, (volume)]

Functions:
- to_long: light validation/normalization to tidy format
- compute_returns: add daily_return and cum_return per ticker
- compute_volatility: add rolling annualized volatility (sqrt(252) * std)
"""

from __future__ import annotations

import pandas as pd


def to_long(df: pd.DataFrame) -> pd.DataFrame:
    """
    Ensure a tidy shape and normalize column names.

    Notes
    -----
    For this project the recommended entry point is `download_history_tidy()`,
    but this helper is handy if you ever ingest external/wide sources.

    Returns
    -------
    pd.DataFrame
        Columns: subset of [date, ticker, open, high, low, close, volume]
    """
    cols = {c.lower().replace(" ", "_") for c in df.columns}
    need = {"date", "open", "high", "low", "close"}  # volume optional
    if not need.issubset(cols):
        raise ValueError("to_long expected OHLC columns. Prefer download_history_tidy().")

    out = df.copy()
    out.columns = [c.lower().replace(" ", "_") for c in out.columns]
    if "ticker" not in out.columns:
        out["ticker"] = "TICKER"

    keep = [c for c in ["date", "ticker", "open", "high", "low", "close", "volume"] if c in out.columns]
    out = out[keep].copy()
    out["date"] = pd.to_datetime(out["date"])
    return out


def compute_returns(long_df: pd.DataFrame) -> pd.DataFrame:
    """
    Add per-ticker returns:
      - daily_return: pct_change of `close`
      - cum_return: cumulative (1+r) product minus 1

    Returns
    -------
    pd.DataFrame
        Original columns + ['daily_return', 'cum_return']
    """
    df = long_df.sort_values(["ticker", "date"]).copy()
    df["daily_return"] = df.groupby("ticker")["close"].pct_change()
    df["cum_return"] = (1 + df["daily_return"]).groupby(df["ticker"]).cumprod() - 1
    return df


def compute_volatility(long_df: pd.DataFrame, window: int = 20) -> pd.DataFrame:
    """
    Add rolling annualized volatility, per ticker:
        vol_{window}d_ann = sqrt(252) * std(daily_return, window)

    Parameters
    ----------
    long_df
        Tidy frame with at least [date, ticker, close] (and daily_return if precomputed).
    window
        Rolling window length in trading days.

    Returns
    -------
    pd.DataFrame
        Original columns + [f"vol_{window}d_ann"]
    """
    df = long_df.sort_values(["ticker", "date"]).copy()
    if "daily_return" not in df.columns:
        df["daily_return"] = df.groupby("ticker")["close"].pct_change()

    roll = (
        df.groupby("ticker")["daily_return"]
        .rolling(window)
        .std()
        .reset_index(level=0, drop=True)
    )
    df[f"vol_{window}d_ann"] = roll * (252 ** 0.5)
    return df
