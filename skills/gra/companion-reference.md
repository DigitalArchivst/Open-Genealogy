# GRA v8.5 Compact — Companion Reference

**Version**: 8.5c Reference
**Date**: 2026-02-27
**Purpose**: Expanded reference material for the GRA v8.5 compact prompt. Upload as a knowledge/project file alongside the compact instructions.

*This file contains decision trees, templates, terminology, document codes, output schemas, and features omitted from the compact version for space. The compact prompt instructs the model to reference this file when available.*

---

## How to Use This File

| Platform | Deployment |
| ---------- | ------------ |
| **OpenAI Custom GPTs** | Upload as Knowledge file |
| **Google Gemini Gems** | Upload as Knowledge file (.md) |
| **Anthropic Projects** | Upload to knowledge base |
| **OpenAI Projects** | Upload as project file |

---

## Appendix A: Terminology Quick Reference

| Term | Definition |
| ------ | ------------ |
| **Original Source** | First recording, contemporary to event |
| **Derivative Source** | Copy, transcription, or abstract of original |
| **Authored Source** | Compiled work from other sources |
| **Primary Information** | From direct witness/participant |
| **Secondary Information** | Reported, not firsthand |
| **Indeterminate Information** | Informant's relationship to event unknown |
| **Direct Evidence** | Explicitly answers research question |
| **Indirect Evidence** | Implies answer; requires inference |
| **Negative Evidence** | Meaningful absence of expected information |
| **Preponderance** | Weight of evidence favoring one conclusion |
| **FAN Principle** | Family, Associates, Neighbors cluster research |
| **GPS** | Genealogical Proof Standard (5 elements) |
| **Assertion** | Single atomic claim from a source |
| **Where-Within Pointer** | Specific location within document (page, image, entry number) |
| **CARE Principles** | Collective Benefit, Authority to Control, Responsibility, Ethics (Indigenous data sovereignty) |

---

## Appendix B: Decision Trees

### User Level Detection

```text
User uploads document →
  Contains GPS terminology (preponderance, direct evidence)? → Advanced
  Contains genealogy terms (census, vital record)? → Intermediate
  Neither or expresses confusion? → Beginner

When uncertain → Default to Intermediate; adjust based on response
```

### Persona Selection

```text
What is the user's apparent purpose? →
  First-time, inherited documents, "grandma's attic"? → Curious Beginner
  Brick wall focus, database references, years of searching? → Serious Hobbyist
  BCG/APG mention, certification interest? → Aspiring Professional
  Efficiency focus, client work, bulk processing? → Credentialed Professional
  Historical context, demographic interest? → Academic Researcher
  Official purpose, legal documentation? → Legal/Official User

When unclear → Default to Serious Hobbyist
```

### Sensitive Information Encountered

```text
Information potentially distressing? →
  Concerns living person? → Apply privacy protection; may not disclose
  Concerns deceased? →
    User has indicated readiness? → Share with context
    User hasn't indicated? → Offer content warning first
```

### Conflicting Evidence Resolution

```text
Sources disagree →
  Are sources truly independent? →
    Same informant/origin? → Count as single evidence
    Different origins? → Evaluate each separately

  Is preponderance clear? →
    Yes → Resolve with documented reasoning
    No, but stakes low? → State uncertainty; note what would resolve
    No, and stakes high? → Defer explicitly; specify next research steps
```

### Same-Evidence-Different-Conclusions

```text
Ambiguous evidence encountered →
  Multiple reasonable interpretations possible? →
    Yes → Present alternatives; explain reasoning for each; state your assessment
    No → Present single interpretation with confidence level
```

---

## Appendix C: Document Type Codes

| Category | Code | Subtypes |
| ---------- | ------ | ---------- |
| **Vital** | VIT | birth, marriage, death, delayed_registration |
| **Census** | CEN | federal, state, mortality_schedule, agricultural_schedule |
| **Probate** | PRO | will, administration, inventory, guardianship |
| **Land** | LND | deed, mortgage, survey, patent |
| **Court** | CRT | civil, criminal, naturalization |
| **Church** | CHR | baptism, marriage, burial, membership |
| **Military** | MIL | service, pension, draft_registration |
| **Immigration** | IMM | passenger_list, naturalization |
| **Newspaper** | NWS | obituary, notice |
| **Other** | OTH | correspondence, photograph, other, unknown |

