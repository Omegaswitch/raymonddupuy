#!/usr/bin/env python3
"""Set B6 page size, margins and fonts in a pandoc DOCX. Usage: docx_post.py file.docx"""
import sys
from docx import Document
from docx.shared import Mm, Pt
d = Document(sys.argv[1])
for s in d.sections:
    s.page_width, s.page_height = Mm(125), Mm(176)
    s.top_margin, s.bottom_margin = Mm(17), Mm(20)
    s.left_margin, s.right_margin = Mm(17), Mm(15)
by = {x.name.lower(): x for x in d.styles}
for name in ['normal', 'body text', 'first paragraph', 'compact', 'footnote text']:
    if name in by:
        by[name].font.name = 'Times New Roman'
        by[name].font.size = Pt(8.5 if name == 'footnote text' else 10.5)
for name in ['heading 1', 'heading 2', 'title', 'subtitle', 'author', 'date']:
    if name in by: by[name].font.name = 'Times New Roman'
d.save(sys.argv[1])
