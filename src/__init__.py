"""
src package

Exports the small public surface used by the Dash layer:
- download_history_tidy: data acquisition (yfinance)
- to_long / compute_returns / compute_volatility: core transforms
"""

from .fetch import download_history_tidy
from .transform import to_long, compute_returns, compute_volatility

__all__ = [
    "download_history_tidy",
    "to_long",
    "compute_returns",
    "compute_volatility",
]
