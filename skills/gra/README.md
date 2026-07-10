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

## Two Editions

v9.0.0 Skill Edition ships one methodology in two builds:

- **Agent edition** — this skill (`SKILL.md` + `references/`).
  Adds file access, consult triggers into the reference files,
  structured output mode, and live-verification offers where
  tools and permission allow.
- **Chat edition** —
  `research/research-assistant-v9.0.0-chat.md` (repository
  root). A self-contained copy-paste prompt, generated from the
  agent edition (never hand-edited), under 8,000 characters.
  Use it for Custom GPTs, Gemini Gems, and plain copy-paste
  chat. Release notes point chat users there.

The chat edition omits the agent-only surfaces (file access,
consult triggers, structured output, live verification) and
carries chat-accurate capability disclosures.

## Legacy v8.5 Links

GRA v8.5 remains available for readers following earlier articles:

- [Compact v8.5 prompt](https://github.com/DigitalArchivst/Open-Genealogy/blob/main/research/research-assistant-v8.5-compact.md)
- [Full v8.5.1c prompt](https://github.com/DigitalArchivst/Open-Genealogy/blob/main/skills/gra/research-assistant-v8.5-full.md)
- [v8.5.1c companion reference](https://github.com/DigitalArchivst/Open-Genealogy/blob/main/skills/gra/companion-reference.md)
- [v8.5.3 full reference](https://github.com/DigitalArchivst/Open-Genealogy/blob/main/skills/gra/references/research-assistant-v8.5-full.md)

## Compatibility

The GRA materials are designed to be portable across agent and
chat tools.

- **Claude Desktop / Claude Code**: Native skill. Install the ZIP as an
  Agent Skill.
- **OpenAI Codex**: Native skill metadata. `agents/openai.yaml` provides
  Codex-facing metadata.
- **ChatGPT**: Prompt/project mode. Use the chat edition as custom
  instructions; upload references as knowledge or context where supported.
- **Google Gemini**: Prompt/gem mode. Use the chat edition as instructions;
  provide references as supporting files or context where supported.
- **LM Studio / local models**: System-prompt mode. Use the chat edition as
  the system prompt; add references when context allows.

## Installation

### Claude Desktop App (Cowork) — easiest

1. **Download:**
   [gra-skill-v9.0.0.zip][gra-v900-zip]
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

- `research/research-assistant-v9.0.0-chat.md` (repository root, <8,000
  characters): the generated chat edition — for GPTs, Gems, and
  copy-paste chat.
- `references/research-assistant-full.md`: Full methodology for
  any LLM chat.
- `references/companion-reference.md`: Upload as a knowledge file
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

## Editions and References

- **Agent**: `SKILL.md`. Best for daily use in Agent Skills clients.
- **Chat**: `research/research-assistant-v9.0.0-chat.md`. Best for Custom GPTs,
  Gems, and copy-paste use.
- **Full**: `references/research-assistant-full.md`. Best for
  deep methodology.
- **Companion**: `references/companion-reference.md`. Best for
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

## Disclosing AI Assistance

When publishing work produced with this assistant's help,
include a disclosure statement. The canonical fill-in template
(also in the companion reference, Appendix J):

> Portions of this work were prepared with the assistance of the
> Genealogical Research Assistant (GRA) v9.0.0 Skill Edition, an
> AI research aid. All sources, citations, and conclusions were
> independently verified by [author's full name] on [date]. The
> author takes professional responsibility for every conclusion.

## Development History

18 months of iterative development (2024-2026):

- v6.1 (Dec 2024) — Foundation
- v7 (Jan 2025) — Enhanced evidence framework
- v8 (Jan 2026) — Synthesized from 5 beta candidates
- v8.5 (Jan 2026) — 12 new features via expert council
- v8.5c (Feb 2026) — 87% compression for multi-platform use
- v8.5.2 (Apr 2026) — Implied-relationship inference guardrail
- v8.5.3 (May 2026) — Packaging release with standalone runtime ZIP
- v9.0.0 (Jul 2026) — Skill Edition: two-edition architecture
  (agent skill + generated chat edition), behavior patches,
  teaching-case anonymization protocol

## License

[Creative Commons BY-NC-SA 4.0](LICENSE)

## Author

**Steve Little** ([@DigitalArchivst](https://github.com/DigitalArchivst))
AI Program Director, National Genealogical Society

---

*Part of the [Open-Genealogy][open-genealogy] toolkit.*

[gra-v900-zip]: https://github.com/DigitalArchivst/Open-Genealogy/releases/download/v9.0.0/gra-skill-v9.0.0.zip
[open-genealogy]: https://github.com/DigitalArchivst/Open-Genealogy
