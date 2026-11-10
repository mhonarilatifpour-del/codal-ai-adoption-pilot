# codal-ai-adoption-pilot

Pilot for extracting and reviewing AI-adoption evidence from Iranian listed companies' annual board activity reports.

## Source PDFs
Place the original reports in `source_pdfs/`. The current pilot contains five company reports for FY 1403.

## Extract text from PDFs
A GitHub Actions workflow is provided at `.github/workflows/extract-pdfs.yml`.

1. Open the repository on GitHub.
2. Select **Actions**.
3. Select **Extract PDF text**.
4. Press **Run workflow**, keep branch `main`, then confirm **Run workflow**.
5. Wait for the workflow to finish. It will commit page-by-page UTF-8 text files and `extraction_summary.json` into `extracted_text/`.

The workflow also runs automatically when files in `source_pdfs/` or the extraction script change.

## Extraction limitations
- Uses the embedded PDF text layer via PyMuPDF.
- Does not perform OCR. Pages with fewer than 80 extracted characters are flagged in `extraction_summary.json` as likely scanned or sparse.
- Extracted text is a research aid, not a verified AI-adoption classification. Every candidate must be reviewed against the original PDF and page number.
