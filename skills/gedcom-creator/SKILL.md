---
name: gedcom-creator
description: >-
  Create GEDCOM 5.5.1 compliant genealogy files from natural language,
  JSON, or markdown table input. Use when the user wants to generate
  a family tree interchange file from research data.
license: MIT
compatibility: Requires Claude Code and Python 3.6+
metadata:
  version: "1.0.0"
  author: Steve Little
  spec: GEDCOM 5.5.1 (1999)
---

# GEDCOM Creator — GEDCOM 5.5.1 File Generator

Create standards-compliant GEDCOM 5.5.1 files from user-provided
genealogical data. Accepts natural language, structured JSON, or
markdown tables.

**This tool records only what you provide. It never invents people,
dates, or places.**

## Design Principle

**The LLM parses and reasons. Code handles mechanics.**

You (Claude) interpret user input and build a canonical JSON
intermediate. The Python script (`scripts/gedcom_builder.py`) handles
GEDCOM rendering, pointer wiring, CONC/CONT splitting, validation,
and file output. You NEVER generate raw GEDCOM text directly.

## Dependencies

Python 3.6+ standard library only. No pip install required.

## When to Auto-Invoke

Auto-invoke when the user wants to create, generate, or build a
GEDCOM file from genealogical data. Trigger phrases:

- "create a GEDCOM"
- "generate a GEDCOM file"
- "build me a GEDCOM"
- "turn this into a GEDCOM"
- "export this as GEDCOM"
- "make a .ged file"

Do NOT auto-invoke for GEDCOM reading, analysis, or visualization.

## What You Can Say

Example prompts to get started:

```text
"Create a GEDCOM for my grandmother Rose Marie Sullivan, born
April 3, 1928 in Boston, Massachusetts, died February 14, 2015
in Quincy, Massachusetts. She married Thomas Patrick O'Brien on
September 12, 1950 in Boston."

"Here's census data I extracted — turn it into a GEDCOM file:
[paste table]"

"Generate a GEDCOM from this JSON: [paste structured data]"
```

## Processing Pipeline

### Step 1: Detect Environment

```bash
echo "MSYSTEM: $MSYSTEM" && uname -s && which python 2>/dev/null || which py 2>/dev/null || echo "python not found"
```

Determine the correct Python command and script path:

| Environment | Python | Script Path |
| ----------- | ------ | ----------- |
| MINGW64 / VS Code | `py` or `python` | `~/.claude/skills/gedcom-creator/scripts/gedcom_builder.py` |
| WSL2 | `python3` | `~/.claude/skills/gedcom-creator/scripts/gedcom_builder.py` |
| macOS / Linux | `python3` | `~/.claude/skills/gedcom-creator/scripts/gedcom_builder.py` |

### Step 2: Parse User Input to JSON Intermediate

Accept input in any of three modes:

**Mode 1 — Conversational (Primary):**
Parse natural language descriptions of people and families into the
canonical JSON format. This is the most common input path.

**Mode 2 — Structured JSON (Advanced):**
Accept JSON matching the canonical schema (see below). Validate and
pass through.

**Mode 3 — Markdown Table (Advanced):**
Parse tabular data into the canonical JSON format.

#### Parsing Rules

- Extract every individual mentioned with all stated facts
- Identify family relationships (spouse, parent, child)
- Normalize dates to GEDCOM format (see Date Mapping below)
- Normalize places to 4-level depth when possible
  (Locality, County, State, Country)
- **NEVER invent data not explicitly stated by the user**
- **NEVER narrow imprecise dates** ("the 1920s" is NOT "ABT 1925")
- When the same name appears multiple times, treat as the same
  person unless context indicates otherwise. If ambiguous, ASK.
- When input contains contradictory facts, HALT and ask the user
- For gender, use what the user states or `U` if unknown.
  NEVER assume gender from names.

#### Date Mapping

| User says | GEDCOM output |
| --------- | ------------- |
| "March 15, 1845" or "15 Mar 1845" | `15 MAR 1845` |
| "around 1868" / "circa 1868" / "about 1868" | `ABT 1868` |
| "before 1870" / "by 1870" | `BEF 1870` |
| "after 1865" / "since 1865" | `AFT 1865` |
| "between 1860 and 1870" | `BET 1860 AND 1870` |
| "the 1860s" | `BET 1860 AND 1869` |
| "mid-1800s" or vague decades | **ASK the user** |
| "2 Feb 1731/32" (dual-dating) | `2 FEB 1731/32` |

### Step 3: Show Confirmation (MANDATORY)

Before generating the GEDCOM, display a human-readable summary and
ask the user to confirm. This step is NOT optional.

Format:

