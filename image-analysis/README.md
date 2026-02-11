# Image Analysis

Prompts for extracting information from historical photographs, documents, and other visual materials relevant to genealogical research.

## When to Use These Prompts

- Analyzing family photographs (portraits, group photos, candid shots)
- Examining historical images (FSA collections, newspaper clippings, postcards)
- Interpreting visual details in document scans (letterheads, seals, stamps, watermarks)
- Dating and locating unidentified photographs
- Extracting text from image edges, borders, and film markings

## Recommended Prompt

| File | Description | Status |
|------|-------------|--------|
| [universal-image-analysis-v3.md](universal-image-analysis-v3.md) | 9-layer forensic image analysis protocol | **recommended** |

## How It Works

The Universal Image Analysis Protocol v3 guides the AI through nine sequential analytical layers:

1. **First Impression & Overview** — what the image shows at a glance
2. **Physical & Technical Properties** — medium, quality, color, materials
3. **Lighting Analysis** — source, direction, mood, intentional shaping
4. **Visual Composition & Design** — layout, elements, typography, color palette
5. **Text & Inscriptions** — complete transcription of all visible text including edges, stamps, and film markings
6. **Content & Subject Matter** — people, places, objects, symbols, and what is absent
7. **Context, Provenance & Historical Reasoning** — dating, location, purpose, creator intent
8. **Interpretive Analysis & Genealogical Significance** — story, cultural values, research leads
9. **Report & Conclusion** — narrative synthesis, summary, and next steps

A **Final Quality Gate** verifies completeness (the "Recreation Test") and enforces uncertainty discipline.

## Origin

Version 3 was synthesized from a feature matrix comparison of three earlier image analysis prompts — each strong in different areas — using the "super-prompt" technique of combining best-in-class features. The comparison evaluated 60 characteristics across the three source prompts. Notable addition in v3: Layer 5 explicitly examines edges, borders, stamps, watermarks, and film markings — features that earlier prompts consistently missed.

## Related

- [Photo Restoration](../photo-restoration/) — for restoring degraded photographs (different purpose: restoration vs. analysis)
- [Transcription](../transcription/) — for handwritten document transcription (text-focused rather than image-focused)
- [Writing Tools: image-citation-builder-v2.md](../writing-tools/image-citation-builder-v2.md) — for creating citations for images after analysis
