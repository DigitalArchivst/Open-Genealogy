# Genealogical Research Assistant — Agent Skill

A research assistant designed to follow GPS methodology, the
Three-Layer Evidence Model, and strict anti-fabrication
principles.

**This assistant never fabricates sources, citations, people,
dates, places, or events. When evidence is insufficient, it
says so.**

This skill follows the open
[Agent Skills](https://agentskills.io) standard and may work
in other compatible tools (Cursor, VS Code, Codex, Gemini CLI,
and others).

The install ZIP is a runtime package: it contains the skill,
license, app metadata, and reference files needed by an agent.
Developer tests and fixtures stay in the repository source tree.

## Compatibility

The GRA materials are designed to be portable across agent and
chat tools.

- **Claude Desktop / Claude Code**: Native skill. Install the ZIP as an
  Agent Skill.
- **OpenAI Codex**: Native skill metadata. `agents/openai.yaml` provides
  Codex-facing metadata.
- **ChatGPT**: Prompt/project mode. Use `SKILL.md` as custom instructions;
  upload references as knowledge or context where supported.
- **Google Gemini**: Prompt/gem mode. Use `SKILL.md` as instructions; provide
  references as supporting files or context where supported.
- **LM Studio / local models**: System-prompt mode. Use `SKILL.md` as the
  system prompt; add references when context allows.

## Installation

### Claude Desktop App (Cowork) — easiest

1. **Download:**
   [gra-skill-v8.5.3.zip][gra-v853-zip]
2. In the Claude desktop app, go to **Customize > Skills**
3. Upload the ZIP file
4. Enable the skill
5. Start researching: "Help me analyze this census record"

### Claude Code (CLI)

```bash
# Download and install in one step:
# Set GRA_ZIP_URL to the release asset URL shown above.
curl -L "$GRA_ZIP_URL" -o /tmp/gra.zip
unzip /tmp/gra.zip -d ~/.claude/skills/

# Or copy manually:
cp -r skills/gra ~/.claude/skills/gra
```

Restart Claude Code. The skill loads automatically for
genealogical research questions.

### Without Claude Code

The prompt files work in any LLM:

- `SKILL.md` (~8KB): System prompt for GPTs, Gems, and Projects.
- `references/research-assistant-v8.5-full.md` (60KB): Full methodology for
  any LLM chat.
- `references/companion-reference.md` (18KB): Upload as a knowledge file
  alongside the compact prompt.

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

- **Compact**: `SKILL.md`, ~8KB. Best for daily use as a skill prompt.
- **Full**: `references/research-assistant-v8.5-full.md`, 60KB. Best for
  deep methodology.
- **Reference**: `references/companion-reference.md`, 18KB. Best for
  templates and schemas.

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
- v8.5.2 (Apr 2026) — Implied-relationship inference guardrail
- v8.5.3 (May 2026) — Packaging release with standalone runtime ZIP

## License

[Creative Commons BY-NC-SA 4.0](LICENSE)

## Author

**Steve Little** ([@DigitalArchivst](https://github.com/DigitalArchivst))
AI Program Director, National Genealogical Society

---

*Part of the [Open-Genealogy][open-genealogy] toolkit.*

[gra-v853-zip]: https://github.com/DigitalArchivst/Open-Genealogy/releases/download/v8.5.3/gra-skill-v8.5.3.zip
[open-genealogy]: https://github.com/DigitalArchivst/Open-Genealogy
