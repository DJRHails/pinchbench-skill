---
id: rli_001_jewelry_design
name: "RLI: Jewelry Design"
category: 3d_modeling
grading_type: hybrid
timeout_seconds: 600
workspace_files:
  - source: rli/public_001/ringdetails.png
    dest: inputs/ringdetails.png
grading_weights:
  automated: 0.4
  llm_judge: 0.6
---

## Prompt

Create a modified version of the provided ring design by replacing the emerald-cut diamond with a marquise-cut diamond. Using the reference photo, render images of the ring with this new diamond shape while maintaining all other design elements.

Provided material: Reference image showing the original ring with emerald-cut diamond, including weight, size, and other specifications (`inputs/ringdetails.png`)

### Deliverables

1. 3D model file with marquise-cut diamond (.3dm format)
2. JPEG Images (minimum 1280x1280 pixels resolution):
   - Rose gold version, front view (.jpg format)
   - Rose gold version, side angle view (.jpg format)
   - Yellow gold version, front view (.jpg format)
   - Yellow gold version, side angle view (.jpg format)

## Expected Behavior

The agent should:

1. Examine the reference image to understand the original ring design and specifications
2. Create a 3D model of the ring replacing the emerald-cut diamond with a marquise-cut diamond
3. Maintain all other design elements from the original ring
4. Render the ring in both rose gold and yellow gold finishes
5. Produce front and side angle views for each gold version
6. Export the 3D model in .3dm format and renders as high-resolution JPEGs

This is a replica of RLI public_001 (Jewelry Design, $50 budget).

## Grading Criteria

- [ ] 3D model file exists in .3dm format
- [ ] Diamond shape is marquise-cut (not emerald-cut)
- [ ] All other design elements maintained from original
- [ ] Rose gold front view render exists (JPEG, >= 1280x1280)
- [ ] Rose gold side angle view render exists (JPEG, >= 1280x1280)
- [ ] Yellow gold front view render exists (JPEG, >= 1280x1280)
- [ ] Yellow gold side angle view render exists (JPEG, >= 1280x1280)
- [ ] Renders show realistic ring appearance

## Automated Checks

```python
def grade(transcript: list, workspace_path: str) -> dict:
    """Grade the Jewelry Design task."""
    from pathlib import Path
    import re

    scores = {}
    workspace = Path(workspace_path)

    # Check for 3D model file (.3dm)
    model_files = list(workspace.rglob("*.3dm"))
    model_files = [
        f for f in model_files
        if "inputs" not in f.relative_to(workspace).parts
    ]
    scores["model_exists"] = 1.0 if model_files else 0.0

    # Check for JPEG renders
    jpg_files = list(workspace.rglob("*.jpg")) + list(
        workspace.rglob("*.jpeg")
    )
    jpg_files = [
        f for f in jpg_files
        if "inputs" not in f.relative_to(workspace).parts
    ]
    scores["renders_exist"] = min(1.0, len(jpg_files) / 4.0)

    # Check render resolution (>= 1280x1280)
    renders_valid = 0
    for f in jpg_files:
        try:
            from PIL import Image

            img = Image.open(f)
            w, h = img.size
            if w >= 1280 and h >= 1280:
                renders_valid += 1
        except Exception:
            pass
    scores["render_resolution"] = (
        min(1.0, renders_valid / 4.0) if jpg_files else 0.0
    )

    # Check filenames for gold variants and views
    all_names = " ".join(f.stem.lower() for f in jpg_files)
    has_rose_gold = bool(
        re.search(
            r"""(?ix) rose.?gold | rosegold""",
            all_names,
        )
    )
    has_yellow_gold = bool(
        re.search(
            r"""(?ix) yellow.?gold | yellowgold""",
            all_names,
        )
    )
    has_front = bool(
        re.search(
            r"""(?ix) front""",
            all_names,
        )
    )
    has_side = bool(
        re.search(
            r"""(?ix) side | angle""",
            all_names,
        )
    )
    variant_score = sum([
        has_rose_gold, has_yellow_gold, has_front, has_side
    ]) / 4.0
    scores["render_variants"] = variant_score

    return scores
```

## LLM Judge Rubric

### Criterion 1: Diamond Shape Accuracy (Weight: 30%)

**Score 1.0**: A marquise-cut diamond is modeled with a recognizably elongated shape and pointed ends, integrated into the ring setting.
**Score 0.0**: No diamond modeled, still shows the original emerald cut, or diamond does not resemble a marquise cut.

### Criterion 2: Design Fidelity (Weight: 25%)

**Score 1.0**: The ring design meaningfully follows the reference image, preserving the band style, setting type, and overall proportions.
**Score 0.0**: No attempt to follow the reference design, or the ring is entirely generic with no recognizable connection to the original.

### Criterion 3: Render Quality (Weight: 25%)

**Score 1.0**: At least two renders are present showing distinguishable rose gold and yellow gold materials with reasonable lighting and reflections.
**Score 0.0**: No usable renders produced, or renders lack any material differentiation between gold types.

### Criterion 4: Deliverable Completeness (Weight: 20%)

**Score 1.0**: A .3dm model file and at least three of the four required JPEG renders (rose gold front, rose gold side, yellow gold front, yellow gold side) are present at minimum 1280x1280 resolution.
**Score 0.0**: No deliverables produced, or only a single file type (model only or renders only) is present.
