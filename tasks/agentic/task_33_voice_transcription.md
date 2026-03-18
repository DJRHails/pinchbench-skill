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

I received a voice note saved as `voice_note.ogg` in my workspace. Please transcribe it to text and save the transcription to `transcription.txt`. Include a brief summary of what the person is talking about at the end of the file, separated by a blank line and prefixed with "Summary: ".

## Expected Behavior

The agent should:

1. Detect that `voice_note.ogg` is an audio file (Ogg Opus format, a common WhatsApp voice note format)
2. Use an available transcription tool or approach to convert the speech to text (e.g. Whisper, a browser-based service, or a built-in speech-to-text tool)
3. Write the transcription to `transcription.txt`
4. Append a brief one-to-two sentence summary at the end, prefixed with "Summary: "

The transcription should capture the substance of what was said. Exact wording may vary across transcription methods.

## Grading Criteria

- [ ] Output file `transcription.txt` created
- [ ] Transcription contains meaningful text (not empty or placeholder)
- [ ] Summary line present and prefixed with "Summary: "

## Automated Checks

```python
def grade(transcript: list, workspace_path: str) -> dict:
    """Grade the voice transcription task with binary outcomes."""
    from pathlib import Path
    import re

    workspace = Path(workspace_path)
    scores = {}

    output_file = workspace / "transcription.txt"

    # Check output file exists
    scores["output file created"] = 1.0 if output_file.exists() else 0.0

    if not output_file.exists():
        scores["transcription has substance"] = 0.0
        scores["summary line present"] = 0.0
        return scores

    content = output_file.read_text().strip()

    # Check transcription is non-trivial (more than 20 words)
    word_count = len(content.split())
    scores["transcription has substance"] = (
        1.0 if word_count > 20 else 0.0
    )

    # Check summary line is present
    summary_pattern = re.compile(
        r"""(?mx)        # multiline, verbose
        ^Summary:\s+     # line starting with "Summary: "
        \S+              # followed by non-whitespace
        """,
    )
    scores["summary line present"] = (
        1.0 if summary_pattern.search(content) else 0.0
    )

    return scores
```
