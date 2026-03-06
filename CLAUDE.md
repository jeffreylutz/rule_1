# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is an investing analysis codebase based on **Phil Town's "Rule #1" investing** methodology. Rule #1 investing focuses on buying wonderful companies at attractive prices using value investing principles.

## Rule #1 Investing Principles

### The Four Ms

All investment decisions must evaluate these four criteria:

1. **Meaning** - Do you understand the business? Only invest in businesses you can explain simply.
2. **Moat** - Does the company have a durable competitive advantage? Look for brands, secrets, tolls, switching costs, or price advantages.
3. **Management** - Is management trustworthy and competent? Evaluate CEO track record, insider ownership, and alignment with shareholders.
4. **Margin of Safety** - Are you buying at a significant discount to intrinsic value? Only buy at 50% of sticker price or less.

### The Big Five Numbers

Evaluate company quality using these five metrics over 10 years:

1. **Return on Equity (ROE)** - Target: ≥10% annually
2. **Equity/Book Value Growth Rate** - Target: ≥10% annually
3. **Earnings Per Share (EPS) Growth Rate** - Target: ≥10% annually
4. **Sales/Revenue Growth Rate** - Target: ≥10% annually
5. **Free Cash Flow (FCF) Growth Rate** - Target: ≥10% annually

All five numbers should show consistent growth above 10% annually over the past 10 years.

### Valuation Methodology

**Sticker Price Calculation:**
- Current EPS × (2 × Expected Growth Rate) × Default P/E of 8.5
- Or use analyst's future EPS estimate × analyst's P/E estimate
- Discount back to present value using minimum acceptable rate of return (typically 15%)

**Margin of Safety (MOS) Price:**
- MOS Price = Sticker Price × 0.50
- Only buy when current price is at or below MOS price

**Ten Cap Price:**
- Another valuation method using Free Cash Flow
- Ten Cap Price = FCF × 10

### Investment Decision Framework

1. **Watchlist** - Companies with meaning and moat worth monitoring
2. **Buy** - Companies meeting all 4 Ms with price ≤ MOS price
3. **Sell** - Exit when price reaches sticker price or fundamentals deteriorate
4. **Hold** - Positions between MOS and sticker price with intact fundamentals

## Key Investment Rules

- Never invest in a business you don't understand
- Always require a 50% margin of safety
- Focus on predictable, consistent businesses (avoid highly cyclical industries)
- Look for owner-operators with "skin in the game"
- Be patient - wait for the right price
- Practice emotional discipline - avoid FOMO and panic selling

## Data Sources & Analysis

When building tools for Rule #1 analysis:
- Historical financial data should cover minimum 10 years
- Focus on TTM (Trailing Twelve Months) for current metrics
- Use CAGR (Compound Annual Growth Rate) for growth calculations
- Track insider ownership and recent insider transactions
- Monitor institutional ownership trends
- Compare valuation against historical P/E ranges

## Anti-Patterns to Avoid

- Don't buy "story stocks" without proven track records
- Avoid companies with inconsistent Big Five numbers
- Don't rationalize buying above sticker price
- Ignore short-term market noise and focus on fundamentals
- Don't invest in industries undergoing rapid technological disruption unless moat is clear

## Related Projects & Resources

### GitHub Repositories

**Fundamental Analysis & Value Investing:**
- **[daniloaleixo/bovespaStockRatings](https://github.com/daniloaleixo/bovespaStockRatings)** (209★) - Fundamental analysis platform for stocks with scoring based on financial indicators
- **[je-suis-tm/quant-trading](https://github.com/je-suis-tm/quant-trading)** (9.3k★) - Python quantitative trading strategies and patterns

**Technical Analysis Libraries:**
- **[bukosabino/ta](https://github.com/bukosabino/ta)** - Technical Analysis Library using Pandas and Numpy
- Useful for supplementing fundamental analysis with technical indicators

**Curated Lists:**
- **[awesome-systematic-trading](https://github.com/paperswithbacktest/awesome-systematic-trading)** - Comprehensive list of trading libraries, strategies, books, and tutorials
- **[Best-Investing-Books](https://github.com/manjunath5496/Best-Investing-Books)** - Collection of investment literature including value investing classics

### Recommended Data APIs for Rule #1 Analysis

**Free/Freemium APIs:**
- **yfinance** - Yahoo Finance data (historical prices, fundamentals, financials)
- **Alpha Vantage** - Free tier includes fundamental data and stock time series
- **Financial Modeling Prep** - Free tier for financial statements and key metrics
- **EDGAR (SEC)** - Direct access to company filings (10-K, 10-Q, 8-K)

**Key Metrics to Extract:**
- Income statements (10 years) - for EPS, Revenue growth
- Balance sheets (10 years) - for Book Value, ROE calculation
- Cash flow statements (10 years) - for Free Cash Flow
- Insider trading data - for management alignment analysis
- Historical P/E ratios - for valuation context

### Phil Town Resources

**Books:**
- "Rule #1: The Simple Strategy for Successful Investing in Only 15 Minutes a Week" (2006)
- "Payback Time: Making Big Money Is the Best Revenge!" (2010)

**Official Resources:**
- Rule #1 Investing website: https://www.ruleoneinvesting.com/
- Rule #1 Podcast & educational content
- Rule #1 calculator tools and templates

**Video Content & Education:**
- **[New Money (Brandon)](https://www.youtube.com/@NewMoneyYouTube)** - YouTube channel focused on value investing, financial analysis, and investment education. Provides practical insights on evaluating companies and understanding market fundamentals.

### Implementation Notes

When building Rule #1 tools, consider these open-source approaches:
- Use `yfinance` or `financialmodelingprep` for fetching historical financial data
- Implement CAGR calculations for the Big Five Numbers
- Build screeners that filter for 10-year consistency in all metrics
- Create watchlist management with MOS price alerts
- Implement insider trading tracking using SEC EDGAR data
- Build simple CLI or web interface for quick company evaluation
