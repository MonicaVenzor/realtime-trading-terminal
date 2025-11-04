"""
Small Plotly figure builders for ad-hoc usage outside Dash callbacks.

The Dash app constructs its figures directly in callbacks, but these helpers
remain useful for notebooks or unit tests.
"""

from __future__ import annotations

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go


def price_lines(df: pd.DataFrame, tickers: list[str]) -> go.Figure:
    sub = df[df["ticker"].isin(tickers)]
    fig = px.line(sub, x="date", y="close", color="ticker", title="Close Price")
    fig.update_layout(margin=dict(l=40, r=20, t=40, b=30))
    return fig


def cumulative_return_lines(df: pd.DataFrame, tickers: list[str]) -> go.Figure:
    sub = df[df["ticker"].isin(tickers)]
    fig = px.line(sub, x="date", y="cum_return", color="ticker", title="Cumulative Return")
    fig.update_layout(margin=dict(l=40, r=20, t=40, b=30), yaxis_tickformat=".0%")
    return fig


def volatility_line(df: pd.DataFrame, ticker: str, window: int = 20) -> go.Figure:
    col = f"vol_{window}d_ann"
    sub = df[(df["ticker"] == ticker) & (df[col].notna())]
    fig = px.line(sub, x="date", y=col, title=f"{ticker} — {window}D Annualized Volatility")
    fig.update_layout(margin=dict(l=40, r=20, t=40, b=30), yaxis_tickformat=".2%")
    return fig
