---
id: rli_010_latex_formatting
name: "RLI: LaTeX Formatting"
category: document_formatting
grading_type: hybrid
timeout_seconds: 600
workspace_files:
  - source: "rli/public_010/3d printer.docx"
    dest: "inputs/3d printer.docx"
  - source: rli/public_010/E1.pdf
    dest: inputs/E1.pdf
  - source: rli/public_010/Figures/
    dest: inputs/Figures/
grading_weights:
  automated: 0.4
  llm_judge: 0.6
---

## Prompt

This is a technical paper on control systems for a 3D printing robot. The paper covers mathematical modeling of DC motors controlling the X, Y, and Z axes of a 3D printer, designing lead compensators for feedback control, and simulating the system in MATLAB/Simulink to print various geometries. We need everything formatted into IEEE conference LaTeX format with proper equation numbering and figure integration.

### Requirements

- Put everything into IEEE conference LaTeX format (two-column layout)
- Label all the math as equations (1), (2), (3), etc.
- Add captions for all figures - if the content is clear from context, write descriptive captions; otherwise write dummy captions as placeholders (client will fill in final captions later)
- Integrate figures referenced in the project outline document (some input figures have duplicates, use the project outline document for reference on which figures to include).
- Include the MATLAB code with proper formatting
- Format the mathematical derivations and transfer functions properly

### Provided material

- `inputs/3d printer.docx` - Project outline including introduction, methodology, and structure for the paper on 3D printer control systems
- `inputs/E1.pdf` - Handwritten mathematical derivations for DC motor modeling, transfer functions, and control system equations
- `inputs/Figures/` - Complete set of simulation results and technical diagrams (69 files total)

### Deliverables

- Complete LaTeX project including:
  - Main LaTeX source file with all content formatted
  - IEEE conference template files
  - All the figures and images used in the paper
  - Compiled PDF output
- Final PDF in IEEE conference format (approximately 14 pages, two-column layout)

## Expected Behavior

The agent should:

1. Read the project outline document (.docx) to understand the paper structure and content
2. Read the handwritten mathematical derivations (E1.pdf) to extract equations
3. Survey the Figures/ directory to understand available diagrams and simulation results
4. Set up an IEEE conference LaTeX template with two-column layout
5. Transcribe all content into LaTeX, including:
   - Introduction, methodology, and other sections from the outline
   - Mathematical equations with proper numbering (1), (2), (3)...
   - Transfer functions and control system derivations
   - MATLAB code blocks with proper formatting
6. Integrate relevant figures with captions (descriptive where content is clear, placeholder otherwise)
7. Handle duplicate figures by referencing the project outline for which to include
8. Compile the LaTeX project to produce a final PDF

This is a replica of RLI public_010 (LaTeX Formatting, $70 budget).

## Grading Criteria

- [ ] Main .tex file exists with IEEE conference formatting
- [ ] Two-column layout used
- [ ] Equations are numbered sequentially (1), (2), (3)...
- [ ] Figures are integrated with captions
- [ ] MATLAB code is included with proper formatting
- [ ] Mathematical derivations and transfer functions are properly typeset
- [ ] IEEE template files included
- [ ] Compiled PDF output exists
- [ ] PDF is approximately 14 pages
- [ ] Content matches the project outline structure

## Automated Checks

```python
def grade(transcript: list, workspace_path: str) -> dict:
    """Grade the LaTeX Formatting task."""
    from pathlib import Path
    import re

    scores = {}
    workspace = Path(workspace_path)

    # Check for .tex file
    tex_files = list(workspace.rglob("*.tex"))
    tex_files = [
        f for f in tex_files
        if "inputs" not in f.relative_to(workspace).parts
    ]
    scores["tex_exists"] = 1.0 if tex_files else 0.0

    # Check for compiled PDF
    pdf_files = list(workspace.rglob("*.pdf"))
    pdf_files = [
        f for f in pdf_files
        if "inputs" not in f.relative_to(workspace).parts
    ]
    scores["pdf_output"] = 1.0 if pdf_files else 0.0

    # Analyze LaTeX content
    tex_content = ""
    for f in tex_files:
        try:
            tex_content += f.read_text(errors="replace")
        except Exception:
            pass

    # Check for IEEE format
    has_ieee = bool(
        re.search(
            r"""(?ix)
            IEEEtran | ieee.?conf | ieee.?journal
            | \\documentclass .* IEEE
            """,
            tex_content,
        )
    )
    scores["ieee_format"] = 1.0 if has_ieee else 0.0

    # Check for two-column layout
    has_twocol = bool(
        re.search(
            r"""(?ix)
            twocolumn | two.?column
            """,
            tex_content,
        )
    )
    scores["two_column"] = 1.0 if has_twocol else 0.0

    # Check for numbered equations
    equation_envs = len(
        re.findall(
            r"""(?x)
            \\begin\{equation\} | \\begin\{align\}
            """,
            tex_content,
        )
    )
    scores["equations_present"] = (
        1.0 if equation_envs >= 5
        else 0.5 if equation_envs >= 2
        else 0.0
    )

    # Check for figures
    figure_refs = len(
        re.findall(
            r"""(?x)
            \\includegraphics
            """,
            tex_content,
        )
    )
    scores["figures_included"] = (
        1.0 if figure_refs >= 10
        else 0.5 if figure_refs >= 3
        else 0.0
    )

    # Check for figure captions
    caption_count = len(
        re.findall(
            r"""(?x)
            \\caption\{
            """,
            tex_content,
        )
    )
    scores["figure_captions"] = (
        1.0 if caption_count >= 10
        else 0.5 if caption_count >= 3
        else 0.0
    )

    # Check for MATLAB code formatting
    has_code = bool(
        re.search(
            r"""(?ix)
            \\begin\{lstlisting\} | \\begin\{verbatim\}
            | \\begin\{minted\} | \\texttt
            | matlab | lstset
            """,
            tex_content,
        )
    )
    scores["code_formatting"] = 1.0 if has_code else 0.0

    return scores
```

## LLM Judge Rubric

### Criterion 1: Content Completeness (Weight: 30%)

**Score 1.0**: The major sections from the project outline are present (introduction, methodology, mathematical modeling, controller design, simulation results, MATLAB code). Handwritten equations from E1.pdf are transcribed. Minor omissions or transcription errors are acceptable.
**Score 0.0**: Most sections from the outline are missing, or no content from the source materials is included.

### Criterion 2: LaTeX and IEEE Formatting (Weight: 30%)

**Score 1.0**: The document uses IEEE conference format with two-column layout. Equations are numbered and typeset in LaTeX math environments. Figures have captions. MATLAB code is formatted in a code environment (lstlisting, verbatim, or similar). Minor formatting issues are acceptable.
**Score 0.0**: No LaTeX formatting applied, or the .tex file is non-functional and does not resemble IEEE format.

### Criterion 3: Figure Integration (Weight: 20%)

**Score 1.0**: Multiple figures from the Figures/ directory are integrated into the document with captions (descriptive or placeholder). Figures are referenced in the text. A few missing or misplaced figures are acceptable.
**Score 0.0**: No figures included from the provided directory, or figures lack any captions.

### Criterion 4: Compiled Output Quality (Weight: 20%)

**Score 1.0**: A compiled PDF exists and renders with equations, figures, and code blocks visible. The document has a professional appearance approximating IEEE conference standards. Minor compilation warnings or visual imperfections are acceptable.
**Score 0.0**: No compiled PDF produced, or the PDF is completely broken with most content missing or unreadable.
