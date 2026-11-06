#!/usr/bin/env python3
"""Post-process pandoc HTML for print: Czech non-breaking spaces, inline footnotes
(for WeasyPrint float: footnote). Usage: prepare.py in.html out.html"""
import sys, re
from bs4 import BeautifulSoup, NavigableString
soup = BeautifulSoup(open(sys.argv[1], encoding='utf-8').read(), 'html.parser')
# footnotes -> inline
notes = {}
sec = soup.find(class_='footnotes')
if sec:
    for li in sec.find_all('li', recursive=True):
        if li.get('id', '').startswith('fn'):
            notes[li['id']] = li
for a in soup.find_all('a', class_='footnote-ref'):
    li = notes[a['href'].lstrip('#')]
    for back in li.find_all('a', class_='footnote-back'): back.decompose()
    span = soup.new_tag('span', attrs={'class': 'fn'})
    for ch in list(li.children):
        if getattr(ch, 'name', None) == 'p':
            for c in list(ch.children): span.append(c.extract())
            span.append(' ')
        else: span.append(ch.extract())
    a.replace_with(span)
if sec: sec.decompose()
# nbsp after one-letter prepositions/conjunctions and before numbers' units
pat = re.compile(r'(?<![\w])([KkSsVvZzOoUuAaIi]) (?=\S)')
def fix(t):
    t = pat.sub('\\1\u00a0', t); t = pat.sub('\\1\u00a0', t)
    return re.sub(r'(\d) (?=(dní|dnů|mší|denár|otčenášů))', '\\1\u00a0', t)
for t in soup.find_all(string=True):
    if t.parent.name in ('script', 'style', 'title'): continue
    n = fix(str(t))
    if n != str(t): t.replace_with(NavigableString(n))
open(sys.argv[2], 'w', encoding='utf-8').write(str(soup))
