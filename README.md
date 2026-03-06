# rule_1

A Python toolkit for **Rule #1 Investing** – the value-investing strategy
popularized by Phil Town (based on Warren Buffett's first rule: *don't lose
money*).

## What is Rule #1 Investing?

Rule #1 investing focuses on buying *wonderful companies* at *attractive
prices*.  The core workflow is:

1. **Find wonderful companies** whose "Big Five" numbers (ROIC, EPS growth,
   Sales growth, Book Value Per Share growth, Free Cash Flow growth) have
   grown at ≥ 10 % per year for 10 years.
2. **Calculate intrinsic value** (the *sticker price*) using a future-PE
   discounted-cash-flow approach.
3. **Buy only at or below** the *Margin of Safety price* (50 % of sticker
   price).

## Installation

```bash
pip install -e .            # core calculations only
pip install -e ".[fetch]"   # + live data via yfinance
pip install -e ".[dev]"     # + pytest for development
```

## Quick start

### Command line

```bash
# Manual values (no network required)
rule1 AAPL --no-fetch --eps 6.57 --growth 0.12 --pe 28 --price 195

# Fetch live data from Yahoo Finance
rule1 MSFT --fetch
```

Example output:

```
  Rule #1 Analysis: AAPL
──────────────────────────────────────────
  Current EPS (TTM):           $6.57
  EPS Growth Rate:             12.0%
  Historical PE:               28.0
──────────────────────────────────────────
  Future EPS (10-yr):          $20.39
  Future PE:                   24.0
  Future Price (10-yr):        $489.39
──────────────────────────────────────────
  Sticker Price (Intrinsic):   $121.02
  MOS Price (Buy Below):       $60.51
──────────────────────────────────────────
  Current Price:               $195.00
  Upside to Sticker:           -37.9%
  Verdict:                     ❌ OVERPRICED – wait
──────────────────────────────────────────
  MARR: 15.0%   MOS: 50.0%   Projection: 10 yrs
```

### Python API

```python
from rule1 import analyze_stock, calculate_growth_rate

# Calculate EPS growth rate from historical data
growth = calculate_growth_rate(past_value=2.50, current_value=6.57, years=10)
print(f"EPS CAGR: {growth:.1%}")   # → EPS CAGR: 10.1%

# Full Rule #1 analysis
result = analyze_stock(
    ticker="AAPL",
    current_eps=6.57,
    eps_growth_rate=0.12,
    historical_pe=28,
    current_price=195.0,
)
print(f"Sticker price : ${result['sticker_price']:.2f}")
print(f"MOS price     : ${result['mos_price']:.2f}")
print(f"On sale?      : {result['is_on_sale']}")
```

## Key formulas

| Value | Formula |
|---|---|
| Future EPS | `EPS × (1 + g)^10` |
| Future PE | `min(2 × g%, historical PE)` |
| Future Price | `Future EPS × Future PE` |
| Sticker Price | `Future Price ÷ (1 + MARR)^10` |
| MOS Price | `Sticker Price × (1 − MOS)` |

Defaults: **MARR = 15 %**, **MOS = 50 %**, **10-year projection**.

## Running tests

```bash
pytest
```
