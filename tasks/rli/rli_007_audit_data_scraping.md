---
id: rli_007_audit_data_scraping
name: "RLI: Security Audit Data Scraping"
category: data_extraction
grading_type: hybrid
timeout_seconds: 600
workspace_files:
  - source: rli/public_007/Audit_Work_PDFs/ackee-blockchain-aave-umbrella-report.pdf
    dest: inputs/Audit_Work_PDFs/ackee-blockchain-aave-umbrella-report.pdf
  - source: rli/public_007/Audit_Work_PDFs/EverSOL SP Audit.pdf
    dest: inputs/Audit_Work_PDFs/EverSOL SP Audit.pdf
  - source: rli/public_007/Audit_Work_PDFs/ackee-good-ghosting-core-files-audit.pdf
    dest: inputs/Audit_Work_PDFs/ackee-good-ghosting-core-files-audit.pdf
grading_weights:
  automated: 0.4
  llm_judge: 0.6
---

## Prompt

Extract relevant data points from each provided report, particularly structured findings, and output them into a specified format.

### Data Extraction

From each PDF report, parse and extract structured information based on the following format:
- Finding Number
- Title (e.g. Requirements Violation, Documentation Mismatch)
- Status
- Severity
- Impact
- Likelihood
- Description
- Recommendation
- Repository URL
- Commit ID

If some of these fields are not present in a given report, leave them out. If other fields are present in a report, include those as well (e.g., "Type" or "Target").

The PDF reports are in `inputs/Audit_Work_PDFs/`.

### Deliverables

Final extracted data in structured text format, containing all findings (one file per report).

## Expected Behavior

The agent should:

1. Discover all PDF files in the `inputs/Audit_Work_PDFs/` directory
2. Parse each PDF to extract text content
3. Identify and extract structured findings from each report
4. For each finding, extract the specified fields (Finding Number, Title, Status, Severity, Impact, Likelihood, Description, Recommendation, Repository URL, Commit ID)
5. Handle missing fields gracefully (omit rather than include empty)
6. Include any additional fields present in the report
7. Output one structured text file per report

This is a replica of RLI public_007 (Security Audit Data Scraping, $60 budget).

## Grading Criteria

- [ ] All PDF files in the input directory are processed
- [ ] Output files are created (one per report)
- [ ] Findings are correctly identified and numbered
- [ ] Required fields are extracted when present (Title, Severity, Description, Recommendation)
- [ ] Missing fields are omitted rather than filled with placeholders
- [ ] Additional fields present in reports are captured
- [ ] Output format is consistent and structured
- [ ] Data accurately reflects the PDF content

## Automated Checks

```python
def grade(transcript: list, workspace_path: str) -> dict:
    """Grade the audit data scraping task."""
    from pathlib import Path
    import re

    scores = {}
    workspace = Path(workspace_path)

    # Count input PDFs
    pdf_dir = workspace / "inputs" / "Audit_Work_PDFs"
    input_pdfs = list(pdf_dir.glob("*.pdf")) if pdf_dir.exists() else []
    num_pdfs = len(input_pdfs)

    # Find output files (not in inputs/)
    output_files = []
    for f in workspace.rglob("*"):
        if f.is_file() and "inputs" not in f.relative_to(workspace).parts:
            if f.suffix in (".txt", ".md", ".json", ".csv", ".yaml", ".yml"):
                output_files.append(f)

    # Check that output files exist
    scores["outputs_created"] = (
        min(1.0, len(output_files) / max(1, num_pdfs))
        if output_files
        else 0.0
    )

    # Check output content quality
    all_output = ""
    for f in output_files:
        all_output += f.read_text(errors="replace")

    # Check for finding-related fields
    field_patterns = {
        "finding_number": r"""(?ix) finding.?\s*(?:number|#|\d)""",
        "title": r"""(?ix) title\s*[:=]""",
        "severity": r"""(?ix) severity\s*[:=]""",
        "description": r"""(?ix) description\s*[:=]""",
        "recommendation": r"""(?ix) recommendation\s*[:=]""",
    }

    fields_found = 0
    for field, pattern in field_patterns.items():
        if re.search(pattern, all_output):
            fields_found += 1

    scores["field_extraction"] = fields_found / len(field_patterns)

    # Check for structured format (consistent structure)
    has_structure = bool(
        re.search(
            r"""(?ix)
            (?:finding | issue | vulnerability) \s* [\#\d]
            """,
            all_output,
        )
    )
    scores["structured_format"] = 1.0 if has_structure else 0.0

    return scores
```

## LLM Judge Rubric

### Criterion 1: Extraction Completeness (Weight: 35%)

**Score 1.0**: All PDFs are processed and findings are extracted with the key available fields. Minor omissions in some fields or a few missed findings are acceptable.
**Score 0.0**: No meaningful extraction performed, or most reports are skipped entirely.

### Criterion 2: Field Accuracy (Weight: 30%)

**Score 1.0**: Extracted fields generally match the PDF content. Severity levels, descriptions, and recommendations are correctly captured with at most minor errors. No fabricated data.
**Score 0.0**: Data is largely fabricated, or most fields are inaccurately extracted.

### Criterion 3: Output Format (Weight: 20%)

**Score 1.0**: Output files use a structured format (e.g., consistent headings, key-value pairs) and one file per report is produced. Minor inconsistencies between files are acceptable.
**Score 0.0**: No usable structured output, or output is a single undifferentiated dump.

### Criterion 4: Handling Edge Cases (Weight: 15%)

**Score 1.0**: Missing fields are omitted rather than filled with placeholders. Different report formats are handled without crashing. Additional fields present in reports are captured where feasible.
**Score 0.0**: Cannot handle variations in report format, or crashes and produces errors on most inputs.
