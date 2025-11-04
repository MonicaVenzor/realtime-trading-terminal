"""
Data acquisition helpers (yfinance).

Provides:
- download_history_tidy: fetch OHLCV for 1..N tickers and return a single
  tidy/long DataFrame with columns:
    [date, ticker, open, high, low, close, volume]
"""

from __future__ import annotations

from typing import Iterable, List
import pandas as pd
import yfinance as yf


def _normalize_columns(df: pd.DataFrame) -> pd.DataFrame:
    """Lowercase, snake_case and ensure the time column is named `date`."""
    out = df.reset_index()  # if DateTimeIndex, becomes `Date` (or `index`)
    out.columns = [str(c).strip().lower().replace(" ", "_") for c in out.columns]
    if "date" not in out.columns and "index" in out.columns:
        out = out.rename(columns={"index": "date"})
    if "close" not in out.columns and "adj_close" in out.columns:
        out = out.rename(columns={"adj_close": "close"})
    return out


def download_history_tidy(
    tickers: Iterable[str],
    period: str = "6mo",
    interval: str = "1d",
    auto_adjust: bool = True,
) -> pd.DataFrame:
    """
    Fetch historical OHLCV for each ticker and concatenate into one tidy frame.

    Parameters
    ----------
    tickers
        Iterable of ticker symbols (e.g., ["AAPL", "MSFT"]).
    period
        yfinance period (e.g., "1mo", "6mo", "1y", "max").
    interval
        yfinance interval (e.g., "1d", "1wk", "1h").
    auto_adjust
        Whether to auto-adjust OHLC for splits/dividends.

    Returns
    -------
    pd.DataFrame
        Columns subset of: [date, open, high, low, close, volume, ticker]
        Sorted by (ticker, date).
    """
    frames: list[pd.DataFrame] = []

    for t in tickers:
        hist = yf.Ticker(t).history(
            period=period, interval=interval, auto_adjust=auto_adjust
        )
        norm = _normalize_columns(hist)

        keep = [c for c in ["date", "open", "high", "low", "close", "volume"] if c in norm.columns]
        if not keep:
            continue

        block = norm[keep].copy()
        block["ticker"] = t
        frames.append(block)

    if not frames:
        raise RuntimeError("No data returned from yfinance. Check tickers/period/interval.")

    df = pd.concat(frames, ignore_index=True)
    df["date"] = pd.to_datetime(df["date"])
    df = df.sort_values(["ticker", "date"]).reset_index(drop=True)
    
    # Drop timezone info to avoid tz-aware comparison errors
    if pd.api.types.is_datetime64tz_dtype(df["date"]):
        df["date"] = df["date"].dt.tz_convert(None)
        
    return df
