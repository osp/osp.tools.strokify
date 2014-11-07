#! /usr/bin/python

import sys
import fontforge

base_font = fontforge.open(sys.argv[1])
new_font = fontforge.open(sys.argv[2])

for glyph in new_font.glyphs():
    new_font.selection.select(glyph.glyphname)
    new_font.copy()
    base_font.selection.select(glyph.glyphname)
    base_font.pasteInto()

base_font.generate("%s.new.ufo" % sys.argv[1])


