"""
App bootstrap.

- Exposes `create_app()` which wires layout + callbacks.
- Points Dash to the /assets folder (logo, styles.css, etc.).
"""

from __future__ import annotations

from pathlib import Path

from dash import Dash
import dash_bootstrap_components as dbc

from .layout import serve_layout
from .callbacks import register_callbacks


# Project root and assets path (…/realtime-trading-terminal/assets)
ROOT = Path(__file__).resolve().parents[1]
ASSETS_DIR = ROOT / "assets"


def create_app() -> Dash:
    """
    Create and configure the Dash application instance.

    Returns
    -------
    dash.Dash
        The configured Dash app.
    """
    app = Dash(
        __name__,
        external_stylesheets=[dbc.themes.BOOTSTRAP],
        suppress_callback_exceptions=True,  # we swap content by tabs
        title="Real-Time Trading Terminal",
        assets_folder=str(ASSETS_DIR),      # serve /assets automatically
        assets_url_path="/assets",
    )

    # Layout as a callable to ensure a fresh layout per request (useful in tests)
    app.layout = serve_layout

    # Register all callbacks (data fetching, graph updates, theme, etc.)
    register_callbacks(app)

    return app

