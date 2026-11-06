#!/usr/bin/env python3
"""Pad a PDF with blank pages to a multiple of N (default 4). Usage: pad_pdf.py in out [N]"""
import sys
from pypdf import PdfReader, PdfWriter
r = PdfReader(sys.argv[1]); w = PdfWriter(); n = int(sys.argv[3]) if len(sys.argv) > 3 else 4
for p in r.pages: w.add_page(p)
box = r.pages[0].mediabox
while len(w.pages) % n: w.add_blank_page(width=box.width, height=box.height)
w.write(sys.argv[2]); print('pages:', len(r.pages), '->', len(w.pages))
