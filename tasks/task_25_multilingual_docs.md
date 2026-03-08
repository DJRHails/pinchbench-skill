---
id: task_25_multilingual_docs
name: Multi-Language Documentation Generator
category: writing
grading_type: hybrid
timeout_seconds: 300
workspace_files:
  - source: payment_api.py
    dest: payment_api.py
---

## Prompt

Generate API documentation from /workspace/payment_api.py in 3 languages: English, Spanish, and Japanese.

For each language:
1. Extract all methods and their signatures
2. Translate docstrings naturally (not literal word-for-word translation)
3. Provide code examples
4. Include request/response formats
5. List error codes and meanings

Write to /workspace/api_docs_en.md, /workspace/api_docs_es.md, and /workspace/api_docs_ja.md.

Also create /workspace/docs_summary.json:
```json
{
  "source_file": "payment_api.py",
  "languages": ["en", "es", "ja"],
  "methods_documented": 2,
  "generated_files": ["api_docs_en.md", "api_docs_es.md", "api_docs_ja.md"]
}
```

## Expected Behavior

The agent should:

1. Read the Python source file containing a `PaymentAPI` class with two methods
2. Generate three separate markdown documentation files, one per language
3. Each doc should cover both `create_payment` and `refund_payment` methods
4. Translations should be natural and idiomatic, not machine-literal
5. Spanish docs should contain Spanish words (pago, transaccion, cliente, etc.)
6. Japanese docs should contain Japanese characters (Hiragana, Katakana, or Kanji)
7. Create a summary JSON with metadata about the generation

## Grading Criteria

- [ ] English documentation file created
- [ ] Spanish documentation file created
- [ ] Japanese documentation file created
- [ ] Summary JSON created with correct structure
- [ ] All docs reference both API methods
- [ ] Spanish doc contains Spanish language text
- [ ] Japanese doc contains Japanese characters
- [ ] Docs are substantive (not just stubs)

## Automated Checks

```python
def grade(transcript: list, workspace_path: str) -> dict:
    from pathlib import Path
    import json
    import re

    scores = {}
    workspace = Path(workspace_path)

    # Check summary JSON
    summary_path = workspace / "docs_summary.json"
    if summary_path.exists():
        try:
            summary = json.loads(summary_path.read_text())
            langs = summary.get("languages", [])
            scores["summary_created"] = 1.0 if len(langs) == 3 else 0.5
        except (json.JSONDecodeError, ValueError):
            scores["summary_created"] = 0.0
    else:
        scores["summary_created"] = 0.0

    # Check each language doc
    for lang, key in [("en", "english_doc"), ("es", "spanish_doc"), ("ja", "japanese_doc")]:
        doc_path = workspace / f"api_docs_{lang}.md"
        if doc_path.exists():
            content = doc_path.read_text()
            if len(content) > 500:
                scores[key] = 1.0
            elif len(content) > 100:
                scores[key] = 0.5
            else:
                scores[key] = 0.25
        else:
            scores[key] = 0.0

    # Check method coverage across docs
    methods_found = 0
    for lang in ["en", "es", "ja"]:
        doc_path = workspace / f"api_docs_{lang}.md"
        if doc_path.exists():
            content = doc_path.read_text().lower()
            if "create_payment" in content or "payment" in content:
                methods_found += 1
    scores["methods_covered"] = 1.0 if methods_found >= 3 else (
        0.5 if methods_found >= 1 else 0.0
    )

    # Check Spanish has Spanish words
    es_path = workspace / "api_docs_es.md"
    if es_path.exists():
        es_content = es_path.read_text().lower()
        spanish_words = [
            "pago", "transacci", "cliente", "cantidad", "moneda",
            "crear", "reembolso", "monto",
        ]
        matches = sum(1 for w in spanish_words if w in es_content)
        scores["spanish_language"] = 1.0 if matches >= 3 else (
            0.5 if matches >= 1 else 0.0
        )
    else:
        scores["spanish_language"] = 0.0

    # Check Japanese has Japanese characters
    ja_path = workspace / "api_docs_ja.md"
    if ja_path.exists():
        ja_content = ja_path.read_text()
        has_japanese = any(
            "\u3040" <= c <= "\u30ff" or "\u4e00" <= c <= "\u9faf"
            for c in ja_content
        )
        scores["japanese_characters"] = 1.0 if has_japanese else 0.0
    else:
        scores["japanese_characters"] = 0.0

    return scores
```

## LLM Judge Rubric

### Criterion 1: Translation Quality (Weight: 40%)

**Score 1.0**: All three language versions read naturally and idiomatically. Spanish uses proper technical terminology (pago, transaccion, solicitud). Japanese uses appropriate technical katakana and natural sentence structure. No machine-translation artifacts.
**Score 0.75**: Translations are mostly natural with minor awkward phrasings. Technical terms are correctly translated in most cases.
**Score 0.5**: Translations are understandable but clearly literal or stilted. Some technical terms are incorrectly translated or left untranslated.
**Score 0.25**: Translations are poor quality — mostly literal word substitution or largely English with scattered translated words.
**Score 0.0**: No meaningful translation present or files missing.

### Criterion 2: Documentation Completeness (Weight: 30%)

**Score 1.0**: Each language doc covers both methods with signatures, parameter descriptions, return types, error conditions, and code examples. Documentation is professional-grade.
**Score 0.75**: Both methods documented with most details. Minor omissions in examples or error handling.
**Score 0.5**: Both methods mentioned but documentation is thin — missing code examples or parameter details.
**Score 0.25**: Only one method documented or documentation is superficial stubs.
**Score 0.0**: No meaningful documentation content.

### Criterion 3: Consistency Across Languages (Weight: 20%)

**Score 1.0**: All three versions cover the same content at the same depth. Structure and formatting are consistent. A reader of any version gets equivalent information.
**Score 0.75**: Mostly consistent with minor variations in depth or structure across languages.
**Score 0.5**: Notable inconsistency — one language has significantly more or less content than others.
**Score 0.25**: Large disparities between language versions.
**Score 0.0**: Only one language produced or versions are incomparable.

### Criterion 4: Code Examples (Weight: 10%)

**Score 1.0**: Each language doc includes working code examples showing how to call both API methods with realistic parameters.
**Score 0.75**: Code examples present for most methods in most languages.
**Score 0.5**: Some code examples present but incomplete or only in one language.
**Score 0.25**: Minimal code examples.
**Score 0.0**: No code examples.
