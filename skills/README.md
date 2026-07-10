# Skills

Agent Skills combine instructions with supporting files for enhanced
functionality. Client support and installation paths vary.

For platform-agnostic prompts, see [Assistants](../assistants/).

## Available Skills

| Skill | Description | Status |
| ----- | ----------- | ------ |
| [GRA v9.2.0](https://github.com/DigitalArchivst/Open-Genealogy/tree/v9.2.0/skills/gra) | GPS-aligned genealogical research assistant Agent and Chat editions | **current release** |
| [GRA v9.0.0](https://github.com/DigitalArchivst/Open-Genealogy/releases/tag/v9.0.0) | Preserved previous GRA release | previous release |
| [gedcom-creator/](gedcom-creator/) | GEDCOM 5.5.1 file generator | stable |

## Current GRA v9.2.0

- [Agent Edition](https://github.com/DigitalArchivst/Open-Genealogy/tree/v9.2.0/skills/gra): immutable release
  skill source.
- [Chat Edition](https://github.com/DigitalArchivst/Open-Genealogy/releases/download/v9.2.0/research-assistant-v9.2.0-chat.md): self-contained
  public prompt for chat, Custom GPT, Gem, and project use.

## Release Artifacts

- [Agent Edition](gra/SKILL.md): v9.2.0 skill instructions.
- [Generated Chat Edition](../research/research-assistant-v9.2.0-chat.md):
  7,968-character prompt for chat, Custom GPT, Gem, and project use.
- [Install and platform matrix](gra/README.md): package, privacy, and client
  guidance for the v9.2.0 release.

The [v9.0.0 release](https://github.com/DigitalArchivst/Open-Genealogy/releases/tag/v9.0.0)
and all retained v8.5 compatibility paths remain available.

## Installation

Copy a skill folder to your Claude Code skills directory:

```bash
cp -r skills/gedcom-creator ~/.claude/skills/gedcom-creator
```

Then restart Claude Code. The skill will be available via
`/gedcom-creator` or natural language.

---

*Part of the [Open-Genealogy](https://github.com/DigitalArchivst/Open-Genealogy) toolkit.*
