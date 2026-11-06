#!/usr/bin/env bash
# Rebuild the book. Run from anywhere. Needs: pandoc>=3 (citeproc built in), python3 with weasyprint,
# beautifulsoup4, pypdf, python-docx.   pip install weasyprint beautifulsoup4 pypdf python-docx
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"; cd "$ROOT"
OUT=book/exports; TMP="$(mktemp -d)"; mkdir -p "$OUT"
python3 scripts/check.py
python3 scripts/make_fonts.py
# combined manuscript in explicit order
: > "$TMP/combined.md"
while IFS= read -r f; do [ -n "$f" ] && { cat "book/$f"; printf '\n\n'; } >> "$TMP/combined.md"; done < book/manuscript-order.txt
# optional frontispiece: book/images/frontispiece.* (see book/images/CREDITS.md)
FRONT=(); for e in jpg png; do [ -f "book/images/frontispiece.$e" ] && FRONT=(-M "frontispiece=images/frontispiece.$e" -M "frontispiece-caption=$(cat book/images/frontispiece-caption.txt 2>/dev/null || true)"); done
pandoc "$TMP/combined.md" --from markdown+fenced_divs --to html5 --standalone --wrap=none \
  --template book/template.html --metadata-file book/metadata.yaml --citeproc --toc --toc-depth=2 --section-divs "${FRONT[@]}" \
  -o "$TMP/book.raw.html"
python3 scripts/prepare.py "$TMP/book.raw.html" book/book.html   # (book.html is a build intermediate)
python3 - <<'PY'
import weasyprint
base = 'book/'
weasyprint.HTML('book/book.html', base_url=base).write_pdf('book/exports/raymond-du-puy-rehole-B6-cteni.pdf')
css = weasyprint.CSS(string='@page { bleed: 3mm; marks: crop; }')
weasyprint.HTML('book/book.html', base_url=base).write_pdf('/tmp/_print_raw.pdf', stylesheets=[css])
PY
python3 scripts/pad_pdf.py /tmp/_print_raw.pdf "$OUT/raymond-du-puy-rehole-B6-tisk-spady3mm.pdf" 4
pandoc "$TMP/combined.md" --from markdown+fenced_divs --to docx --metadata-file book/metadata.yaml --citeproc --toc --toc-depth=2 -o "$OUT/raymond-du-puy-rehole.docx"
python3 scripts/docx_post.py "$OUT/raymond-du-puy-rehole.docx"
rm -f book/book.html "$TMP"/*; echo "Built into $OUT"
