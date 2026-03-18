---
id: task_33_voice_transcription
name: Voice Note Question
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

The agent receives only a voice note file with no text instructions. The voice note
asks: "Can you tell the rules about expensing travel to and from work as a
self-employed person?"

The agent should:

1. Notice the `.ogg` audio file in its workspace
2. Transcribe or otherwise understand the audio content
3. Recognise the question being asked
4. Reply with an answer about self-employed travel expense rules

This tests whether the agent can handle a non-text input modality, understand the
request, and provide a substantive answer — all without explicit text instructions.

## Grading Criteria

- [ ] Agent transcribes or understands the voice note
- [ ] Reply mentions travel or commuting expenses
- [ ] Reply mentions self-employment or self-employed
- [ ] Reply provides substantive guidance (not just a restatement of the question)

## Automated Checks

```python
def grade(transcript: list, workspace_path: str) -> dict:
    """Grade whether the agent answered the voice note question."""
    import re

    # Collect all assistant text from the transcript
    assistant_text = ""
    for event in transcript:
        if event.get("type") != "message":
            continue
        msg = event.get("message", {})
        if msg.get("role") != "assistant":
            continue
        for block in msg.get("content", []):
            if block.get("type") == "text":
                assistant_text += " " + block.get("text", "")

    lower = assistant_text.lower()
    scores = {}

    # Did the agent mention travel/commuting expenses?
    travel_pattern = re.compile(
        r"""(?ix)
        travel | commut | mileage | journey
        """,
    )
    scores["mentions travel expenses"] = (
        1.0 if travel_pattern.search(lower) else 0.0
    )

    # Did the agent mention self-employment?
    self_emp_pattern = re.compile(
        r"""(?ix)
        self[- ]?employ | sole \s+ trader | freelanc | business \s+ owner
        """,
    )
    scores["mentions self-employment"] = (
        1.0 if self_emp_pattern.search(lower) else 0.0
    )

    # Is the answer substantive (more than just restating the question)?
    word_count = len(assistant_text.split())
    scores["substantive answer"] = (
        1.0 if word_count > 50 else 0.0
    )

    return scores
```
