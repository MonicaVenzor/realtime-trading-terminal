"""
Static layout / UI structure (Navbar, controls, tabs, cards).
"""

from __future__ import annotations

from dash import html, dcc
import dash_bootstrap_components as dbc


TICKER_OPTIONS = ["AAPL", "MSFT", "NVDA", "GOOGL", "AMZN", "META"]


def kpi_card(value_id: str, title: str, spark_id: str) -> dbc.Card:
    """Reusable KPI card with a title, value, and sparkline area."""
    return dbc.Card(
        dbc.CardBody(
            [
                html.Div(title, className="kpi-title"),
                html.H4("—", id=value_id, className="kpi-value"),
                dcc.Graph(
                    id=spark_id,
                    config={"displayModeBar": False},
                    style={"height": "46px", "marginTop": "6px"},
                ),
            ]
        ),
        # Keep cards subtle; visual weight comes from the graphs themselves
        className="kpi-card",
    )


def serve_layout():
    """
    Provide the root layout. We mount `data-theme="dark"` initially and
    flip it via callbacks to allow CSS `[data-theme=…]` selectors.
    """
    return html.Div(
        id="root-container",
        **{"data-theme": "dark"},
        children=[
            dbc.Container(
                [
                    # ===== NAVBAR =====
                    dbc.Navbar(
                        dbc.Container(
                            [
                                # LEFT: Yahoo brand logo
                                html.Div(
                                    html.Img(
                                        src="/assets/logo.png",
                                        className="brand-logo",
                                        style={"height": "28px", "width": "auto"},
                                        alt="Yahoo Finance",
                                    ),
                                    className="d-flex align-items-center gap-2 flex-grow-0 justify-content-start",
                                ),

                                # CENTER: single centered title
                                html.Div(
                                    html.H4(
                                        " Real-Time Trading Terminal ",
                                        className="text-center mb-0 brand-title-lg",
                                    ),
                                    className="mx-auto flex-grow-1 text-center",
                                ),

                                # RIGHT: author + theme toggle
                                html.Div(
                                    [
                                        html.Small(
                                            "by Monica Venzor", className="brand-subtitle me-3"
                                        ),
                                        dbc.RadioItems(
                                            id="theme-toggle",
                                            options=[
                                                {"label": "Light", "value": "light"},
                                                {"label": "Dark", "value": "dark"},
                                            ],
                                            value="dark",
                                            inline=True,
                                            className="theme-toggle",
                                        ),
                                    ],
                                    className="d-flex align-items-center justify-content-end",
                                ),
                            ]
                        ),
                        color="transparent",
                        dark=True,
                        className="nav-wrap",
                    ),

                    # ===== CONTROLS =====
                    dbc.Row(
                        [
                            dbc.Col(
                                dcc.Dropdown(
                                    id="ticker-select",
                                    options=[{"label": x, "value": x} for x in TICKER_OPTIONS],
                                    value=["AAPL", "MSFT", "NVDA"],
                                    multi=True,
                                    placeholder="Select one or more tickers…",
                                ),
                                md=6,
                            ),
                            dbc.Col(dcc.DatePickerRange(id="date-range", clearable=True), md=4),
                            dbc.Col(
                                dcc.Dropdown(
                                    id="interval-select",
                                    options=[
                                        {"label": lbl, "value": val}
                                        for lbl, val in [("1 Day", "1d"), ("1 Week", "1wk"), ("1 Month", "1mo")]
                                    ],
                                    value="1d",
                                    clearable=False,
                                ),
                                md=2,
                            ),
                        ],
                        className="mb-3",
                    ),

                    # ===== KPI CARDS =====
                    dbc.Row(
                        [
                            dbc.Col(kpi_card("kpi-price", "Last Close", "spark-price"), md=4),
                            dbc.Col(kpi_card("kpi-cum", "Cumulative Return", "spark-cum"), md=4),
                            dbc.Col(kpi_card("kpi-vol", "Volatility (20D, annualized)", "spark-vol"), md=4),
                        ],
                        className="mb-3",
                    ),

                    # ===== TABS =====
                    dbc.Tabs(
                        id="chart-tabs",
                        active_tab="price",
                        className="mb-3",
                        children=[
                            dbc.Tab(label="Price", tab_id="price"),
                            dbc.Tab(label="Candlesticks (single ticker)", tab_id="candle"),
                            dbc.Tab(label="Cumulative Return", tab_id="cum"),
                        ],
                    ),

                    # ===== MAIN CHARTS =====
                    dbc.Row(
                        [
                            dbc.Col(
                                dbc.Card(
                                    dbc.CardBody(dcc.Loading(dcc.Graph(id="main-chart"), type="dot")),
                                    className="chart-card",
                                ),
                                md=8,
                            ),
                            dbc.Col(
                                dbc.Card(
                                    dbc.CardBody(dcc.Loading(dcc.Graph(id="vol-chart"), type="dot")),
                                    className="chart-card",
                                ),
                                md=4,
                            ),
                        ],
                        className="mb-3",
                    ),

                    # ===== MINI ANALYTICS =====
                    dbc.Row(
                        [
                            dbc.Col(
                                dbc.Card(
                                    dbc.CardBody(dcc.Loading(dcc.Graph(id="ret-bar"), type="dot")),
                                    className="chart-card",
                                ),
                                md=8,
                            ),
                            dbc.Col(
                                dbc.Card(
                                    dbc.CardBody(dcc.Loading(dcc.Graph(id="corr-heatmap"), type="dot")),
                                    className="chart-card",
                                ),
                                md=4,
                            ),
                        ],
                        className="mt-3",
                    ),

                    html.Div(id="metrics-summary", className="mt-2 small text-muted"),
                    dcc.Store(id="theme-store", data="dark"),
                ],
                fluid=True,
            )
        ],
    )
