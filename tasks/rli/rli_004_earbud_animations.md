---
id: rli_004_earbud_animations
name: "RLI: 3D Earbud Product Animations"
category: 3d_modeling
grading_type: hybrid
timeout_seconds: 600
workspace_files:
  - source: rli/public_004/earbuds_back.jpg
    dest: inputs/earbuds_back.jpg
  - source: rli/public_004/earbuds_front.jpg
    dest: inputs/earbuds_front.jpg
  - source: rli/public_004/earbuds_top.jpg
    dest: inputs/earbuds_top.jpg
  - source: rli/public_004/replaceable_battery.jpg
    dest: inputs/replaceable_battery.jpg
  - source: rli/public_004/charging_case.jpg
    dest: inputs/charging_case.jpg
grading_weights:
  automated: 0.4
  llm_judge: 0.6
---

## Prompt

We need high-quality animations to showcase the features of a new earbuds design and the case. Create high-quality 3D product demonstration videos that effectively communicates the key features and benefits of the earbuds. We need 5 short, engaging animations to be used in marketing materials. The key features are:
- Silicone, airpod-like tips
- Stem of earbud swaps out for a replaceable battery
- Sleek charging case
- L/R indicator decal

### Provided material

- Earbuds image in `inputs/earbuds_back.jpg`
- Earbuds image in `inputs/earbuds_front.jpg`
- Earbuds image in `inputs/earbuds_top.jpg`
- Image demonstrating replaceable battery functionality in `inputs/replaceable_battery.jpg`
- Image of portable charging case in `inputs/charging_case.jpg`

### Deliverables

- Five short clips showcasing the different features of the earbuds (MP4 format)
- 3D models for the earbuds and case (e.g., .fbx format)

## Expected Behavior

The agent should:

1. Study the provided reference images to understand the earbud design from multiple angles
2. Create 3D models of the earbuds and charging case based on the reference images
3. Produce five short animation clips, each showcasing a different key feature:
   - Silicone tips design
   - Replaceable battery mechanism (stem swap)
   - Charging case design and functionality
   - L/R indicator decals
   - Overall product showcase
4. Export 3D models in .fbx format
5. Render animations as MP4 video files

This is a replica of RLI public_004 (3D Animations for Earbud Product, $500 budget).

## Grading Criteria

- [ ] At least five MP4 video clips produced
- [ ] 3D model files exist (.fbx or similar format)
- [ ] Silicone tips feature is showcased in a clip
- [ ] Replaceable battery mechanism is demonstrated
- [ ] Charging case is shown in a clip
- [ ] L/R indicator is visible in a clip
- [ ] Animations show smooth camera movement and transitions
- [ ] Models resemble the reference images

## Automated Checks

```python
def grade(transcript: list, workspace_path: str) -> dict:
    """Grade the 3D Earbud Product Animations task."""
    from pathlib import Path

    scores = {}
    workspace = Path(workspace_path)

    # Check for MP4 output files
    mp4_files = list(workspace.rglob("*.mp4"))
    mp4_files = [
        f for f in mp4_files
        if "inputs" not in f.relative_to(workspace).parts
    ]
    scores["video_count"] = min(1.0, len(mp4_files) / 5.0)

    # Check for 3D model files
    model_extensions = (
        ".fbx", ".obj", ".blend", ".glb", ".gltf", ".3ds", ".stl"
    )
    model_files = []
    for ext in model_extensions:
        model_files.extend(workspace.rglob(f"*{ext}"))
    model_files = [
        f for f in model_files
        if "inputs" not in f.relative_to(workspace).parts
    ]
    scores["models_exist"] = 1.0 if model_files else 0.0

    # Check video properties
    valid_videos = 0
    if mp4_files:
        for video in mp4_files:
            try:
                file_size = video.stat().st_size
                if file_size > 100_000:
                    valid_videos += 1
            except Exception:
                pass
    scores["videos_nontrivial"] = (
        min(1.0, valid_videos / 5.0) if mp4_files else 0.0
    )

    # Check video filenames or content for feature coverage
    all_names = " ".join(
        f.stem.lower() for f in mp4_files
    )
    feature_keywords = [
        "tip", "silicone", "battery", "replace",
        "case", "charg", "indicator", "decal",
    ]
    features_found = sum(
        1 for kw in feature_keywords
        if kw in all_names
    )
    scores["feature_coverage"] = min(
        1.0, features_found / 4.0
    )

    return scores
```

## LLM Judge Rubric

### Criterion 1: 3D Model Quality (Weight: 30%)

**Score 1.0**: 3D models of the earbuds and case are present and recognizably resemble earbuds with key design elements (tips, stem, case) identifiable.
**Score 0.0**: No 3D models produced, or models are unrecognizable as earbuds.

### Criterion 2: Animation Quality and Feature Showcase (Weight: 30%)

**Score 1.0**: At least three animation clips are present with visible motion (camera movement, object animation, or transitions) that showcase different aspects of the product.
**Score 0.0**: No animation clips produced, or output is entirely static with no motion.

### Criterion 3: Feature Completeness (Weight: 25%)

**Score 1.0**: At least three of the four key features (silicone tips, replaceable battery mechanism, charging case, L/R indicator decals) are identifiably showcased across the clips.
**Score 0.0**: Fewer than two features are identifiable, or no features are demonstrated in the output.

### Criterion 4: Marketing Suitability (Weight: 15%)

**Score 1.0**: Clips have reasonable lighting and composition that convey the product clearly enough to be used in a product context (e.g., website or social media).
**Score 0.0**: Output is unusable for any marketing purpose due to broken rendering, missing content, or incoherent presentation.
