---
id: rli_002_animated_video
name: "RLI: Tree Services Animated Video"
category: multimedia
grading_type: hybrid
timeout_seconds: 600
workspace_files:
  - source: rli/public_002/VoiceOver.wav
    dest: inputs/VoiceOver.wav
grading_weights:
  automated: 0.4
  llm_judge: 0.6
---

## Prompt

Create a 2D animated video that explains and shows the process of trimming, pruning, stump removal, and tree health maintenance. The video should educate potential customers on the process and build trust in the brand through a short, informative video.

### Requirements

- Audience: Homeowners, Real estate developers, Facility managers, Landscapers, Anyone in need of tree maintenance or removal
- Tone: Professional yet friendly, instilling confidence and reliability
- Length: Around 60 seconds
- Visual Preference: Bold font, natural color palette (greens, browns, light blues), nature-related icons and illustrations, subtle use of characters (e.g., workers, trees, property)
- Video style: Flat design / modern style, subtle transitions and motion graphics, clean 2D animation, icon-based with light character use, no subtitles

### Script

Welcome to Skyline Tree Services, your trusted partner for all tree care needs.
And here's how we do it:
1. We start with a thorough consultation to understand your tree care needs.
2. Whether it's shaping your tree, pruning it, bracing it, removing a stump, or grinding it, our experts conduct a detailed assessment of your tree's health and structure.
3. We create a customized care plan tailored to each tree's specific requirements.
4. Using the latest technology and techniques, our skilled team performs the work efficiently and safely.
5. At Skyline Tree Services, safety is our top priority. We ensure all precautions are taken to protect your property and our team.
6. Once the job is done, we clean up thoroughly, leaving your space as beautiful as we found it.
And here's how we work at Skyline Tree Services. Contact us and let us help you care for your trees.

Provided material: Raw voiceover audio file (`inputs/VoiceOver.wav`)

### Deliverables

2D animated video with audio from the provided voiceover (MP4, 1080p resolution)

## Expected Behavior

The agent should:

1. Listen to the provided voiceover audio to understand timing and pacing
2. Create 2D animated visuals that illustrate each step of the script
3. Use a natural color palette (greens, browns, light blues) with flat design style
4. Include nature-related icons, illustrations, and subtle character use
5. Synchronize the animation with the provided voiceover audio
6. Export as MP4 at 1080p resolution, approximately 60 seconds long

This is a replica of RLI public_002 (Tree Services Animated Video, $80 budget).

## Grading Criteria

- [ ] MP4 video file exists
- [ ] Video resolution is 1080p (1920x1080)
- [ ] Video length is approximately 60 seconds
- [ ] Audio from provided voiceover is included
- [ ] 2D animated visuals are present (not static slides)
- [ ] Natural color palette used (greens, browns, light blues)
- [ ] Flat design / modern style
- [ ] Content follows the provided script sequence
- [ ] No subtitles in the video

## Automated Checks

```python
def grade(transcript: list, workspace_path: str) -> dict:
    """Grade the Tree Services Animated Video task."""
    from pathlib import Path

    scores = {}
    workspace = Path(workspace_path)

    # Check for MP4 output
    mp4_files = list(workspace.rglob("*.mp4"))
    mp4_files = [
        f for f in mp4_files
        if "inputs" not in f.relative_to(workspace).parts
    ]
    scores["video_exists"] = 1.0 if mp4_files else 0.0

    if mp4_files:
        video = mp4_files[0]
        file_size = video.stat().st_size

        # Check file is non-trivial (> 500KB for a 60s video)
        scores["video_nontrivial"] = (
            1.0 if file_size > 500_000 else 0.0
        )

        # Check video properties with ffprobe
        try:
            import subprocess

            result = subprocess.run(
                [
                    "ffprobe",
                    "-v", "quiet",
                    "-print_format", "json",
                    "-show_streams",
                    "-show_format",
                    str(video),
                ],
                capture_output=True,
                text=True,
                timeout=30,
            )
            import json

            info = json.loads(result.stdout)

            # Check for video stream
            video_streams = [
                s for s in info.get("streams", [])
                if s.get("codec_type") == "video"
            ]
            scores["has_video_stream"] = (
                1.0 if video_streams else 0.0
            )

            # Check resolution (1080p)
            if video_streams:
                height = int(video_streams[0].get("height", 0))
                scores["resolution_1080p"] = (
                    1.0 if height >= 1080 else 0.5 if height >= 720 else 0.0
                )

            # Check for audio stream
            audio_streams = [
                s for s in info.get("streams", [])
                if s.get("codec_type") == "audio"
            ]
            scores["has_audio"] = (
                1.0 if audio_streams else 0.0
            )

            # Check duration (~60 seconds, allow 30-120s)
            duration = float(
                info.get("format", {}).get("duration", 0)
            )
            if 30 <= duration <= 120:
                scores["duration_appropriate"] = 1.0
            elif 15 <= duration <= 180:
                scores["duration_appropriate"] = 0.5
            else:
                scores["duration_appropriate"] = 0.0
        except Exception:
            scores["has_video_stream"] = 0.0
            scores["has_audio"] = 0.0
            scores["duration_appropriate"] = 0.0
    else:
        scores["video_nontrivial"] = 0.0
        scores["has_video_stream"] = 0.0
        scores["has_audio"] = 0.0
        scores["duration_appropriate"] = 0.0

    return scores
```

## LLM Judge Rubric

### Criterion 1: Animation Quality (Weight: 30%)

**Score 1.0**: The video contains meaningful 2D animation with visible motion (not just static slides with fade transitions). Visuals include icons, illustrations, or characters that move or transition on screen.
**Score 0.0**: No animation present, only static images, or no visual content at all.

### Criterion 2: Script and Content Alignment (Weight: 30%)

**Score 1.0**: Visuals illustrate at least half of the script steps (consultation, assessment, care plan, execution, safety, cleanup) in a recognizable sequence that relates to the voiceover content.
**Score 0.0**: Visuals are unrelated to the script, or no visual content accompanies the audio.

### Criterion 3: Visual Design (Weight: 20%)

**Score 1.0**: The video uses a nature-appropriate color palette (greens, browns, or light blues) and maintains a clean, modern aesthetic consistent with a tree services brand.
**Score 0.0**: No design effort applied, colors are completely unrelated to the nature/tree services theme, or visual style is incoherent.

### Criterion 4: Audio Integration (Weight: 20%)

**Score 1.0**: The provided voiceover audio is included in the video and the video length approximately matches the audio duration.
**Score 0.0**: No audio present, wrong audio used, or the audio is completely out of sync with the video length.
