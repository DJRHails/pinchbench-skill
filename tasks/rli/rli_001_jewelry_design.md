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

**Score 1.0**: The marquise-cut diamond is correctly modeled with the distinctive elongated shape and pointed ends. Proportions are realistic and the diamond is well-integrated into the ring setting.
**Score 0.75**: Diamond shape is recognizably marquise but proportions may be slightly off or integration with the setting has minor issues.
**Score 0.5**: Diamond shape attempts marquise but is not clearly distinguishable from other cuts, or has notable proportion issues.
**Score 0.25**: Diamond is present but does not resemble a marquise cut.
**Score 0.0**: No diamond modeled or still shows the original emerald cut.

### Criterion 2: Design Fidelity (Weight: 25%)

**Score 1.0**: All other design elements from the reference image are faithfully maintained — band style, setting type, proportions, and decorative details match the original.
**Score 0.75**: Most design elements are preserved with minor deviations from the reference.
**Score 0.5**: Some design elements maintained but noticeable differences from the original ring design.
**Score 0.25**: Ring is generic and does not closely follow the reference design.
**Score 0.0**: No attempt to follow the reference design.

### Criterion 3: Render Quality (Weight: 25%)

**Score 1.0**: All four required renders are present with photorealistic quality. Rose gold and yellow gold materials are distinct and accurate. Lighting, reflections, and shadows are professional-grade.
**Score 0.75**: All renders present with good quality. Materials are distinguishable but may lack photorealism.
**Score 0.5**: Some renders present but quality is mediocre, or material differentiation is weak.
**Score 0.25**: Minimal renders with poor quality or missing gold variants.
**Score 0.0**: No usable renders produced.

### Criterion 4: Deliverable Completeness (Weight: 20%)

**Score 1.0**: All deliverables present — .3dm model file, four JPEG renders at minimum 1280x1280, correctly named and organized.
**Score 0.75**: Most deliverables present with minor issues (e.g., one render slightly under resolution).
**Score 0.5**: Some deliverables missing (e.g., missing model file or only two of four renders).
**Score 0.25**: Only a few deliverables present.
**Score 0.0**: No deliverables produced.
