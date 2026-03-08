---
id: task_32_competitive_intel
name: Competitive Intelligence Report
category: research
grading_type: hybrid
timeout_seconds: 300
workspace_files: []
---

## Prompt

Generate a competitive intelligence report for "Anthropic" in the AI/LLM space.

Research:
1. Identify top 3 competitors (OpenAI, Google DeepMind, etc.)
2. For each competitor:
   - Latest product announcements
   - Pricing strategy
   - Key differentiators
   - Recent funding/valuation
   - Market positioning
3. SWOT analysis for Anthropic vs competitors
4. Market trends and opportunities

Write to /workspace/competitive_intelligence_report.md with:
- Executive Summary (2-3 paragraphs)
- Competitor Analysis (detailed profile per competitor)
- SWOT Analysis for Anthropic
- Market Trends section
- Recommendations
- Sources (with URLs)

Also write structured data to /workspace/competitor_data.json.

## Expected Behavior

The agent should:

1. Use web search to research Anthropic's competitive landscape
2. Identify and profile at least 3 major competitors (OpenAI, Google/DeepMind, Meta, etc.)
3. Compile a professional-grade competitive analysis report in Markdown
4. Include a SWOT analysis with strengths, weaknesses, opportunities, and threats
5. Cite sources with URLs where possible
6. Create a companion JSON file with structured competitor data
7. The report should be substantive (>2000 characters) and well-organized

## Grading Criteria

- [ ] Markdown report file created
- [ ] Report has executive summary section
- [ ] Report has SWOT analysis section
- [ ] Report has recommendations section
- [ ] Report mentions at least 3 competitors
- [ ] Report includes source URLs
- [ ] Structured JSON data file created
- [ ] Report is substantive (>2000 chars)

## Automated Checks

```python
def grade(transcript: list, workspace_path: str) -> dict:
    from pathlib import Path
    import json
    import re

    scores = {}
    workspace = Path(workspace_path)

    report_path = workspace / "competitive_intelligence_report.md"
    if not report_path.exists():
        return {
            "report_created": 0.0,
            "has_executive_summary": 0.0,
            "has_swot": 0.0,
            "has_recommendations": 0.0,
            "competitors_mentioned": 0.0,
            "has_sources": 0.0,
            "json_data_created": 0.0,
            "report_substantive": 0.0,
        }

    report = report_path.read_text()
    report_lower = report.lower()
    scores["report_created"] = 1.0

    scores["has_executive_summary"] = 1.0 if re.search(
        r"executive\s+summary|overview|introduction", report_lower,
    ) else 0.0

    scores["has_swot"] = 1.0 if "swot" in report_lower else 0.0

    scores["has_recommendations"] = 1.0 if re.search(
        r"recommend|strategic.+action|next.+step", report_lower,
    ) else 0.0

    competitors = ["openai", "google", "deepmind", "meta", "microsoft", "mistral", "cohere"]
    found = sum(1 for c in competitors if c in report_lower)
    if found >= 3:
        scores["competitors_mentioned"] = 1.0
    elif found >= 2:
        scores["competitors_mentioned"] = 0.5
    else:
        scores["competitors_mentioned"] = 0.0

    scores["has_sources"] = 1.0 if "http" in report else 0.0

    data_path = workspace / "competitor_data.json"
    if data_path.exists():
        try:
            json.loads(data_path.read_text())
            scores["json_data_created"] = 1.0
        except (json.JSONDecodeError, ValueError):
            scores["json_data_created"] = 0.0
    else:
        scores["json_data_created"] = 0.0

    scores["report_substantive"] = 1.0 if len(report) > 2000 else (
        0.5 if len(report) > 1000 else 0.0
    )

    return scores
```

## LLM Judge Rubric

### Criterion 1: Research Depth (Weight: 35%)

**Score 1.0**: Report contains specific, current information about each competitor — concrete product names, recent announcements, funding rounds, and pricing details. Evidence of web research with cited sources. Information goes beyond surface-level knowledge.
**Score 0.75**: Good detail on most competitors. Some information is specific and current, but a few profiles rely on general knowledge.
**Score 0.5**: Report covers competitors at a surface level. Information is mostly accurate but lacks recent developments or specificity.
**Score 0.25**: Report has minimal detail or relies entirely on outdated knowledge.
**Score 0.0**: No meaningful competitor analysis.

### Criterion 2: SWOT Analysis Quality (Weight: 25%)

**Score 1.0**: SWOT analysis is insightful and specific to Anthropic. Strengths cite concrete differentiators (safety research, Constitutional AI, Claude capabilities). Weaknesses are honest and specific. Opportunities and threats reflect current market dynamics.
**Score 0.75**: SWOT is reasonable with good specificity in most quadrants.
**Score 0.5**: SWOT exists but is generic — could apply to any AI company.
**Score 0.25**: SWOT is superficial or clearly padded.
**Score 0.0**: No SWOT analysis.

### Criterion 3: Analytical Quality (Weight: 25%)

**Score 1.0**: Report reads like a professional market analysis. Makes meaningful comparisons between companies, identifies strategic positioning differences, and draws actionable conclusions. Executive summary distills key takeaways effectively.
**Score 0.75**: Good analysis with reasonable comparisons. Could be more nuanced.
**Score 0.5**: Information presented but reads more like a list of facts than strategic analysis.
**Score 0.25**: Mostly raw information with minimal synthesis.
**Score 0.0**: No analytical content.

### Criterion 3: Report Structure (Weight: 15%)

**Score 1.0**: Excellently organized with clear hierarchy, consistent formatting, and professional Markdown. Easy to navigate and extract key information.
**Score 0.75**: Well-organized with minor formatting inconsistencies.
**Score 0.5**: Basic structure but inconsistent formatting or missing key sections.
**Score 0.25**: Poorly organized or difficult to navigate.
**Score 0.0**: No discernible structure.
