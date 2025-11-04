"""
All Dash callbacks: data fetch, transformations and figure rendering.
"""

from __future__ import annotations

from functools import lru_cache

import pandas as pd
from dash import Dash, Input, Output
import plotly.express as px
import plotly.graph_objects as go

from src.fetch import download_history_tidy
from src.transform import compute_returns, compute_volatility


# ---------- Yahoo-inspired color system ----------

YH_PURPLE   = "#6001D2"
YH_PURPLE_2 = "#7A37FF"
YH_MAGENTA  = "#FF1A8C"
YH_CYAN     = "#00D3F0"
YH_TEAL     = "#00C08B"
YH_YELLOW   = "#FFC043"
YH_SLATE    = "#4B5563"

# Line series palette (max ~6 series before repeating)
YH_COLORWAY = [YH_PURPLE, YH_CYAN, YH_MAGENTA, YH_TEAL, YH_PURPLE_2, YH_YELLOW]

# Diverging scale for correlations: -1 (blue) → 0 (light) → +1 (purple)
YH_DIVERGING = [
    [0.0,  "#1B9CE5"],
    [0.5,  "#F5F5F5"],
    [1.0,  YH_PURPLE],
]


# ---------- Plot helpers ----------

def apply_template(fig: go.Figure, theme: str) -> go.Figure:
    """Apply uniform layout: centered title, subtle grids, theme bg."""
    is_dark = theme == "dark"
    fig.update_layout(
        template="plotly_dark" if is_dark else "plotly",
        margin=dict(l=40, r=20, t=50, b=40),
        colorway=YH_COLORWAY,
        title_x=0.5,
        title_xanchor="center",
        title_font=dict(size=18, family="Inter, system-ui, -apple-system, Segoe UI, Roboto, Arial"),
        paper_bgcolor="#0f1115" if is_dark else "#ffffff",
        plot_bgcolor="#151923" if is_dark else "#ffffff",
        xaxis=dict(showgrid=True, gridcolor="rgba(255,255,255,.06)" if is_dark else "rgba(0,0,0,.07)"),
        yaxis=dict(showgrid=True, gridcolor="rgba(255,255,255,.06)" if is_dark else "rgba(0,0,0,.07)"),
    )
    return fig


def sparkline(x, y, theme: str) -> go.Figure:
    """Sparkline for KPI cards (no axes, no title)."""
    fig = go.Figure(
        go.Scatter(x=x, y=y, mode="lines", line=dict(width=2, color=YH_PURPLE))
    )
    fig.update_layout(
        title=None,
        margin=dict(l=0, r=0, t=0, b=0),
        xaxis=dict(visible=False),
        yaxis=dict(visible=False),
        template="plotly_dark" if theme == "dark" else "plotly",
    )
    return fig


# ---------- Data layer (cached) ----------

@lru_cache(maxsize=64)
def _cached_fetch(tickers_key: str, interval: str) -> pd.DataFrame:
    """
    Fetch market data and compute metrics, cached by (tickers_key, interval).

    tickers_key : str
        Comma-joined tickers, e.g. "AAPL,MSFT,NVDA" to make it hashable for LRU cache.
    """
    tickers = tickers_key.split(",")
    df = download_history_tidy(tickers, period="12mo", interval=interval)
    df = compute_returns(df)
    df = compute_volatility(df, window=20)
    return df


# ---------- Callback registration ----------

