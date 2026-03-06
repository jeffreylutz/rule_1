"""Tests for rule1.calculator module."""

import pytest

from rule1.calculator import (
    calculate_growth_rate,
    calculate_future_eps,
    calculate_future_pe,
    calculate_future_price,
    calculate_sticker_price,
    calculate_mos_price,
    analyze_stock,
)


# ---------------------------------------------------------------------------
# calculate_growth_rate
# ---------------------------------------------------------------------------

class TestCalculateGrowthRate:
    def test_ten_percent_growth(self):
        # $1 growing to $2.594 over 10 years ≈ 10% CAGR
        rate = calculate_growth_rate(past_value=1.0, current_value=2.5937, years=10)
        assert abs(rate - 0.10) < 0.001

    def test_zero_growth(self):
        rate = calculate_growth_rate(past_value=5.0, current_value=5.0, years=5)
        assert abs(rate) < 1e-9

    def test_one_year(self):
        rate = calculate_growth_rate(past_value=100.0, current_value=115.0, years=1)
        assert abs(rate - 0.15) < 1e-9

    def test_invalid_years(self):
        with pytest.raises(ValueError, match="years must be a positive integer"):
            calculate_growth_rate(1.0, 2.0, 0)

    def test_invalid_past_value(self):
        with pytest.raises(ValueError, match="past_value must be positive"):
            calculate_growth_rate(0.0, 2.0, 10)

    def test_invalid_current_value(self):
        with pytest.raises(ValueError, match="current_value must be positive"):
            calculate_growth_rate(1.0, -2.0, 10)


# ---------------------------------------------------------------------------
# calculate_future_eps
# ---------------------------------------------------------------------------

class TestCalculateFutureEps:
    def test_basic(self):
        # $1 EPS at 10% for 10 years
        future = calculate_future_eps(current_eps=1.0, growth_rate=0.10, years=10)
        assert abs(future - 2.5937) < 0.001

    def test_zero_growth(self):
        future = calculate_future_eps(current_eps=5.0, growth_rate=0.0, years=10)
        assert abs(future - 5.0) < 1e-9

    def test_invalid_eps(self):
        with pytest.raises(ValueError, match="current_eps must be positive"):
            calculate_future_eps(current_eps=0.0, growth_rate=0.10)


# ---------------------------------------------------------------------------
# calculate_future_pe
# ---------------------------------------------------------------------------

class TestCalculateFuturePe:
    def test_no_historical_pe(self):
        # 15% growth → 2 × 15 = 30
        pe = calculate_future_pe(analyst_growth_rate=0.15)
        assert abs(pe - 30.0) < 1e-9

    def test_historical_pe_is_lower(self):
        # 15% growth → rule_pe = 30; historical = 20 → use 20
        pe = calculate_future_pe(analyst_growth_rate=0.15, historical_pe=20.0)
        assert abs(pe - 20.0) < 1e-9

    def test_rule_pe_is_lower(self):
        # 10% growth → rule_pe = 20; historical = 40 → use 20
        pe = calculate_future_pe(analyst_growth_rate=0.10, historical_pe=40.0)
        assert abs(pe - 20.0) < 1e-9

    def test_invalid_growth(self):
        with pytest.raises(ValueError, match="analyst_growth_rate must be positive"):
            calculate_future_pe(analyst_growth_rate=0.0)


# ---------------------------------------------------------------------------
# calculate_future_price
# ---------------------------------------------------------------------------

class TestCalculateFuturePrice:
    def test_basic(self):
        price = calculate_future_price(future_eps=5.0, future_pe=20.0)
        assert abs(price - 100.0) < 1e-9

    def test_invalid_eps(self):
        with pytest.raises(ValueError):
            calculate_future_price(future_eps=0.0, future_pe=20.0)

    def test_invalid_pe(self):
        with pytest.raises(ValueError):
            calculate_future_price(future_eps=5.0, future_pe=-1.0)


# ---------------------------------------------------------------------------
# calculate_sticker_price
# ---------------------------------------------------------------------------

