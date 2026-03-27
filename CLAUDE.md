# CLAUDE.md — Open-Genealogy (Project Level)

> This file provides project-specific context for Claude Code sessions.
> It works alongside your laptop-wide `~/.claude/CLAUDE.md` which holds
> your personal identity, preferences, and cross-project conventions.
> Together they form an interlocking pair: personal context flows down
> from `~/.claude/CLAUDE.md`; project context lives here.

## Project Overview

**Open-Genealogy** is a toolkit of AI prompts and utilities for genealogical
research, designed to follow the Genealogical Proof Standard (GPS). Created by
Steve Little ([@DigitalArchivst](https://github.com/DigitalArchivst)).

License: Creative Commons BY-NC-SA 4.0

## Repository Structure

```
research/           # GPS-based research methodology prompts
transcription/      # Diplomatic transcription / OCR-HTR prompts
image-analysis/     # Forensic historical photograph analysis
hebrew-headstones/  # Jewish cemetery headstone analysis with gematria
photo-restoration/  # Historical photograph restoration workflows
writing-tools/      # Narrative, editing, fact extraction, language advising
assistants/         # Complete AI personas for ongoing work
scripts/            # Python audio transcription utilities
gpt-configs/       # OpenAI Custom GPT specifications
benchmark/          # AI model evaluation framework for GPS tasks
media/              # Supporting audio/media files
```

## Conventions

### Naming & Versioning

- Prompts follow `[descriptive-name]-v[N].md` (e.g., `research-assistant-v8.md`)
- Compact/compressed variants: `[name]-v[N]-compact.md` or `[name]-v[N]-compressed.md`
- Status labels in INDEX.md: **recommended**, **stable**, **previous**, **legacy**, **reference**
- Legacy versions live in `[category]/archive/` subdirectories

### File Formats

- All prompts are Markdown (`.md`)
- PDFs and DOCX are gitignored except deliberate deliverables
- Internal planning docs (`*-gap-analysis.md`, `*-pdr.md`) are gitignored

### Documentation Hierarchy

- `README.md` — Quick-start navigation
- `INDEX.md` — Complete catalog with status indicators
- `ANNOTATED-INDEX.md` — Detailed ~125-word descriptions per section
- `GETTING-STARTED.md` — Comprehensive onboarding guide
- `TOUR-REPORT.md` — Guided walkthrough

## Domain Knowledge

### Genealogical Proof Standard (GPS)

This project is methodologically aligned with:
- Mills, *Evidence Explained*, 4th ed. (2024)
- BCG, *Genealogy Standards*, 2nd ed. revised (2021)

Key concepts embedded in prompts:
- **Source classification**: Original / Derivative / Authored
- **Information classification**: Primary / Secondary
- **Evidence classification**: Direct / Indirect / Negative
- **Anti-fabrication**: Never invent sources, citations, or facts
- **Epistemic transparency**: Separate what sources state from inference from uncertainty

### Terminology Precision

Use GPS-correct vocabulary in all contributions:
- "Source" not "Primary Source" (sources are classified, not inherently primary)
- "Evidence" not "Primary Evidence"
- "Information" has a specific GPS meaning distinct from common usage

## Working in This Repo

- When editing prompts, preserve the existing section structure and guardrails
- Prompt-injection resistance is a feature, not boilerplate — do not remove it
- Version bumps (v8 → v9) represent significant methodology changes
- Compact variants must stay functionally equivalent to their full versions
- The benchmark framework evaluates models against GPS methodology — maintain objectivity

## Interlocking with ~/.claude/CLAUDE.md

This project-level file handles *what* (domain, structure, standards).
Your laptop-wide `~/.claude/CLAUDE.md` should handle *who* and *how*:

- Your identity and role (researcher, developer, author)
- Communication preferences (tone, verbosity, format)
- Cross-project conventions (git workflow, code style, commit style)
- Tool preferences and environment details

Claude Code merges both files automatically — no duplication needed.
If a convention is project-specific, put it here. If it's personal, put it there.
