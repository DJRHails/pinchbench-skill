---
id: rli_005_cad_models
name: "RLI: Building Vent CAD Models"
category: 3d_modeling
grading_type: hybrid
timeout_seconds: 600
workspace_files:
  - source: "rli/public_005/Mushroom Head Ventilation Reference.png"
    dest: "inputs/Mushroom Head Ventilation Reference.png"
  - source: "rli/public_005/Whirlybird Ventilation Reference.png"
    dest: "inputs/Whirlybird Ventilation Reference.png"
grading_weights:
  automated: 0.4
  llm_judge: 0.6
---

## Prompt

Create 3D CAD models of the building vent products offered in construction projects. Provide also exploded views of the vent products to show how to assemble them.

The provided reference images are for visual style guidance only. The models must be built to the dimensional specifications listed below.

### Vent types

**1. Mushroom Head Ventilation:**
- Commonly used in RVs, motorhomes, and trailers.
- Installed on roofs to allow fresh air in and release excess moisture and indoor air, preventing mold growth and damp conditions.
- Dimensions:
   - Bottom plate diameter: 18", with 7 bolt holes - Bolt 5/16'' x 3 3/8''
   - Middle plate diameter: 17", with 3 bolt holes - Bolt 3/16'' x 1 1/8''
   - Mushroom head cover diameter: 18", height: 9".

**2. Whirlybird Ventilation:**
- Recognizable by its dome shape, it is a wind-powered system used in warmer climates.
- Reduces high temperatures in summer and removes excess humidity in winter.
- The dome has engineered fins that rotate in the wind, creating a vacuum to extract hot air.
- Dimension:
   - Bottom plate diameter: 18", with 7 bolt holes - Bolt 5/16'' x 3 3/8''
   - Middle plate diameter: 17.5", with 3 bolt holes - Bolt 3/16'' x 1 1/8''
   - Dome diameter: 16", height: 9.5".

### Provided material

- A photo of the mushroom head vent type in `inputs/Mushroom Head Ventilation Reference.png`
- A photo of the whirlybird vent type in `inputs/Whirlybird Ventilation Reference.png`

### Design & Assembly Assumptions

The specifications above provide the primary control dimensions. You are expected to apply standard design practices for all undefined geometry, including:
- Component Geometry: Design logical, functional shapes (e.g., raised necks, flanges) to create a stackable assembly from the listed parts. The 'Bottom plate' and 'Middle plate' must be designed with interlocking features (e.g., hexagonal, star-shaped, etc.) to ensure proper alignment. The specific geometry of this interlock is not defined and is left to the designer's discretion.
- Bolt Placement: Use standard Bolt Circle Diameters (BCDs) appropriate for the given plate diameters.
- Mushroom Head Vent Internals: No need to model the internals. Just model the mounting and housing for the vent.
- Whirlybird Internals: Model a simplified, standard internal assembly (axle, bracing, etc.) to ensure the exploded view is mechanically complete.

### Deliverables

- 3D CAD Models in .stp/.step format of the Mushroom Head Vent and Whirlybird Vent
- 3D CAD Models in .stp/.step format of the exploded Mushroom Head Vent and Whirlybird Vent
- Exploded view assembly drawings (PDF format) showing bolt sizes and indicating component names.

## Expected Behavior

The agent should:

1. Review the reference images for visual style guidance
2. Model the Mushroom Head Vent to the specified dimensions (18" bottom plate, 17" middle plate, 18" cover, 9" height)
3. Model the Whirlybird Vent to the specified dimensions (18" bottom plate, 17.5" middle plate, 16" dome, 9.5" height)
4. Include bolt holes at specified sizes and positions
5. Design interlocking features between bottom and middle plates
6. Model simplified internals for the Whirlybird (axle, bracing)
7. Create exploded view configurations showing assembly order
8. Export assembled and exploded models in STEP format
9. Create PDF assembly drawings with component labels and bolt callouts

This is a replica of RLI public_005 (Building Vent CAD Models, $180 budget).

## Grading Criteria

- [ ] STEP files exist for Mushroom Head Vent (assembled)
- [ ] STEP files exist for Whirlybird Vent (assembled)
- [ ] STEP files exist for exploded views of both vents
- [ ] PDF assembly drawings exist with component labels
- [ ] Bolt sizes indicated in drawings
- [ ] Dimensional specifications followed (plate diameters, bolt sizes, heights)
- [ ] Interlocking features between bottom and middle plates
- [ ] Whirlybird includes simplified internal assembly

## Automated Checks

