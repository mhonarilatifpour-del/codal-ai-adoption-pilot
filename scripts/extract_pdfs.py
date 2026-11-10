from pathlib import Path
import json
import re
import sys
import fitz  # PyMuPDF

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "source_pdfs"
OUT = ROOT / "extracted_text"
OUT.mkdir(parents=True, exist_ok=True)

def normalize_text(value: str) -> str:
    value = value.replace("\u064a", "\u06cc").replace("\u0643", "\u06a9")
    value = value.replace("\u200c", "‌")
    value = re.sub(r"[ \t]+", " ", value)
    value = re.sub(r"\n{3,}", "\n\n", value)
    return value.strip()

summary = []
pdfs = sorted(p for p in SOURCE.glob("*.pdf") if p.is_file())
if not pdfs:
    print("No PDF files found in source_pdfs/", file=sys.stderr)
    sys.exit(2)

for pdf_path in pdfs:
    doc = fitz.open(pdf_path)
    pages = []
    char_counts = []
    for page_number, page in enumerate(doc, start=1):
        text = normalize_text(page.get_text("text", sort=True))
        char_counts.append(len(text))
        pages.append(f"\n\n{'=' * 24}\nPAGE {page_number}\n{'=' * 24}\n{text}")
    full_text = (
        f"Source file: {pdf_path.name}\n"
        f"Page count: {len(doc)}\n"
        f"Extraction: PyMuPDF text layer (OCR not performed)\n"
        + "".join(pages)
    )
    output_path = OUT / (pdf_path.stem + ".txt")
    output_path.write_text(full_text, encoding="utf-8")
    total_chars = sum(char_counts)
    low_text_pages = [i + 1 for i, count in enumerate(char_counts) if count < 80]
    summary.append({
        "source_file": pdf_path.name,
        "output_file": output_path.relative_to(ROOT).as_posix(),
        "page_count": len(doc),
        "total_extracted_characters": total_chars,
        "pages_with_under_80_characters": low_text_pages,
        "likely_scanned_or_sparse": bool(low_text_pages),
        "ocr_performed": False,
    })
    doc.close()
    print(f"{pdf_path.name}: {len(char_counts)} pages, {total_chars} chars -> {output_path}")

(OUT / "extraction_summary.json").write_text(
    json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8"
)
print(f"Processed {len(summary)} PDF files.")
