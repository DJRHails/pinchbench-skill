---
id: task_29_portfolio_optimization
name: Financial Portfolio Optimization
category: finance
grading_type: hybrid
timeout_seconds: 300
workspace_files: []
---

## Prompt

Create an optimized investment portfolio of $10,000 across tech stocks.

Steps:
1. Get current prices for: AAPL, GOOGL, MSFT, NVDA, TSLA
2. Calculate each stock's risk profile from recent trends
3. Fetch recent news/sentiment for each stock
4. Calculate optimal allocation using a risk-adjusted approach
5. Generate buy recommendations (shares to purchase for each stock)

Write to /workspace/portfolio_allocation.json:
```json
{
  "total_budget": 10000,
  "date": "2026-03-08",
  "stocks": [
    {
      "ticker": "AAPL",
      "current_price": 185.50,
      "allocation_pct": 25,
      "allocation_usd": 2500,
      "shares_to_buy": 13,
      "rationale": "Strong fundamentals, moderate volatility"
    }
  ],
  "expected_annual_return": "12%",
  "risk_level": "moderate",
  "leftover_cash": 15.50
}
```

## Expected Behavior

The agent should:

1. Look up current or recent stock prices for all five tickers
2. Analyze risk/reward characteristics for each stock
3. Propose percentage allocations that sum to approximately 100%
4. Calculate dollar amounts and whole shares to buy within the $10,000 budget
5. Account for leftover cash (budget minus total shares cost)
6. Provide rationale for each allocation decision

## Grading Criteria

- [ ] Portfolio JSON file created
- [ ] All 5 tickers present
- [ ] Budget is $10,000
- [ ] Allocation percentages sum to approximately 100%
- [ ] Total allocated USD does not exceed budget
- [ ] Each stock has current_price, allocation_pct, shares_to_buy
- [ ] Prices are positive and realistic

## Automated Checks

```python
def grade(transcript: list, workspace_path: str) -> dict:
    from pathlib import Path
    import json

    scores = {}
    workspace = Path(workspace_path)

    path = workspace / "portfolio_allocation.json"
    if not path.exists():
        return {
            "file_created": 0.0,
            "all_tickers": 0.0,
            "correct_budget": 0.0,
            "pct_sum_valid": 0.0,
            "within_budget": 0.0,
            "stock_fields": 0.0,
            "prices_realistic": 0.0,
        }

    try:
        portfolio = json.loads(path.read_text())
    except (json.JSONDecodeError, ValueError):
        return {
            "file_created": 0.0,
            "all_tickers": 0.0,
            "correct_budget": 0.0,
            "pct_sum_valid": 0.0,
            "within_budget": 0.0,
            "stock_fields": 0.0,
            "prices_realistic": 0.0,
        }

    scores["file_created"] = 1.0

    stocks = portfolio.get("stocks", [])
    tickers = {s.get("ticker", "").upper() for s in stocks}
    expected = {"AAPL", "GOOGL", "MSFT", "NVDA", "TSLA"}
    scores["all_tickers"] = 1.0 if expected <= tickers else (
        0.5 if len(expected & tickers) >= 3 else 0.0
    )

    budget = portfolio.get("total_budget", 0)
    scores["correct_budget"] = 1.0 if budget == 10000 else 0.0

    pcts = [s.get("allocation_pct", 0) for s in stocks]
    total_pct = sum(p for p in pcts if isinstance(p, (int, float)))
    scores["pct_sum_valid"] = 1.0 if 95 <= total_pct <= 105 else (
        0.5 if 80 <= total_pct <= 120 else 0.0
    )

    usds = [
        s.get("allocation_usd", 0) for s in stocks
        if isinstance(s.get("allocation_usd"), (int, float))
    ]
    total_usd = sum(usds)
    scores["within_budget"] = 1.0 if 0 < total_usd <= 10000 else 0.0

    required = ["current_price", "allocation_pct", "shares_to_buy"]
    all_fields = all(
        all(k in s for k in required) for s in stocks
    ) if stocks else False
    scores["stock_fields"] = 1.0 if all_fields else 0.0

    prices = [
        s.get("current_price", 0) for s in stocks
        if isinstance(s.get("current_price"), (int, float))
    ]
    scores["prices_realistic"] = 1.0 if (
        prices and all(p > 0 for p in prices)
    ) else 0.0

    return scores
```

## LLM Judge Rubric

### Criterion 1: Investment Rationale (Weight: 40%)

**Score 1.0**: Each stock has a specific, well-reasoned rationale citing recent performance, market position, or sector trends. Allocations reflect the stated risk/reward analysis. The portfolio as a whole has a coherent strategy.
**Score 0.75**: Most stocks have reasonable rationales. Allocation logic is mostly sound.
**Score 0.5**: Rationales are present but generic ("good company", "tech leader"). Allocations seem arbitrary.
**Score 0.25**: Minimal or boilerplate rationales with no clear investment thesis.
**Score 0.0**: No rationales or completely nonsensical investment logic.

### Criterion 2: Data Quality (Weight: 30%)

**Score 1.0**: Stock prices are current and realistic (within 10% of actual market prices). Shares-to-buy calculations are mathematically correct. Leftover cash is accurately computed.
**Score 0.75**: Prices are in the right ballpark. Minor calculation errors.
**Score 0.5**: Some prices seem outdated or estimates. Notable calculation errors.
**Score 0.25**: Prices are clearly fabricated or wildly inaccurate.
**Score 0.0**: No meaningful price data.

### Criterion 3: Portfolio Construction (Weight: 30%)

**Score 1.0**: Portfolio is well-diversified across the five stocks. No single stock dominates excessively (unless justified). Risk level assessment is consistent with the allocation. Expected return estimate is reasonable for the portfolio composition.
**Score 0.75**: Reasonable diversification with minor concentration issues.
**Score 0.5**: Portfolio is overly concentrated or diversification rationale is weak.
**Score 0.25**: Portfolio construction shows no understanding of diversification principles.
**Score 0.0**: Portfolio is invalid or single-stock.
