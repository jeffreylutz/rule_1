"""Rule #1 Investing toolkit.

Rule #1 Investing is a value investing strategy popularized by Phil Town.
The core principle: don't lose money. Find wonderful companies at attractive
prices by analyzing the "Big Five" growth numbers and computing intrinsic
value (sticker price) and margin-of-safety price.
"""

from rule1.calculator import (
    calculate_growth_rate,
    calculate_sticker_price,
    calculate_mos_price,
    calculate_future_eps,
    calculate_future_pe,
    calculate_future_price,
    analyze_stock,
)
from rule1.data import get_stock_data

__all__ = [
    "calculate_growth_rate",
    "calculate_sticker_price",
    "calculate_mos_price",
    "calculate_future_eps",
    "calculate_future_pe",
    "calculate_future_price",
    "analyze_stock",
    "get_stock_data",
]
