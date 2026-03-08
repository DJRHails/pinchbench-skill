---
id: rli_009_happiness_dashboard
name: "RLI: World Happiness Dashboard"
category: web_development
grading_type: hybrid
timeout_seconds: 600
workspace_files:
  - source: rli/public_009/DataForFigure2.1WHR2021C2.xls
    dest: inputs/DataForFigure2.1WHR2021C2.xls
grading_weights:
  automated: 0.4
  llm_judge: 0.6
---

## Prompt

Build an intuitive, self-hosted interactive dashboard that lets visitors explore why some countries score higher than others in the World Happiness Report.

### Requirements

- Overview: The dashboard should include an overview map showing each country's overall happiness score.
- Data: use the provided data as the sole source for country scores and component metrics.
- Map: display each country shaded on a gradient that reflects its overall happiness score; add hover and click interactions that surface the country name and exact value.
- Detailed chart: place a second visual (e.g., stacked bar or spider chart) beside or beneath the map. This chart should be linked to the map, so when the reader interacts with one country on the map, the same country in the second chart is highlighted.
- Design: intuitive, user-friendly, and align with the theme of happiness.

The happiness data is available at `inputs/DataForFigure2.1WHR2021C2.xls`.

### Deliverables

A complete, self-contained dashboard package (HTML, CSS, JavaScript, and any required libraries).

## Expected Behavior

The agent should:

1. Read the provided XLS file to understand the data structure
2. Create a self-contained HTML/CSS/JS dashboard
3. Include a choropleth world map colored by happiness score
4. Include a linked detail chart (bar, spider, or similar) showing score components
5. Implement hover/click interactions between map and chart
6. Ensure the dashboard is self-contained (no server required)

This is a replica of RLI public_009 (World Happiness Dashboard, $120 budget).

## Grading Criteria

- [ ] Dashboard HTML file exists and is loadable
- [ ] World map visualization showing countries colored by happiness score
- [ ] Hover interaction shows country name and happiness score
- [ ] Click interaction selects a country for detail view
- [ ] Second chart shows component breakdown for selected country
- [ ] Map and chart are linked (interaction on one updates the other)
- [ ] Data sourced from the provided XLS file
- [ ] Self-contained package (no external server required)
- [ ] Responsive, user-friendly design

## Automated Checks

```python
def grade(transcript: list, workspace_path: str) -> dict:
    """Grade the World Happiness Dashboard task."""
    from pathlib import Path
    import re

    scores = {}
    workspace = Path(workspace_path)

    # Check for HTML file
    html_files = list(workspace.rglob("*.html"))
    # Exclude input files
    html_files = [
        f for f in html_files
        if "inputs" not in f.relative_to(workspace).parts
    ]
    scores["html_exists"] = 1.0 if html_files else 0.0

    # Collect all HTML + JS content
    all_content = ""
    for f in html_files:
        all_content += f.read_text(errors="replace")
    for f in workspace.rglob("*.js"):
        if "inputs" not in f.relative_to(workspace).parts:
            all_content += f.read_text(errors="replace")

    # Check for map visualization
    has_map = bool(
        re.search(
            r"""(?ix)
            choropleth | world.?map | geo.?json | topojson
            | d3\.geo | leaflet | mapbox
            | country.?map | svg.?map
            """,
            all_content,
        )
    )
    scores["map_visualization"] = 1.0 if has_map else 0.0

    # Check for chart visualization
    has_chart = bool(
        re.search(
            r"""(?ix)
            bar.?chart | spider.?chart | radar.?chart
            | chart\.js | d3\.scale | plotly
            | stacked.?bar | component.?chart
            """,
            all_content,
        )
    )
    scores["detail_chart"] = 1.0 if has_chart else 0.0

    # Check for interactivity
    has_interaction = bool(
        re.search(
            r"""(?ix)
            click | hover | mouseover | mouseenter
            | addEventListener | on\s*\(
            | tooltip | popup
            """,
            all_content,
        )
    )
    scores["interactivity"] = 1.0 if has_interaction else 0.0

    # Check for happiness data references
    has_data = bool(
        re.search(
            r"""(?ix)
            happiness | ladder.?score | life.?ladder
            | gdp | social.?support | life.?expectancy
            | generosity | corruption | freedom
            """,
            all_content,
        )
    )
    scores["data_integration"] = 1.0 if has_data else 0.0

    # Check for linked behavior between map and chart
    has_linked = bool(
        re.search(
            r"""(?ix)
            select.?country | highlight | update.?chart
            | on.?click.+chart | linked | sync
            """,
            all_content,
        )
    )
    scores["linked_visuals"] = 1.0 if has_linked else 0.0

    return scores
```

## LLM Judge Rubric

### Criterion 1: Map Visualization (Weight: 30%)

**Score 1.0**: Beautiful choropleth world map with gradient coloring by happiness score. All countries are visible and correctly colored. Hover shows country name and exact score value. Smooth transitions and professional styling.
**Score 0.75**: Functional map with most countries colored correctly. Hover works but may have minor issues with some countries.
**Score 0.5**: Basic map present but incomplete coverage, missing hover, or incorrect color mapping.
**Score 0.25**: Minimal map attempt — perhaps a placeholder or very few countries shown.
**Score 0.0**: No map visualization present.

### Criterion 2: Detail Chart & Linkage (Weight: 30%)

**Score 1.0**: Second chart (bar, spider, or similar) shows component breakdown for selected country. Clicking a country on the map updates the chart. Visual linkage is clear and intuitive.
**Score 0.75**: Chart exists and updates on country selection, but may have minor visual or data issues.
**Score 0.5**: Chart exists but is not properly linked to the map, or shows incorrect data.
**Score 0.25**: Static chart with no interactivity or linkage.
**Score 0.0**: No secondary chart present.

### Criterion 3: Data Accuracy (Weight: 20%)

**Score 1.0**: Dashboard correctly reads and displays all data from the provided XLS file. Country scores and component values match the source data.
**Score 0.75**: Most data is correct with minor discrepancies or missing countries.
**Score 0.5**: Some data is present but significant accuracy issues or many missing countries.
**Score 0.25**: Data appears hardcoded or does not match the source file.
**Score 0.0**: No data integration or completely wrong values.

### Criterion 4: Design & Usability (Weight: 20%)

**Score 1.0**: Professional, polished design aligned with the happiness theme. Intuitive layout, clear legends, readable labels, good color choices. Works well on different screen sizes.
**Score 0.75**: Good design with minor polish issues. Usable and readable.
**Score 0.5**: Functional but basic design. May be cluttered or hard to navigate.
**Score 0.25**: Poor visual design that hinders usability.
**Score 0.0**: Unusable or no design effort.