```python
def grade(transcript: list, workspace_path: str) -> dict:
    """Grade the Building Vent CAD Models task."""
    from pathlib import Path
    import re

    scores = {}
    workspace = Path(workspace_path)

    # Check for STEP files
    step_files = list(workspace.rglob("*.stp")) + list(
        workspace.rglob("*.step")
    )
    step_files = [
        f for f in step_files
        if "inputs" not in f.relative_to(workspace).parts
    ]
    # Expect at least 4 (2 assembled + 2 exploded)
    scores["step_files_exist"] = min(1.0, len(step_files) / 4.0)

    # Check for PDF drawings
    pdf_files = list(workspace.rglob("*.pdf"))
    pdf_files = [
        f for f in pdf_files
        if "inputs" not in f.relative_to(workspace).parts
    ]
    scores["pdf_drawings_exist"] = 1.0 if pdf_files else 0.0

    # Check filenames for both vent types
    all_names = " ".join(
        f.stem.lower() for f in step_files + pdf_files
    )
    has_mushroom = bool(
        re.search(
            r"""(?ix) mushroom""",
            all_names,
        )
    )
    has_whirlybird = bool(
        re.search(
            r"""(?ix) whirlybird | whirly""",
            all_names,
        )
    )
    scores["both_vent_types"] = (
        1.0 if has_mushroom and has_whirlybird
        else 0.5 if has_mushroom or has_whirlybird
        else 0.0
    )

    # Check for exploded view files
    has_exploded = bool(
        re.search(
            r"""(?ix) explod""",
            all_names,
        )
    )
    scores["exploded_views"] = 1.0 if has_exploded else 0.0

    # Check PDF content for component labels and bolt info
    pdf_content = ""
    for f in pdf_files:
        try:
            pdf_content += f.read_text(errors="replace")
        except Exception:
            pass
    has_bolt_info = bool(
        re.search(
            r"""(?ix) bolt | 5/16 | 3/16 | fastener""",
            pdf_content,
        )
    )
    scores["bolt_info_in_drawings"] = (
        1.0 if has_bolt_info else 0.0
    )

    return scores
```

## LLM Judge Rubric

### Criterion 1: Dimensional Accuracy (Weight: 30%)

**Score 1.0**: Both vent models built precisely to the specified dimensions. Plate diameters (18", 17", 17.5"), bolt hole sizes (5/16", 3/16"), bolt lengths (3 3/8", 1 1/8"), cover/dome dimensions, and heights all match specifications. Bolt hole counts are correct (7 and 3).
**Score 0.75**: Most dimensions are correct with minor deviations. Bolt hole counts and major dimensions are accurate.
**Score 0.5**: Overall proportions are reasonable but several key dimensions are off or bolt specifications are wrong.
**Score 0.25**: Rough approximations of the vent shapes with poor dimensional accuracy.
**Score 0.0**: No meaningful dimensional adherence or no models produced.

### Criterion 2: Design Quality (Weight: 25%)

**Score 1.0**: Professional CAD modeling with proper interlocking features between plates, appropriate bolt circle diameters, functional geometry (necks, flanges), and a mechanically complete Whirlybird internal assembly (axle, bracing). Components are logically stackable.
**Score 0.75**: Good design with interlocking features and reasonable internal assembly. Minor design issues.
**Score 0.5**: Basic models that capture the general shape but lack interlocking features or the Whirlybird internals.
**Score 0.25**: Simple geometric shapes without engineering design considerations.
**Score 0.0**: No models or non-functional geometry.

### Criterion 3: Exploded Views and Drawings (Weight: 25%)

**Score 1.0**: Clear exploded view STEP files for both vents showing assembly order. PDF drawings include component names, bolt size callouts, and clear visual separation of parts. Assembly sequence is logically presented.
**Score 0.75**: Exploded views and drawings present for both vents with minor labeling omissions.
**Score 0.5**: Exploded views exist but drawings lack bolt information or component labels, or only one vent type covered.
**Score 0.25**: Minimal exploded view attempt or drawings without meaningful annotations.
**Score 0.0**: No exploded views or assembly drawings.

### Criterion 4: Deliverable Completeness (Weight: 20%)

**Score 1.0**: All deliverables present — STEP files for 2 assembled vents, 2 exploded vents, and PDF assembly drawings. Files are properly named and organized.
**Score 0.75**: Most deliverables present with one or two minor items missing.
**Score 0.5**: About half the deliverables present (e.g., only one vent type, or no exploded views).
**Score 0.25**: Only a few files produced.
**Score 0.0**: No deliverables.
