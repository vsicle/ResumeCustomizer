# AGENTS.md

## PROJECT MISSION
Build a python-based "Resume Compiler" that dynamically generates single-page, strictly formatted PDFs from a master JSON data source and a target Job Description (JD).

## ARCHITECTURE STACK
1. **Data Layer:** `data/master_resume.json` (The single source of truth).
2. **Logic Layer:** Python 3.12+ (Script `builder.py`).
   - Uses `jinja2` for templating.
   - Uses `spacy` or `nltk` for keyword extraction from Job Descriptions.
   - Implements a "Space Budget" algorithm to ensure 1-page output.
3. **Presentation Layer:** LaTeX (`templates/resume.tex`).
   - Uses `pdflatex` for rendering.
   - strict strict layout control (no flowable text that breaks pages).

## CORE RULES (STRICT)
1. **Formatting:** The output PDF must NEVER exceed 1 page.
2. **Templating:** Use Jinja2 delimiters in LaTeX: `\BLOCK{ variable }`.
3. **Dependencies:** No heavy frameworks. Use standard libraries where possible.
4. **Output:** Code must be modular. Separate the "scorer" logic from the "renderer" logic.

## DATA SCHEMA
The `master_resume.json` must follow this schema structure:
- `basics`: { name, contact, education }
- `skills`: { languages, tools, frameworks }
- `experience`: [ { company, role, dates, bullets: [], tags: [] } ]
- `projects`: [ { name, tech_stack, bullets: [], tags: [] } ]