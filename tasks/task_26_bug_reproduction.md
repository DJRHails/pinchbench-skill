---
id: task_26_bug_reproduction
name: Bug Reproduction from Report
category: coding
grading_type: hybrid
timeout_seconds: 240
workspace_files:
  - source: bug_report_4521.txt
    dest: bug_report_4521.txt
---

## Prompt

Analyze /workspace/bug_report_4521.txt and create an automated reproduction test.

Steps:
1. Extract bug details (root cause hypothesis, affected component)
2. Write a Python test script that reproduces the bug scenario
3. The script should:
   - Set up test environment (mock the login endpoint)
   - Execute the reproduction steps with special characters in password
   - Assert expected vs actual behavior
   - Log the bug evidence
4. Run the test script to verify it executes
5. Document findings

Write test to /workspace/reproduce_bug_4521.py
Write findings to /workspace/bug_analysis_4521.json:
```json
{
  "bug_id": 4521,
  "root_cause_hypothesis": "...",
  "affected_component": "...",
  "reproduction_success": true,
  "error_message": "...",
  "suggested_fix": "...",
  "test_script_path": "/workspace/reproduce_bug_4521.py"
}
```

## Expected Behavior

The agent should:

1. Read the bug report describing a login failure with special characters in passwords
2. Hypothesize the root cause (likely insufficient character escaping/encoding)
3. Write a Python test script that demonstrates the issue
4. The script should be valid Python with test functions or assertions
5. Create a JSON analysis file identifying the root cause and suggesting a fix
6. The hypothesis should mention special characters, encoding, or escaping

## Grading Criteria

- [ ] Test script created as valid Python
- [ ] Test script references passwords with special characters
- [ ] Analysis JSON created with correct bug_id
- [ ] Root cause hypothesis mentions character handling
- [ ] Suggested fix is actionable
- [ ] Script was executed by the agent

## Automated Checks

```python
def grade(transcript: list, workspace_path: str) -> dict:
    from pathlib import Path
    import json
    import re
    import ast

    scores = {}
    workspace = Path(workspace_path)

    # Check test script exists and is valid Python
    script_path = workspace / "reproduce_bug_4521.py"
    if script_path.exists():
        content = script_path.read_text()
        scores["script_created"] = 1.0

        try:
            ast.parse(content)
            scores["valid_python"] = 1.0
        except SyntaxError:
            scores["valid_python"] = 0.0

        has_password_ref = bool(re.search(
            r"password|P@ssw0rd|special.?char", content, re.IGNORECASE,
        ))
        scores["references_special_chars"] = 1.0 if has_password_ref else 0.0
    else:
        scores["script_created"] = 0.0
        scores["valid_python"] = 0.0
        scores["references_special_chars"] = 0.0

    # Check analysis JSON
    analysis_path = workspace / "bug_analysis_4521.json"
    if analysis_path.exists():
        try:
            analysis = json.loads(analysis_path.read_text())
        except (json.JSONDecodeError, ValueError):
            scores["analysis_created"] = 0.0
            scores["correct_bug_id"] = 0.0
            scores["hypothesis_quality"] = 0.0
            scores["has_fix"] = 0.0
            return scores

        scores["analysis_created"] = 1.0
        scores["correct_bug_id"] = 1.0 if analysis.get("bug_id") == 4521 else 0.0

        hypothesis = str(analysis.get("root_cause_hypothesis", "")).lower()
        keywords = [
            "special", "character", "encod", "escap",
            "sanitiz", "url.?encod", "percent.?encod",
        ]
        matches = sum(
            1 for k in keywords if re.search(k, hypothesis)
        )
        if matches >= 2:
            scores["hypothesis_quality"] = 1.0
        elif matches >= 1:
            scores["hypothesis_quality"] = 0.5
        else:
            scores["hypothesis_quality"] = 0.0

        fix = str(analysis.get("suggested_fix", ""))
        scores["has_fix"] = 1.0 if len(fix) > 20 else 0.0
    else:
        scores["analysis_created"] = 0.0
        scores["correct_bug_id"] = 0.0
        scores["hypothesis_quality"] = 0.0
        scores["has_fix"] = 0.0

    return scores
```

## LLM Judge Rubric

### Criterion 1: Root Cause Analysis (Weight: 35%)

**Score 1.0**: Hypothesis correctly identifies the core issue — insufficient handling of special characters (e.g., `@`, `!`) in password processing, likely due to missing URL encoding, improper SQL escaping, or unescaped characters in request body serialization. The explanation is specific and technically accurate.
**Score 0.75**: Hypothesis identifies character handling as the problem area but lacks specificity about the exact mechanism.
**Score 0.5**: Hypothesis is vaguely related to input handling but doesn't clearly pinpoint special character encoding.
**Score 0.25**: Hypothesis is tangentially related or overly generic ("input validation issue").
**Score 0.0**: No hypothesis or completely wrong diagnosis.

### Criterion 2: Test Script Quality (Weight: 35%)

**Score 1.0**: Test script is well-structured Python that clearly demonstrates the bug. Uses a mock/simulated login endpoint, tests both working (normal password) and failing (special character password) cases, and includes meaningful assertions. Script can be executed.
**Score 0.75**: Test script demonstrates the scenario with reasonable structure. May be missing the comparison between normal and special-character passwords.
**Score 0.5**: Test script exists and is valid Python but is simplistic — perhaps just a function with the password string, without meaningful test logic.
**Score 0.25**: Test script exists but has significant issues (syntax errors, no actual test logic).
**Score 0.0**: No test script or script is empty.

### Criterion 3: Fix Suggestion (Weight: 30%)

**Score 1.0**: Suggested fix is specific and actionable — e.g., "use proper URL encoding for password before sending", "use parameterized queries", or "ensure the HTTP client properly escapes request body". Includes code snippet or library recommendation.
**Score 0.75**: Fix suggestion is reasonable and actionable but less specific.
**Score 0.5**: Fix suggestion is correct direction but too vague to implement.
**Score 0.25**: Fix suggestion is generic ("fix the bug", "validate input").
**Score 0.0**: No fix suggested.
