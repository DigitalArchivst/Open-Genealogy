# GEDCOM Creator — Claude Code Skill

Create GEDCOM 5.5.1 compliant genealogy files from natural language
descriptions, structured JSON, or markdown tables.

**This tool is designed and instructed to record only what you provide,
without inventing people, dates, or places. AI output can still be wrong,
so a human must verify the preview and generated GEDCOM.**

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
it by hand requires understanding the schema in [SKILL.md](SKILL.md). For most
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
python scripts/test_gedcom_builder.py
```

The suite regenerates both examples and normalizes only the dynamic
header date before comparison.

## Input Validation

Record IDs and pointer targets use the unwrapped GEDCOM xref form: 1-20
ASCII letters, digits, or underscores, such as `I1` or `S_CENSUS`.
Do not include `@` signs in JSON IDs or pointers. IDs must be unique
across individuals, families, sources, and repositories; `U1` is
reserved for the generated submitter record.

Event dates may use a three- or four-digit year, month and year, or
day-month-year using three-letter uppercase months. The accepted qualifiers are `ABT`,
`BEF`, `AFT`, `CAL`, and `EST`. The accepted compound forms are
`BET ... AND ...`, `FROM ... TO ...`, `FROM ...`, and `TO ...`.
Dual years such as `2 FEB 1731/32` are accepted. This is lexical
validation only; the script does not verify that a date existed on a
particular calendar.

Malformed or duplicate IDs and malformed dates stop the build before
auto-repair or rendering. Malformed and unresolved pointers fail final
validation, and the command does not write a GEDCOM file.

## Living-Person Privacy

By default, a family record keeps spouse and child links but suppresses
its events, dates, places, notes, and citations whenever any linked
spouse is redacted. This prevents family facts from identifying a
living person through a deceased spouse's record.

This is pseudonymization, not anonymization. A redacted name becomes
`[Living] /[Living]/`, but retained family links, sex values, record IDs,
deceased relatives, and other tree context may still permit
re-identification. The script also omits source records that are no
longer cited after redaction and repositories that are no longer used,
which prevents their titles, publication details, notes, names, and
addresses from leaking into the output. These controls reduce exposure;
they do not make a GEDCOM safe to publish without human review.

The `--deceased-before YEAR` cutoff applies only when the person has at
least one dated event, every available event date has a finite upper
bound, and the latest upper bound is before the cutoff. Undated people
and open-ended dates such as `AFT 1900` or `FROM 1900` remain redacted.

For a reviewed private-use file only, the narrow override retains those
family details while individual living-person records remain redacted:

```bash
python scripts/gedcom_builder.py private-input.json \
  --include-redacted-family-details --output private-family.ged
```

The script prints a privacy warning whenever that override exposes
family details linked to a redacted spouse. `--include-living` and
`--all-deceased` are broader overrides that bypass individual redaction
too. Review any overridden file before sharing, uploading, or publishing.

## What This Is Not

This is not a replacement for genealogy software. It does not search
databases, connect to online trees, or verify your research. It
translates your existing data into a standard file format that any
genealogy program can import. Human verification remains necessary for
names, relationships, dates, places, citations, privacy decisions, and
the final file before it is shared or uploaded.

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

The MIT License applies only to
[`scripts/gedcom_builder.py`](scripts/gedcom_builder.py); see the
package [LICENSE](LICENSE) for complete terms and the primary evidence
for that narrow scope. The README, `SKILL.md`, tests, and examples are
not included in that MIT grant and remain under the repository
[LICENSE](../../LICENSE) unless separately stated.

---

*Part of the [Open-Genealogy](https://github.com/DigitalArchivst/Open-Genealogy) toolkit.*
