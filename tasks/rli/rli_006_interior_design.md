---
id: rli_006_interior_design
name: "RLI: Apartment Interior Design"
category: design
grading_type: hybrid
timeout_seconds: 600
workspace_files:
  - source: "rli/public_006/cadastral floor plan.jpg"
    dest: "inputs/cadastral floor plan.jpg"
  - source: rli/public_006/bathroom.jpg
    dest: inputs/bathroom.jpg
  - source: "rli/public_006/additional measurements.jpg"
    dest: "inputs/additional measurements.jpg"
  - source: rli/public_006/bathroom_photos/
    dest: inputs/bathroom_photos/
grading_weights:
  automated: 0.4
  llm_judge: 0.6
---

## Prompt

Please design the following:
- Bathroom: 3 interior design options for the existing bathroom (wall-hung WC in the indicated location).
- Apartment: 6 furniture layout options; pick one "final" option for detailed plans.

### Notes

- Cadastral notation is "room no. / gross area (meters squared)".
- Rooms in cadastral plan:
  - Rooms 27, 28, 29: habitable rooms
  - Room 26: kitchen
  - Room 26a: living room
  - Room 26b: veranda
  - Room 25: bathroom
  - Room 24: hallway
- There is a door from the living room to the veranda, as shown in `inputs/additional measurements.jpg`
- Dimensions in deliverables are design intent; contractor to verify all on site.

### Provided material

- Cadastral floor plan (metric): `inputs/cadastral floor plan.jpg`
- Zoomed bathroom plan: `inputs/bathroom.jpg`
- Site photos: `inputs/bathroom_photos/photo_#_y.jpg`
- Additional measurements of the bathroom, living room, and veranda: `inputs/additional measurements.jpg`

### Deliverables

**Bathroom interior design - 3 options:**
- Renders: At least 3 views per option, at least 1200 pixels on long edge. Include one render from the top (JPG)
- Material board: one combined sheet per option showing the renders + finish swatches
- Wall finish images: high-res JPGs of each finish used.
- 3D source: supply native file (SKP)
- Design intent only: no engineering calcs; contractor/MEP to verify.

**Furniture layouts - 6 options:**
- One PDF floor plan per option, imperial dimensions (feet-inches) for key clearances and furniture sizes.
- One consolidated DWG containing all options.

**"Final" chosen furniture option; extra plans:**
- RCP & lighting plan: show ceiling levels, fixture symbols, mounting heights, and a legend (PDF)
- Toilet installation plan: locate the wall-hung toilet and built-in floor drain with horizontal dimensions in imperial units and outline the plasterboard boxing; no further details required (PDF)
- Electrical equipment layout: outlets, switches, appliance points, mounting heights, legend (circuiting by electrician) (PDF)
- Floor finishes plan: hatch/legend showing material zones and transition/threshold locations (PDF)

**CAD trace of cadastral plan:**
- Provide a clean DWG + PDF. Trace to scale, align walls, doors, windows

## Expected Behavior

The agent should:

1. Analyze the cadastral floor plan and additional measurements to understand the apartment layout
2. Study the bathroom photos and zoomed plan for the existing bathroom conditions
3. Create 3 distinct bathroom interior design options with wall-hung WC placement
4. Render each bathroom option from at least 3 views (including a top view)
5. Create material boards and finish samples for each bathroom option
6. Develop 6 furniture layout options for the apartment
7. Select one "final" option and create detailed plans (RCP, electrical, toilet installation, floor finishes)
8. Trace the cadastral plan into clean CAD format
9. Export all files in the specified formats (JPG, SKP, PDF, DWG)

This is a replica of RLI public_006 (Apartment Interior Design, $1950 budget).

## Grading Criteria

- [ ] 3 bathroom design options with renders (at least 3 views each, including top view)
- [ ] Material boards for each bathroom option
- [ ] Wall finish images provided
- [ ] SKP file for 3D bathroom model
- [ ] 6 furniture layout PDFs with imperial dimensions
- [ ] Consolidated DWG with all furniture layouts
- [ ] RCP & lighting plan (PDF) for final option
- [ ] Toilet installation plan (PDF) for final option
- [ ] Electrical equipment layout (PDF) for final option
- [ ] Floor finishes plan (PDF) for final option
- [ ] CAD trace of cadastral plan (DWG + PDF)

