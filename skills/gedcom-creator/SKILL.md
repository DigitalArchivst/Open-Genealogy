---
name: gedcom-creator
description: >-
  Create GEDCOM 5.5.1 compliant genealogy files from natural language,
  JSON, or markdown table input. Use when the user wants to generate
  a family tree interchange file from research data.
license: MIT
compatibility: Requires Claude Code and Python 3.6+
metadata:
  version: "1.3.0"
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
- **Contradictions across sources:** When different documents disagree,
  present both readings and ask the user to resolve.
- **Contradictions within a single source:** Record the most internally
  consistent reading. Add a NOTE documenting both values and flag it
  in the confirmation preview. Example: "Source gives marriage as both
  1789 and 1791. ABT 1789 used; user should verify."
  **Tiebreaker:** If no reading is more internally consistent than
  another, record BOTH readings in a NOTE and leave the DATE field
  empty. Flag for user resolution in the confirmation preview. Do
  not silently pick one.
- For gender, use what the user states or `U` if unknown.
  NEVER assume gender from names.

#### Parish Register Table Formats

When the user provides data from English parish registers, expect
these table structures:

**Baptisms:**

```text
| Date | Child | Father | Mother | Notes | Source |
| 14 Feb 1603/04 | William | William Whitchurch | | | PR, f.12r |
| 3 May 1606 | Robert | William Whitchurch | Anne | | PR, f.14v |
| 11 Jan 1610/11 | Samuel | William Whitchurch | | base born | PR, f.17v |
```

Parsing notes for baptisms:

- Mother is frequently absent in pre-1640 registers. Do NOT infer
  her. Treat blank as unrecorded, not "unknown wife."
- "base born" / "bastard" / "illegitimate" means no father should
  be assigned to the family unit. Link child to mother only.
- Use `BAPM` (baptism) for English parish register entries, not
  `CHR` (christening) unless the register explicitly says christening.
- Folio references (f.12r, f.14v) are standard manuscript citations.

**Marriages:**

```text
| Date | Groom | Bride | By | Notes | Source |
| 15 Oct 1601 | William Whitchurch | Anne [unknown] | banns | | PR, f.8r |
| 22 Nov 1635 | Robert Whitchurch | Jane Harding | licence | | PR, f.31v |
```

Parsing notes: "By" column (banns/licence) is genealogically
significant. Bride's maiden surname is often absent in early
registers — do NOT fabricate it.

**Burials:**

```text
| Date | Name | Descriptor | Notes | Source |
| 8 Mar 1641/42 | William Whitchurch | senior | | PR, f.42r |
| 14 Jun 1643 | Anne Whitchurch | wife of William | | PR, f.43v |
| 2 Dec 1680 | William Whitchurch | | | PR, f.67r |
```

Parsing notes: The **Descriptor column is critical** for
disambiguation. Preserve descriptors verbatim ("senior,"
"the elder," "wife of William," "widow," "son of Robert").
These are primary disambiguation evidence. A burial with no
descriptor in a period when multiple people share the name is
genuinely ambiguous — flag it in the confirmation preview with
an `AMBIGUOUS:` prefix and list candidate IDs. Do not create a
GEDCOM record for the burial until the user resolves which
individual it belongs to.

