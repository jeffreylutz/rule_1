"""Core Rule #1 investing calculations.

The Rule #1 method (Phil Town) involves:
1. Evaluating the "Big Five" growth numbers (must be >= 10% for 10 years):
   - Return on Investment Capital (ROIC)
   - Earnings Per Share (EPS) growth
   - Sales/Revenue growth
   - Book Value Per Share (BVPS) growth
   - Free Cash Flow (FCF) growth
2. Calculating intrinsic value (sticker price) using a future PE model.
3. Buying only when the current price is at or below the Margin of Safety
   price (50% of sticker price).
"""

from __future__ import annotations

DEFAULT_MARR = 0.15  # Minimum Acceptable Rate of Return (15%)
DEFAULT_MOS = 0.50  # Margin of Safety (50%)
DEFAULT_PROJECTION_YEARS = 10


def calculate_growth_rate(past_value: float, current_value: float, years: int) -> float:
    """Calculate the Compound Annual Growth Rate (CAGR).

    Args:
        past_value: The value at the beginning of the period.
        current_value: The value at the end of the period.
        years: Number of years between the two values.

    Returns:
        CAGR as a decimal (e.g. 0.10 for 10%).

    Raises:
        ValueError: If past_value or years are not positive.
    """
    if years <= 0:
        raise ValueError("years must be a positive integer")
    if past_value <= 0:
        raise ValueError("past_value must be positive")
    if current_value <= 0:
        raise ValueError("current_value must be positive")
    return (current_value / past_value) ** (1.0 / years) - 1.0


def calculate_future_eps(
    current_eps: float,
    growth_rate: float,
    years: int = DEFAULT_PROJECTION_YEARS,
) -> float:
    """Project future EPS based on the estimated growth rate.

    Args:
        current_eps: Current earnings per share.
        growth_rate: Expected annual EPS growth rate (decimal).
        years: Number of years to project (default 10).

    Returns:
        Projected EPS.

    Raises:
        ValueError: If current_eps is not positive.
    """
    if current_eps <= 0:
        raise ValueError("current_eps must be positive")
    return current_eps * (1.0 + growth_rate) ** years


def calculate_future_pe(
    analyst_growth_rate: float,
    historical_pe: float | None = None,
) -> float:
    """Estimate the future PE ratio.

    Rule #1 uses the lower of:
      - the historical (average) PE ratio
      - 2 × the growth rate expressed as a percentage

    If no historical PE is provided, 2 × growth% is used.

    Args:
        analyst_growth_rate: Analyst's estimated annual EPS growth rate (decimal).
        historical_pe: Historical average PE ratio (optional).

    Returns:
        Estimated future PE ratio.

    Raises:
        ValueError: If analyst_growth_rate is not positive.
    """
    if analyst_growth_rate <= 0:
        raise ValueError("analyst_growth_rate must be positive")
    rule_pe = 2.0 * (analyst_growth_rate * 100.0)
    if historical_pe is not None and historical_pe > 0:
        return min(rule_pe, historical_pe)
    return rule_pe


def calculate_future_price(future_eps: float, future_pe: float) -> float:
    """Calculate the projected future stock price.

    Args:
        future_eps: Projected future EPS.
        future_pe: Estimated future PE ratio.

    Returns:
        Projected future price.

    Raises:
        ValueError: If future_eps or future_pe are not positive.
    """
    if future_eps <= 0:
        raise ValueError("future_eps must be positive")
    if future_pe <= 0:
        raise ValueError("future_pe must be positive")
    return future_eps * future_pe


def calculate_sticker_price(
    future_price: float,
    marr: float = DEFAULT_MARR,
    years: int = DEFAULT_PROJECTION_YEARS,
) -> float:
    """Calculate the sticker price (intrinsic value) today.

    Discounts the future price back to the present using the Minimum
    Acceptable Rate of Return (MARR), which defaults to 15%.

    Args:
        future_price: The projected stock price in ``years`` years.
        marr: Minimum Acceptable Rate of Return (default 0.15).
        years: Projection horizon in years (default 10).

    Returns:
        Sticker price (intrinsic / fair value) today.

    Raises:
        ValueError: If future_price is not positive or marr is not positive.
    """
    if future_price <= 0:
        raise ValueError("future_price must be positive")
    if marr <= 0:
        raise ValueError("marr must be positive")
    return future_price / (1.0 + marr) ** years


def calculate_mos_price(
    sticker_price: float,
    margin_of_safety: float = DEFAULT_MOS,
) -> float:
    """Calculate the Margin of Safety (MOS) price.

    This is the maximum price you should pay for the stock.  The default
    margin of safety is 50%, meaning you buy at half the sticker price.

    Args:
        sticker_price: The intrinsic / fair value of the stock.
        margin_of_safety: Safety discount as a decimal (default 0.50).

    Returns:
        MOS buy price.

    Raises:
        ValueError: If sticker_price is not positive or margin_of_safety is
            not between 0 and 1 (exclusive).
    """
    if sticker_price <= 0:
        raise ValueError("sticker_price must be positive")
    if not (0.0 < margin_of_safety < 1.0):
        raise ValueError("margin_of_safety must be greater than 0 and less than 1")
    return sticker_price * (1.0 - margin_of_safety)


def analyze_stock(
    ticker: str,
    current_eps: float,
    eps_growth_rate: float,
    historical_pe: float | None = None,
    current_price: float | None = None,
    marr: float = DEFAULT_MARR,
    margin_of_safety: float = DEFAULT_MOS,
    years: int = DEFAULT_PROJECTION_YEARS,
) -> dict:
    """Run a complete Rule #1 analysis for a stock.

    Args:
        ticker: Stock ticker symbol (used for display only in this function).
        current_eps: Current (TTM) earnings per share.
        eps_growth_rate: Estimated annual EPS growth rate (decimal).
        historical_pe: Historical average PE ratio (optional).
        current_price: Current stock price (optional, used to evaluate buy).
        marr: Minimum Acceptable Rate of Return (default 0.15).
        margin_of_safety: Safety discount (default 0.50).
        years: Projection horizon in years (default 10).

    Returns:
        A dictionary with all Rule #1 intermediate and final values.
    """
    future_eps = calculate_future_eps(current_eps, eps_growth_rate, years)
    future_pe = calculate_future_pe(eps_growth_rate, historical_pe)
    future_price = calculate_future_price(future_eps, future_pe)
    sticker_price = calculate_sticker_price(future_price, marr, years)
    mos_price = calculate_mos_price(sticker_price, margin_of_safety)

    result = {
        "ticker": ticker.upper(),
        "current_eps": current_eps,
        "eps_growth_rate": eps_growth_rate,
        "historical_pe": historical_pe,
        "future_eps": round(future_eps, 2),
        "future_pe": round(future_pe, 2),
        "future_price": round(future_price, 2),
        "sticker_price": round(sticker_price, 2),
        "mos_price": round(mos_price, 2),
        "marr": marr,
        "margin_of_safety": margin_of_safety,
        "projection_years": years,
    }

    if current_price is not None:
        result["current_price"] = current_price
        result["is_on_sale"] = current_price <= mos_price
        result["upside_pct"] = round((sticker_price / current_price - 1.0) * 100.0, 1)

    return result
