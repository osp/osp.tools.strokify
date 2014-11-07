#!/usr/bin/env python
#-*- coding: utf-8 -*-

from xml.dom.minidom import parse as parseXml
import sys
import glob
import fontforge



# Gets list of wanted glyphs
f = open("glyphs.txt", "r")
letters = f.read().splitlines()
f.close()

#STROKE_FONT = "%s-stroke.ufo" % sys.argv[1].replace(" ", "-")
STROKE_FONT = "%s-stroke.ufo" % sys.argv[1]
GLYPH_DIR = "%s/glyphs/" % STROKE_FONT

for letter in letters:
    letter = letter.split("/")[-1].replace(".svg", "")
    char = fontforge.unicodeFromName(letter)

    if char == -1:
        char = letter.replace("&#", "").replace(";", "")
        letter = fontforge.nameFromUnicode(int(char))
    print "letter: %s" % letter
    print "char: %s" % char


    # Gets the XML of the glyph
    try: 
        letter = letter.replace("&#", "").replace(";", "")
        letter = fontforge.nameFromUnicode(int(char))
        # In UFO, capital characters have an underscore in their name: "A" -> "A_.glif"
        if letter[0].isupper(): 
            if len(letter) == 1:
                letter = letter + "_"
            elif len(letter) == 2:
                letter = letter[0] + "_" + letter[1] + "_"
            else:
                letter = letter[0] + "_" + letter[1:]
            #letter = letter.lower()
        if letter[0:3] == "uni": 
            continue
            #letter = "uni" + letter[3:].upper() + "_"



        glyph = parseXml("%s%s.glif" % (GLYPH_DIR, letter))
        # Gets contours descriptions of the glyph
        contours = glyph.getElementsByTagName("contour")

        for contour in contours:
            try:
                # Checks type of first node of the countour
                type= contour.childNodes[1].attributes["type"].value
                if type == "move":
                    # Should be ok already
                    pass
                elif type == "line":
                    # Changing type "line" to "move"
                    contour.childNodes[1].attributes["type"].value = "move"
                elif type == "curve":
                    # Putting curve point at the end of the contour
                    contour.appendChild(contour.childNodes[1])
                    # Changing first "line" to "move"
                    contour.childNodes[2].attributes["type"].value = "move"
            except KeyError:
                print "Did not work."
                pass


        # Saves XML
        f = open("%s%s.glif" % (GLYPH_DIR, letter), "w")
        f.write(glyph.toxml())
        f.close()
    except IOError:
        # In case it still doesn't work, it passes. i.e: €
        print "%s did not work." % char
        pass

