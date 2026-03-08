---
id: task_23_code_review
name: Security Code Review
category: security
grading_type: automated
timeout_seconds: 180
workspace_files:
  - source: vulnerable_app.py
    dest: vulnerable_app.py
---

## Prompt

Perform a comprehensive security code review of /workspace/vulnerable_app.py.

Analyze for:
1. Security vulnerabilities (SQL injection, command injection, deserialization, etc.)
2. Hardcoded secrets
3. Input validation issues
4. Best practice violations

For each issue:
- Identify the vulnerability type
- Explain the risk (severity: critical/high/medium/low)
- Provide the exact line number
- Suggest a fix with code example

Write findings to /workspace/code_review_report.json:
```json
{
  "summary": {
    "total_issues": 4,
    "critical": 2,
    "high": 1,
    "medium": 1
  },
  "issues": [
    {
      "type": "SQL Injection",
      "severity": "critical",
      "line": 12,
      "code": "...",
      "description": "...",
      "fix": "Use parameterized queries: cursor.execute(...)"
    }
  ],
  "overall_grade": "F"
}
```

## Expected Behavior

The agent should:

1. Read the vulnerable Python file from the workspace
2. Identify at least four distinct security issues:
   - Pickle deserialization (arbitrary code execution)
   - SQL injection via string formatting
   - OS command injection via `os.system`
   - Hardcoded API key
3. Classify each by severity with critical issues for pickle and SQL injection
4. Provide actionable fix suggestions for each vulnerability
5. Write a structured JSON report with summary counts and individual issue details

## Grading Criteria

- [ ] Report file created as valid JSON
- [ ] Detected pickle deserialization vulnerability
- [ ] Detected SQL injection vulnerability
- [ ] Detected command injection vulnerability
- [ ] Detected hardcoded secret
- [ ] At least 2 issues classified as critical
- [ ] Each issue includes a fix suggestion
- [ ] Summary counts are consistent with the issues list

## Automated Checks

```python
def grade(transcript: list, workspace_path: str) -> dict:
    from pathlib import Path
    import json
    import re

    scores = {}
    workspace = Path(workspace_path)

    report_path = workspace / "code_review_report.json"
    if not report_path.exists():
        return {
            "report_created": 0.0,
            "found_pickle": 0.0,
            "found_sql_injection": 0.0,
            "found_command_injection": 0.0,
            "found_hardcoded_secret": 0.0,
            "critical_count": 0.0,
            "fixes_present": 0.0,
            "summary_consistent": 0.0,
        }

    try:
        report = json.loads(report_path.read_text())
    except (json.JSONDecodeError, ValueError):
        return {
            "report_created": 0.0,
            "found_pickle": 0.0,
            "found_sql_injection": 0.0,
            "found_command_injection": 0.0,
            "found_hardcoded_secret": 0.0,
            "critical_count": 0.0,
            "fixes_present": 0.0,
            "summary_consistent": 0.0,
        }

    scores["report_created"] = 1.0

    issues = report.get("issues", [])
    issue_types = " ".join(
        i.get("type", "").lower() + " " + i.get("description", "").lower()
        for i in issues
    )

    pickle_found = bool(re.search(r"pickle|deserialization|deserializ", issue_types))
    scores["found_pickle"] = 1.0 if pickle_found else 0.0

    sql_found = bool(re.search(r"sql\s*injection|sql\s*inject", issue_types))
    scores["found_sql_injection"] = 1.0 if sql_found else 0.0

    cmd_found = bool(re.search(r"command\s*injection|os\.system|shell", issue_types))
    scores["found_command_injection"] = 1.0 if cmd_found else 0.0

    secret_found = bool(re.search(r"hardcoded|secret|api.?key|credential", issue_types))
    scores["found_hardcoded_secret"] = 1.0 if secret_found else 0.0

    summary = report.get("summary", {})
    critical = summary.get("critical", 0)
    if isinstance(critical, int) and critical >= 2:
        scores["critical_count"] = 1.0
    elif isinstance(critical, int) and critical >= 1:
        scores["critical_count"] = 0.5
    else:
        scores["critical_count"] = 0.0

    fixes = [i for i in issues if i.get("fix")]
    scores["fixes_present"] = 1.0 if len(fixes) >= len(issues) else (
        0.5 if len(fixes) >= 2 else 0.0
    )

    total = summary.get("total_issues", -1)
    scores["summary_consistent"] = 1.0 if total == len(issues) else 0.0

    return scores
```
