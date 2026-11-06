#!/usr/bin/env python3
"""Structural checks (NOT proof of translation accuracy).
Run from repo root: python3 scripts/check.py"""
import re, sys, glob, pathlib
root = pathlib.Path(__file__).resolve().parent.parent
err = []
order = [l.strip() for l in (root/'book/manuscript-order.txt').read_text().splitlines() if l.strip()]
files = []
for o in order:
    p = (root/'book'/o).resolve()
    if not p.exists(): err.append(f'missing in manuscript-order: {o}')
    files.append(p)
text = {p: p.read_text() for p in files if p.exists()}
# translation files all listed, in sorted order
tr = sorted((root/'translation').glob('*.md'))
listed = [p for p in files if p.parent == (root/'translation').resolve()]
if [p.name for p in tr] != [p.name for p in listed]: err.append('translation files not all listed in sorted order')
# footnotes
alltxt = '\n'.join(text.values())
refs = re.findall(r'\[\^([^\]]+)\](?!:)', alltxt)
defs = re.findall(r'^\[\^([^\]]+)\]:', alltxt, re.M)
for r in set(refs):
    if r not in defs: err.append(f'footnote ref without definition: {r}')
for d in set(defs):
    if d not in refs: err.append(f'footnote definition never referenced: {d}')
if len(defs) != len(set(defs)): err.append('duplicate footnote ids')
# citation keys
bib = (root/'bibliography.bib').read_text()
bkeys = set(re.findall(r'^@\w+\{([^,]+),', bib, re.M))
cited = set(re.findall(r'@([A-Za-z][\w:-]*)', ' '.join(re.findall(r'\[(@[^\]]+)\]', alltxt))))
listed_keys = set(' '.join(re.findall(r'<!-- keys: ([^>]*?) -->', alltxt)).split())
for c_ in cited - listed_keys: err.append(f'cited key missing from bibliography page: {c_}')
for c in cited:
    if c not in bkeys: err.append(f'citation key not in bibliography.bib: {c}')
# passage ids: transcription vs translation
src = (root/'source/transcription/000-rule-en-king-1934.md').read_text()
sid = re.findall(r'\{#(rule-[a-z0-9-]*-p\d+[a-z]*)\}', src)
tid = []
for p in tr: tid += re.findall(r'\{#(rule-[a-z0-9-]*-p\d+[a-z]*)\}', p.read_text())
if len(set(tid)) != len(tid): err.append('duplicate passage ids in translation')
if sorted(sid) != sorted(tid): err.append(f'passage id mismatch: src-only {set(sid)-set(tid)}, tr-only {set(tid)-set(sid)}')
# King notes: transcription vs translation
sk = set(re.findall(r'^\[\^(k\d+-\d+)\]:', src, re.M)); tk = {d.replace('k-','k').replace('-','-',1) for d in defs if d.startswith('k-')}
tk = {'k'+d[2:] for d in defs if d.startswith('k-')}
if sk != tk: err.append(f'King notes mismatch: {sk ^ tk}')
# digits sanity: numbers in source passage vs translation (rough)
print('passages:', len(sid), 'footnotes:', len(defs), 'citations:', len(cited))
if err: print('\n'.join('ERROR: '+e for e in err)); sys.exit(1)
print('structural checks passed')
