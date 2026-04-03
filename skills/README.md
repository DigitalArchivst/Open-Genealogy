# Skills

Claude Code skills that combine prompts with companion scripts for
enhanced functionality.

Skills require [Claude Code](https://claude.ai/code). For
platform-agnostic prompts, see [Assistants](../assistants/).

## Available Skills

| Skill | Description | Status |
| ----- | ----------- | ------ |
| [gra/](gra/) | GPS-aligned genealogical research assistant | **new** |
| [gedcom-creator/](gedcom-creator/) | GEDCOM 5.5.1 file generator | stable |

## Installation

Copy a skill folder to your Claude Code skills directory:

```bash
cp -r skills/gedcom-creator ~/.claude/skills/gedcom-creator
```

Then restart Claude Code. The skill will be available via
`/gedcom-creator` or natural language.

---

*Part of the [Open-Genealogy](https://github.com/DigitalArchivst/Open-Genealogy) toolkit.*