def register_callbacks(app: Dash) -> None:
    """
    Wire all Dash callbacks to the provided `app`.
    """

    # Persist selected theme in hidden Store
    @app.callback(Output("theme-store", "data"), Input("theme-toggle", "value"))
    def _persist_theme(v: str | None) -> str:
        return v or "dark"

    # Reflect theme into a data attribute for CSS (`[data-theme="…"]` selectors)
    @app.callback(Output("root-container", "data-theme"), Input("theme-store", "data"))
    def _apply_theme(theme_value: str | None) -> str:
        return theme_value or "dark"

    @app.callback(
        Output("main-chart", "figure"),
        Output("vol-chart", "figure"),
        Output("kpi-price", "children"),
        Output("kpi-cum", "children"),
        Output("kpi-vol", "children"),
        Output("metrics-summary", "children"),
        # KPI sparklines
        Output("spark-price", "figure"),
        Output("spark-cum", "figure"),
        Output("spark-vol", "figure"),
        # Mini analytics
        Output("ret-bar", "figure"),
        Output("corr-heatmap", "figure"),
        Input("ticker-select", "value"),
        Input("date-range", "start_date"),
        Input("date-range", "end_date"),
        Input("interval-select", "value"),
        Input("chart-tabs", "active_tab"),
        Input("theme-store", "data"),
        prevent_initial_call=False,
    )
    def update_main(tickers, start_date, end_date, interval, tab, theme):
        # Empty state
        if not tickers:
            empty = go.Figure()
            return (empty, empty, "—", "—", "—", "Select at least one ticker.",
                    empty, empty, empty, empty, empty)

        # Fetch + precompute
        tickers_key = ",".join(tickers)
        long = _cached_fetch(tickers_key, interval)

        # Optional date filter
        if start_date and end_date:
            m = (long["date"] >= pd.to_datetime(start_date)) & (long["date"] <= pd.to_datetime(end_date))
            long = long[m]

        # ----- Main chart (tabbed) -----
        if tab == "cum":
            fig_main = px.line(
                long, x="date", y="cum_return", color="ticker",
                title="Cumulative Return", color_discrete_sequence=YH_COLORWAY
            )
            fig_main.update_layout(yaxis_tickformat=".0%")

        elif tab == "candle" and isinstance(tickers, list) and len(tickers) == 1:
            t = tickers[0]
            sub = long[long["ticker"] == t]
            fig_main = go.Figure(
                [go.Candlestick(x=sub["date"], open=sub["open"], high=sub["high"], low=sub["low"], close=sub["close"])]
            ).update_layout(title=f"{t} — Candlestick", xaxis_rangeslider_visible=False)

        else:
            fig_main = px.line(
                long, x="date", y="close", color="ticker",
                title="Close Price", color_discrete_sequence=YH_COLORWAY
            )

        fig_main = apply_template(fig_main, theme)

        # ----- Volatility (first ticker) -----
        pick = tickers[0] if isinstance(tickers, list) else tickers
        vol = long[(long["ticker"] == pick) & (long["vol_20d_ann"].notna())]
        if vol.empty:
            fig_vol = go.Figure().update_layout(title="Volatility")
        else:
            fig_vol = px.line(
                vol, x="date", y="vol_20d_ann",
                title=f"{pick} — 20D Annualized Volatility",
                color_discrete_sequence=[YH_PURPLE],
            )
            fig_vol.update_layout(yaxis_tickformat=".2%")
        fig_vol = apply_template(fig_vol, theme)

        # ----- KPI values (first ticker) -----
        sub = long[long["ticker"] == pick].dropna(subset=["close"])
        last_close = sub["close"].iloc[-1] if not sub.empty else None
        last_cum   = sub["cum_return"].iloc[-1] if "cum_return" in sub and not sub.empty else None
        last_vol   = sub["vol_20d_ann"].dropna().iloc[-1] if "vol_20d_ann" in sub and sub["vol_20d_ann"].notna().any() else None

        k_price = f"${last_close:,.2f}" if last_close is not None else "—"
        k_cum   = f"{last_cum:.1%}" if last_cum is not None else "—"
        k_vol   = f"{last_vol:.1%}" if last_vol is not None else "—"

        # ----- Summary for all tickers -----
        parts: list[str] = []
        for t in (tickers if isinstance(tickers, list) else [tickers]):
            s = long[long["ticker"] == t].dropna(subset=["close"])
            if s.empty:
                continue
            c  = s["close"].iloc[-1]
            cu = s["cum_return"].iloc[-1] if "cum_return" in s else None
            vv = s["vol_20d_ann"].dropna().iloc[-1] if "vol_20d_ann" in s and s["vol_20d_ann"].notna().any() else None
            parts.append(f"{t}: Close={c:,.2f} | Cum={'' if cu is None else f'{cu:.1%}'} | Vol20D={'' if vv is None else f'{vv:.1%}'}")
        summary = "  •  ".join(parts)

        # ----- KPI sparklines (last ~60 points of first ticker) -----
        tail = sub.tail(60) if not sub.empty else pd.DataFrame(columns=sub.columns)
        spark_price = sparkline(tail["date"], tail["close"], theme)
        spark_cum   = sparkline(tail["date"], tail["cum_return"], theme)
        spark_vol   = sparkline(tail["date"], tail["vol_20d_ann"], theme)

        # ----- Daily returns bar -----
        bars = sub.dropna(subset=["daily_return"]).tail(120)
        if bars.empty:
            ret_bar = go.Figure()
        else:
            ret_bar = px.bar(
                bars, x="date", y="daily_return",
                title=f"{pick} — Daily Returns",
                color_discrete_sequence=[YH_PURPLE],
            )
            ret_bar.update_layout(yaxis_tickformat=".1%")
            ret_bar = apply_template(ret_bar, theme)

        # ----- Correlation heatmap (selected tickers) -----
        wide = (long.pivot_table(index="date", columns="ticker", values="daily_return").dropna(how="all"))
        if wide.empty or wide.shape[1] < 2:
            corr_heat = go.Figure()
        else:
            corr = wide.corr()
            corr_heat = px.imshow(
                corr, text_auto=".2f", title="Return Correlation",
                zmin=-1, zmax=1, color_continuous_scale=YH_DIVERGING,
            )
            corr_heat = apply_template(corr_heat, theme)

        return (fig_main, fig_vol, k_price, k_cum, k_vol, summary,
                spark_price, spark_cum, spark_vol, ret_bar, corr_heat)
