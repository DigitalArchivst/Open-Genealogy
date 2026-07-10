# Image Analysis

Prompts for extracting information from historical photographs, documents, and other visual materials relevant to genealogical research.

## When to Use These Prompts

- Analyzing family photographs (portraits, group photos, candid shots)
- Examining historical images (FSA collections, newspaper clippings, postcards)
- Interpreting visual details in document scans (letterheads, seals, stamps, watermarks)
- Dating and locating unidentified photographs
- Extracting text from image edges, borders, and film markings

## Recommended Prompt

> [!CAUTION]
> The four-model companion PDF is a preserved historical teaching artifact, not a controlled comparison. Its winner and categorical no-fabrication conclusions are withdrawn pending comparable reruns and claim-level ground truth. Read the [methodology note](deep-look-v2-four-models-methodology-note.md) before using it.

| File | Description | Status |
| --- | --- | --- |
| [deep-look-v2.md](deep-look-v2.md) | 10-layer forensic image analysis with structured data extraction and catalog record | **recommended** |
| [Deep-Look-v2-Four-Models-Full-Results.pdf](Deep-Look-v2-Four-Models-Full-Results.pdf) | Historical four-output report with full outputs and a context-tainted scoring matrix | preserved companion |
| [Four-model methodology note](deep-look-v2-four-models-methodology-note.md) | Current errata, withdrawn claims, teaching scope, and rerun requirements | **read first** |
| [universal-image-analysis-v3.md](universal-image-analysis-v3.md) | 9-layer forensic image analysis protocol | previous version |

Rights and reuse, including the Bower photograph exclusion: [RIGHTS.md](RIGHTS.md).

## How It Works

Deep Look v2 guides the AI through ten sequential analytical layers:

1. **First Impression** — what the image shows at a glance
2. **Physical & Technical Properties** — medium, process, condition, color, materials
3. **Lighting** — source, direction, quality, shadows, intentional shaping
4. **Composition & Design** — layout, composition principles, elements, typography, palette
5. **Text & Inscriptions** — complete transcription including edges, stamps, watermarks, film markings, multi-hand analysis, archaic term translation
6. **Deep Description** — people, places, objects, symbols, and what is absent
7. **Structured Data Extraction** — facts extracted into tables (people, dates/locations, other data) with confidence ratings
8. **Context & Provenance** — dating, geography, purpose, artistic lineage, authenticity
9. **Interpretation & Research Leads** — story, values, significance, genealogical leads (record sets, repositories, search strategies)
10. **Report & Catalog Record** — narrative synthesis, conclusion, archival catalog entry with keywords and alt-text

A **Quality Gate** verifies completeness (the "Recreation Test"), flags uncertainties, and suggests next steps.

## Origin

Deep Look v2 was created by merging two complementary prompts through an expert council process:

- **Universal Image Interrogation Protocol v2** — strong on visual description, composition, and interpretive analysis
- **Historical Document Analysis Framework** — strong on structured data extraction, metadata, and cataloging

The merge was informed by Universal Image Analysis v3 (the previous recommended prompt in this folder), which contributed lighting analysis, composition principles, "what is absent" analysis, artistic lineage, and narrative synthesis. A five-expert council (archival scientist, art historian, genealogist, prompt engineer, information architect) reconciled priorities and reviewed the final structure. The prompt was then field-tested in the preserved four-output exercise. Because that exercise used unequal context and lacks claim-level ground truth, it does not confirm that Layer 7 improves observational accuracy; it remains useful for teaching and for forming hypotheses to test in a controlled rerun.

## Related

- [Photo Restoration](../photo-restoration/) — for restoring degraded photographs (different purpose: restoration vs. analysis)
- [Transcription](../transcription/) — for handwritten document transcription (text-focused rather than image-focused)
- [Writing Tools: image-citation-builder-v2.md](../writing-tools/image-citation-builder-v2.md) — for creating citations for images after analysis
