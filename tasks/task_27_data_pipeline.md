---
id: task_27_data_pipeline
name: Data Quality Pipeline
category: data
grading_type: automated
timeout_seconds: 240
workspace_files:
  - source: raw_user_data.csv
    dest: raw_user_data.csv
---

## Prompt

Build a data quality pipeline for /workspace/raw_user_data.csv.

Steps:
1. Load and analyze the raw data
2. Detect data quality issues:
   - Duplicates (same email, case-insensitive)
   - Missing values
   - Invalid dates (e.g. month 13)
   - Invalid email formats (missing TLD)
   - Negative revenue values
3. Clean the data:
   - Deduplicate (keep most recent by signup_date)
   - Lowercase all emails
   - Remove or flag invalid records
   - Handle missing values
4. Generate quality report
5. Write cleaned data

Write cleaned data to /workspace/cleaned_user_data.csv
Write quality report to /workspace/data_quality_report.json:
```json
{
  "raw_records": 8,
  "cleaned_records": 5,
  "issues_found": {
    "duplicates": 3,
    "missing_values": 2,
    "invalid_dates": 1,
    "invalid_emails": 1,
    "negative_values": 1
  },
  "removed_records": [
    {"user_id": 3, "reason": "invalid date and invalid email"}
  ],
  "transformations_applied": ["lowercase_emails", "deduplicate"]
}
```

## Expected Behavior

The agent should:

1. Load the CSV file containing 8 records with deliberate quality issues
2. Detect specific issues in the data:
   - Duplicate emails: alice@example.com (rows 1 and 8), DUPLICATE/duplicate@example.com (rows 4 and 5)
   - Missing values: row 2 (missing revenue), row 7 (missing signup_date)
   - Invalid date: row 3 (2026-13-45 — month 13 is invalid)
   - Invalid email: row 3 (charlie@example — no TLD)
   - Negative revenue: row 6 (-100.00)
3. Clean the data by removing or correcting invalid records
4. Write both a cleaned CSV and a structured quality report
5. The cleaned dataset should have fewer than 8 records

## Grading Criteria

- [ ] Cleaned CSV file created
- [ ] Quality report JSON created
- [ ] Report identifies correct raw record count (8)
- [ ] Cleaned records fewer than raw (some removed)
- [ ] Detected duplicate emails
- [ ] Detected invalid date
- [ ] Detected invalid email format
- [ ] Detected negative revenue value
- [ ] Cleaned CSV is valid with header row

## Automated Checks

```python
def grade(transcript: list, workspace_path: str) -> dict:
    from pathlib import Path
    import json

    scores = {}
    workspace = Path(workspace_path)

    # Check cleaned CSV
    cleaned_path = workspace / "cleaned_user_data.csv"
    if cleaned_path.exists():
        content = cleaned_path.read_text().strip()
        lines = content.split("\n")
        scores["cleaned_csv_created"] = 1.0
        has_header = "user_id" in lines[0].lower() if lines else False
        scores["csv_has_header"] = 1.0 if has_header else 0.0
        data_rows = len(lines) - 1 if has_header else len(lines)
        scores["csv_has_data"] = 1.0 if data_rows > 0 else 0.0
    else:
        scores["cleaned_csv_created"] = 0.0
        scores["csv_has_header"] = 0.0
        scores["csv_has_data"] = 0.0

    # Check quality report
    report_path = workspace / "data_quality_report.json"
    if not report_path.exists():
        scores["report_created"] = 0.0
        scores["raw_count_correct"] = 0.0
        scores["cleaned_fewer"] = 0.0
        scores["found_duplicates"] = 0.0
        scores["found_invalid_dates"] = 0.0
        scores["found_invalid_emails"] = 0.0
        scores["found_negative_values"] = 0.0
        return scores

    try:
        report = json.loads(report_path.read_text())
    except (json.JSONDecodeError, ValueError):
        scores["report_created"] = 0.0
        scores["raw_count_correct"] = 0.0
        scores["cleaned_fewer"] = 0.0
        scores["found_duplicates"] = 0.0
        scores["found_invalid_dates"] = 0.0
        scores["found_invalid_emails"] = 0.0
        scores["found_negative_values"] = 0.0
        return scores

    scores["report_created"] = 1.0

    raw = report.get("raw_records", 0)
    scores["raw_count_correct"] = 1.0 if raw == 8 else 0.0

    cleaned = report.get("cleaned_records", 8)
    scores["cleaned_fewer"] = 1.0 if cleaned < 8 else 0.0

    issues = report.get("issues_found", {})

    dupes = issues.get("duplicates", 0)
    scores["found_duplicates"] = 1.0 if dupes >= 2 else (
        0.5 if dupes >= 1 else 0.0
    )

    invalid_dates = issues.get("invalid_dates", 0)
    scores["found_invalid_dates"] = 1.0 if invalid_dates >= 1 else 0.0

    invalid_emails = issues.get("invalid_emails", 0)
    scores["found_invalid_emails"] = 1.0 if invalid_emails >= 1 else 0.0

    neg = issues.get("negative_values", 0)
    scores["found_negative_values"] = 1.0 if neg >= 1 else 0.0

    return scores
```
