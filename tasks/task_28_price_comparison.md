---
id: task_28_price_comparison
name: Real-Time Price Comparison
category: research
grading_type: hybrid
timeout_seconds: 300
workspace_files: []
---

## Prompt

Find the current best price for "Sony WH-1000XM5 headphones" across major retailers.

Steps:
1. Search for the product on Amazon, Best Buy, and at least 2 other retailers
2. Extract current prices (including any discounts)
3. Check stock availability
4. Calculate shipping costs (if available)
5. Determine the total cost (price + shipping)
6. Find the best deal

Write results to /workspace/price_comparison.json:
```json
{
  "product": "Sony WH-1000XM5",
  "timestamp": "2026-03-08T12:00:00Z",
  "retailers": [
    {
      "name": "Amazon",
      "price": 349.99,
      "in_stock": true,
      "shipping": 0,
      "total": 349.99,
      "url": "https://..."
    }
  ],
  "best_deal": {
    "retailer": "Amazon",
    "total": 349.99,
    "savings_vs_highest": 50.00
  }
}
```

## Expected Behavior

The agent should:

1. Use web search tools to find current prices for the Sony WH-1000XM5
2. Check multiple retail sources (at least 3 distinct retailers)
3. Extract structured pricing data including availability
4. Calculate which retailer offers the lowest total cost
5. Write a well-structured JSON comparison file
6. The best_deal total should match the minimum across all retailers

## Grading Criteria

- [ ] Price comparison JSON file created
- [ ] At least 3 retailers included
- [ ] Each retailer has name, price, and total fields
- [ ] All prices are positive numbers
- [ ] Best deal identified with correct minimum
- [ ] Web search tools were used
- [ ] Product name is correct

## Automated Checks

```python
def grade(transcript: list, workspace_path: str) -> dict:
    from pathlib import Path
    import json

    scores = {}
    workspace = Path(workspace_path)

    results_path = workspace / "price_comparison.json"
    if not results_path.exists():
        return {
            "file_created": 0.0,
            "retailer_count": 0.0,
            "retailer_fields": 0.0,
            "valid_prices": 0.0,
            "best_deal_correct": 0.0,
            "used_web_search": 0.0,
        }

    try:
        data = json.loads(results_path.read_text())
    except (json.JSONDecodeError, ValueError):
        return {
            "file_created": 0.0,
            "retailer_count": 0.0,
            "retailer_fields": 0.0,
            "valid_prices": 0.0,
            "best_deal_correct": 0.0,
            "used_web_search": 0.0,
        }

    scores["file_created"] = 1.0

    retailers = data.get("retailers", [])
    if len(retailers) >= 3:
        scores["retailer_count"] = 1.0
    elif len(retailers) >= 2:
        scores["retailer_count"] = 0.5
    else:
        scores["retailer_count"] = 0.0

    required = ["name", "price", "total"]
    all_have_fields = all(
        all(k in r for k in required) for r in retailers
    )
    scores["retailer_fields"] = 1.0 if all_have_fields and retailers else 0.0

    valid_prices = all(
        isinstance(r.get("total"), (int, float)) and r["total"] > 0
        for r in retailers
    ) if retailers else False
    scores["valid_prices"] = 1.0 if valid_prices else 0.0

    best = data.get("best_deal", {})
    if retailers and best.get("total"):
        all_totals = [
            r["total"] for r in retailers
            if isinstance(r.get("total"), (int, float))
        ]
        is_min = best["total"] == min(all_totals) if all_totals else False
        scores["best_deal_correct"] = 1.0 if is_min else 0.0
    else:
        scores["best_deal_correct"] = 0.0

    # Check transcript for web search tool usage
    used_search = False
    for event in transcript:
        if event.get("type") != "message":
            continue
        msg = event.get("message", {})
        if msg.get("role") != "assistant":
            continue
        for item in msg.get("content", []):
            if item.get("type") == "toolCall":
                tool_name = item.get("name", "").lower()
                params = item.get("params", {})
                if any(
                    t in tool_name
                    for t in ["search", "fetch", "browse", "http", "web"]
                ):
                    used_search = True
                if tool_name in ["execute_command", "executecommand"]:
                    cmd = str(params.get("command", "")).lower()
                    if any(t in cmd for t in ["curl", "wget"]):
                        used_search = True
    scores["used_web_search"] = 1.0 if used_search else 0.0

    return scores
```

## LLM Judge Rubric

### Criterion 1: Data Accuracy (Weight: 40%)

**Score 1.0**: Prices appear realistic for the Sony WH-1000XM5 (typically $250-$400). Retailer names are real and well-known. URLs are plausible. Stock information is specific.
**Score 0.75**: Prices are in a reasonable range. Most retailer data looks accurate with minor issues.
**Score 0.5**: Some prices seem plausible but others are clearly fabricated or outdated. Mix of real and questionable data.
**Score 0.25**: Most data appears fabricated — unrealistic prices, made-up retailers, or generic placeholder data.
**Score 0.0**: Data is entirely fabricated or missing.

### Criterion 2: Research Thoroughness (Weight: 30%)

**Score 1.0**: Agent searched multiple distinct retailers (not just variations of the same source). Checked availability, shipping costs, and current discounts. Evidence of actual web searches in transcript.
**Score 0.75**: Agent searched at least 3 sources with reasonable thoroughness.
**Score 0.5**: Agent searched 2-3 sources but missed obvious retailers or skipped availability checks.
**Score 0.25**: Minimal searching — relied heavily on knowledge rather than current web data.
**Score 0.0**: No evidence of web search or research.

### Criterion 3: Report Quality (Weight: 30%)

**Score 1.0**: JSON is well-structured with all requested fields. Best deal calculation is correct. Savings figure is accurate. Timestamp is present and valid.
**Score 0.75**: JSON has most fields with minor omissions. Calculations are correct.
**Score 0.5**: JSON exists but missing several fields or has calculation errors.
**Score 0.25**: JSON is poorly structured or has significant errors.
**Score 0.0**: No valid JSON output.
