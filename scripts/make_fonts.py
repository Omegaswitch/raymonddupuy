#!/usr/bin/env python3
"""Merge the Latin and Latin-Extended subsets of EB Garamond (SIL OFL, @fontsource/eb-garamond)
into one TTF per style at book/fonts/build/ (needed so Czech diacritics render in WeasyPrint).
Build-time only; the merged files are not committed."""
import pathlib
from fontTools.ttLib import TTFont
from fontTools.merge import Merger
d = pathlib.Path(__file__).resolve().parent.parent/'book/fonts'; (d/'build').mkdir(exist_ok=True)
for w in ('400', '700'):
    for st in ('normal', 'italic'):
        fs = []
        for part in ('latin', 'latin-ext'):
            t = TTFont(d/f'eb-garamond-{part}-{w}-{st}.woff'); t.flavor = None
            o = d/'build'/f'{part}-{w}-{st}.ttf'; t.save(o); fs.append(str(o))
        Merger().merge(fs).save(d/'build'/f'EBGaramond-{w}-{st}.ttf')