**Important:** When a burial entry mentions a person (e.g., "Anne,
wife of William"), ensure that person gets a BURI event on their
own INDI record — not just a mention in someone else's NOTE. This
helps the living-person filter correctly identify them as deceased.

**Wills (supplementary):**

```text
| Date | Testator | Relationships | Probate | Source |
| 12 Jan 1641/42 | William Whitchurch | wife Anne; son Robert; son William; dau Joan | 3 Apr 1642 | TNA PROB 11/189 |
```

The Relationships column provides direct evidence for family
links. Each named relationship becomes a source citation on the
FAM record (see Family-Level Source Citations below).

#### Name Disambiguation for Recycled Names

When processing registers where the same given names repeat across
generations (e.g., successive William Whitchurches), maintain a
mental "person register" with active date windows:

**Step 1: Assign active windows.**
Each known individual gets a plausible active range:
baptism + 16 years to baptism + 55 years (for fathering children).

**Step 2: When a new entry names a person, check candidates.**

- **Exactly one candidate** in the active window: assign
  tentatively. Add a NOTE: "Assigned to [ID] based on date
  plausibility."
- **Zero candidates**: create a new individual. Add a NOTE:
  "New individual — no existing candidate in active window."
- **Multiple candidates**: DO NOT ASSIGN. Flag as ambiguous:
  "AMBIGUOUS: [entry] could be [I3] (bapt. 1580) or [I7]
  (bapt. 1610). User must resolve."

**Step 3: Use register descriptors as primary evidence.**
"Senior" / "junior" / "the elder" / "wife of" / "son of" —
these disambiguate directly. Note: in English registers,
senior/junior means elder/younger currently alive in the parish,
NOT necessarily father/son.

**Step 4: Use wills to confirm or resolve.**
A will naming "my son William" written by a William who was
buried the following week is direct relationship evidence.

**Step 5: Use spousal co-occurrence.**
If baptism entries name the mother as "Anne" from 1601-1615 and
"Joan" from 1618-1630, check the burial register for an Anne
between 1615-1618. If found: one man, sequential wives. If not:
possibly two different men.

**NEVER silently merge ambiguous individuals.** Present all
ambiguities in the confirmation step for the user to resolve.

#### Date Mapping

| User says | GEDCOM output |
| --------- | ------------- |
| "March 15, 1845" or "15 Mar 1845" | `15 MAR 1845` |
| "around 1868" / "circa 1868" / "about 1868" | `ABT 1868` |
| "before 1870" / "by 1870" | `BEF 1870` |
| "after 1865" / "since 1865" | `AFT 1865` |
| "between 1860 and 1870" | `BET 1860 AND 1870` |
| "the 1860s" | `BET 1860 AND 1869` |
| "from 1870 to 1880" / service period | `FROM 1870 TO 1880` |
| "mid-1800s" or vague decades | **ASK the user** |
| "aged 20 at marriage in 1789" | `CAL 1769` (calculated from stated age) |
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

**Family Role column format:**

- Single role: `Spouse in F1` or `Child in F1`
- Multiple roles: `Child in F1; Spouse in F2` (semicolon-separated)
- No family links: `Unlinked`

This column is derived from `family_child` and `family_spouse` in
the JSON — it is display-only and not stored.

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
      "source_citations": [],
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

### Event Parsing Conventions

| Tag | What to extract | Date | Common in |
| --- | --------------- | ---- | --------- |
| `MILI` | Military service, rank | Service period (`FROM...TO`) | Biographies, obituaries, pensions |
| `PROB` | Probate of a will | Probate date (not will date) | Court records, will tables |
| `WILL` | Writing of a will | Date will was written | Will tables (separate from PROB) |
| `OCCU` | Occupation or profession | Period if known | Census, directories, obituaries |
| `RESI` | Residence | Period of residence | Census, directories, letters |

For PROB and WILL from the same document: create both events on
the same individual. The will-writing date goes on WILL; the
probate date goes on PROB.

### Nested Sources

When the user's input is an authored source (newspaper article,
biography, county history) that describes a derivative source
(a will, deed, court record), create separate SOUR records:

```json
"sources": [
  {
    "id": "S1",
    "title": "Springfield Gazette, 14 May 1909",
    "author": "William Curtis",
    "notes": ["Authored source; secondary information for events"]
  },
  {
    "id": "S2",
    "title": "Will of John Smith, 1794",
    "notes": ["Derivative source, described in S1"]
  }
]
```

Cite S1 on events described in the article (BIRT, DEAT, MILI).
Cite S2 on relationships established by the will (FAM-level SOUR).
This preserves the citation chain a researcher needs to follow
back to the original document.

### Living Person Handling

The Python script auto-redacts presumed-living individuals using
a layered detection system:

1. **Death indicators:** DEAT, BURI, or PROB event → deceased
2. **Birth year:** BIRT/BAPM/CHR date 110+ years ago → deceased
3. **Any-event inference:** OCCU in 1794 → born no later than 1779
   → deceased. Uses minimum-age assumptions per event type.
4. **Default:** No dates, no death evidence → presume living

Redaction: NAME becomes `[Living] /[Living]/`, events stripped.

**Override flags:**

- `--all-deceased` — skip all redaction (for historical sources
  where everyone is obviously deceased)
- `--deceased-before YEAR` — treat individuals with all events
  before YEAR as deceased (for mixed modern/historical datasets)
- `--include-living` — skip all redaction (legacy flag; prefer
  `--all-deceased` for historical data)

