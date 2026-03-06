"""Stock data retrieval for Rule #1 analysis.

Uses ``yfinance`` to fetch publicly available fundamental and price data.
"""

from __future__ import annotations

from typing import Any


def get_stock_data(ticker: str) -> dict[str, Any]:
    """Fetch key Rule #1 data for a stock ticker using yfinance.

    Retrieves:
    - Current price
    - Trailing EPS (TTM)
    - Trailing PE ratio
    - Forward EPS growth estimate (5-year analyst estimate where available)

    Args:
        ticker: Stock ticker symbol (e.g. ``"AAPL"``).

    Returns:
        Dictionary with the following keys (values may be ``None`` if
        unavailable):
        - ``ticker`` (str)
        - ``current_price`` (float or None)
        - ``eps_ttm`` (float or None)
        - ``trailing_pe`` (float or None)
        - ``forward_eps`` (float or None)
        - ``eps_growth_5y`` (float or None) – analyst 5-year EPS growth estimate

    Raises:
        ImportError: If ``yfinance`` is not installed.
        ValueError: If the ticker symbol is not found / returns no data.
    """
    try:
        import yfinance as yf
    except ImportError as exc:
        raise ImportError(
            "yfinance is required for data fetching. "
            "Install it with: pip install yfinance"
        ) from exc

    info: dict[str, Any] = yf.Ticker(ticker).info
    if not info or info.get("quoteType") is None:
        raise ValueError(f"No data found for ticker '{ticker}'")

    def _safe(key: str) -> float | None:
        val = info.get(key)
        try:
            return float(val) if val is not None else None
        except (TypeError, ValueError):
            return None

    current_price = _safe("currentPrice") or _safe("regularMarketPrice")
    eps_ttm = _safe("trailingEps")
    trailing_pe = _safe("trailingPE")
    forward_eps = _safe("forwardEps")

    # yfinance exposes analyst 5-year growth estimate as earningsGrowth
    # (a decimal) or earningsQuarterlyGrowth; prefer the growth estimates
    earnings_growth = _safe("earningsGrowth")

    return {
        "ticker": ticker.upper(),
        "current_price": current_price,
        "eps_ttm": eps_ttm,
        "trailing_pe": trailing_pe,
        "forward_eps": forward_eps,
        "eps_growth_5y": earnings_growth,
    }
