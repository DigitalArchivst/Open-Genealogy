# Product Requirements Document: GPS-Grade Genealogical Record Analysis from Submitted Record Images

**Version**: 1.0
**Status**: Draft
**Author**: Steve Little
**AI Collaboration**: Claude Opus 4.5
**Date**: January 2026
**License**: CC BY-NC-SA 4.0

---

## Table of Contents

1. [Executive Summary](#1-executive-summary)
2. [Problem Statement](#2-problem-statement)
3. [Product Vision](#3-product-vision)
4. [User Personas](#4-user-personas)
5. [Scope and Boundaries](#5-scope-and-boundaries)
6. [Functional Requirements](#6-functional-requirements)
7. [Data Model Specification](#7-data-model-specification)
8. [Processing Pipeline](#8-processing-pipeline)
9. [Evidence Analysis Framework](#9-evidence-analysis-framework)
10. [Quality Standards](#10-quality-standards)
11. [Error Handling and Edge Cases](#11-error-handling-and-edge-cases)
12. [Privacy and Ethical Requirements](#12-privacy-and-ethical-requirements)
13. [Output Specifications](#13-output-specifications)
14. [Success Metrics](#14-success-metrics)
15. [Implementation Guidance for Claude](#15-implementation-guidance-for-claude)
16. [Dependencies and Constraints](#16-dependencies-and-constraints)
17. [Glossary](#17-glossary)
18. [Appendices](#18-appendices)

---

## 1. Executive Summary

### 1.1 Purpose

This PRD defines requirements for an AI-powered system designed to guide analysis of submitted genealogical record images into GPS-informed analytical outputs. The system produces accurate transcriptions, rigorous source/information/evidence characterization, cross-record correlation, conflict resolution, and actionable research plans—all while maintaining the epistemic humility and methodological rigor demanded by professional genealogical standards.

### 1.2 Core Capability

Given one or more record images, the system produces:

- **Verbatim transcriptions** with uncertainty markers
- **Structured abstracts** preserving as-stated content alongside normalized data
- **Atomized assertions** with provenance chains and "where-within" pointers
- **Source/Information/Evidence characterization** per GPS methodology
- **Cross-record correlation** (timeline, locality, FAN analysis, identity resolution)
- **Conflict detection and resolution** with explicit reasoning
- **Conclusion vehicle** (proof statement, summary, or argument) appropriate to evidence strength
- **Research plan** for gaps and unresolved conflicts
- **Complete citations** enabling independent verification

### 1.3 Governing Standard

All analysis adheres to the **Genealogical Proof Standard (GPS)** as defined by the Board for Certification of Genealogists, incorporating the evidence analysis framework from Elizabeth Shown Mills' *Evidence Explained*.

---

## 2. Problem Statement

### 2.1 The Gap in Current AI Genealogy Tools

Existing AI tools for genealogical research typically:

1. **Conflate source, information, and evidence**—treating "source quality" as monolithic rather than recognizing that a single source contains multiple information types serving as different evidence types depending on the research question

2. **Fail to atomize claims**—producing narrative summaries that obscure which specific facts come from which specific locations in which specific documents

3. **Over-conclude from insufficient evidence**—presenting plausible inferences as established facts, particularly around identity resolution across records

4. **Ignore or paper over conflicts**—either failing to detect when sources disagree or silently picking one version without explanation

5. **Produce citations that lack "where-within" precision**—citing "the 1870 census" rather than "1870 U.S. census, Kentucky, Breathitt County, population schedule, p. 12, dwelling 89, family 91, line 28"

6. **Lack epistemic humility**—failing to distinguish proved, probable, possible, and not proved conclusions

### 2.2 Consequences of These Gaps

- **Error propagation**: Unqualified conclusions enter family trees and propagate virally
- **Wasted research effort**: Users pursue paths based on conflated identities or ignored conflicts
- **Broken proof chains**: Conclusions that cannot withstand scrutiny because reasoning is implicit
- **Professional disqualification**: Output unsuitable for publication, certification applications, or legal contexts

### 2.3 The Opportunity

An AI system designed to follow GPS methodology can:

- **Democratize professional-quality analysis** for users who lack formal training
- **Accelerate expert workflows** by handling mechanical extraction and classification
- **Model good methodology** through transparent, structured output
- **Build genealogical literacy** by making the reasoning visible

---

## 3. Product Vision

### 3.1 Vision Statement

Improve how genealogists interact with record images by providing AI analysis that aims to follow the same methodological standards expected of credentialed professionals—not as a replacement for human judgment, but as a rigorous first pass that surfaces what the records contain, how confident we can be, what conflicts exist, and what remains unknown.

### 3.2 Design Principles

#### 3.2.1 Separation of Concerns

The system maintains strict separation between:

- **Source** (the container): Original, Derivative, or Authored
- **Information** (the content): Primary, Secondary, or Indeterminate
- **Evidence** (the relevance): Direct, Indirect, or Negative

This separation is non-negotiable. A death certificate is an Original source containing Primary information (date of death from attending physician) and Secondary information (birth date from informant's memory) that may serve as Direct evidence (for death) or Indirect evidence (for birth year).

#### 3.2.2 Atomization with Provenance

Every genealogically meaningful claim becomes a discrete assertion linked to:

- The specific document (doc_id)
- The specific image (image_id)
- The specific location within the image (region_bbox, line_ref)
- The source/information/evidence characterization
- A confidence score with rationale

This enables downstream systems and human reviewers to verify any claim by returning to the exact location in the exact record.

#### 3.2.3 Correlation Before Conclusion

The system never assumes two records describe the same person merely because names match. Identity resolution requires:

- Timeline consistency (ages, dates, locations)
- Relationship consistency (same family members appearing)
- FAN pattern consistency (same witnesses, neighbors, associates)
- Explicit acknowledgment when identity remains uncertain

#### 3.2.4 Conflicts Are Features, Not Bugs

When sources disagree, the system:

- Explicitly identifies the conflict
- Characterizes each side (source type, information type, informant proximity, independence)
- Applies preponderance principles with documented reasoning
- Either resolves with explanation or defers with specification of what would resolve it

Silently ignoring conflicts is a system failure.

#### 3.2.5 Calibrated Confidence

The system distinguishes:

| Level | Meaning | Language Pattern |
|-------|---------|------------------|
| **Proved** | GPS standard met | "The evidence establishes..." |
| **Probable** | Preponderance supports; minor gaps | "Evidence suggests..." |
| **Possible** | Consistent with evidence; significant gaps | "One possibility is..." |
| **Not Proved** | Insufficient evidence | "Cannot be determined from available evidence" |
| **Disproved** | Evidence contradicts | "Evidence contradicts the claim that..." |

Over-concluding damages credibility and propagates errors.

#### 3.2.6 Transparency of Reasoning

All analytical conclusions include explicit reasoning. The user should be able to follow the chain from raw image → transcription → assertion → characterization → correlation → conflict resolution → conclusion. Black-box conclusions are unacceptable.

---

## 4. User Personas

### 4.1 Primary Personas

#### 4.1.1 The Curious Beginner

**Profile**: Recently discovered family history interest; has a box of old documents from grandparents; no formal genealogical training; vocabulary limited to common terms.

**Needs**:
- Understand what their documents actually say (transcription)
- Learn what the documents mean genealogically (explanation)
- Know what to look for next (guided research direction)
- Avoid common beginner mistakes (methodology guardrails)

**System Response**: Full explanations of document types, terminology definitions, step-by-step guidance, encouraging tone, protection from over-conclusion.

#### 4.1.2 The Serious Hobbyist

**Profile**: Several years of research experience; comfortable with major databases; working on specific brick walls; understands basic GPS concepts but doesn't consistently apply them.

**Needs**:
- Extract maximum information from difficult documents
- Understand evidence quality for decision-making
- Identify conflicts they may have overlooked
- Get concrete next-step suggestions with reasoning

**System Response**: Moderate explanation depth, focus on GPS characterization, explicit conflict detection, prioritized research suggestions with rationale.

#### 4.1.3 The Aspiring Professional

**Profile**: Working toward certification or considering professional work; actively studying GPS methodology; wants to see rigorous analysis modeled.

**Needs**:
- GPS-informed analysis as a learning model
- Explicit application of preponderance principles
- Citation formatting per Evidence Explained
- Proof vehicle selection guidance

**System Response**: Minimal explanation of basics, full technical output, peer-level discourse, detailed methodology notes, publication-ready formatting options.

#### 4.1.4 The Credentialed Professional

**Profile**: BCG-certified or APG member; handles client work; needs efficiency on mechanical tasks; expects GPS-quality output.

**Needs**:
- Rapid, accurate transcription of routine documents
- Pre-structured evidence tables
- Conflict detection as quality control
- Output compatible with professional workflows

**System Response**: Compact technical output, minimal scaffolding, efficiency-optimized presentation, structured data export.

### 4.2 Secondary Personas

#### 4.2.1 The Academic Researcher

**Profile**: Historian, demographer, or social scientist using genealogical records as historical sources; may not know genealogical terminology but has strong source criticism skills.

**Needs**:
- Accurate extraction from historical documents
- Understanding of record creation context
- Aggregated data suitable for analysis
- Citation standards compatible with academic norms

#### 4.2.2 The Legal/Official User

**Profile**: Heir searching, tribal enrollment, citizenship documentation; needs documentation for official purposes.

**Needs**:
- Clear chain of evidence
- Explicit uncertainty acknowledgment
- Understanding that AI analysis is not legal authentication
- Guidance toward appropriate professional/legal resources

---

## 5. Scope and Boundaries

### 5.1 In Scope

#### 5.1.1 Document Types Supported

The system processes genealogically relevant record images including but not limited to:

| Category | Examples |
|----------|----------|
| **Vital Records** | Birth, marriage, death certificates; delayed registrations |
| **Census Records** | Federal, state, territorial, colonial enumerations |
| **Probate Records** | Wills, administrations, inventories, guardianships, distributions |
| **Land Records** | Deeds, mortgages, plats, surveys, grants, patents |
| **Court Records** | Civil suits, criminal cases, naturalizations, name changes |
| **Church Records** | Baptisms, confirmations, marriages, burials, membership |
| **Military Records** | Service records, pensions, draft registrations, muster rolls |
| **Immigration Records** | Passenger lists, naturalization papers, alien registrations |
| **Tax Records** | Personal property, real property, poll taxes |
| **Newspapers** | Obituaries, marriage notices, legal notices, local news |
| **Correspondence** | Letters, postcards with genealogical content |
| **Photographs** | When context/captions provide genealogical information |

#### 5.1.2 Analysis Capabilities

- Verbatim transcription with uncertainty markers
- Structured abstraction and normalization
- Source/Information/Evidence classification per GPS
- Multi-document correlation (timeline, locality, FAN)
- Identity hypothesis generation and scoring
- Conflict detection and resolution
- Conclusion drafting in appropriate proof vehicle
- Citation generation per Evidence Explained patterns
- Research plan generation with prioritized next steps

#### 5.1.3 Output Formats

- Structured data (JSON-compatible for downstream processing)
- Human-readable narrative report
- Evidence tables and matrices
- Timeline visualizations (textual)
- FAN cluster listings
- Citation sets
- Search log templates

### 5.2 Out of Scope

#### 5.2.1 Explicit Exclusions

| Exclusion | Rationale |
|-----------|-----------|
| **Legal authentication** | AI analysis cannot substitute for court-accepted authentication |
| **DNA analysis interpretation** | Requires specialized genetic genealogy expertise; may be future extension |
| **Database searching** | System analyzes provided images; does not access external databases |
| **Living person research** | Privacy protections preclude unauthorized research on living individuals |
| **Original record access** | System works with user-provided images; cannot retrieve records independently |
| **Translation services** | Non-English documents require human translation before analysis; system notes language |
| **Paleography training** | System attempts transcription but does not teach handwriting analysis |
| **Legal advice** | Questions about inheritance, citizenship, property rights require attorneys |

#### 5.2.2 Capability Limitations

- **Severely damaged documents**: System extracts what is legible; does not fabricate missing text
- **Highly stylized scripts**: Some historical hands may exceed recognition capability; system flags limitations
- **Non-Latin scripts**: Initial scope limited to Latin-alphabet documents
- **Complex legal instruments**: Deeds with metes-and-bounds may require specialized knowledge; system provides best-effort extraction

### 5.3 Future Considerations

The following may be considered for future versions:

- DNA evidence integration framework
- Multi-language support with translation
- Direct database API integration
- Collaborative case file management
- Publication-ready document generation
- Confidence calibration learning from expert feedback

---

## 6. Functional Requirements

### 6.1 Image Intake and Quality Assessment

#### FR-1.1: Image Acceptance

The system SHALL accept common image formats (JPEG, PNG, TIFF, PDF) containing genealogical records.

**Acceptance Criteria**:
- System processes images up to [size limit] without failure
- Multi-page PDFs are parsed into individual page images
- System reports unsupported formats with actionable guidance

#### FR-1.2: Quality Assessment

The system SHALL assess image quality and report limitations affecting analysis.

**Quality Indicators**:
- Orientation (rotation needed?)
- Skew (deskewing needed?)
- Contrast/exposure (key text readable?)
- Resolution (sufficient for character recognition?)
- Completeness (document fully visible or cropped?)
- Damage (tears, stains, fading affecting content?)
- Handwriting density (typed vs. handwritten; script style)
- Language detection (Latin-alphabet; other)

**Acceptance Criteria**:
- System auto-corrects orientation when detectable
- System reports quality issues with specific affected regions
- System proceeds with analysis even when quality is imperfect, noting limitations
- System flags "needs_better_copy" when key content is unreadable

#### FR-1.3: Image Segmentation

The system SHALL segment images into functional regions.

**Region Types**:
- Printed headers/titles
- Form fields/labels
- Handwritten content areas
- Tabular data (census grids, etc.)
- Marginal annotations
- Signatures
- Official stamps/seals
- Page numbers

**Acceptance Criteria**:
- Each region has a bounding box for "where-within" citation
- Segmentation errors are recoverable (manual correction pathway exists)
- Multi-column layouts are parsed in correct reading order

### 6.2 Document Grouping and Identification

#### FR-2.1: Multi-Image Grouping

The system SHALL group related images into single document packets.

**Grouping Logic**:
- Same document type and form layout
- Continuous page numbering
- Shared identifying headers
- Front/back of same physical document
- Multi-page instruments (deeds, wills spanning pages)

**Acceptance Criteria**:
- System correctly groups multi-page documents >90% of cases
- User can override grouping decisions
- Each document packet receives unique doc_id

#### FR-2.2: Document Type Identification

The system SHALL identify document type from visual and textual cues.

**Identification Features**:
- Explicit titles ("Certificate of Death," "Schedule 1—Free Inhabitants")
- Form layout patterns (census grids, vital record fields, deed paragraph blocks)
- Jurisdictional markers (state seals, court names)
- Temporal markers (form revision dates, legal boilerplate)

**Supported Classifications**:
```
vital_birth, vital_marriage, vital_death, vital_delayed
census_federal, census_state, census_mortality, census_agricultural
probate_will, probate_administration, probate_inventory, probate_guardianship
land_deed, land_mortgage, land_survey, land_patent
court_civil, court_criminal, court_naturalization
church_baptism, church_marriage, church_burial, church_membership
military_service, military_pension, military_draft
immigration_passenger, immigration_naturalization
newspaper_obituary, newspaper_notice
correspondence, photograph, other, unknown
```

**Acceptance Criteria**:
- System identifies document type for >85% of standard record types
- System marks "unknown" rather than guessing when uncertain
- User can override document type classification

#### FR-2.3: Document Context Extraction

The system SHALL extract key contextual metadata from each document.

**Required Metadata**:
- Event date(s) (date of the event being recorded)
- Record date(s) (date the record was created)
- Filing/registration date(s) (date officially filed, if different)
- Jurisdiction as stated (verbatim from document)
- Jurisdiction standardized (normalized hierarchy: Country > State/Province > County/Parish > Town/District)
- Creating authority (clerk, registrar, minister, enumerator, notary)
- Record purpose (registration, taxation, property transfer, sacrament, enumeration)
- Repository (if stated or user-provided; otherwise "repository not provided")

**Acceptance Criteria**:
- Dates parsed into ISO format with precision flags (exact/circa/range)
- Jurisdiction normalization handles historical boundary changes where detectable
- Missing metadata explicitly marked as unknown rather than omitted

### 6.3 Source Characterization

#### FR-3.1: Source Type Classification

The system SHALL classify each document's source type per GPS definitions.

| Source Type | Definition | Classification Criteria |
|-------------|------------|------------------------|
| **Original** | The first recording of an event, made at or near the time by someone with reason to know | Register entries, original certificates, courthouse deed books, contemporary diaries |
| **Derivative** | Any copy, transcription, index, abstract, or reproduction of another record | Microfilm, digitized images of originals (still derivative of the physical), published abstracts, database transcriptions, certified copies |
| **Authored** | A narrative or compilation created from other sources | County histories, compiled genealogies, lineage society applications, biographical sketches |

**Acceptance Criteria**:
- Every document receives exactly one source type classification
- Classification includes reasoning notes explaining the determination
- System distinguishes "digitized original image" (Derivative of physical Original) from "database transcription" (Derivative of Derivative)

#### FR-3.2: Provenance Chain Documentation

The system SHALL document the provenance chain from creation to user access where determinable.

**Provenance Elements**:
- Creation context (who, when, why, authority)
- Preservation history (if known)
- Transfer history (custody changes)
- Digitization pathway (who digitized, from what)
- Indexing pathway (if accessed via index)
- Access method (how user obtained image)

**Acceptance Criteria**:
- System records known provenance elements
- Unknown elements explicitly marked rather than omitted
- Derivative chains clearly documented (e.g., "transcription of index of microfilm of original register")

### 6.4 Transcription

#### FR-4.1: Verbatim Transcription

The system SHALL produce verbatim transcription of document text preserving original spelling, abbreviations, and punctuation.

**Transcription Standards**:
- Preserve original spelling (including errors)
- Preserve original abbreviations (expand in abstract, not transcription)
- Preserve original punctuation
- Preserve line breaks where meaningful (poetry, legal instruments)
- Maintain original capitalization

**Uncertainty Markers**:
```
[illegible]         — text completely unreadable
[illegible word]    — one word unreadable
[illegible, ~3 words] — estimated extent of illegible text
[?reading]          — uncertain reading, single best guess
[Hugh/Henry?]       — uncertain reading, multiple candidates
[blank]             — space intentionally left blank in original
[torn]              — text lost to physical damage
[stained]           — text obscured by stain
[faded]             — text faded beyond legibility
```

**Acceptance Criteria**:
- Transcription accuracy >95% for clearly legible text
- All uncertainty explicitly marked with appropriate marker
- No fabrication of illegible text under any circumstances
- Each transcribed segment linked to image region (where-within pointer)

#### FR-4.2: Where-Within Pointers

The system SHALL attach precise location pointers to all transcribed content.

**Pointer Components**:
- image_id: Which image in the set
- region_bbox: Bounding box coordinates [x1, y1, x2, y2]
- line_ref: Line number within region (where applicable)
- entry_ref: Entry number for enumerated documents (census, registers)

**Acceptance Criteria**:
- Any claim can be traced to exact image location
- Pointers enable automated highlighting in image viewer
- Citation generation uses pointers for "where-within" specificity

### 6.5 Abstraction and Normalization

#### FR-5.1: Structured Abstraction

The system SHALL extract genealogically relevant information into structured fields appropriate to document type.

**Common Fields (All Document Types)**:
- Persons named (with roles)
- Dates (event, record, filing)
- Places (event location, residence, origin)
- Relationships stated
- Witnesses/officials/informants

**Document-Type-Specific Fields**:

*Vital—Birth*:
```
child_name, child_sex, birth_date, birth_place, birth_time
father_name, father_age, father_birthplace, father_occupation, father_residence
mother_name, mother_maiden, mother_age, mother_birthplace, mother_residence
informant_name, informant_relationship
attendant_name, attendant_type (physician/midwife)
registration_date, registration_place, certificate_number
```

*Vital—Marriage*:
```
groom_name, groom_age, groom_birthplace, groom_residence, groom_occupation
groom_marital_status, groom_parents
bride_name, bride_age, bride_birthplace, bride_residence
bride_marital_status, bride_parents
marriage_date, marriage_place, officiant_name, officiant_type
witnesses[], license_date, certificate_number
```

*Vital—Death*:
```
decedent_name, decedent_sex, death_date, death_place, death_time
age_at_death, birth_date_stated, birthplace_stated
residence_at_death, occupation
marital_status, spouse_name
father_name, father_birthplace, mother_name, mother_maiden, mother_birthplace
cause_of_death, contributing_causes, duration_of_illness
informant_name, informant_relationship, informant_address
burial_date, burial_place, funeral_home
certificate_number, registration_date
```

*Census*:
```
enumeration_date, enumeration_district, sheet_number, line_number
dwelling_number, family_number
household_members[]:
  name, relationship_to_head, sex, race_as_recorded, age
  marital_status, birth_year_calculated, birthplace
  father_birthplace, mother_birthplace
  occupation, industry, employment_status
  literacy, school_attendance
  owned_or_rented, value_of_home, farm_or_house
```

*Probate—Will*:
```
testator_name, testator_residence
will_date, probate_date, codicil_dates[]
executor_names[], witnesses[]
beneficiaries[]: name, relationship_stated, bequest_description
real_property_mentioned[], personal_property_mentioned[]
conditions, trusts, guardianship_provisions
```

*Land—Deed*:
```
grantor_names[], grantor_residences[]
grantee_names[], grantee_residences[]
deed_date, recording_date, deed_book, page_number
consideration (price/exchange)
property_description (metes_and_bounds, lot_number, acreage)
witnesses[], acknowledgment_date, notary_name
```

**Acceptance Criteria**:
- All genealogically relevant information extracted
- Field names consistent across documents of same type
- Extraction errors bounded by uncertainty markers from transcription

#### FR-5.2: Dual-Value Retention

The system SHALL retain both as-stated and normalized values for key fields.

**Normalization Targets**:
- Names: `{as_stated: "Jno. Smith", normalized: "John Smith", confidence: 0.95}`
- Dates: `{as_stated: "15 Feby 1842", normalized: "1842-02-15", precision: "day"}`
- Places: `{as_stated: "Wilkes Co., N.C.", normalized: {country: "United States", state: "North Carolina", county: "Wilkes County"}, note: "Ashe County formed from Wilkes 1799"}`
- Ages: `{as_stated: "42", normalized_birth_year: "1828", calculated_from: "1870 census date"}`

**Acceptance Criteria**:
- Original values never lost in normalization
- Normalization confidence explicitly stated
- Historical jurisdiction changes noted where relevant

### 6.6 Assertion Atomization

#### FR-6.1: Claim Atomization

The system SHALL decompose extracted information into atomic assertions.

**Assertion Structure**:
```
assertion_id: unique identifier
subject_entity: {entity_id, entity_type, name}
predicate: relationship/attribute type
value: {as_stated, normalized}
date_context: {date_or_range, precision}
place_context: {as_stated, normalized_hierarchy}
source_pointer: {doc_id, image_id, region_bbox, line_ref}
information_type: Primary | Secondary | Indeterminate
evidence_type: Direct | Indirect | Negative
confidence: {score: 0.0-1.0, rationale: "..."}
notes: additional context, alternate readings
```

**Atomization Rules**:
- One assertion per discrete fact
- Compound statements split: "Mary, daughter of John and Sarah" → two assertions (Mary child_of John; Mary child_of Sarah)
- Implicit facts made explicit: "age 42" → birth year assertion with "calculated" note
- Relationships bidirectional where appropriate

**Acceptance Criteria**:
- Every genealogical claim traceable to single assertion
- No information loss from abstraction to atomization
- Assertions enable graph-based analysis

#### FR-6.2: Information Type Classification

The system SHALL classify each assertion's information type based on informant knowledge proximity.

| Information Type | Definition | Classification Criteria |
|------------------|------------|------------------------|
| **Primary** | Informant had firsthand knowledge—was participant or direct witness | Parent reporting child's birth, spouse reporting marriage, physician certifying death cause |
| **Secondary** | Informant is reporting what they heard, read, or were told | Child reporting parent's birthplace, informant on death certificate reporting birth date |
| **Indeterminate** | Informant's relationship to the fact cannot be determined | Many census entries, unsigned records, unclear informant identity |

**Classification Requirements**:
- Consider who provided each specific fact (not just who signed the document)
- Consider temporal proximity (contemporaneous vs. later recollection)
- Consider relationship to the event (participant vs. bystander vs. hearsay)
- When uncertain, classify as Indeterminate rather than guessing

**Acceptance Criteria**:
- Every assertion receives information type classification
- Classification includes brief rationale
- Same document may have assertions with different information types

#### FR-6.3: Evidence Type Classification

The system SHALL classify each assertion's evidence type relative to the research question.

| Evidence Type | Definition | Classification Criteria |
|---------------|------------|------------------------|
| **Direct** | Assertion explicitly answers the research question without additional reasoning | Birth certificate naming parents for parentage question |
| **Indirect** | Assertion contributes to answering the question but requires inference | Co-residence patterns for relationship questions, age consistency for identity questions |
| **Negative** | Meaningful absence of expected assertion after demonstrated search | Name missing from tax list where land ownership is documented |

**Classification Requirements**:
- Evidence type is always relative to a specific question
- Same assertion may be Direct for one question, Indirect for another
- Negative evidence requires demonstrating the search scope, not just noting absence

**Acceptance Criteria**:
- Evidence type classified against stated or inferred research question
- When no research question specified, system uses default: "What genealogically relevant facts can be established?"
- Negative evidence only claimed when search scope documented

### 6.7 Entity Resolution

#### FR-7.1: Entity Extraction

The system SHALL create entity records for all persons, places, and organizations mentioned.

**Person Entity Fields**:
```
entity_id: unique identifier
entity_type: Person
names[]: {name_value, name_type (given/surname/full/nickname/maiden), source_pointer}
sex_gender: {as_recorded, confidence}
race_ethnicity: {as_recorded, historical_context_note}
attributes[]: {attribute_type, value, date_context, source_pointer}
events[]: {event_type, date, place, role, source_pointer}
relationships[]: {relationship_type, related_entity_id, source_pointer}
identity_cluster_id: links records believed to represent same individual
```

**Place Entity Fields**:
```
entity_id: unique identifier
entity_type: Place
names[]: {name_value, name_type (current/historical/variant), effective_dates}
hierarchy: {country, state_province, county_parish, town_district}
coordinates: {latitude, longitude} (if determinable)
jurisdiction_history[]: {parent_jurisdiction, effective_dates}
```

**Acceptance Criteria**:
- All named entities extracted
- Variant spellings linked to same entity where determinable
- Entity records enable cross-document correlation

#### FR-7.2: Identity Hypothesis Generation

The system SHALL generate and score hypotheses about whether entities across documents represent the same individual.

**Matching Criteria**:
- Name similarity (accounting for spelling variation, initials, nicknames)
- Age consistency (birth year overlap within tolerance)
- Location continuity (plausible residence/migration pattern)
- Family consistency (same spouse, children, parents)
- FAN consistency (same witnesses, neighbors, associates)
- Occupation/attribute consistency

**Hypothesis Structure**:
```
hypothesis_id: unique identifier
entity_ids[]: entities potentially representing same person
evidence_features[]:
  - feature_type: name_match | age_overlap | same_spouse | same_children | same_neighbor | same_witness | ...
  - weight: contribution to hypothesis score
  - source_pointers[]
confidence_score: 0.0-1.0
supporting_factors: narrative summary
contradicting_factors: narrative summary
resolution_status: merged | separate | uncertain
```

**Acceptance Criteria**:
- System does not merge entities by name alone
- Uncertainty preserved when evidence insufficient
- Multiple hypotheses maintained when warranted
- Merge/separate decisions include explicit reasoning

#### FR-7.3: Identity Cluster Management

The system SHALL maintain identity clusters linking entity records believed to represent the same individual.

**Cluster Rules**:
- Entities merged into cluster only when correlation supports it
- Cluster maintains all constituent entity_ids
- Cluster accessible by any constituent entity_id
- Cluster can be split if evidence later contradicts

**Acceptance Criteria**:
- One individual = one cluster (when determinable)
- Uncertain cases maintain separate clusters with "possible merge" notation
- Cluster membership auditable through hypothesis records

### 6.8 Correlation Products

#### FR-8.1: Timeline Construction

The system SHALL construct chronological timelines for each identity cluster.

**Timeline Entry Structure**:
```
timeline_id: cluster reference
entries[]:
  date: {value, precision (day/month/year/decade/range)}
  event_type: birth | marriage | death | residence | property | military | court | ...
  description: brief summary
  place: standardized location
  source_pointers[]
  confidence: score with rationale
```

**Timeline Validation**:
- Detect impossible sequences (death before birth, marriage before age 12)
- Flag improbable sequences (childbirth after age 50, 120-year lifespan)
- Note gaps requiring research

**Acceptance Criteria**:
- All dated assertions appear in timeline
- Impossible/improbable sequences flagged for review
- Timeline gaps explicitly noted

#### FR-8.2: Locality Model

The system SHALL construct locality models tracking geographic patterns.

**Locality Model Structure**:
```
cluster_id: identity cluster reference
residences[]:
  place: {as_stated, normalized_hierarchy}
  date_range: {start, end, precision}
  source_pointers[]
  event_context: (census enumeration / deed residence / tax list / ...)
migration_path[]: ordered sequence of residences
jurisdiction_notes[]: historical boundary changes affecting this cluster
```

**Acceptance Criteria**:
- All place references integrated
- Migration patterns surfaced for analysis
- Jurisdiction changes noted where affecting interpretation

#### FR-8.3: FAN (Family-Associates-Neighbors) Graph

The system SHALL construct FAN graphs tracking relational patterns.

**FAN Graph Structure**:
```
cluster_id: target identity cluster
family_members[]:
  entity_id, relationship_type, evidence_strength, source_pointers[]
associates[]:
  entity_id, association_type (witness / bondsman / executor / co-worker / ...)
  occasions[]: {date, context, source_pointer}
neighbors[]:
  entity_id, proximity_type (adjacent_census / adjacent_land / same_district / ...)
  occasions[]: {date, context, source_pointer}
repeated_patterns[]:
  pattern_description: "Same witness at marriage and child's baptism"
  entities_involved[]
  source_pointers[]
  inference: what the pattern might indicate
```

**Acceptance Criteria**:
- All non-target persons extracted and classified
- Repeated appearances across records highlighted
- FAN patterns surfaced as potential indirect evidence

### 6.9 Conflict Detection and Resolution

#### FR-9.1: Conflict Detection

The system SHALL detect conflicts between assertions within an identity cluster.

**Conflict Types**:
- Date conflicts: Different birth/marriage/death dates
- Place conflicts: Different birthplace/residence/death place
- Relationship conflicts: Different stated parents/spouses/children
- Attribute conflicts: Different race, occupation, literacy stated
- Identity conflicts: Evidence suggesting cluster contains multiple individuals

**Conflict Structure**:
```
conflict_id: unique identifier
conflict_type: date | place | relationship | attribute | identity
dimension: specific attribute in conflict (birth_date, birthplace, father_name, ...)
assertions_in_conflict[]:
  assertion_id
  value_stated
  doc_id, source_type, information_type
  informant (if known)
  temporal_proximity: how close to event was recording
  independence: is this independent of other conflicting assertions
analysis: why conflict exists (informant memory, derivative error, different individuals, ...)
resolution_status: Resolved | Deferred
resolution_argument: (if Resolved) explanation of preponderance decision
required_future_work: (if Deferred) what would resolve the conflict
```

**Acceptance Criteria**:
- All conflicts detected and documented
- No conflicts silently ignored
- Conflict structure supports resolution analysis

#### FR-9.2: Conflict Resolution

The system SHALL apply preponderance principles to resolve conflicts where evidence warrants.

**Preponderance Principles** (in order of typical weight):

1. **Temporal proximity**: Recording closer to event generally more reliable than later recollection
2. **Informant knowledge**: Primary information over Secondary; participant over bystander
3. **Source independence**: Multiple independent sources agreeing outweigh single source
4. **Source type**: Original source data over Derivative copying errors
5. **Informant bias**: Disinterested informant over one with motive to misstate
6. **Internal consistency**: Source consistent with itself over self-contradicting source
7. **External consistency**: Source consistent with established facts over outlier

**Resolution Requirements**:
- Apply principles explicitly
- Weight evidence, don't just count sources
- Document reasoning transparently
- Acknowledge when resolution is judgment call

**Acceptance Criteria**:
- Resolved conflicts include explicit preponderance analysis
- Resolution argument traceable to specific evidence
- Close calls acknowledged as close calls

#### FR-9.3: Conflict Deferral

The system SHALL defer resolution when evidence is insufficient.

**Deferral Criteria**:
- Equal-quality sources irreconcilably conflict
- Critical records known to exist but not provided
- Resolution requires expertise beyond system capability
- Evidence genuinely ambiguous

**Deferral Structure**:
```
resolution_status: Deferred
deferral_reason: why resolution cannot be made
required_records[]: what would resolve it
required_expertise: if specialist knowledge needed
research_recommendation: specific next steps
```

**Acceptance Criteria**:
- Deferred conflicts do not block other analysis
- Deferral includes actionable research direction
- System does not force resolution when evidence insufficient

### 6.10 Conclusion Generation

#### FR-10.1: Research Question Formalization

The system SHALL formalize the research question before generating conclusions.

**Question Sources**:
- User-provided explicit question
- Inferred from user context ("I'm trying to find John's parents")
- Default question when neither provided: "What genealogically relevant facts can be established from these records about [named individuals]?"

**Question Structure**:
```
question_id: unique identifier
question_text: natural language statement
question_type: identity | parentage | marriage | death | residence | relationship | event | other
target_subjects[]: entity references
constraints: time range, jurisdiction, etc.
status: provisional | confirmed
```

**Acceptance Criteria**:
- Every analysis has an explicit research question
- Provisional questions flagged for user confirmation
- Evidence relevance assessed against question

#### FR-10.2: Evidence Sufficiency Assessment

The system SHALL assess whether evidence is sufficient for a GPS-informed conclusion.

**Sufficiency Criteria**:
- Is research reasonably exhaustive for the question? (Usually "not yet" with user-provided images only)
- Are sources adequately identified and cited?
- Is evidence thoroughly analyzed (source/information/evidence classifications)?
- Are conflicts resolved or explicitly deferred?
- Is a coherent conclusion possible?

**Assessment Output**:
```
exhaustiveness_assessment:
  status: sufficient | insufficient | not_assessable
  reasoning: what was searched, what known sources are missing
  critical_gaps[]: specific records that would strengthen conclusion
evidence_quality_assessment:
  direct_evidence_count: N
  indirect_evidence_count: M
  conflicting_evidence: present | absent
  conflict_resolution: complete | partial | deferred
conclusion_readiness:
  vehicle_appropriate: proof_statement | proof_summary | proof_argument | research_report_only
  confidence_warranted: proved | probable | possible | not_proved
```

**Acceptance Criteria**:
- Every analysis includes sufficiency assessment
- Gaps explicitly enumerated
- Appropriate conclusion vehicle selected

#### FR-10.3: Conclusion Drafting

The system SHALL draft a conclusion in the appropriate proof vehicle.

**Proof Statement** (when evidence is direct, consistent, and simple):
```
Single sentence or short paragraph:
"[Subject] was born [date] in [place], the [son/daughter] of [parents], as
established by [direct evidence 1] and [direct evidence 2]."
```

**Proof Summary** (when evidence requires some explanation):
```
1-3 paragraphs:
- State conclusion
- Summarize supporting evidence with characterizations
- Address minor conflicts with resolution reasoning
- Note limitations
```

**Proof Argument** (when evidence is indirect, complex, or conflicting):
```
Extended narrative:
- Introduction: research question and scope
- Evidence presentation: each source analyzed
- Correlation: how evidence fits together
- Conflict resolution: each conflict addressed
- Conclusion: reasoned determination with confidence level
- Limitations: what remains uncertain
```

**Research Report** (when evidence insufficient for conclusion):
```
- State research question
- Summarize evidence gathered
- Note conflicts unresolved
- Explain why conclusion not yet warranted
- Provide detailed research plan
```

**Acceptance Criteria**:
- Vehicle matches evidence strength
- All key evidence cited in conclusion
- Confidence level explicitly stated
- No over-conclusion beyond evidence warrant

### 6.11 Citation Generation

#### FR-11.1: Citation Element Capture

The system SHALL capture all elements needed for complete citation.

**Required Elements** (Evidence Explained model):
1. **Who**: Creator, author, informant, agency
2. **What**: Title, record type, description
3. **When**: Creation date, event date, access date
4. **Where**: Repository, publication, database, URL
5. **Where-within**: Page, entry, line, certificate number, deed book/page, image number

**Citation Structure**:
```
citation_id: unique identifier
doc_id: document reference
elements:
  creator: agency or person who created record
  title: record series or document type
  record_date: when record was created
  event_date: when event occurred (if different)
  jurisdiction: governmental authority
  repository: holding institution
  collection: within repository
  format: original | microfilm | digital_image | database_entry
  access_path: URL, film number, call number
  where_within:
    volume | book | page | entry | line | certificate_number | dwelling | family | etc.
  access_date: when user accessed digital copy
first_reference: full citation form
subsequent_reference: short citation form
```

**Acceptance Criteria**:
- All known elements captured
- Unknown elements explicitly marked
- Format distinguishes image-of-original from derivative

#### FR-11.2: Citation Formatting

The system SHALL format citations per Evidence Explained patterns.

**Example Formats by Record Type**:

*Census*:
```
1870 U.S. census, [State], [County], [Township/City], population schedule,
p. [page], dwelling [N], family [N], [Head of household]; digital image,
[Database], [URL] : [access date]; citing National Archives microfilm [film].
```

*Vital Record*:
```
[State], [County], [Record type], [Year], certificate [number], [Subject name];
[Repository], [City]; [access method if digital].
```

*Deed*:
```
[County], [State], Deed Book [volume]:[page], [Grantor] to [Grantee],
[date]; [Repository]; [access method].
```

**Acceptance Criteria**:
- Citations follow Evidence Explained patterns
- Both first-reference and subsequent-reference forms available
- Missing elements noted: "repository not provided; from user-supplied image"

### 6.12 Research Plan Generation

#### FR-12.1: Gap Identification

The system SHALL identify research gaps requiring further work.

**Gap Types**:
- Missing standard records (no census, no vital records, no probate)
- Incomplete time coverage (gap years in timeline)
- Unresolved conflicts requiring additional evidence
- Identity hypotheses needing confirmation
- FAN members not yet researched

**Gap Structure**:
```
gap_id: unique identifier
gap_type: missing_record | timeline_gap | unresolved_conflict | identity_uncertain | fan_unexplored
description: what is missing or uncertain
impact: how this gap affects conclusions
priority: critical | high | medium | low
rationale: why this priority
```

**Acceptance Criteria**:
- All gaps explicitly enumerated
- Impact on conclusions stated
- Priorities justified

#### FR-12.2: Record Recommendations

The system SHALL recommend specific records to pursue.

**Recommendation Categories**:
- Vital records: birth, marriage, death; delayed registrations
- Census: federal, state, territorial; mortality schedules
- Probate: wills, administrations, guardianships, inventories
- Land: deeds, mortgages, surveys, tax lists
- Court: civil, criminal, equity, naturalization
- Church: baptisms, marriages, burials, membership
- Military: service, pension, draft registration
- Newspapers: obituaries, legal notices, social columns
- Immigration: passenger lists, naturalization
- Local histories, city directories, biographies

**Recommendation Structure**:
```
recommendation_id: unique identifier
record_type: specific record category
target_person: who to search for
target_jurisdiction: where to search
target_date_range: when to search
expected_content: what this record might provide
priority: critical | high | medium | low
rationale: why this record might help
repository_suggestions[]: where to look
search_tips: specific search strategies
```

**Acceptance Criteria**:
- Recommendations specific enough to act on
- Priorities reflect research question needs
- Repository guidance included where possible

#### FR-12.3: Search Log Template

The system SHALL provide a search log template for tracking research.

**Template Structure**:
```
SEARCH LOG for [Research Question]
Subject: [Person/Family]

| Date | Repository | Collection/Database | Search Terms | Results | Citation |
|------|------------|---------------------|--------------|---------|----------|
| | | | | [Positive/Negative/Inconclusive] | |

Negative Search Documentation:
"Searched [repository] [collection] for [terms] covering [date range].
No relevant records found. Search date: [date]."
```

**Acceptance Criteria**:
- Template supports tracking both positive and negative results
- Negative search documentation structured for proof arguments
- Template exportable for user's research management

---

## 7. Data Model Specification

### 7.1 Core Entities

```
CaseFile
├── case_id: string
├── created_at: datetime
├── research_question: ResearchQuestion
├── document_packets[]: DocumentPacket[]
├── assertions[]: Assertion[]
├── entity_index: EntityIndex
├── timelines[]: Timeline[]
├── fan_graphs[]: FANGraph[]
├── conflicts[]: Conflict[]
├── conclusion: Conclusion
├── citations[]: Citation[]
├── research_plan: ResearchPlan
└── metadata: CaseMetadata

DocumentPacket
├── doc_id: string
├── doc_type: DocTypeEnum
├── images[]: ImageRecord[]
├── source_characterization: SourceCharacterization
├── transcription: Transcription
├── abstract: DocumentAbstract
├── assertions[]: assertion_id[]
└── citation: Citation

ImageRecord
├── image_id: string
├── filename: string
├── uploaded_at: datetime
├── user_notes: string
├── quality_assessment: QualityAssessment
├── segmentation: Segmentation
└── raw_data: binary | path

Assertion
├── assertion_id: string
├── subject_entity_id: string
├── predicate: PredicateEnum
├── value: AssertionValue
├── date_context: DateContext
├── place_context: PlaceContext
├── source_pointer: SourcePointer
├── information_type: InformationTypeEnum
├── evidence_type: EvidenceTypeEnum
├── confidence: ConfidenceScore
└── notes: string

Entity (Person | Place | Organization)
├── entity_id: string
├── entity_type: EntityTypeEnum
├── names[]: NameRecord[]
├── attributes[]: AttributeRecord[]
├── events[]: EventRecord[]
├── relationships[]: RelationshipRecord[]
└── identity_cluster_id: string

IdentityCluster
├── cluster_id: string
├── constituent_entities[]: entity_id[]
├── hypotheses[]: IdentityHypothesis[]
├── primary_name: string
├── merged_timeline: Timeline
└── resolution_status: ClusterStatusEnum

Conflict
├── conflict_id: string
├── conflict_type: ConflictTypeEnum
├── dimension: string
├── assertions_in_conflict[]: ConflictAssertion[]
├── analysis: string
├── resolution_status: ResolutionStatusEnum
├── resolution_argument: string
└── required_future_work: string

Conclusion
├── conclusion_id: string
├── research_question_id: string
├── vehicle: ProofVehicleEnum
├── confidence_level: ConfidenceLevelEnum
├── conclusion_text: string
├── supporting_assertions[]: assertion_id[]
├── conflicts_addressed[]: conflict_id[]
├── scope_notes: string
└── limitations: string[]
```

### 7.2 Enumeration Types

```
DocTypeEnum: vital_birth | vital_marriage | vital_death | vital_delayed |
             census_federal | census_state | census_mortality |
             probate_will | probate_administration | probate_inventory |
             land_deed | land_mortgage | land_survey |
             court_civil | court_criminal | court_naturalization |
             church_baptism | church_marriage | church_burial |
             military_service | military_pension | military_draft |
             immigration_passenger | newspaper_obituary |
             correspondence | photograph | other | unknown

SourceTypeEnum: Original | Derivative | Authored

InformationTypeEnum: Primary | Secondary | Indeterminate

EvidenceTypeEnum: Direct | Indirect | Negative

ConfidenceLevelEnum: Proved | Probable | Possible | NotProved | Disproved

ProofVehicleEnum: ProofStatement | ProofSummary | ProofArgument | ResearchReport

ResolutionStatusEnum: Resolved | Deferred

EntityTypeEnum: Person | Place | Organization

ClusterStatusEnum: Confirmed | Probable | Uncertain | Split
```

### 7.3 Supporting Structures

```
SourcePointer
├── doc_id: string
├── image_id: string
├── region_bbox: [x1, y1, x2, y2]
├── line_ref: string
└── entry_ref: string

ConfidenceScore
├── score: float (0.0-1.0)
└── rationale: string

DateContext
├── date_value: string (ISO or range)
├── precision: day | month | year | decade | range | circa
├── as_stated: string
└── calculation_note: string

PlaceContext
├── as_stated: string
├── normalized: PlaceHierarchy
└── jurisdiction_note: string

PlaceHierarchy
├── country: string
├── state_province: string
├── county_parish: string
├── town_district: string
├── address: string
└── coordinates: [lat, lon]

AssertionValue
├── as_stated: string
├── normalized: any
├── normalization_confidence: float
└── alternate_readings[]: string[]

QualityAssessment
├── orientation: upright | rotated_90 | rotated_180 | rotated_270
├── skew_degrees: float
├── blur_level: none | slight | moderate | severe
├── contrast: good | fair | poor
├── completeness: complete | cropped | partial
├── damage: none | minor | moderate | severe
├── handwriting_density: typed | sparse_handwriting | dense_handwriting
├── language: string
└── needs_better_copy: boolean

Segmentation
├── regions[]: SegmentRegion[]
└── reading_order[]: region_id[]

SegmentRegion
├── region_id: string
├── region_type: header | form_field | body | table | margin | signature | seal
├── bbox: [x1, y1, x2, y2]
└── content_preview: string
```

---

## 8. Processing Pipeline

### 8.1 Pipeline Overview

```
┌─────────────────────────────────────────────────────────────────────────┐
│                              INPUT                                       │
│  Images[] + UserGoal (optional)                                         │
└─────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────┐
│  PHASE 0: INITIALIZATION                                                │
│  Create CaseFile, formalize research question                           │
└─────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────┐
│  PHASE 1: IMAGE INTAKE & QUALITY CONTROL                                │
│  Assess quality, rotate/deskew, segment regions                         │
└─────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────┐
│  PHASE 2: DOCUMENT GROUPING                                             │
│  Cluster images into DocumentPackets, assign doc_ids                    │
└─────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────┐
│  PHASE 3: DOCUMENT IDENTIFICATION                                       │
│  Determine doc_type, extract context, classify source type              │
└─────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────┐
│  PHASE 4: TRANSCRIPTION                                                 │
│  Verbatim transcription with uncertainty markers and where-within       │
└─────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────┐
│  PHASE 5: ABSTRACTION                                                   │
│  Extract structured fields, normalize with dual-value retention         │
└─────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────┐
│  PHASE 6: ASSERTION ATOMIZATION                                         │
│  Create atomic claims with source/information/evidence classification   │
└─────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────┐
│  PHASE 7: ENTITY RESOLUTION                                             │
│  Extract entities, generate identity hypotheses, build clusters         │
└─────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────┐
│  PHASE 8: CORRELATION                                                   │
│  Build timelines, locality models, FAN graphs                           │
└─────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────┐
│  PHASE 9: CONFLICT DETECTION & RESOLUTION                               │
│  Identify conflicts, apply preponderance, resolve or defer              │
└─────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────┐
│  PHASE 10: EVIDENCE SYNTHESIS                                           │
│  Assess sufficiency, build evidence matrix, select proof vehicle        │
└─────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────┐
│  PHASE 11: CONCLUSION WRITING                                           │
│  Draft conclusion in appropriate vehicle with scope notes               │
└─────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────┐
│  PHASE 12: CITATION GENERATION                                          │
│  Complete citations with all known elements                             │
└─────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────┐
│  PHASE 13: RESEARCH PLAN                                                │
│  Identify gaps, recommend records, provide search log template          │
└─────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────┐
│  PHASE 14: PRIVACY REVIEW                                               │
│  Apply living-person protections, flag sensitive content                │
└─────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                              OUTPUT                                      │
│  CaseFile (structured) + Human-readable narrative report                │
└─────────────────────────────────────────────────────────────────────────┘
```

### 8.2 Phase Dependencies

| Phase | Requires | Produces |
|-------|----------|----------|
| 0: Initialization | Input images, user goal | CaseFile shell, research question |
| 1: Image Intake | Raw images | ImageRecords with quality assessments |
| 2: Grouping | ImageRecords | DocumentPackets (empty) |
| 3: Identification | DocumentPackets | doc_type, context, source characterization |
| 4: Transcription | Segmented images | Verbatim text with pointers |
| 5: Abstraction | Transcription | Structured fields, normalized values |
| 6: Atomization | Abstract | Assertions with classifications |
| 7: Entity Resolution | Assertions | Entities, identity clusters |
| 8: Correlation | Entities, clusters | Timelines, locality, FAN graphs |
| 9: Conflict Resolution | Assertions, clusters | Conflicts with resolutions/deferrals |
| 10: Synthesis | All above | Evidence matrix, vehicle selection |
| 11: Conclusion | Synthesis | Draft conclusion text |
| 12: Citations | Documents, pointers | Formatted citations |
| 13: Research Plan | Gaps, conflicts | Recommendations, search log |
| 14: Privacy Review | All output | Redacted/flagged output |

### 8.3 Error Recovery Paths

Each phase includes error handling that allows the pipeline to continue:

| Phase | Potential Failure | Recovery |
|-------|-------------------|----------|
| 1: Image Intake | Unreadable image | Flag "needs_better_copy"; continue with readable portions |
| 2: Grouping | Uncertain clustering | Create separate packets; note "possibly related" |
| 3: Identification | Unknown doc_type | Mark "unknown"; use generic extraction |
| 4: Transcription | Illegible text | Use uncertainty markers; continue |
| 5: Abstraction | Unparseable format | Extract what's possible; flag gaps |
| 6: Atomization | Ambiguous statement | Create multiple assertions with alternates |
| 7: Entity Resolution | Unresolvable identity | Maintain separate clusters |
| 8: Correlation | Insufficient data | Note gaps in timeline/FAN |
| 9: Conflict Resolution | Irreconcilable conflict | Defer with research recommendation |
| 10: Synthesis | Insufficient evidence | Select research_report vehicle |
| 11: Conclusion | Cannot conclude | State what can and cannot be determined |

---

## 9. Evidence Analysis Framework

### 9.1 The Three-Layer Model (Mandatory Application)

Every piece of information processed by the system MUST be analyzed through the three-layer model. This is not optional.

#### Layer 1: Source Classification

**Question**: What is this container and how did it come into existence?

| Classification | Criteria | Examples |
|----------------|----------|----------|
| **Original** | First recording; created at or near the time of the event by someone with reason to know | Church register entry made by minister at baptism; deed recorded by county clerk at time of sale; diary entry written that day |
| **Derivative** | Copy, transcription, abstract, extract, or reproduction of another record | Microfilm of original register; published deed abstracts; database index entry; certified copy of certificate |
| **Authored** | Narrative or compilation created from other sources | County history chapter; compiled genealogy; lineage society application |

**Classification Process**:
1. Identify the record's purpose and creation context
2. Determine if this is the first recording or a copy/compilation
3. If derivative, trace the chain back to original where possible
4. Document the classification with reasoning

#### Layer 2: Information Classification

**Question**: How did the informant know this specific fact?

| Classification | Criteria | Examples |
|----------------|----------|----------|
| **Primary** | Informant had firsthand knowledge—direct witness or participant | Mother reporting newborn's birth date; groom providing his own age; physician certifying cause of death |
| **Secondary** | Informant reporting what they heard, read, or were told | Adult child reporting deceased parent's birthplace; census informant reporting neighbor's age |
| **Indeterminate** | Informant's relationship to the fact cannot be determined | Census data when household respondent unknown; unsigned records |

**Classification Process**:
1. Identify who provided this specific piece of information (not just who signed the document)
2. Determine that person's relationship to the fact stated
3. Consider temporal proximity—how long after the event?
4. Apply appropriate classification with reasoning
5. Note: Same document often contains multiple information types

#### Layer 3: Evidence Classification

**Question**: How does this information relate to my research question?

| Classification | Criteria | Examples |
|----------------|----------|----------|
| **Direct** | Explicitly answers the research question without additional reasoning | Birth certificate stating parents' names answers "Who were the parents?" |
| **Indirect** | Contributes to answering but requires inference or combination with other evidence | Consistent co-residence across censuses suggests family relationship |
| **Negative** | Meaningful absence of expected information after demonstrated search | Target not in tax list where property ownership documented |

**Classification Process**:
1. State the research question explicitly
2. Determine if the information directly answers the question
3. If not direct, assess whether it contributes through inference
4. For negative evidence, document the search scope and expected finding
5. Note: Same information may be different evidence types for different questions

### 9.2 Information Type Assessment Matrix

For each document type, common information elements and their typical classifications:

#### Death Certificate

| Information Element | Typical Info Type | Rationale |
|---------------------|-------------------|-----------|
| Date of death | Primary | Attending physician present or near time |
| Place of death | Primary | Observable by certifier |
| Cause of death | Primary | Professional medical determination |
| Decedent's birth date | Secondary | Informant reporting from memory/hearsay |
| Decedent's birthplace | Secondary | Informant reporting from memory/hearsay |
| Parents' names | Secondary | Informant reporting from memory/hearsay |
| Decedent's age | Secondary/Indeterminate | Calculated or estimated |
| Marital status | Indeterminate | Source of information often unclear |
| Occupation | Indeterminate | May be outdated; source unclear |

#### Census Record

| Information Element | Typical Info Type | Rationale |
|---------------------|-------------------|-----------|
| Presence in household | Primary | Enumerator's direct observation |
| Relationship to head | Indeterminate | Reported by household informant (unknown who) |
| Age | Indeterminate | Often estimated; informant unknown |
| Birthplace | Secondary | Informant reporting others' origins |
| Occupation | Indeterminate | Reported; accuracy varies |
| Literacy | Primary/Indeterminate | May be tested or reported |

#### Marriage Record

| Information Element | Typical Info Type | Rationale |
|---------------------|-------------------|-----------|
| Marriage date | Primary | Officiant present |
| Marriage place | Primary | Officiant present |
| Names of parties | Primary | Parties present (usually) |
| Ages of parties | Primary/Secondary | Self-reported; may be inflated/deflated |
| Residences | Primary | Self-reported at time |
| Parents' names | Secondary | Parties reporting |
| Witnesses present | Primary | Direct observation |

### 9.3 Preponderance Analysis Framework

When conflicts arise, apply this structured analysis:

#### Step 1: Characterize Each Conflicting Assertion

For each assertion in conflict, document:

```
Assertion: [exact claim]
Source: [doc_id] — [SourceType]
Information: [InformationType] — informant: [who, if known]
Temporal proximity: [time from event to recording]
Independence: [Is this independent of other conflicting assertions?]
Derivative risk: [How many copy generations from original?]
Bias assessment: [Did informant have motive to misstate?]
```

#### Step 2: Apply Preponderance Principles

Evaluate each factor:

| Factor | Assertion A | Assertion B | Favors |
|--------|-------------|-------------|--------|
| Temporal proximity | | | |
| Informant knowledge | | | |
| Source independence | | | |
| Original vs. derivative | | | |
| Informant bias | | | |
| Internal consistency | | | |
| External consistency | | | |

#### Step 3: Determine Resolution or Deferral

- **Resolve** if preponderance clearly favors one side AND reasoning is documentable
- **Defer** if evidence is balanced, critical records missing, or resolution requires expertise beyond available

#### Step 4: Document Reasoning

Write explicit resolution argument or deferral rationale that a third party could evaluate.

---

## 10. Quality Standards

### 10.1 GPS Compliance Checklist

Before any output is finalized, verify:

#### Element 1: Reasonably Exhaustive Research
- [ ] All provided images analyzed
- [ ] Research gaps explicitly identified
- [ ] Next-step records recommended
- [ ] Search scope limitations acknowledged

#### Element 2: Complete, Accurate Citations
- [ ] Every assertion has source pointer
- [ ] Citations include all five elements (who, what, when, where, where-within)
- [ ] Unknown elements explicitly marked
- [ ] Access pathway documented

#### Element 3: Analysis and Correlation
- [ ] Source type classified for each document
- [ ] Information type classified for each assertion
- [ ] Evidence type classified against research question
- [ ] Timeline constructed
- [ ] FAN patterns identified

#### Element 4: Conflict Resolution
- [ ] All conflicts detected
- [ ] Each conflict characterized (both sides)
- [ ] Resolution or deferral documented
- [ ] Reasoning explicit and traceable

#### Element 5: Coherent Written Conclusion
- [ ] Research question stated
- [ ] Appropriate proof vehicle selected
- [ ] Confidence level explicit
- [ ] Limitations acknowledged
- [ ] Reasoning transparent

### 10.2 Terminology Compliance

The system MUST adhere to GPS terminology:

| NEVER Say | ALWAYS Say | Context |
|-----------|------------|---------|
| "Primary source" | "Original source" | When describing the container/record |
| "Secondary source" | "Derivative source" | When describing copies/transcriptions |
| "Primary evidence" | "Direct evidence" | When evidence explicitly answers question |
| "Secondary evidence" | "Indirect evidence" | When evidence requires inference |

"Primary" and "Secondary" are ONLY used for INFORMATION, describing informant's knowledge proximity.

### 10.3 Anti-Fabrication Standards

The system SHALL NOT:

- Invent text for illegible portions
- Create sources that don't exist
- Generate citations without corresponding documents
- Present inferences as established facts
- Merge identities without documented correlation
- Resolve conflicts without explicit reasoning
- Claim exhaustive research when only analyzing provided images

### 10.4 Accuracy Targets

| Metric | Target | Measurement |
|--------|--------|-------------|
| Transcription accuracy (legible text) | >95% character accuracy | Comparison to expert transcription |
| Document type identification | >85% correct classification | Against labeled test set |
| Source type classification | >95% correct | Expert review |
| Information type classification | >90% correct | Expert review |
| Conflict detection | >95% recall | All conflicts identified |
| False positive rate (identity merging) | <5% | No incorrect merges |

### 10.5 Output Validation

Each output MUST pass:

1. **Traceability check**: Every claim traces to source pointer
2. **Terminology check**: No forbidden terminology used
3. **Consistency check**: No internal contradictions
4. **Completeness check**: All required output sections present
5. **Confidence calibration check**: Conclusion strength matches evidence strength

---

## 11. Error Handling and Edge Cases

### 11.1 Image Quality Failures

#### Scenario: Completely Illegible Document

**System Response**:
- Create DocumentPacket with doc_id
- Set quality_assessment.damage = severe
- Set needs_better_copy = true
- Do NOT attempt transcription fabrication
- Output: "Document [doc_id] could not be analyzed due to [quality issue]. A higher-resolution or better-preserved copy is needed."

#### Scenario: Partially Legible Document

**System Response**:
- Transcribe legible portions
- Mark illegible portions with `[illegible]` or `[illegible, ~N words]`
- Note affected information in abstract
- Proceed with available data
- Flag confidence reduction in affected assertions

#### Scenario: Multi-Language Document

**System Response**:
- Detect non-English content
- Transcribe if Latin alphabet (noting language)
- Note: "Translation required for full analysis"
- Extract what is extractable without translation
- Recommend translation before GPS-informed analysis

### 11.2 Document Identification Failures

#### Scenario: Unknown Document Type

**System Response**:
- Set doc_type = unknown
- Apply generic extraction (names, dates, places, relationships)
- Note: "Document type could not be determined; generic extraction applied"
- User may provide document type to enable specialized extraction

#### Scenario: Mislabeled/Deceptive Document

**System Response**:
- Note discrepancy: "Document labeled as [X] but appears to be [Y]"
- Analyze based on actual content
- Flag for user verification
- Consider both interpretations if genuinely ambiguous

### 11.3 Identity Resolution Failures

#### Scenario: Same-Name Different-Person

**System Response**:
- Maintain separate identity clusters
- Document distinguishing evidence
- Note: "Multiple individuals named [Name] identified; maintained as separate pending distinguishing evidence"
- Recommend records that would distinguish

#### Scenario: Name Variation Uncertainty

**System Response**:
- Create hypothesis linking variants
- Score hypothesis with evidence features
- If score < threshold, maintain separate entities with "possible same person" link
- Document what would confirm or refute

#### Scenario: Complex Family Structures

**System Response**:
- Model actual stated relationships without assuming nuclear family
- Handle blended families, multiple marriages, adopted/foster children
- Note when records use ambiguous terms ("mother" might be biological, step-, or foster)
- Avoid imposing modern family concepts on historical records

### 11.4 Conflict Scenarios

#### Scenario: Irreconcilable Conflict

**System Response**:
- Document both positions fully
- Apply preponderance analysis
- If genuinely balanced: defer with explicit statement
- Note: "Evidence is evenly balanced between [X] and [Y]. Resolution requires [specific records]."

#### Scenario: Self-Contradicting Source

**System Response**:
- Note internal contradiction
- Treat each claim separately
- Reduce confidence for both
- Consider whether contradiction invalidates source reliability

#### Scenario: Fraud/Forgery Indicators

**System Response**:
- Note suspicious elements (anachronistic content, inconsistent handwriting, etc.)
- Do NOT accuse fraud definitively
- Output: "This document contains elements inconsistent with its claimed date/origin: [specifics]. Expert authentication recommended before relying on this source."

### 11.5 Privacy Edge Cases

#### Scenario: Potentially Living Person

**System Response**:
- Apply conservative interpretation (if could be living, treat as living)
- Redact identifying details in output
- Note: "Potentially living individual; identifying details withheld"
- Offer full details only with user confirmation of privacy context

#### Scenario: Sensitive Historical Information

**System Response**:
- Flag content type: "Contains sensitive information regarding [category]"
- Offer content warning: "Would you like a general summary first, or specific details?"
- Provide historical context for sensitive records (institutionalization, criminal records)
- Never make moral judgments about historical individuals

---

## 12. Privacy and Ethical Requirements

### 12.1 Living Person Protection

#### Definition of "Potentially Living"

A person is treated as potentially living if:
- Born less than 100 years ago AND death not documented, OR
- Death not documented AND age at last record would make current age <100, OR
- User indicates person may be living, OR
- Any uncertainty exists

#### Protected Information (Never Disclosed Without Explicit Permission)

- Current addresses or contact information
- Social Security numbers or government ID numbers
- Current employment details
- Financial information
- Medical/health information
- Information enabling identity theft

#### Permitted Information (With Appropriate Context)

- Historical vital events (birth, marriage) if person clearly deceased
- Information already in public domain
- Information user explicitly states is for private use

### 12.2 Sensitive Content Handling

#### Content Categories Requiring Care

| Category | Examples | Handling Protocol |
|----------|----------|-------------------|
| Unknown parentage | NPEs, adoptions, donor conception, illegitimacy records | Content warning; user controls disclosure pace |
| Criminal history | Arrests, convictions, incarceration | Historical context; avoid moral judgment |
| Institutionalization | Asylums, poorhouses, orphanages | De-stigmatizing framing; historical context |
| Cause of death | Suicide, violence, stigmatized disease | Sensitive framing; content warning if graphic |
| Racial classification | Historical racial categories | Note as "race as recorded"; historical context |
| Enslavement records | Inventories, bills of sale | Acknowledge human dignity; historical context |

#### Handling Protocol

1. **Detection**: System identifies sensitive content categories
2. **Flagging**: Output includes content advisory
3. **Staging**: Offer general summary before specific details
4. **Context**: Provide historical framing for outdated/harmful categories
5. **Respect**: Honor user's choice not to receive details

### 12.3 Cultural Competency

#### CARE Principles (Indigenous Data)

When records involve Indigenous peoples:
- **Collective Benefit**: Consider community interests, not just individual researcher
- **Authority to Control**: Acknowledge community rights over their data
- **Responsibility**: Note researcher accountability to communities
- **Ethics**: Respect community-defined ethical frameworks

#### Diverse Family Structures

Recognize and accurately model:
- Extended family households
- Chosen family and fictive kinship
- Polygamous families (where historically/legally present)
- Same-sex partnerships (historical and modern)
- Adoption, fostering, guardianship
- Community child-rearing practices

#### Naming Practices

Handle appropriately:
- Patronymics/matronymics (not surnames)
- Clan names
- Names that change at life stages
- Titles and honorifics
- Transliterated names
- Imposed names vs. chosen names

### 12.4 Ethical Boundaries

#### The System Will Not:

- Help identify living persons for harassment
- Assist in circumventing adoption privacy laws
- Generate "evidence" to support predetermined conclusions
- Validate genealogical claims without evidence (e.g., false heritage claims)
- Produce analysis intended to harm subjects or descendants

#### The System Will:

- Maintain intellectual honesty even when findings are unwelcome
- Acknowledge limitations and uncertainties
- Recommend professional help when appropriate
- Protect vulnerable individuals
- Respect user's choice to discontinue inquiry

---

## 13. Output Specifications

### 13.1 Structured Output (JSON Schema)

The system produces structured output conforming to the CaseFile schema (Section 7.1) for:
- Downstream processing
- Integration with genealogy software
- Database storage
- API responses

### 13.2 Human-Readable Narrative Report

In addition to structured data, the system produces a narrative report following this outline:

```markdown
# Genealogical Analysis Report

## Research Question
[Formal statement of the question being addressed]

## Documents Analyzed
[List of documents with brief descriptions and source characterizations]

## Transcriptions
[Full transcriptions organized by document, with uncertainty markers]

## Abstracts
[Structured extractions organized by document]

## Evidence Analysis

### Source Assessment
[Source type classifications with reasoning]

### Information Quality
[Information type classifications for key facts]

### Evidence Relevance
[Evidence type classifications against research question]

## Correlation Analysis

### Timeline
[Chronological arrangement of events]

### Locality Analysis
[Geographic patterns and movements]

### FAN Analysis
[Family, Associates, Neighbors patterns]

## Identity Analysis
[Entity resolution results, hypotheses, clusters]

## Conflicts and Resolution
[Each conflict with characterization and resolution/deferral]

## Conclusion
[Appropriate proof vehicle with confidence level]

### Scope Notes
[What was analyzed, what was not assessable]

### Limitations
[Gaps, uncertainties, caveats]

## Citations
[Complete citations for all documents]

## Research Plan

### Gaps Identified
[Specific gaps in evidence]

### Recommended Records
[Prioritized list with rationale]

### Search Log Template
[Ready-to-use tracking template]

---
*Analysis generated [date] using GPS-Grade Genealogical Record Analysis*
*This analysis is based solely on user-provided images and does not constitute exhaustive research*
```

### 13.3 Adaptive Output Formatting

Output depth adapts to user level:

| Component | Beginner | Intermediate | Advanced |
|-----------|----------|--------------|----------|
| Terminology | Define all terms | Define GPS terms | Assume knowledge |
| Transcription | Full with guides | Full | Full |
| Abstract | Explained | Standard | Compact |
| Evidence analysis | Step-by-step | Summarized | Tabular |
| Conclusion | Thorough explanation | Standard | Compact |
| Research plan | Highly detailed | Prioritized | Gap list only |

### 13.4 Export Formats

The system supports export in:
- JSON (full structured data)
- Markdown (narrative report)
- CSV (assertions table, evidence matrix)
- GEDCOM-compatible (where applicable)
- Plain text (transcriptions only)

---

## 14. Success Metrics

### 14.1 Accuracy Metrics

| Metric | Definition | Target | Measurement Method |
|--------|------------|--------|-------------------|
| Transcription accuracy | Character-level accuracy on legible text | >95% | Expert comparison |
| Document classification accuracy | Correct doc_type assignment | >85% | Labeled test set |
| Source type accuracy | Correct Original/Derivative/Authored | >95% | Expert review |
| Information type accuracy | Correct Primary/Secondary/Indeterminate | >90% | Expert review |
| Entity extraction recall | Named entities correctly identified | >95% | Expert annotation |
| Conflict detection recall | True conflicts identified | >95% | Expert review |
| Identity merge precision | Correct merges / all merges | >95% | Expert validation |
| Identity merge recall | Correct merges / true same-person pairs | >80% | Expert validation |

### 14.2 Quality Metrics

| Metric | Definition | Target |
|--------|------------|--------|
| GPS compliance rate | Outputs passing GPS checklist | >95% |
| Terminology compliance | No forbidden terminology | 100% |
| Citation completeness | Citations with all available elements | >95% |
| Conflict resolution quality | Expert-agreed resolutions | >85% |
| Research plan actionability | Recommendations deemed actionable | >90% |

### 14.3 User Experience Metrics

| Metric | Definition | Target |
|--------|------------|--------|
| Task completion rate | Users complete intended analysis | >85% |
| User satisfaction | Post-task satisfaction rating | >4.0/5.0 |
| Error recovery rate | Users successfully recover from errors | >90% |
| Level-appropriate calibration | Response matches user level | >85% |

### 14.4 Safety Metrics

| Metric | Definition | Target |
|--------|------------|--------|
| Fabrication rate | Fabricated content in output | 0% |
| Privacy violation rate | Unauthorized disclosure of protected info | 0% |
| Over-conclusion rate | Conclusions exceeding evidence warrant | <5% |
| Sensitive content handling | Appropriate handling of flagged content | 100% |

---

## 15. Implementation Guidance for Claude

### 15.1 Processing Approach

When implementing this PRD, Claude should:

1. **Process systematically through phases** — Do not skip phases; each builds on prior outputs

2. **Maintain explicit state** — Track current phase, processed documents, pending assertions, open conflicts

3. **Apply three-layer analysis to every information element** — This is not optional; it is the core methodology

4. **Never fabricate** — When uncertain, say so; when illegible, mark it; when evidence insufficient, acknowledge it

5. **Preserve uncertainty** — Resist the temptation to over-conclude; calibrated confidence is more valuable than false certainty

6. **Document reasoning** — Every classification, resolution, and conclusion should have traceable reasoning

7. **Respect terminology** — Internalize the GPS vocabulary; violations undermine credibility

### 15.2 Decision Framework

When facing analytical choices:

```
Is this fact stated or inferred?
├── Stated → extract and cite
└── Inferred → mark as inference with reasoning

Is this identity certain or hypothesized?
├── Certain (strong correlation) → merge clusters
└── Uncertain → maintain separate with hypothesis link

Is this conflict resolvable?
├── Clear preponderance → resolve with argument
└── Balanced/insufficient → defer with research direction

Is this conclusion warranted?
├── Direct, consistent evidence → proof statement
├── Some complexity/minor conflicts → proof summary
├── Indirect/major conflicts → proof argument
└── Insufficient evidence → research report only
```

### 15.3 Output Calibration

Match output to user needs:

- **Beginner**: Prioritize explanation and guidance over comprehensiveness
- **Intermediate**: Balance analysis with actionable next steps
- **Advanced**: Maximize information density; minimize scaffolding

When uncertain of user level, default to intermediate and adjust based on responses.

### 15.4 Error Communication

When things go wrong:

- **Acknowledge** the limitation clearly
- **Explain** what prevented full analysis
- **Provide** what can be provided
- **Recommend** how to overcome the limitation
- **Never** pretend the limitation doesn't exist

### 15.5 Self-Check Protocol

Before finalizing any output, verify:

- [ ] Did I apply three-layer analysis to all information?
- [ ] Did I use correct GPS terminology throughout?
- [ ] Did I cite sources for all claims?
- [ ] Did I identify all conflicts?
- [ ] Did I calibrate confidence appropriately?
- [ ] Did I protect living persons?
- [ ] Did I avoid fabrication?
- [ ] Did I provide actionable next steps?

---

## 16. Dependencies and Constraints

### 16.1 Input Dependencies

| Dependency | Requirement | Fallback |
|------------|-------------|----------|
| Image quality | Legible key text | Partial analysis with limitations noted |
| Image format | JPEG, PNG, TIFF, PDF | Report unsupported format |
| Complete document | Full document visible | Note cropping; analyze available |
| User context | Claimed persons, goals | Infer from content; use default question |
| Repository information | Where document was obtained | Note "repository not provided" |

### 16.2 Capability Constraints

| Constraint | Impact | Mitigation |
|------------|--------|------------|
| No external database access | Cannot verify against other records | Recommend specific searches to user |
| No legal authentication | Output not valid for legal proceedings | Clear disclaimer; recommend professionals |
| English-language processing | Limited non-English analysis | Note language; recommend translation |
| Historical hand recognition | Some scripts exceed capability | Note illegibility; don't fabricate |
| Single-session analysis | No persistent memory across sessions | Complete output each session |

### 16.3 Methodological Constraints

| Constraint | Requirement |
|------------|-------------|
| GPS compliance | All analysis follows GPS methodology |
| Evidence-based conclusions | No conclusions beyond evidence warrant |
| Explicit uncertainty | All uncertainty acknowledged |
| Transparent reasoning | All decisions documented |
| Privacy protection | Living persons protected |

### 16.4 Known Limitations

The system acknowledges these limitations in output:

- Analysis based solely on provided images; not exhaustive research
- Image quality affects transcription accuracy
- Identity resolution may require additional records
- Some conflicts may not be resolvable with provided evidence
- Historical context may affect interpretation
- AI analysis does not constitute expert authentication

---

## 17. Glossary

### GPS and Evidence Terms

| Term | Definition |
|------|------------|
| **Genealogical Proof Standard (GPS)** | The professional standard requiring reasonably exhaustive research, complete citations, thorough analysis, conflict resolution, and coherent written conclusion |
| **Original Source** | First recording of information, made at or near the time of the event |
| **Derivative Source** | Copy, transcription, abstract, or reproduction of another record |
| **Authored Source** | Narrative or compilation created from other sources |
| **Primary Information** | Information from someone with firsthand knowledge |
| **Secondary Information** | Information from someone reporting what they heard or were told |
| **Indeterminate Information** | Information where informant's knowledge cannot be determined |
| **Direct Evidence** | Information that explicitly answers the research question |
| **Indirect Evidence** | Information that requires inference to answer the research question |
| **Negative Evidence** | Meaningful absence of expected information |
| **Preponderance** | The weight of evidence favoring one conclusion over another |
| **Proof Statement** | Single-sentence conclusion for simple, consistent evidence |
| **Proof Summary** | Brief narrative for evidence requiring some explanation |
| **Proof Argument** | Extended narrative for complex or conflicting evidence |

### Technical Terms

| Term | Definition |
|------|------------|
| **Assertion** | A single, atomic claim about a subject with full provenance |
| **Where-within** | Precise location within a document (page, line, entry) |
| **Source Pointer** | Reference linking an assertion to exact document location |
| **Identity Cluster** | Collection of entity records believed to represent the same individual |
| **Identity Hypothesis** | Scored proposal that two entities represent the same person |
| **FAN** | Family, Associates, Neighbors — the cluster surrounding a research subject |
| **Document Packet** | A logical document potentially spanning multiple images |
| **Confidence Score** | Numerical rating (0.0-1.0) of certainty with rationale |

### Record Types

| Term | Definition |
|------|------------|
| **Vital Record** | Government-issued birth, marriage, death record |
| **Census** | Official population enumeration |
| **Probate** | Court records dealing with estates of deceased persons |
| **Deed** | Legal document transferring property ownership |
| **Church Record** | Records created by religious institutions (baptism, marriage, burial) |

---

## 18. Appendices

### Appendix A: Evidence Table Template

```
| # | Source | Claim | Source Type | Info Type | Informant | Evidence Type | Confidence | Notes |
|---|--------|-------|-------------|-----------|-----------|---------------|------------|-------|
|   |        |       | O/D/A       | P/S/I     |           | D/I/N         | 0.0-1.0    |       |
```

### Appendix B: Conflict Resolution Template

```
CONFLICT: [Dimension in conflict, e.g., "Birth year of John Smith"]

ASSERTION A:
- Claim: [exact statement]
- Source: [doc_id] — [Source Type]
- Information: [Info Type] — Informant: [who]
- Temporal proximity: [years from event]
- Independence: [yes/no from other assertions]

ASSERTION B:
- Claim: [exact statement]
- Source: [doc_id] — [Source Type]
- Information: [Info Type] — Informant: [who]
- Temporal proximity: [years from event]
- Independence: [yes/no from other assertions]

PREPONDERANCE ANALYSIS:
| Factor | A | B | Favors |
|--------|---|---|--------|
| Temporal proximity | | | |
| Informant knowledge | | | |
| Source independence | | | |
| Original vs. derivative | | | |
| Informant bias | | | |

RESOLUTION: [ ] Resolved → [conclusion] with reasoning: [explanation]
             [ ] Deferred → [why] — Would resolve with: [records needed]
```

### Appendix C: Search Log Template

```
SEARCH LOG
Research Question: ________________________________
Subject: _________________________________________

| Date | Repository | Collection | Search Terms | Date Range | Result | Citation |
|------|------------|------------|--------------|------------|--------|----------|
|      |            |            |              |            | P/N/I  |          |

P = Positive (found relevant record)
N = Negative (searched, nothing found)
I = Inconclusive (partial results, needs follow-up)

NEGATIVE SEARCH DOCUMENTATION:
"Searched [repository], [collection], for [subject] using [terms], covering [date range].
No relevant records found. Search conducted [date]."
```

### Appendix D: Citation Format Examples

**Census (Federal)**:
```
1870 U.S. census, Ashe County, North Carolina, population schedule, Jefferson Township,
p. 12, dwelling 89, family 91, John Smith household; digital image, Ancestry.com
(https://www.ancestry.com : accessed 15 Jan 2026); citing NARA microfilm M593, roll 1125.
```

**Vital Record (Birth)**:
```
North Carolina, Ashe County, Register of Births, vol. 1, p. 45, no. 234, Mary Jane Smith,
15 Mar 1892; Ashe County Register of Deeds, Jefferson, North Carolina.
```

**Deed**:
```
Ashe County, North Carolina, Deed Book 12:345, John Smith to William Jones, 1 Jun 1875;
Ashe County Register of Deeds, Jefferson, North Carolina; digital image, FamilySearch
(https://www.familysearch.org : accessed 15 Jan 2026).
```

**Church Record**:
```
St. Mary's Catholic Church (Jefferson, Ashe County, North Carolina), Baptismal Register,
vol. 2, p. 78, entry for Mary Jane Smith, 20 Mar 1892; Diocese of Charlotte Archives,
Charlotte, North Carolina.
```

**Newspaper Obituary**:
```
"John Smith," obituary, Ashe County Tribune (Jefferson, North Carolina), 15 Jun 1920, p. 3,
col. 2; digital image, Newspapers.com (https://www.newspapers.com : accessed 15 Jan 2026).
```

---

## Document History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | January 2026 | Steve Little / Claude Opus 4.5 | Initial PRD |

---

*This PRD is designed to follow the Genealogical Proof Standard as defined by the Board for Certification of Genealogists and incorporates the evidence analysis framework from Elizabeth Shown Mills' Evidence Explained.*

*Released under Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International (CC BY-NC-SA 4.0)*
