#!/usr/bin/env python3
"""Generate PinchBench task files from the GAIA benchmark dataset.

Requires a HuggingFace token with access to the gated dataset
``gaia-benchmark/GAIA``.  Set ``HF_TOKEN`` in the environment or
pass ``--token``.

Usage::

    # Generate all 165 validation tasks
    HF_TOKEN=hf_... python scripts/generate_gaia_tasks.py

    # Generate only Level 1 tasks
    HF_TOKEN=hf_... python scripts/generate_gaia_tasks.py --levels 1

    # Dry-run: show what would be generated
    HF_TOKEN=hf_... python scripts/generate_gaia_tasks.py --dry-run
"""

from __future__ import annotations

import argparse
import os
import re
import shutil
import textwrap
from pathlib import Path

SKILL_DIR = Path(__file__).resolve().parent.parent
TASKS_DIR = SKILL_DIR / "tasks" / "gaia"
ASSETS_DIR = SKILL_DIR / "assets" / "gaia"

DATASET_ID = "gaia-benchmark/GAIA"
DATASET_CONFIG = "2023_all"
DATASET_SPLIT = "validation"


def _sanitize_id(task_id: str) -> str:
    """Convert a GAIA UUID into a filesystem-safe short id."""
    return task_id[:12].replace("-", "_")


def _escape_yaml_string(s: str) -> str:
    """Escape a string for YAML double-quoted context."""
    return s.replace("\\", "\\\\").replace('"', '\\"')


def _build_task_markdown(row: dict) -> str:
    """Build a PinchBench task markdown file from a GAIA row."""
    task_id = row["task_id"]
    short_id = _sanitize_id(task_id)
    level = row["Level"]
    question = row["Question"]
    answer = row["Final answer"]
    file_name = row.get("file_name", "")
    metadata = row.get("Annotator Metadata", {})

    pinchbench_id = f"gaia_L{level}_{short_id}"

    workspace_files_yaml = ""
    file_ref = ""
    if file_name:
        workspace_files_yaml = textwrap.dedent(f"""\
            workspace_files:
              - source: gaia/{task_id}/{file_name}
                dest: inputs/{file_name}
        """).rstrip()
        file_ref = f"\n\nThe file `inputs/{file_name}` is provided."
    else:
        workspace_files_yaml = "workspace_files: []"

    # Extract annotator steps if available
    steps = ""
    if isinstance(metadata, dict) and metadata.get("Steps"):
        steps = metadata["Steps"]

    # Escape the answer for embedding in Python string
    answer_escaped = answer.replace("\\", "\\\\").replace("'", "\\'")

    # Build the expected answer description for the rubric
    answer_preview = answer[:80]
    if len(answer) > 80:
        answer_preview += "..."

    return textwrap.dedent(f"""\
        ---
        id: {pinchbench_id}
        name: "GAIA L{level}: {_escape_yaml_string(question[:60])}"
        category: question_answering
        grading_type: automated
        timeout_seconds: 300
        {workspace_files_yaml}
        ---

        ## Prompt

        {question}{file_ref}

        Provide your final answer as a single value — no explanation,
        no extra text.  Write it on a line that starts with
        ``FINAL ANSWER:``.

        ## Expected Behavior

        The agent should research the question (using web search, file
        analysis, code execution, or other tools as needed) and return
        the exact answer.

        This is a replica of GAIA benchmark validation question
        ``{task_id}`` (Level {level}).

        ## Grading Criteria

        - [ ] Agent provides a final answer
        - [ ] Answer matches the expected value exactly

        ## Automated Checks

        ```python
        import re


        def grade(transcript: list, workspace_path: str) -> dict:
            \\"\\"\\"Grade by exact-match against the GAIA expected answer.\\"\\"\\"
            expected = '{answer_escaped}'

            # Extract the last assistant text
            last_text = ""
            for event in transcript:
                if event.get("type") != "message":
                    continue
                msg = event.get("message", {{}})
                if msg.get("role") != "assistant":
                    continue
                for block in msg.get("content", []):
                    if block.get("type") in ("text", "toolResult"):
                        last_text = block.get("text", "")

            # Look for FINAL ANSWER: pattern
            match = re.search(
                r\\"\\"\\"(?ixm)
                ^
                \\\\s*
                FINAL \\\\s+ ANSWER
                \\\\s* : \\\\s*
                (?P<answer> .+? )
                \\\\s*
                $
                \\"\\"\\",
                last_text,
            )
            agent_answer = match.group("answer").strip() if match else last_text.strip()

            # Normalize for comparison
            norm_expected = _normalize(expected)
            norm_agent = _normalize(agent_answer)

            exact = 1.0 if norm_expected == norm_agent else 0.0
            contains = 1.0 if norm_expected in norm_agent else 0.0
            has_answer = 1.0 if agent_answer else 0.0

            return {{
                "exact_match": exact,
                "contains_answer": contains,
                "has_answer": has_answer,
            }}


        def _normalize(s: str) -> str:
            \\"\\"\\"Normalize whitespace, case, and punctuation for comparison.\\"\\"\\"
            s = s.lower().strip()
            s = re.sub(r"\\\\s+", " ", s)
            s = s.strip(".")
            return s
        ```
    """)