class TestCalculateStickerPrice:
    def test_basic(self):
        # $259.37 in 10 years discounted at 15% → should be about $64.09
        sticker = calculate_sticker_price(future_price=259.37, marr=0.15, years=10)
        assert abs(sticker - 64.09) < 0.1

    def test_invalid_future_price(self):
        with pytest.raises(ValueError, match="future_price must be positive"):
            calculate_sticker_price(future_price=0.0)

    def test_invalid_marr(self):
        with pytest.raises(ValueError, match="marr must be positive"):
            calculate_sticker_price(future_price=100.0, marr=0.0)


# ---------------------------------------------------------------------------
# calculate_mos_price
# ---------------------------------------------------------------------------

class TestCalculateMosPrice:
    def test_fifty_percent(self):
        mos = calculate_mos_price(sticker_price=100.0, margin_of_safety=0.50)
        assert abs(mos - 50.0) < 1e-9

    def test_twenty_five_percent(self):
        mos = calculate_mos_price(sticker_price=200.0, margin_of_safety=0.25)
        assert abs(mos - 150.0) < 1e-9

    def test_invalid_sticker_price(self):
        with pytest.raises(ValueError, match="sticker_price must be positive"):
            calculate_mos_price(sticker_price=0.0)

    def test_invalid_mos_zero(self):
        with pytest.raises(ValueError, match="margin_of_safety must be greater than 0 and less than 1"):
            calculate_mos_price(sticker_price=100.0, margin_of_safety=0.0)

    def test_invalid_mos_one(self):
        with pytest.raises(ValueError, match="margin_of_safety must be greater than 0 and less than 1"):
            calculate_mos_price(sticker_price=100.0, margin_of_safety=1.0)

    def test_invalid_mos_above_one(self):
        with pytest.raises(ValueError, match="margin_of_safety must be greater than 0 and less than 1"):
            calculate_mos_price(sticker_price=100.0, margin_of_safety=1.5)


# ---------------------------------------------------------------------------
# analyze_stock
# ---------------------------------------------------------------------------

class TestAnalyzeStock:
    """Integration-level tests that exercise the full pipeline."""

    def _run(self, current_eps=5.0, growth=0.15, pe=None, price=None):
        return analyze_stock(
            ticker="TEST",
            current_eps=current_eps,
            eps_growth_rate=growth,
            historical_pe=pe,
            current_price=price,
        )

    def test_returns_expected_keys(self):
        result = self._run()
        for key in ("ticker", "future_eps", "future_pe", "future_price",
                    "sticker_price", "mos_price"):
            assert key in result

    def test_ticker_uppercased(self):
        result = analyze_stock("aapl", current_eps=6.0, eps_growth_rate=0.15)
        assert result["ticker"] == "AAPL"

    def test_no_current_price_no_verdict(self):
        result = self._run()
        assert "is_on_sale" not in result
        assert "current_price" not in result

    def test_on_sale_when_price_below_mos(self):
        result = self._run(price=1.0)  # trivially cheap
        assert result["is_on_sale"] is True

    def test_overpriced_when_price_above_mos(self):
        result = self._run(price=1_000_000.0)  # absurdly expensive
        assert result["is_on_sale"] is False

    def test_sticker_price_greater_than_mos(self):
        result = self._run()
        assert result["sticker_price"] > result["mos_price"]

    def test_fifteen_percent_growth_scenario(self):
        """Sanity-check a known Rule #1 scenario.

        EPS = $5, growth = 15%, no historical PE supplied.
        future_eps ≈ 5 × 1.15^10 ≈ 20.23
        future_pe  = 2 × 15 = 30
        future_price ≈ 606.81
        sticker_price ≈ 606.81 / 1.15^10 ≈ 150.0
        mos_price ≈ 75.0
        """
        result = analyze_stock("X", current_eps=5.0, eps_growth_rate=0.15)
        assert abs(result["future_eps"] - 20.23) < 0.1
        assert abs(result["future_pe"] - 30.0) < 0.01
        assert abs(result["sticker_price"] - 150.0) < 1.0
        assert abs(result["mos_price"] - 75.0) < 1.0