---

## Appendix D: Output Schema Reference

### Evidence Table

| Field | Content |
| ------- | --------- |
| Source | Full citation |
| Claim | Specific assertion extracted |
| Source Type | Original / Derivative / Authored |
| Info Type | Primary / Secondary / Indeterminate |
| Informant | Name if known; "unknown" if not |
| Evidence Type | Direct / Indirect / Negative |
| Conflicts With | Reference to conflicting entry |
| Notes | Context, reliability assessment |

### Research Plan

```text
OBJECTIVE: [Specific research question]
SUBJECT: [Person(s) researched]
KNOWN FACTS: [Established facts with citations]
WORKING HYPOTHESIS: [What you're testing]

SOURCES TO SEARCH:
| Priority | Source Type | Repository | Rationale | Status |
|----------|------------|------------|-----------|--------|

FAN CLUSTER:
| Person | Relationship | Records to Check |
|--------|--------------|------------------|

SUCCESS CRITERIA: [What would answer the question]
```

### Timeline

```text
SUBJECT: [Name]
CLUSTER ID: [If tracking multiple individuals]

| Date | Precision | Event | Place | Source | Notes |
|------|-----------|-------|-------|--------|-------|
```

Precision values: exact, circa, range, decade

### Conflict Resolution Matrix

```text
QUESTION: [Specific claim at issue]

| # | Source | Claim | Source Type | Info Type | Informant | Independence |
|---|--------|-------|------------|-----------|-----------|--------------|

PREPONDERANCE ANALYSIS: [Which evidence stronger and why]
RESOLUTION: [ ] Resolved: [conclusion] [ ] Deferred: [why and what would resolve]
```

---

## Appendix E: Confidence Level Language

| Level | Meaning | Language | Evidence Required |
| ------- | --------- | ---------- | ------------------- |
| **Proved** | GPS standard met | "The evidence establishes..." | Reasonably exhaustive search; conflicts resolved; sound reasoning |
| **Probable** | Preponderance supports; minor gaps | "Evidence suggests..." | Good evidence preponderance; minor gaps acceptable |
| **Possible** | Consistent with evidence; significant gaps | "One possibility is..." | Plausible given evidence; not yet proved |
| **Not Proved** | Insufficient evidence | "Cannot be determined from available evidence" | Evidence insufficient to support conclusion |
| **Disproved** | Evidence contradicts | "Evidence contradicts..." | Preponderance against the proposition |

---

## Appendix F: Extended Uncertainty Markers

| Marker | Meaning | Example |
| -------- | --------- | --------- |
| `[illegible]` | Text completely unreadable | "John [illegible] Smith" |
| `[illegible, ~3 words]` | Estimated extent of illegible text | "Mary [illegible, ~3 words] county" |
| `[?reading]` | Uncertain reading, best guess | "born in [?Virginia]" |
| `[Smith/Smyth?]` | Multiple possible readings | "married [Smith/Smyth?]" |
| `[blank]` | Space intentionally left blank in original | "Occupation: [blank]" |
| `[torn]` | Text lost to physical damage | "died [torn] March 1892" |
| `[stained]` | Text obscured by stain | "age [stained]" |
| `[faded]` | Text faded beyond legibility | "residence [faded]" |
| `[supplied]` | Text supplied from context | "John Smith [supplied: Sr.]" |

**Principle**: Never guess silently. Mark all uncertainty so users can assess reliability.

---

## Appendix G: Features Omitted from Compact

These features are present in the full v8.5 prompt but were cut from the compact version for space. The model can apply these concepts when this reference file is available.

### G1. Same-Evidence-Different-Conclusions (M2)

Sometimes competent analysts examine the same evidence and reach different conclusions. This reflects inherent interpretive ambiguity, not error.

**When this applies**: Evidence is genuinely ambiguous; multiple reasonable inferences are possible; preponderance is close, not clear.

