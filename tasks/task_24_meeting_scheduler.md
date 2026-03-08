---
id: task_24_meeting_scheduler
name: Meeting Scheduler with Conflict Resolution
category: reasoning
grading_type: automated
timeout_seconds: 180
workspace_files:
  - path: "calendars.json"
    content: |
      {
        "person_a": [
          {"date": "2026-02-24", "start": "09:00", "end": "10:00", "title": "Standup"},
          {"date": "2026-02-24", "start": "14:00", "end": "15:30", "title": "Client call"},
          {"date": "2026-02-25", "start": "10:00", "end": "11:00", "title": "Review"}
        ],
        "person_b": [
          {"date": "2026-02-24", "start": "10:00", "end": "12:00", "title": "Deep work"},
          {"date": "2026-02-24", "start": "13:00", "end": "14:00", "title": "Lunch"},
          {"date": "2026-02-25", "start": "09:00", "end": "10:00", "title": "Gym"}
        ],
        "person_c": [
          {"date": "2026-02-24", "start": "11:00", "end": "12:00", "title": "Meeting"},
          {"date": "2026-02-25", "start": "14:00", "end": "16:00", "title": "Workshop"}
        ]
      }
---

## Prompt

Schedule a 1-hour meeting for Person A, B, and C within the analysis period (2026-02-24 to 2026-02-25).

Requirements:
- Read calendar data from /workspace/calendars.json
- Find optimal time slots with no conflicts
- Prefer morning slots (before 12:00)
- All times are in the same local timezone
- If conflicts exist, suggest which person should reschedule what

Write to /workspace/meeting_recommendations.json:
```json
{
  "requested_duration": 60,
  "analysis_period": "2026-02-24 to 2026-02-25",
  "recommendations": [
    {
      "rank": 1,
      "date": "YYYY-MM-DD",
      "start_time": "HH:MM",
      "end_time": "HH:MM",
      "reason": "No conflicts, morning slot",
      "conflicts": []
    }
  ],
  "if_no_slots": {
    "suggested_reschedules": [
      {
        "person": "Person B",
        "event": "Deep work",
        "original_time": "10:00-12:00",
        "reason": "Flexible block, can be moved"
      }
    ]
  }
}
```

## Expected Behavior

The agent should:

1. Parse the calendar JSON with events for three people
2. Identify free 1-hour windows across both days where all three are available
3. Rank slots by preference (morning over afternoon)
4. If no conflict-free slots exist, suggest which event to reschedule

Available free windows (all three free) include:
- 2026-02-25 10:00-11:00 (after B's gym, before nothing for A until Review ends at 11:00 — actually A has Review 10-11, so this conflicts)
- 2026-02-25 11:00-14:00 range (A free after Review, B free, C free until Workshop at 14:00)

The best conflict-free slot is 2026-02-25 11:00-12:00 or later morning/early afternoon.

## Grading Criteria

- [ ] Recommendations file created as valid JSON
- [ ] At least one recommendation present
- [ ] Each recommendation has date, start_time, end_time, rank
- [ ] Top recommendation has no conflicts with any person's calendar
- [ ] Recommended slot is exactly 1 hour
- [ ] Slot falls within the analysis period

## Automated Checks

```python
def grade(transcript: list, workspace_path: str) -> dict:
    from pathlib import Path
    import json

    scores = {}
    workspace = Path(workspace_path)

    recs_path = workspace / "meeting_recommendations.json"
    if not recs_path.exists():
        return {
            "file_created": 0.0,
            "has_recommendations": 0.0,
            "has_required_fields": 0.0,
            "top_no_conflicts": 0.0,
            "slot_duration_correct": 0.0,
            "within_period": 0.0,
        }

    try:
        recs = json.loads(recs_path.read_text())
    except (json.JSONDecodeError, ValueError):
        return {
            "file_created": 0.0,
            "has_recommendations": 0.0,
            "has_required_fields": 0.0,
            "top_no_conflicts": 0.0,
            "slot_duration_correct": 0.0,
            "within_period": 0.0,
        }

    scores["file_created"] = 1.0

    recommendations = recs.get("recommendations", [])
    scores["has_recommendations"] = 1.0 if len(recommendations) > 0 else 0.0

    if not recommendations:
        scores["has_required_fields"] = 0.0
        scores["top_no_conflicts"] = 0.0
        scores["slot_duration_correct"] = 0.0
        scores["within_period"] = 0.0
        return scores

    required = ["date", "start_time", "end_time", "rank"]
    top = recommendations[0]
    has_fields = all(k in top for k in required)
    scores["has_required_fields"] = 1.0 if has_fields else 0.0

    conflicts = top.get("conflicts")
    if conflicts is not None and len(conflicts) == 0:
        scores["top_no_conflicts"] = 1.0
    elif conflicts is not None:
        scores["top_no_conflicts"] = 0.0
    else:
        # No conflicts field — check via calendar data
        scores["top_no_conflicts"] = 0.5

    # Check 1-hour duration
    start = top.get("start_time", "")
    end = top.get("end_time", "")
    try:
        sh, sm = int(start.split(":")[0]), int(start.split(":")[1])
        eh, em = int(end.split(":")[0]), int(end.split(":")[1])
        duration = (eh * 60 + em) - (sh * 60 + sm)
        scores["slot_duration_correct"] = 1.0 if duration == 60 else 0.0
    except (ValueError, IndexError):
        scores["slot_duration_correct"] = 0.0

    date = top.get("date", "")
    scores["within_period"] = 1.0 if date in (
        "2026-02-24", "2026-02-25",
    ) else 0.0

    return scores
```
