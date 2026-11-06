# Řehole Raymonda du Puy — Czech translation project

Scholarly Czech translation of the **Rule of Raymond du Puy** (Hospitallers of St John, Jerusalem), version-controlled with a reproducible book build.

## Exact source
E. J. King, *The Rule, Statutes and Customs of the Hospitallers, 1099–1310* (London: Methuen, 1934), Part III, **pp. 20–28** — an **English translation** (from Old French with Latin variants), read via an Internet Archive scan of the AMS Press reprint. **This is a translation of King's English, not of the Latin/Old French.** Only the Rule (preamble + §§1–19) is translated. Details and limits: `source/source-description.md`.

## Layout
`source/` source description, transcription (passage IDs) · `translation/` one file per section · `research/` evidence · `glossary.md`, `decisions.md`, `bibliography.bib` · `review/` progress, issues, completeness · `book/` metadata, front/back matter, `manuscript-order.txt`, styles, fonts, `exports/` · `scripts/`.

## Status
Complete first draft of all 20 passages; self-checked against the source (not independent review); no Czech expert review; rights unresolved; no images yet. See `review/progress.md` and `review/unresolved-issues.md`.

## Build
Dependencies: pandoc ≥ 3.1 (built-in citeproc), Python 3, `pip install weasyprint beautifulsoup4 pypdf python-docx fonttools` (WeasyPrint 70 used). Font: EB Garamond (SIL OFL, from npm `@fontsource/eb-garamond`, kept in `book/fonts/`).
```bash
bash scripts/build.sh
```
Outputs in `book/exports/`: `…-B6-cteni.pdf` (reading, trim size B6), `…-B6-tisk-spady3mm.pdf` (print version: 3 mm bleed, crop marks, padded to a multiple of 4 pages), `….docx` (B6 page size). Never edit exports by hand.

**B6:** ISO 216 B6 = 125 × 176 mm (verified only from a secondary source, papersizes.io; ISO text not opened). Margins 17/20 mm top/bottom, 15/19 mm outer/inner, 10.5 pt EB Garamond. Printer requirements (PDF/X, bleed, imposition, paper) must be confirmed with the printer; the print PDF is not certified PDF/X.