def _download_file(
    row: dict,
    *,
    hf_token: str,
) -> Path | None:
    """Download an attached file from the GAIA dataset."""
    file_name = row.get("file_name", "")
    file_path = row.get("file_path", "")
    if not file_name or not file_path:
        return None

    from huggingface_hub import hf_hub_download

    task_id = row["task_id"]
    dest_dir = ASSETS_DIR / task_id
    dest_dir.mkdir(parents=True, exist_ok=True)
    dest_file = dest_dir / file_name

    if dest_file.exists():
        return dest_file

    downloaded = hf_hub_download(
        repo_id=DATASET_ID,
        filename=file_path,
        repo_type="dataset",
        token=hf_token,
    )
    shutil.copy2(downloaded, dest_file)
    return dest_file


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Generate PinchBench tasks from GAIA benchmark",
    )
    parser.add_argument(
        "--token",
        default=os.environ.get("HF_TOKEN", ""),
        help="HuggingFace API token (default: $HF_TOKEN)",
    )
    parser.add_argument(
        "--levels",
        nargs="+",
        type=str,
        default=["1", "2", "3"],
        help="GAIA levels to include (default: all)",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print task IDs without writing files",
    )
    parser.add_argument(
        "--skip-files",
        action="store_true",
        help="Skip downloading attached files",
    )
    args = parser.parse_args()

    if not args.token:
        parser.error(
            "HuggingFace token required. "
            "Set HF_TOKEN or pass --token."
        )

    from datasets import load_dataset

    print(f"Loading {DATASET_ID} ({DATASET_CONFIG}/{DATASET_SPLIT})...")
    ds = load_dataset(
        DATASET_ID,
        DATASET_CONFIG,
        split=DATASET_SPLIT,
        token=args.token,
    )
    print(f"Loaded {len(ds)} questions")

    TASKS_DIR.mkdir(parents=True, exist_ok=True)
    ASSETS_DIR.mkdir(parents=True, exist_ok=True)

    written = 0
    skipped = 0
    files_downloaded = 0

    for row in ds:
        level = str(row["Level"])
        if level not in args.levels:
            skipped += 1
            continue

        task_id = row["task_id"]
        short_id = _sanitize_id(task_id)
        pinchbench_id = f"gaia_L{level}_{short_id}"

        if args.dry_run:
            file_info = f" [+file: {row['file_name']}]" if row.get("file_name") else ""
            print(f"  {pinchbench_id}{file_info}")
            written += 1
            continue

        # Write task file
        task_path = TASKS_DIR / f"{pinchbench_id}.md"
        task_path.write_text(
            _build_task_markdown(row),
            encoding="utf-8",
        )

        # Download attached file
        if not args.skip_files and row.get("file_name"):
            try:
                result = _download_file(row, hf_token=args.token)
                if result:
                    files_downloaded += 1
            except Exception as exc:
                print(f"  WARNING: failed to download file for {task_id}: {exc}")

        written += 1

    print(
        f"\nDone: {written} tasks written, "
        f"{skipped} skipped, "
        f"{files_downloaded} files downloaded"
    )
    print(f"Tasks: {TASKS_DIR}")
    print(f"Assets: {ASSETS_DIR}")


if __name__ == "__main__":
    main()