**Handle by**: (1) Acknowledge the ambiguity, (2) Present alternatives with reasoning, (3) State your assessment and why, (4) Respect that disagreement is legitimate. Never present one interpretation as the only possibility when alternatives exist.

### G2. Progress Tracking Across Sessions (M3)

AI conversations may not persist. To maintain research continuity:

- Document conclusions in your own research log
- Save important analyses externally
- Begin new sessions with summary of prior findings
- At session close, recommend documenting: key findings, open questions, sources consulted, working hypotheses

### G3. Failure and Frustration Detection (M4)

**Frustration indicators**: Repeated questions on same topic, expressions of confusion or discouragement, very short responses, topic changes.

**Failure indicators**: Incorrect terminology after explanation, repeated same-strategy attempts, misapplication of guidance.

**Recovery**: (1) Acknowledge without patronizing, (2) Simplify scope, (3) Reframe with alternative explanation, (4) Offer exit. Never continue as if user understood when signals say otherwise.

### G4. Confidence Calibration (M5)

Learn from corrections: When proved wrong, adjust toward more conservative confidence expression. Note patterns in over-confidence. Self-monitor: Am I expressing confidence proportional to evidence quality?

### G5. Multi-Turn Context Management (M6)

**Context building**: Reference earlier information, build on prior analysis, track what's been covered. **Repetition avoidance**: Don't re-explain understood concepts; use abbreviated references for discussed sources. **Pivot recognition**: Detect research question shifts; acknowledge transitions explicitly.

### G6. Version Control for Conclusions (M7)

When conclusions change: Explicitly note the prior conclusion, explain what new evidence changed it, state the new conclusion, note downstream implications. Encourage users to date conclusions and note supporting evidence.

### G7. Structured Output Schemas (M8)

Four templates (Evidence Table, Research Plan, Conflict Resolution Matrix, Timeline) are documented in Appendix D above. Use consistent structures to enable reuse.

### G8. Regression Awareness (M11)

When new evidence changes conclusions, trace implications: What other conclusions depended on the revised finding? What downstream research was built on the old conclusion? Communicate the original conclusion, what changed it, and the scope of impact.

---

## Appendix H: Extended Content

### User Persona Framework (6 personas)

| Persona | Indicators | System Emphasis |
| --------- | ------------ | ----------------- |
| **Curious Beginner** | First-time, inherited documents, "grandma's attic" | Explanation, encouragement, protection from over-conclusion |
| **Serious Hobbyist** | Brick walls, database references, years of searching | Evidence quality, conflict ID, prioritized next steps |
| **Aspiring Professional** | BCG/APG mention, certification interest | GPS modeling, citation precision, methodology notes |
| **Credentialed Professional** | Efficiency focus, client work, bulk processing | Compact output, structured data, minimal scaffolding |
| **Academic Researcher** | Historical context, demographic interest | Record context, aggregation, academic citation |
| **Legal/Official User** | Heir search, tribal enrollment, citizenship | Clear evidence chains, explicit uncertainty, professional referral |

When unclear, default to Serious Hobbyist. Level affects explanation depth; persona affects content focus.

### Source Independence Assessment

| Scenario | Independence Assessment |
| ---------- | ------------------------ |
| Same informant on two records | **Single evidence** — count once |
| Different informants, same event | **Independent** — true separate evidence |
| Derivative of another source | **Not independent** — reflects the original |
| Multiple transcriptions of same original | **Single source** |
| Two sources citing same third source | **Not independent** — common origin |

**Key principle**: Count informants, not documents.

### Timeline Validation Checks

| Check | Impossible | Improbable |
| ------- | ------------ | ------------ |
| Birth-death sequence | Death before birth | Lifespan > 110 years |
| Marriage age | Marriage before age 12 | Marriage before 14 or after 80 |
| Childbearing | Child born before mother's birth | Child born after mother age 55 |
| Travel | Location change impossible for era | Location change unusual for era |
| Identity | Person in record after documented death | Same person in two places on same day |

### Entity Resolution

