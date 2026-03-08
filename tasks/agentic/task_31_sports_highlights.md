---
id: task_31_sports_highlights
name: Sports Highlight Retrieval
category: media
grading_type: hybrid
timeout_seconds: 300
workspace_files: []
---

## Prompt

Find the last goal scored in Arsenal's most recent Premier League match.

Steps:
1. Search for Arsenal's most recent match (date, opponent, score)
2. Search for video highlights of that match
3. Find the specific goal clip (if multiple goals, get the last one)
4. Download the video clip to /workspace/arsenal_last_goal.mp4
5. Extract metadata: goal scorer, minute, match details

Write metadata to /workspace/arsenal_goal_metadata.json:
```json
{
  "match_date": "2026-03-01",
  "opponent": "Chelsea",
  "score": "2-1",
  "goal_scorer": "Saka",
  "minute": 78,
  "video_url": "https://...",
  "file_path": "/workspace/arsenal_last_goal.mp4"
}
```

## Expected Behavior

The agent should:

1. Use web search to find Arsenal's latest Premier League result
2. Identify the match date, opponent, final score, and goal scorers
3. Search for video highlights of that specific match
4. Attempt to download a goal clip (this may fail due to DRM or geo-restrictions)
5. If download fails, at minimum capture the video URL
6. Write structured metadata about the match and goal

The key demonstration is the agent's ability to navigate real-time sports data and media sources. Full video download is a bonus — the metadata and URL are the primary outputs.

## Grading Criteria

- [ ] Metadata JSON file created
- [ ] Match date is a valid date string
- [ ] Opponent team name is present
- [ ] Score is present in valid format
- [ ] Goal scorer name identified
- [ ] Goal minute is a number
- [ ] Video URL or downloaded file present
- [ ] Web search tools used

## Automated Checks

```python
def grade(transcript: list, workspace_path: str) -> dict:
    from pathlib import Path
    import json
    import re

    scores = {}
    workspace = Path(workspace_path)

    path = workspace / "arsenal_goal_metadata.json"
    if not path.exists():
        return {
            "metadata_created": 0.0,
            "has_match_date": 0.0,
            "has_opponent": 0.0,
            "has_score": 0.0,
            "has_goal_scorer": 0.0,
            "has_minute": 0.0,
            "has_video": 0.0,
            "used_web_search": 0.0,
        }

    try:
        metadata = json.loads(path.read_text())
    except (json.JSONDecodeError, ValueError):
        return {
            "metadata_created": 0.0,
            "has_match_date": 0.0,
            "has_opponent": 0.0,
            "has_score": 0.0,
            "has_goal_scorer": 0.0,
            "has_minute": 0.0,
            "has_video": 0.0,
            "used_web_search": 0.0,
        }

    scores["metadata_created"] = 1.0

    date = str(metadata.get("match_date", ""))
    scores["has_match_date"] = 1.0 if re.match(
        r"\d{4}-\d{2}-\d{2}", date,
    ) else 0.0

    opponent = str(metadata.get("opponent", ""))
    scores["has_opponent"] = 1.0 if len(opponent) > 2 else 0.0

    score_val = str(metadata.get("score", ""))
    scores["has_score"] = 1.0 if re.search(r"\d+\s*-\s*\d+", score_val) else 0.0

    scorer = str(metadata.get("goal_scorer", ""))
    scores["has_goal_scorer"] = 1.0 if len(scorer) > 2 else 0.0

    minute = metadata.get("minute")
    scores["has_minute"] = 1.0 if isinstance(minute, (int, float)) else 0.0

    video_path = workspace / "arsenal_last_goal.mp4"
    video_url = str(metadata.get("video_url", ""))
    if video_path.exists() and video_path.stat().st_size > 100_000:
        scores["has_video"] = 1.0
    elif video_url and len(video_url) > 10:
        scores["has_video"] = 0.75
    else:
        scores["has_video"] = 0.0

    # Check for web search usage
    used_search = False
    for event in transcript:
        if event.get("type") != "message":
            continue
        msg = event.get("message", {})
        if msg.get("role") != "assistant":
            continue
        for item in msg.get("content", []):
            if item.get("type") == "toolCall":
                tool_name = item.get("name", "").lower()
                if any(
                    t in tool_name
                    for t in ["search", "fetch", "browse", "web"]
                ):
                    used_search = True
    scores["used_web_search"] = 1.0 if used_search else 0.0

    return scores
```

## LLM Judge Rubric

### Criterion 1: Information Accuracy (Weight: 40%)

**Score 1.0**: Match details are verifiably correct — the match date, opponent, and score match Arsenal's actual most recent Premier League fixture. Goal scorer and minute are accurate.
**Score 0.75**: Match identification is correct but minor details (exact minute, scorer for multi-goal matches) may be slightly off.
**Score 0.5**: Agent found a recent Arsenal match but not necessarily the most recent, or some details are incorrect.
**Score 0.25**: Agent found Arsenal-related information but significant factual errors.
**Score 0.0**: No match information found or completely wrong data.

### Criterion 2: Media Retrieval (Weight: 30%)

**Score 1.0**: Agent downloaded an actual video clip of the goal. File is a valid video (>100KB).
**Score 0.75**: Agent found a direct video URL pointing to the specific match highlights.
**Score 0.5**: Agent found a general highlights page URL but not a direct video link.
**Score 0.25**: Agent attempted to find video but only found text descriptions.
**Score 0.0**: No video or URL found.

### Criterion 3: Research Process (Weight: 30%)

**Score 1.0**: Agent demonstrated a logical research workflow — searched for the match, confirmed details from multiple sources, then sought video content. Transcript shows purposeful tool usage.
**Score 0.75**: Good research process with minor inefficiencies.
**Score 0.5**: Research was somewhat scattered but ultimately produced results.
**Score 0.25**: Research process was inefficient with many dead ends and minimal results.
**Score 0.0**: No evidence of systematic research.
