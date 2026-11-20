---
name: pdf-conversion-tool
description: "Convert a searchable or scanned PDF to an editable document. Inspect reading order, tables and uncertain content, and deliver the actual requested file."
---

# PDF Conversion Tool

For an editable DOCX, inspect the actual supplied PDF and use real document paragraphs and tables. The helper in scripts/pdf_work.py needs Python 3 with pypdf, pypdfium2, Pillow and python-docx; use an existing installation or explain the missing dependency. The package does not include these libraries. From the skill directory run python scripts/pdf_work.py inspect INPUT.pdf inspected. Inspect the returned text and actual rendered page PNGs for columns, boxes, ambiguous glyphs and table boundaries. For image-only pages, read the generated page image with the client’s local image reader or OCR and verify uncertain readings visually. Work column by column, then place each row’s cells in their proper headers. Create a UTF-8 JSON list of blocks in verified reading order: {"heading":"Title"}, {"text":"Paragraph"}, or {"rows":[["Name","Count"],["Example","4"]]}. Run python scripts/pdf_work.py export blocks.json OUTPUT.docx, reopen the result and check its headings, tables, identifier strings, and obscured cells against the source. Supply a real downloadable file. Do not replace editable contents with a page image. For other requested formats, use tools actually available and verify the resulting file before claiming support. Complex input may require a specific limitation report.

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
