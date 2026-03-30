# GEDCOM Creator — Claude Code Skill

Create GEDCOM 5.5.1 compliant genealogy files from natural language
descriptions, structured JSON, or markdown tables.

**This tool records only what you provide. It never invents people,
dates, or places.**

## Two Usage Paths

### With Claude Code (recommended)

1. Copy this folder to `~/.claude/skills/gedcom-creator/`
2. Restart Claude Code
3. Say: "Create a GEDCOM for my grandmother Rose Marie Sullivan,
   born April 3, 1928 in Boston, Massachusetts..."
4. Confirm the preview, receive your .ged file

### Without Claude Code (advanced)

The Python script works standalone with a JSON input file:

```bash
python scripts/gedcom_builder.py examples/sample-input.json \
  --output family.ged --submitter "Your Name"
```

The JSON format is designed for LLM-to-script communication. Writing
it by hand requires understanding the schema in SKILL.md. For most
users, the Claude Code path is significantly easier.

## Prerequisites

- Python 3.6+ (standard library only — no pip install required)
- For Claude Code path: Claude Code installed

## Quick Test

```bash
python scripts/gedcom_builder.py examples/sample-input.json
```

Expected output: validation passed, 5 individuals, 1 family, 2 sources.

## Regression Test

```bash
python scripts/gedcom_builder.py examples/sample-input.json \
  -o /tmp/test.ged -s "Your Name"
diff /tmp/test.ged examples/expected-output.ged
```

## What This Is Not

This is not a replacement for genealogy software. It does not search
databases, connect to online trees, or verify your research. It
translates your existing data into a standard file format that any
genealogy program can import.

## Platform Notes

| Platform | Python command |
| -------- | ------------- |
| Windows | `py` or `python` |
| macOS | `python3` |
| Linux | `python3` |

## Companion Tool

See [gedcom-analysis-v3.md](../../assistants/gedcom-analysis-v3.md)
to analyze and understand existing GEDCOM files.

## License

MIT (Python script). See repository [LICENSE](../../LICENSE) for
prompt content.

---

*Part of the [Open-Genealogy](https://github.com/DigitalArchivst/Open-Genealogy) toolkit.*
