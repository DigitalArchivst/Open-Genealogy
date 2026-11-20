"""Inspect PDF input and export a reader-checked set of paragraphs and tables to DOCX."""

import argparse
import hashlib
import json
from pathlib import Path


def inspect_pdf(source, destination):
    import pypdfium2 as pdfium
    from pypdf import PdfReader

    destination.mkdir(exist_ok=True, parents=True)
    reader = PdfReader(source)
    document = pdfium.PdfDocument(source)
    pages = []
    try:
        for index, pdf_page in enumerate(reader.pages):
            text = pdf_page.extract_text(extraction_mode="layout") or ""
            page = document[index]
            try:
                bitmap = page.render(scale=2)
                try:
                    raster = destination / f"page-{index+1:03}.png"
                    bitmap.to_pil().save(raster)
                finally:
                    bitmap.close()
            finally:
                page.close()
            pages.append({"page": index+1, "image": raster.name, "selectable_text": text})
    finally:
        document.close()
    result = {"sha256": hashlib.sha256(source.read_bytes()).hexdigest(), "pages": pages}
    (destination / "pages.json").write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf8")
    print(json.dumps(result, ensure_ascii=False))


def export_docx(block_file, target):
    from docx import Document

    blocks = json.loads(block_file.read_text(encoding="utf-8-sig"))
    if not isinstance(blocks, list) or not blocks:
        raise ValueError("Provide a nonempty ordered list of text or table blocks.")
    document = Document()
    for block in blocks:
        if "rows" in block:
            rows = block["rows"]
            if not rows or not rows[0] or any(len(row) != len(rows[0]) for row in rows):
                raise ValueError("Each table must be rectangular and contain at least one cell.")
            table = document.add_table(rows=len(rows), cols=len(rows[0]))
            table.style = "Table Grid"
            for i, row in enumerate(rows):
                for j, text in enumerate(row):
                    table.cell(i, j).text = str(text)
        elif "heading" in block:
            document.add_heading(str(block["heading"]), level=int(block.get("level",1)))
        elif "text" in block:
            document.add_paragraph(str(block["text"]))
        else:
            raise ValueError("Use a heading, text, or rows block.")
    document.save(target)
    opened = Document(target)
    print(json.dumps({"file":target.name,"paragraphs":len(opened.paragraphs),
                      "tables":[[len(t.rows),len(t.columns)] for t in opened.tables]}))


if __name__ == "__main__":
    options = argparse.ArgumentParser(description=__doc__)
    options.add_argument("task", choices=("inspect","export"))
    options.add_argument("input",type=Path)
    options.add_argument("output",type=Path)
    args = options.parse_args()
    if args.task == "inspect":
        inspect_pdf(args.input,args.output)
    else:
        export_docx(args.input,args.output)
