#!/usr/bin/env python
#-*- coding: utf-8 -*-

#    Copyright (C) 2014 OSP (Stéphanie Vilayphiou) and Christoph Haag.
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.

import sys
import subprocess, shlex
import fontforge


font_file = sys.argv[1]
convert = sys.argv[2]


tmp_dir = "tmp"

# Gets list of wanted glyphs
f = open("glyphs.test.txt", "r")
glyphs = f.read().splitlines()
f.close()

# Gets fontname out of font file
font = fontforge.open(font_file)
fontname = font.familyname
print fontname

Yshift = 35

def makeSVG(fontname, Yshift, tmp_dir, glyph):
    f = open("%s/%s.svg" % (tmp_dir, glyph), "w")
    svg = """<?xml version="1.0" encoding="UTF-8" standalone="no"?>
    <svg width="4000" height="4500" id="svg" version="1.1"
         xmlns:inkscape="http://www.inkscape.org/namespaces/inkscape"
         >
    <g inkscape:label="letter" inkscape:groupmode="layer" id="X">
    <flowRoot xml:space="preserve" id="flowRoot"
         style="font-size:4000px;
                font-style:normal;
                font-variant:normal;
                font-weight:normal;
                font-stretch:normal;
                text-align:center;
                line-height:100%%;
                letter-spacing:0px;
                word-spacing:0px;
                writing-mode:lr-tb;
                text-anchor:middle;
                fill:#000000;
                fill-opacity:1;
                stroke:none;
                font-family: %s;
                -inkscape-font-specification: %s"
        >
     <flowRegion id="flowRegion">
    <rect id="rect" width="4000" height="4500" x="0" y="-%d" />
    </flowRegion><flowPara id="flowPara">%s</flowPara></flowRoot>
    </g>
    </svg> """ % (fontname, fontname, Yshift, glyph)
    f.write(svg)
    f.close()

for glyph in glyphs:
    basename = "%s/%s" % (tmp_dir, glyph)
    makeSVG(fontname, Yshift, tmp_dir, glyph)

    print "Export SVG into PNG"
    inkscape = "inkscape --export-png=%s.png --export-background=#ffffff --export-width=4000 %s.svg" % (basename, basename)
    p = subprocess.call(shlex.split(inkscape))

    # This is only for Steph's machine which fails on autotracing png, but it makes the script super slow
    if convert == "convert":
        print "Convert PNG to GIF"
        imagemagick = "convert %s.png %s.gif" % (basename, basename)
        p = subprocess.call(shlex.split(imagemagick))

    print "Vectorize bitmap with stroke"
    autotrace = "autotrace -centerline -color-count=2 -background-color=ffffff -output-file=%s.svg %s.gif" % (basename, basename)
    p = subprocess.call(shlex.split(autotrace))

    # Setting "stroke" to "none" forces stroke import in Fontforge
    style = "style=\"stroke:none;fill:none;\""

    # Apply stroke style
    sed = "sed -i 's/style=\"[^\"]*\"/%s/g' %s.svg" % (style, basename)
    p = subprocess.call(shlex.split(sed))

print "Launching svg2ufo"
svg2ufo = "python svg2ufo.py %s" % fontname
p = subprocess.call(shlex.split(svg2ufo))

print "Attempt to open closed paths"
ufoclean = "python openClosedPaths.py %s-stroke.ufo" % fontname
p = subprocess.call(shlex.split(ufoclean))
