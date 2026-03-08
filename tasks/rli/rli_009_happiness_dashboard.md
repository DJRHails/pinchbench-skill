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

**Score 1.0**: A choropleth world map is present with countries colored by happiness score. Hover or click interaction shows the country name and score value. Minor gaps in country coverage or styling are acceptable.
**Score 0.0**: No map visualization present, or the map is a non-functional placeholder with no data-driven coloring.

### Criterion 2: Detail Chart & Linkage (Weight: 30%)

**Score 1.0**: A second chart (bar, spider, or similar) exists showing component breakdown. Interacting with a country on the map updates or highlights the corresponding data in the chart. Minor visual issues are acceptable.
**Score 0.0**: No secondary chart present, or the chart is completely unlinked from the map with no interactive behavior.

### Criterion 3: Data Accuracy (Weight: 20%)

**Score 1.0**: The dashboard uses data from the provided XLS file. Country scores and component values are generally consistent with the source data. Minor discrepancies or a few missing countries are acceptable.
**Score 0.0**: No data integration from the XLS file, data is entirely hardcoded with wrong values, or the dashboard shows no meaningful data.

### Criterion 4: Design & Usability (Weight: 20%)

**Score 1.0**: The dashboard has a coherent visual design with readable labels, a color legend, and a usable layout. It does not require a server to run. Minor polish issues are acceptable.
**Score 0.0**: The dashboard is unusable, has no design effort, or fails to load in a browser.