## Automated Checks

```python
def grade(transcript: list, workspace_path: str) -> dict:
    """Grade the Apartment Interior Design task."""
    from pathlib import Path
    import re

    scores = {}
    workspace = Path(workspace_path)

    # Check for render images (bathroom options)
    jpg_files = list(workspace.rglob("*.jpg")) + list(
        workspace.rglob("*.jpeg")
    )
    jpg_files = [
        f for f in jpg_files
        if "inputs" not in f.relative_to(workspace).parts
    ]
    # Expect at least 9 renders (3 options x 3 views)
    scores["bathroom_renders"] = min(1.0, len(jpg_files) / 9.0)

    # Check for SKP file
    skp_files = list(workspace.rglob("*.skp"))
    skp_files = [
        f for f in skp_files
        if "inputs" not in f.relative_to(workspace).parts
    ]
    scores["skp_model"] = 1.0 if skp_files else 0.0

    # Check for PDF deliverables
    pdf_files = list(workspace.rglob("*.pdf"))
    pdf_files = [
        f for f in pdf_files
        if "inputs" not in f.relative_to(workspace).parts
    ]
    # Expect at least 10 PDFs (6 layouts + RCP + toilet
    # + electrical + floor finishes)
    scores["pdf_deliverables"] = min(1.0, len(pdf_files) / 10.0)

    # Check for DWG files
    dwg_files = list(workspace.rglob("*.dwg"))
    dwg_files = [
        f for f in dwg_files
        if "inputs" not in f.relative_to(workspace).parts
    ]
    scores["dwg_files"] = 1.0 if dwg_files else 0.0

    # Check PDF and file names for key plan types
    all_names = " ".join(
        f.stem.lower() for f in pdf_files + dwg_files + jpg_files
    )
    plan_types = {
        "lighting": r"""(?ix) rcp | light | ceil""",
        "electrical": r"""(?ix) electr | outlet | switch""",
        "toilet": r"""(?ix) toilet | wc | install""",
        "floor_finish": r"""(?ix) floor | finish | material""",
        "furniture_layout": r"""(?ix) furniture | layout | option""",
    }
    plans_found = sum(
        1 for pattern in plan_types.values()
        if re.search(pattern, all_names)
    )
    scores["plan_coverage"] = plans_found / len(plan_types)

    return scores
```

## LLM Judge Rubric

### Criterion 1: Bathroom Design Quality (Weight: 30%)

**Score 1.0**: At least two bathroom design options are present with renders (including a top view) and material boards. Wall-hung WC is positioned. Designs show practical consideration of the existing space. Minor omissions in render count or material board detail are acceptable.
**Score 0.0**: Fewer than two bathroom options produced, or no renders/material boards exist.

### Criterion 2: Furniture Layouts (Weight: 25%)

**Score 1.0**: At least four furniture layout options are provided as floor plans with imperial dimensions for key clearances and furniture sizes. Layouts are practical and respect room proportions. Minor formatting issues are acceptable.
**Score 0.0**: Fewer than three layout options produced, or layouts lack any dimensioning.

### Criterion 3: Detailed Plans for Final Option (Weight: 25%)

**Score 1.0**: At least three of the four detailed plans are present for the chosen final option (RCP/lighting, toilet installation, electrical layout, floor finishes). Plans include symbols, legends, or dimensions as appropriate.
**Score 0.0**: Fewer than two detailed plans produced, or plans lack meaningful content.

### Criterion 4: CAD Trace and File Completeness (Weight: 20%)

**Score 1.0**: A CAD trace of the cadastral plan exists in DWG or PDF format with walls, doors, and windows traced. Deliverable files are provided in the requested formats (JPG, SKP, PDF, DWG). Minor alignment issues are acceptable.
**Score 0.0**: No CAD trace produced, or most required file formats are missing.