**Important:** A WILL event is NOT a death indicator. Living people
draft wills. PROB (probate) IS a death indicator because probate
follows death. Historical wills without a PROB event are still
caught by the any-event date inference system (a WILL in 1642
implies birth no later than 1624 → deceased).

**WILL and PROB event ownership:** Both tags go on the **testator's**
INDI record only. Named beneficiaries ("my wife Anne," "my son
Robert") are documented via FAM-level source citations and NOTEs —
never by adding WILL or PROB events to the beneficiary's record.

### Size Limits (v1)

| Limit | Value |
| ----- | ----- |
| Individuals | 200 |
| Families | 100 |
| Sources | 50 |

**Proactive check:** Before full extraction, estimate the likely
individual count from the source. If it appears to exceed ~50
individuals per prompt or ~200 total, suggest batch mode before
building the JSON intermediate.

If input exceeds limits, use batch mode (below).

## Batch Mode (Multi-Source Input)

When the user is processing a large source (parish register, set of
wills, census pages) that exceeds a single prompt:

1. **Parse each batch independently** to canonical JSON.
2. **Write each batch** to a numbered file:
   `<project>-batch-01.json`, `<project>-batch-02.json`, etc.
3. **Show a running summary** after each batch:
   "Batch 2: 18 individuals, 4 families. Running total: 38 I, 9 F."
4. **Before writing a new batch**, read prior batch files to check
   for existing individuals. Reference their existing ID — do NOT
   create duplicates.
5. **Generate once at the end** with all batch files:

```bash
python scripts/gedcom_builder.py batch-01.json batch-02.json \
  --output parish-register.ged --submitter "User Name"
```

The script merges all files, checks for duplicate IDs, and
validates the combined graph.

**ID convention:** Each batch starts numbering where the previous
ended. Read the last batch file to determine next available IDs.
If the environment does not support file reads (e.g., standalone
prompt in ChatGPT), maintain a running ID counter in conversation
context instead.

**Suggest batch mode when:**

- User mentions a register, collection, or set of documents
- Input would exceed ~50 individuals in a single prompt
- User says "I have more to add" or "there are 20 wills too"

## Family-Level Source Citations

When a source (such as a will) establishes a family relationship
rather than an individual event, attach the citation to the FAM
record — not to an individual's event.

The family JSON supports `source_citations`:

```json
{
  "id": "F1",
  "spouse1": "I1",
  "spouse2": "",
  "children": ["I2", "I3"],
  "events": [],
  "source_citations": [
    {
      "source_id": "S1",
      "source_page": "Will names 'my son Robert' as executor",
      "quality": 3
    }
  ],
  "notes": [
    "Relationship established by will of William Whitchurch (1650). Names Robert as son and executor."
  ]
}
```

This produces GEDCOM:

```text
0 @F1@ FAM
1 HUSB @I1@
1 CHIL @I2@
1 CHIL @I3@
1 NOTE Relationship established by will of William Whitchurch...
1 SOUR @S1@
2 PAGE Will names 'my son Robert' as executor
2 QUAY 3
```

**QUAY values:** 0=unreliable, 1=questionable, 2=secondary,
3=direct and primary. A testator naming his own children is QUAY 3.

Use this pattern for wills, settlements, court records, or any
source that directly establishes who belongs to a family.

## Known Limitations

**HUSB/WIFE tags and same-sex couples:** GEDCOM 5.5.1 defines only
HUSB and WIFE as spouse tags — there is no gender-neutral alternative.
The script uses individual sex fields to guide assignment (M→HUSB,
F→WIFE) and swaps when sex fields indicate the default is wrong. For
same-sex couples, a NOTE documents that positional assignment was used
and no gender assumption is intended. GEDCOM 7.0 addresses this
limitation; GEDCOM 5.5.1 does not.

## Anti-Fabrication Rules

You MUST NOT:

- Invent individuals not provided by the user
- Fill gaps in a pedigree with plausible ancestors
- Generate dates, places, or events not explicitly provided
- Narrow imprecise dates ("the 1920s" MUST NOT become "ABT 1925")
- Assume gender from names
- Create source citations the user did not provide
- Infer places from context
- Infer relationships from naming patterns alone (e.g., "William
  son of William" identifies the father's given name but is NOT
  proof of which William is the father — in a recycled-name parish,
  it could be father, grandfather, uncle, or godfather. Only assign
  when the register explicitly states the relationship or when
  disambiguation evidence resolves to exactly one candidate.)

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
