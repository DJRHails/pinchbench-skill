---
id: rli_008_music_arrangement
name: "RLI: Music Transcription and Arrangement"
category: multimedia
grading_type: llm_judge
timeout_seconds: 600
workspace_files: []
---

## Prompt

Please make an arrangement of "Singing In The Rain" for a small house concert. The instruments we will have in the concert are:
- Piano
- B-flat trumpet
- Trombone
- Tenor saxophone
- Bassoon
- Double bass
- Vocals
(one of each)

I want the arrangement to be as close as possible to the version by Max Raabe and the Palast Orchester as played here: https://www.youtube.com/watch?v=VP1cllftq5o. You won't be able to perfectly recreate it, since we have far fewer instruments, but all the main parts of their arrangement should be present in the arrangement you create.

For the vocals, just put the notes. There is no need to include the lyrics.

Provided material: None

### Deliverables

- The full score of the arrangement (PDF and MusicXML formats)
- A MIDI export of the score
- A recording / audio rendering of the arrangement (MP3)

## Expected Behavior

The agent should:

1. Reference the Max Raabe and Palast Orchester version of "Singing In The Rain"
2. Transcribe the main parts and arrangement from that version
3. Adapt the arrangement for the specified 7-instrument ensemble (piano, B-flat trumpet, trombone, tenor saxophone, bassoon, double bass, vocals)
4. Distribute the orchestral parts across the available instruments while preserving the character of the original arrangement
5. Handle transposition for B-flat instruments (trumpet, tenor saxophone)
6. Create a full score with all parts
7. Export in PDF, MusicXML, MIDI, and MP3 formats
8. Include vocal melody as notes without lyrics

This is a replica of RLI public_008 (Music Transcription and Arrangement, $500 budget).

## Grading Criteria

- [ ] Full score PDF exists with all 7 instrument parts
- [ ] MusicXML file exists
- [ ] MIDI file exists
- [ ] MP3 audio rendering exists
- [ ] All instruments present: piano, B-flat trumpet, trombone, tenor saxophone, bassoon, double bass, vocals
- [ ] B-flat instruments correctly transposed
- [ ] Arrangement reflects the Max Raabe/Palast Orchester style
- [ ] Vocal part shows notes without lyrics

## Automated Checks

```python
def grade(transcript: list, workspace_path: str) -> dict:
    """Grade the Music Arrangement task."""
    from pathlib import Path
    import re

    scores = {}
    workspace = Path(workspace_path)

    # Check for PDF score
    pdf_files = list(workspace.rglob("*.pdf"))
    pdf_files = [
        f for f in pdf_files
        if "inputs" not in f.relative_to(workspace).parts
    ]
    scores["pdf_score"] = 1.0 if pdf_files else 0.0

    # Check for MusicXML
    xml_files = list(workspace.rglob("*.musicxml")) + list(
        workspace.rglob("*.mxl")
    ) + list(workspace.rglob("*.xml"))
    xml_files = [
        f for f in xml_files
        if "inputs" not in f.relative_to(workspace).parts
    ]
    scores["musicxml_exists"] = 1.0 if xml_files else 0.0

    # Check for MIDI
    midi_files = list(workspace.rglob("*.mid")) + list(
        workspace.rglob("*.midi")
    )
    midi_files = [
        f for f in midi_files
        if "inputs" not in f.relative_to(workspace).parts
    ]
    scores["midi_exists"] = 1.0 if midi_files else 0.0

    # Check for MP3 rendering
    mp3_files = list(workspace.rglob("*.mp3"))
    mp3_files = [
        f for f in mp3_files
        if "inputs" not in f.relative_to(workspace).parts
    ]
    scores["mp3_exists"] = 1.0 if mp3_files else 0.0

    # Check MusicXML content for instruments
    xml_content = ""
    for f in xml_files:
        try:
            xml_content += f.read_text(errors="replace")
        except Exception:
            pass

    instruments = [
        "piano", "trumpet", "trombone",
        "saxophone", "bassoon", "bass", "vocal",
    ]
    instruments_found = sum(
        1 for inst in instruments
        if re.search(
            r"""(?ix)""" + re.escape(inst),
            xml_content,
        )
    )
    scores["instruments_in_score"] = min(
        1.0, instruments_found / 5.0
    )

    return scores
```

## LLM Judge Rubric

### Criterion 1: Arrangement Quality (Weight: 35%)

**Score 1.0**: The arrangement is a recognizable version of "Singing In The Rain" that reflects the Max Raabe/Palast Orchester style. Main melodic lines and harmonies are present, and the overall 1920s-30s feel is conveyed despite the reduced instrumentation. Some simplification of orchestral elements is acceptable.
**Score 0.0**: No arrangement produced, completely wrong song, or the arrangement bears no resemblance to the specified version.

### Criterion 2: Instrumentation and Transposition (Weight: 25%)

**Score 1.0**: At least 5 of the 7 specified instruments have written parts. B-flat instruments are transposed (or a clear attempt is made). Vocal melody is notated without lyrics. Parts are generally playable for the intended instruments.
**Score 0.0**: Most instrument parts are missing, or notation is fundamentally incorrect (e.g., no transposition attempted, wrong clefs throughout).

### Criterion 3: Score Presentation (Weight: 20%)

**Score 1.0**: A full score PDF exists with clear notation, instrument labels, key signatures, and time signatures. The score is readable by performers, even if dynamics or articulations are sparse.
**Score 0.0**: No usable score produced, or the score is so poorly formatted that it cannot be read by performers.

### Criterion 4: Deliverable Completeness (Weight: 20%)

**Score 1.0**: At least three of the four deliverables are present and functional (PDF score, MusicXML, MIDI, MP3). Files open correctly in appropriate software.
**Score 0.0**: Fewer than two deliverables produced, or most files are corrupted/non-functional.
