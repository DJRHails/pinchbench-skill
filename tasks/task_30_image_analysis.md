---
id: task_30_image_analysis
name: Batch Image Analysis
category: media
grading_type: hybrid
timeout_seconds: 300
workspace_files: []
---

## Prompt

Perform batch image analysis on tech company logos.

Steps:
1. Search for and download logos of: Apple, Google, Microsoft, Amazon, Meta
2. Save each logo to /workspace/logos/
3. For each logo, analyze:
   - Dominant colors (hex codes)
   - Image dimensions
   - File size
   - Design style (minimalist, detailed, etc.)
   - Brand sentiment (modern, corporate, friendly, etc.)
4. Generate comparison report

Write metadata to /workspace/logo_analysis.json:
```json
{
  "total_images": 5,
  "images": [
    {
      "company": "Apple",
      "filename": "apple_logo.png",
      "dimensions": "1024x1024",
      "file_size_kb": 45,
      "dominant_colors": ["#000000", "#ffffff"],
      "style": "minimalist",
      "sentiment": "modern"
    }
  ],
  "insights": {
    "most_common_style": "minimalist",
    "average_file_size_kb": 50,
    "color_palette_summary": "Tech logos favor monochrome and blue tones"
  }
}
```

## Expected Behavior

The agent should:

1. Use web search and/or browser tools to find official logos for the five companies
2. Download logo images to a `/workspace/logos/` directory
3. Analyze each image for visual properties (colors, dimensions, file size)
4. Classify design style and brand sentiment
5. Generate a structured analysis JSON with per-image metadata
6. Include cross-company insights

If the agent cannot download actual images, it should still produce the analysis based on known logo characteristics.

## Grading Criteria

- [ ] Analysis JSON file created
- [ ] At least 3 companies analyzed
- [ ] Each image entry has company name and dominant_colors
- [ ] Each image entry has style classification
- [ ] Insights section generated
- [ ] Logo files downloaded (bonus)

## Automated Checks

```python
def grade(transcript: list, workspace_path: str) -> dict:
    from pathlib import Path
    import json

    scores = {}
    workspace = Path(workspace_path)

    path = workspace / "logo_analysis.json"
    if not path.exists():
        return {
            "file_created": 0.0,
            "company_count": 0.0,
            "has_colors": 0.0,
            "has_styles": 0.0,
            "has_insights": 0.0,
            "logos_downloaded": 0.0,
        }

    try:
        analysis = json.loads(path.read_text())
    except (json.JSONDecodeError, ValueError):
        return {
            "file_created": 0.0,
            "company_count": 0.0,
            "has_colors": 0.0,
            "has_styles": 0.0,
            "has_insights": 0.0,
            "logos_downloaded": 0.0,
        }

    scores["file_created"] = 1.0

    images = analysis.get("images", [])
    if len(images) >= 5:
        scores["company_count"] = 1.0
    elif len(images) >= 3:
        scores["company_count"] = 0.5
    else:
        scores["company_count"] = 0.0

    has_colors = all(
        "dominant_colors" in img and len(img["dominant_colors"]) > 0
        for img in images
    ) if images else False
    scores["has_colors"] = 1.0 if has_colors else 0.0

    has_styles = all(
        "style" in img for img in images
    ) if images else False
    scores["has_styles"] = 1.0 if has_styles else 0.0

    scores["has_insights"] = 1.0 if "insights" in analysis else 0.0

    logos_dir = workspace / "logos"
    if logos_dir.exists():
        logo_files = list(logos_dir.glob("*"))
        if len(logo_files) >= 5:
            scores["logos_downloaded"] = 1.0
        elif len(logo_files) >= 3:
            scores["logos_downloaded"] = 0.5
        else:
            scores["logos_downloaded"] = 0.25
    else:
        scores["logos_downloaded"] = 0.0

    return scores
```

## LLM Judge Rubric

### Criterion 1: Analysis Accuracy (Weight: 40%)

**Score 1.0**: Color analysis is plausible for each company's actual logo (e.g., Apple uses monochrome, Google uses red/blue/yellow/green, Microsoft uses four-color grid). Style classifications are appropriate. Dimensions and file sizes are realistic.
**Score 0.75**: Most analyses are plausible with minor inaccuracies in colors or style.
**Score 0.5**: Some analyses are correct but others have clear errors about well-known logos.
**Score 0.25**: Analysis appears largely fabricated without reference to actual logos.
**Score 0.0**: No meaningful analysis.

### Criterion 2: Image Acquisition (Weight: 30%)

**Score 1.0**: Agent successfully downloaded 5 actual logo image files. Files are real images (not empty or corrupt). Evidence of web browsing/downloading in transcript.
**Score 0.75**: Downloaded 3-4 logos successfully.
**Score 0.5**: Downloaded 1-2 logos or used alternative approach (described logos from knowledge).
**Score 0.25**: Attempted to download but failed for most. Analysis based on knowledge only.
**Score 0.0**: No download attempts and no knowledge-based analysis.

### Criterion 3: Insights Quality (Weight: 30%)

**Score 1.0**: Cross-company insights are thoughtful and accurate — identifies real design trends across tech logos (e.g., trend toward simplification, common color palettes, flat design). Average calculations are correct.
**Score 0.75**: Insights are reasonable with minor inaccuracies or missed observations.
**Score 0.5**: Insights exist but are superficial or generic.
**Score 0.25**: Minimal insights with no real analytical value.
**Score 0.0**: No insights section.
