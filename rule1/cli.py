"""Command-line interface for Rule #1 investing analysis."""

from __future__ import annotations

import argparse
import sys

from rule1.calculator import DEFAULT_MARR, DEFAULT_MOS, DEFAULT_PROJECTION_YEARS, analyze_stock


def _fmt_currency(value: float | None) -> str:
    if value is None:
        return "N/A"
    return f"${value:,.2f}"


def _fmt_pct(value: float | None) -> str:
    if value is None:
        return "N/A"
    return f"{value * 100:.1f}%"


def run_analysis(args: argparse.Namespace) -> int:
    """Execute analysis and print results. Returns exit code."""
    ticker = args.ticker.upper()

    if args.fetch:
        try:
            from rule1.data import get_stock_data

            print(f"Fetching data for {ticker}…")
            data = get_stock_data(ticker)
        except (ImportError, ValueError) as exc:
            print(f"Error: {exc}", file=sys.stderr)
            return 1

        current_eps = data.get("eps_ttm") or args.eps
        current_price = data.get("current_price") or args.price
        historical_pe = data.get("trailing_pe") or args.pe
        eps_growth = data.get("eps_growth_5y") or args.growth

        if current_eps is None:
            print("Error: EPS could not be fetched. Provide --eps.", file=sys.stderr)
            return 1
        if eps_growth is None:
            print("Error: Growth rate could not be fetched. Provide --growth.", file=sys.stderr)
            return 1
    else:
        current_eps = args.eps
        current_price = args.price
        historical_pe = args.pe
        eps_growth = args.growth

        if current_eps is None:
            print("Error: --eps is required when --no-fetch is set.", file=sys.stderr)
            return 1
        if eps_growth is None:
            print("Error: --growth is required when --no-fetch is set.", file=sys.stderr)
            return 1

    try:
        result = analyze_stock(
            ticker=ticker,
            current_eps=current_eps,
            eps_growth_rate=eps_growth,
            historical_pe=historical_pe,
            current_price=current_price,
            marr=args.marr,
            margin_of_safety=args.mos,
            years=args.years,
        )
    except ValueError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1

    _print_results(result)
    return 0


def _print_results(result: dict) -> None:
    ticker = result["ticker"]
    width = 42
    separator = "─" * width

    print()
    print(f"  Rule #1 Analysis: {ticker}")
    print(separator)
    print(f"  {'Current EPS (TTM):':<28} {_fmt_currency(result['current_eps'])}")
    print(f"  {'EPS Growth Rate:':<28} {_fmt_pct(result['eps_growth_rate'])}")
    print(f"  {'Historical PE:':<28} {result['historical_pe'] or 'N/A'}")
    print(separator)
    print(f"  {'Future EPS (10-yr):':<28} {_fmt_currency(result['future_eps'])}")
    print(f"  {'Future PE:':<28} {result['future_pe']}")
    print(f"  {'Future Price (10-yr):':<28} {_fmt_currency(result['future_price'])}")
    print(separator)
    print(f"  {'Sticker Price (Intrinsic):':<28} {_fmt_currency(result['sticker_price'])}")
    print(f"  {'MOS Price (Buy Below):':<28} {_fmt_currency(result['mos_price'])}")

    if "current_price" in result:
        current_price = result["current_price"]
        is_on_sale = result["is_on_sale"]
        upside_pct = result["upside_pct"]
        print(separator)
        print(f"  {'Current Price:':<28} {_fmt_currency(current_price)}")
        print(f"  {'Upside to Sticker:':<28} {upside_pct}%")
        verdict = "✅ ON SALE – consider buying" if is_on_sale else "❌ OVERPRICED – wait"
        print(f"  {'Verdict:':<28} {verdict}")

    print(separator)
    print(f"  MARR: {_fmt_pct(result['marr'])}   MOS: {_fmt_pct(result['margin_of_safety'])}   "
          f"Projection: {result['projection_years']} yrs")
    print()


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="rule1",
        description="Rule #1 Investing – sticker price and margin-of-safety calculator",
    )
    parser.add_argument("ticker", help="Stock ticker symbol (e.g. AAPL)")
    parser.add_argument("--eps", type=float, default=None,
                        help="Current EPS (TTM). Auto-fetched if --fetch is set.")
    parser.add_argument("--growth", type=float, default=None,
                        help="Expected annual EPS growth rate as a decimal (e.g. 0.15 for 15%%). "
                             "Auto-fetched if --fetch is set.")
    parser.add_argument("--pe", type=float, default=None,
                        help="Historical average PE ratio (optional).")
    parser.add_argument("--price", type=float, default=None,
                        help="Current stock price (optional, for buy/hold verdict).")
    parser.add_argument("--marr", type=float, default=DEFAULT_MARR,
                        help=f"Minimum Acceptable Rate of Return (default {DEFAULT_MARR}).")
    parser.add_argument("--mos", type=float, default=DEFAULT_MOS,
                        help=f"Margin of Safety fraction (default {DEFAULT_MOS}).")
    parser.add_argument("--years", type=int, default=DEFAULT_PROJECTION_YEARS,
                        help=f"Projection horizon in years (default {DEFAULT_PROJECTION_YEARS}).")
    parser.add_argument("--fetch", dest="fetch", action="store_true", default=True,
                        help="Fetch live data from Yahoo Finance (default).")
    parser.add_argument("--no-fetch", dest="fetch", action="store_false",
                        help="Do not fetch live data; all values must be provided manually.")
    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()
    sys.exit(run_analysis(args))


if __name__ == "__main__":
    main()
