---
id: task_33_voice_transcription
name: Voice Note Transcription
category: media
grading_type: automated
timeout_seconds: 300
workspace_files:
  - source: voice_note.ogg
    dest: voice_note.ogg
---

## Prompt

*[voice_note.ogg attached]*

## Expected Behavior

The agent receives only a voice note file with no text instructions. It should:

1. Notice the `.ogg` audio file in its workspace
2. Independently decide to transcribe it
3. Use an available transcription tool or approach (Whisper, browser-based service, built-in STT)
4. Save the transcription to a text file in the workspace

This tests whether the agent can handle a non-text input modality and take appropriate action without explicit instructions.

## Grading Criteria

- [ ] Agent identifies the file as audio
- [ ] Agent attempts transcription
- [ ] A text file with the transcription is created in the workspace
- [ ] Transcription contains meaningful text (not empty or placeholder)

## Automated Checks

```python
def grade(transcript: list, workspace_path: str) -> dict:
    """Grade the voice transcription task with binary outcomes."""
    from pathlib import Path

    workspace = Path(workspace_path)
    scores = {}

    # Find any .txt file that could be a transcription output
    txt_files = [
        f for f in workspace.rglob("*.txt")
        if f.stat().st_size > 0
    ]

    scores["transcription file created"] = (
        1.0 if txt_files else 0.0
    )

    if not txt_files:
        scores["transcription has substance"] = 0.0
        return scores

    # Check the largest txt file for substance
    best = max(txt_files, key=lambda f: f.stat().st_size)
    content = best.read_text().strip()
    word_count = len(content.split())

    scores["transcription has substance"] = (
        1.0 if word_count > 20 else 0.0
    )

    return scores
```