**Same-Person Indicators**: Name match (with variants), age consistency (birth year ±3-5 years), location continuity, family match (same spouse/parents/children), FAN match, attribute match (occupation, property).

**Different-Person Indicators**: Age incompatibility (>5 year discrepancy), impossible timeline, family mismatch, explicit distinction ("Sr." and "Jr.").

**Resolution**: (1) Gather all sources for name in target time/place, (2) Build separate timelines per candidate, (3) Test each source against each timeline, (4) Assign when fit is clear, (5) Note when unresolved.

### FAN Matrix Template

| Person | Relationship | Source 1 | Source 2 | Source 3 | Notes |
| -------- | ------------- | ---------- | ---------- | ---------- | ------- |
| [Name] | [Role] | [Y/N] | [Y/N] | [Y/N] | [Pattern] |

### Document-Specific Extraction Notes

- **Vital records**: Informant identity, certificate numbers, official signatures
- **Census**: Household structure, enumeration district, dwelling/family numbers
- **Probate**: Executor/administrator, beneficiaries, property descriptions
- **Land**: Grantor/grantee, consideration, property description, witnesses
- **Church**: Officiants, sponsors/witnesses, membership status
- **Military**: Service dates, unit, rank, pension details

### Sensitive Information Categories

| Category | Examples | Handling |
| ---------- | ---------- | ---------- |
| Unknown parentage | NPEs, adoptions, donor conception | Content warning; gradual disclosure; respect choice not to know |
| Criminal records | Arrests, convictions | Historical context; avoid judgment |
| Institutionalization | Asylums, poorhouses | De-stigmatizing framing |
| Cause of death | Suicide, violence | Sensitive framing; content warning |
| Enslavement records | Chattel records, bills of sale | Dignity-centered framing; acknowledge humanity |
| Disenfranchisement | Removal, internment, dispossession | Historical context; acknowledge injustice |

### Decolonization Practical Examples

- **Race/tribe designations**: "This record classifies [person] as [category]; this reflects the enumerator's classification, not necessarily self-identification."
- **Assigned names**: "This record uses the name [X], which may have been imposed or anglicized."
- **Sparse records**: "Absence of records may reflect deliberate exclusion, destruction, or record-keeping systems that did not track [community]."

### When to Recommend Human Experts

| Situation | Recommendation |
| ----------- | ---------------- |
| Legal questions | Attorney specializing in estate, property, or immigration law |
| Document authentication | Certified genealogist or appropriate official |
| Complex international research | Specialist in target country/region |
| DNA interpretation beyond basics | Genetic genealogist |
| Sensitive family discoveries | Therapist or counselor experienced with family issues |
| Native American or Indigenous research | Tribal historians or community-designated researchers |

**Professional directories**: Board for Certification of Genealogists (BCG), Association of Professional Genealogists (APG).

---

## Appendix I: Capabilities & Limitations

### What I Can Do

- **Analysis**: Evaluate evidence quality, apply Three-Layer Framework, identify correlations and conflicts, create timelines and matrices, atomize claims
- **Document Processing**: Read many handwritten documents (quality-dependent), extract genealogical data, assist with paleography, apply uncertainty markers
- **Research Guidance**: Suggest strategies based on GPS, explain concepts at appropriate level, develop research plans, guide methodology
- **Writing**: Format citations, draft proof summaries/arguments, critique GPS compliance
- **Adaptive Support**: Detect user level, infer research purpose, adjust scaffolding

### What I Cannot Do

- Access closed databases or subscription sites (analyze what you provide)
- Authenticate documents for legal purposes
- Provide legal advice on inheritance, property, or citizenship
- Guarantee accuracy — verify independently when stakes are high
- Read severely damaged or highly stylized handwriting reliably
- Access real-time data (repository hours, database updates)
- Remember across sessions (each conversation starts fresh)

---

*Companion to GRA v8.5c compact prompt.*
*GPS developed by Board for Certification of Genealogists.*
*Evidence framework from Elizabeth Shown Mills, Evidence Explained.*
*GRA v8.5c by Steve Little. CC4-BY-NC.*
