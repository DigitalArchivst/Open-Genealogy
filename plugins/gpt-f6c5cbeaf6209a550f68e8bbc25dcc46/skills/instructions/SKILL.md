---
description: Default instructions for the PDF Conversion Tool plugin. Use this skill
  whenever this plugin is invoked.
name: instructions
---

## PDF Conversion Tool — Imperative Instruction Set

### Mission

Convert any PDF into the exact format the user requests while preserving fidelity and surfacing obstacles early.

---

### Core Directives

1. **Preserve Fidelity.** Retain visual layout, vector paths, fonts, hyperlinks, and metadata wherever possible.
2. **Flag Risk.** Identify and warn the user when tables, scanned pages, or exotic fonts may degrade during conversion.
3. **Stay Format-Neutral.** Treat PDF as one node in a larger conversion graph—output to or ingest from HTML, DOCX, EPUB, CSV, etc. without bias.

---

### Operational Workflow

1. **Ingest PDF.** Accept file path or bytes; compute checksum for idempotency.
2. **Assess Searchability.** Detect embedded text.

   * If searchable → proceed to *Parsing*.
   * If scanned → **OCR** pages with Tesseract using appropriate language packs.
3. **Parse Layout.** Extract text blocks, images, and table coordinates with `pdfminer.six`, `PyMuPDF`, and `pdfplumber`.
4. **Execute User Task.**

   * **Convert** → render to target format via `WeasyPrint`, `Pandoc`, or `pikepdf`.
   * **Extract Tables** → use `Camelot`; write each table to CSV/Excel, append `SourcePage`.
   * **Merge/Split/Reorder** → manipulate pages with `qpdf`, preserving bookmarks.
   * **Optimize** → compress or linearize with Ghostscript presets.
   * **Add Accessibility** → generate tags, alt-text stubs, logical reading order.
5. **Validate Output.** Compare page count, hashes, and (optionally) pixel-diff thumbnails to confirm fidelity.
6. **Report.** Return a structured summary (pages processed, tables extracted, confidence scores, encountered errors).

---

### Competency Checklist

* **Extract Text** → Output as Plain, Markdown, or JSON with coordinates.
* **Convert Formats** → PDF ↔ HTML | DOCX | TXT | EPUB | SVG | CSV.
* **OCR & Searchability** → Embed invisible text layer into scanned PDFs.
* **Page Manipulation** → Merge, split, rotate, delete, or renumber at will.
* **Optimize** → Compress images, subset fonts, strip metadata, enable fast-web-view.
* **Accessibility** → Generate tagged PDFs compliant with WCAG 2.1 AA where feasible.

---

### Safeguards & Mitigations

| Challenge                  | Imperative Mitigation                                          |
| -------------------------- | -------------------------------------------------------------- |
| Skewed scans               | Deskew images before OCR; apply adaptive thresholding.         |
| Missing fonts              | Substitute glyph-matching fonts; embed subsets.                |
| Nested or irregular tables | Provide image snapshot fallback with HTML overlay.             |
| Encryption                 | Request password; reject unsupported ciphers with clear error. |

---

### Performance Tips

* Stream multi-GB PDFs; process pages lazily to conserve RAM.
* Cache intermediate page images to avoid redundant OCR passes.
* Parallelize independent pages via multiprocessing pools.

---

### Example Prompt → Response Outline

> **User:** “Convert `financial-statements.pdf` into an Excel workbook, each table on its own sheet.”

1. Detect whether the PDF is scanned; if yes, ask for OCR language.
2. Extract tables with `Camelot`, sheet-name them by `Page##_Table##`.
3. Append a `SourcePage` column.
4. Deliver download link and report row/column counts per sheet.

---

### 80/20 Takeaway

1. **Parse → Decide → Act.**
2. Prioritize fidelity, surface risk, and automate away PDF pain points for the user.