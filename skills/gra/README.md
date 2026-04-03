# Genealogical Research Assistant — Claude Code Skill

A research assistant designed to follow GPS methodology, the
Three-Layer Evidence Model, and strict anti-fabrication
principles.

**This assistant never fabricates sources, citations, people, dates,
places, or events. When evidence is insufficient, it says so.**

## Installation

### With Claude Code

1. Copy this folder to `~/.claude/skills/gra/`
2. Restart Claude Code
3. Start researching: "Help me analyze this census record" or
   "Classify this source for me"

### Without Claude Code

The prompt files work in any LLM:

| File | Size | Use For |
| ---- | ---- | ------- |
| `SKILL.md` | ~8KB | System prompt for GPTs, Gems, Projects |
| `research-assistant-v8.5-full.md` | 60KB | Full methodology for any LLM chat |
| `companion-reference.md` | 18KB | Upload as knowledge file alongside compact |

## What You Can Say

```text
"Analyze this death certificate for me."

"I found two census records that disagree on my grandmother's
birth year. Help me resolve the conflict."

"Is this an original or derivative source?"

"Help me write a proof summary for the identity of William
Smith in the 1850 census."

"What records should I look for next? I'm stuck on my
great-grandfather in 1880s Virginia."
```

## What This Is Not

This is not a database. It does not search records, connect to
online trees, or access subscription sites. It analyzes what you
provide — documents, transcriptions, research questions.

It does not authenticate documents for legal purposes, provide
legal advice, or guarantee accuracy. It does not replace a
genealogist. It helps you become a better one.

## Three Versions, One Methodology

| Version | File | Size | Best For |
| ------- | ---- | ---- | -------- |
| Compact | `SKILL.md` | ~8KB | Daily use, skill prompt |
| Full | `research-assistant-v8.5-full.md` | 60KB | Deep methodology |
| Reference | `companion-reference.md` | 18KB | Templates, schemas |

The compact version captures the core GPS methodology. The full
version adds detailed protocols for user calibration, document
analysis, structured output, regression awareness, and more. The
companion reference provides the templates and decision trees
cut from the compact for space.

In Claude Code, all three files are available. The compact loads
as the skill prompt; the full version and reference are consulted
as needed.

## The Methodology

The Genealogical Proof Standard (GPS) has five elements:

1. **Reasonably exhaustive research** — search proportional to
   complexity
2. **Complete citations** — who, what, when, where, where-within
3. **Thorough analysis** — classify every source, information
   type, and evidence type
4. **Resolution of conflicts** — preponderance hierarchy, not
   cherry-picking
5. **Written conclusion** — proof statement, summary, or argument

The Three-Layer Evidence Model classifies:

- **Sources**: Original, Derivative, or Authored
- **Information**: Primary, Secondary, or Indeterminate
- **Evidence**: Direct, Indirect, or Negative

Never "primary source." Never "secondary source." Those are
library science terms. In genealogy, we say "original source
containing primary information that serves as direct evidence."

## Development History

18 months of iterative development (2024-2026):

- v6.1 (Dec 2024) — Foundation
- v7 (Jan 2025) — Enhanced evidence framework
- v8 (Jan 2026) — Synthesized from 5 beta candidates
- v8.5 (Jan 2026) — 12 new features via expert council
- v8.5c (Feb 2026) — 87% compression for multi-platform use

## License

[Creative Commons BY-NC-SA 4.0](../../LICENSE)

## Author

**Steve Little** ([@DigitalArchivst](https://github.com/DigitalArchivst))
AI Program Director, National Genealogical Society

---

*Part of the [Open-Genealogy](https://github.com/DigitalArchivst/Open-Genealogy) toolkit.*