```text
=== GEDCOM Preview ===

Individuals: [count]
Families: [count]
Sources: [count]

| ID | Name | Birth | Death | Family Role |
| -- | ---- | ----- | ----- | ----------- |
| I1 | John Smith | 15 MAR 1845, Richmond, VA | 2 JAN 1920, Henrico Co, VA | Spouse in F1 |
| I2 | Mary Jones | | | Spouse in F1 |
| I3 | William Smith | 1870 | | Child in F1 |

Date interpretations:
  - "around 1868" → ABT 1868

Shall I generate the GEDCOM file?
```

If the user says yes (or equivalent), proceed. If they correct
anything, update the JSON intermediate and re-confirm.

### Step 4: Generate GEDCOM via Python Script

Write the canonical JSON to a temp file, then invoke the builder:

```bash
# Write JSON intermediate to temp file
cat > /tmp/gedcom_input.json << 'JSONEOF'
[paste the canonical JSON here]
JSONEOF

# Run the builder
python ~/.claude/skills/gedcom-creator/scripts/gedcom_builder.py \
  /tmp/gedcom_input.json \
  --output "path/to/output.ged" \
  --submitter "User Name"
```

If no output path is specified, default to
`<first-surname>-family.ged` in the current directory.

### Step 5: Report Results

Display the output report from the script. It will include:

- File path and size
- Individual, family, and source counts
- Living person redactions (who and why)
- Validation status (passed/failed with details)
- Distribution warning

## Canonical JSON Schema

This is what you produce; the Python script consumes it.

```json
{
  "submitter": "string",
  "individuals": [
    {
      "id": "I1",
      "given": "John",
      "surname": "Smith",
      "prefix": "",
      "suffix": "",
      "nickname": "",
      "sex": "M",
      "events": [
        {
          "type": "BIRT",
          "date": "15 MAR 1845",
          "place": "Richmond, Henrico County, Virginia, USA",
          "source_id": "S1",
          "source_page": "page 42"
        }
      ],
      "notes": [],
      "family_child": "F0",
      "family_child_pedi": "birth",
      "family_spouse": ["F1"]
    }
  ],
  "families": [
    {
      "id": "F1",
      "spouse1": "I1",
      "spouse2": "I2",
      "children": ["I3", "I4"],
      "events": [
        {
          "type": "MARR",
          "date": "10 JUN 1868",
          "place": "Richmond, Henrico County, Virginia, USA"
        }
      ],
      "notes": []
    }
  ],
  "sources": [
    {
      "id": "S1",
      "title": "1870 Federal Census",
      "author": "",
      "publication": "",
      "repository_id": "R1",
      "notes": []
    }
  ],
  "repositories": [
    {
      "id": "R1",
      "name": "National Archives",
      "address": ""
    }
  ]
}
```

### Supported Event Types

Individual events (under INDI):
`BIRT`, `DEAT`, `BURI`, `CHR`, `BAPM`, `RESI`, `OCCU`, `CENS`,
`IMMI`, `EMIG`, `NATU`, `MILI`, `PROB`, `WILL`, `ADOP`

Family events (under FAM):
`MARR`, `DIV`

### Living Person Handling

The Python script auto-redacts presumed-living individuals:

- No death event AND birth within 110 years → living
- No death event AND no birth date → presume living
- Redaction: NAME becomes `[Living] /[Living]/`, events stripped

The user can override with `--include-living` flag if creating a
private file. Warn them if they do.

### Size Limits (v1)

| Limit | Value |
| ----- | ----- |
| Individuals | 200 |
| Families | 100 |
| Sources | 50 |

If input exceeds limits, warn and suggest splitting into multiple
files.

## Anti-Fabrication Rules

You MUST NOT:

- Invent individuals not provided by the user
- Fill gaps in a pedigree with plausible ancestors
- Generate dates, places, or events not explicitly provided
- Narrow imprecise dates ("the 1920s" MUST NOT become "ABT 1925")
- Assume gender from names
- Create source citations the user did not provide
- Infer places from context

When data is missing, omit the field. **An incomplete GEDCOM is
always preferable to an inaccurate one.**

## Error Handling

If the Python script reports validation errors, display them in
plain English:

| Script error | User-facing message |
| ------------ | ------------------- |
| `DANGLING_POINTER: @I3@` | "Sarah Smith (I3) is referenced but no record was provided. Add her or remove the reference?" |
| `BIDIRECTIONAL_MISMATCH: I2 FAMC F1` | "Mary Jones is listed as child of Family 1, but Family 1 doesn't list her as a child. Fixing..." |
| `CYCLE_DETECTED: I1 -> I2 -> I1` | "Circular relationship found: John is parent of Mary, but Mary is also parent of John. Please correct." |
| `INVALID_DATE: xyz` | "Could not parse date 'xyz'. Please provide in a format like 'March 15, 1845' or 'ABT 1868'." |

## Files in This Skill

```text
gedcom-creator/
  SKILL.md              — This file
  README.md             — Installation and usage guide
  scripts/
    gedcom_builder.py   — Python companion script (MIT license)
  examples/
    sample-input.json   — Example structured input
    expected-output.ged — Known-good output for regression testing
```
