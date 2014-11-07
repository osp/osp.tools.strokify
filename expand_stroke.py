#!/usr/bin/env python
#-*- coding: utf-8 -*-

import fontforge
import glob
import sys

LETTERS_DIR = "./tmp"

FONT_NAME = "%s" % sys.argv[1].replace(" ", "-")
BASE_FONT = "./i/%s.sfd" % FONT_NAME
FONT = "%s-stroke.ufo" % FONT_NAME
BASE_NAME = sys.argv[2]
WEIGHT = int(sys.argv[3])


def expand(char, WEIGHT=200):
    font[char].stroke("circular", WEIGHT, "round", "round", "cleanup")
    font[char].removeOverlap()

    # Gets original font bearings
    left = original[char].left_side_bearing
    right = original[char].right_side_bearing

    # Sets current bearings to 0
    font[char].left_side_bearing = 0
    font[char].right_side_bearing = 0

    # Gets drawing width
    width = font[char].width

    # Resize the width with original bearings
    font[char].width = left + width + right
    font[char].left_side_bearing = left
    font[char].right_side_bearing = right


original = fontforge.open(BASE_FONT)
font = fontforge.open(FONT)

#letters = "kK"
letters = glob.glob("%s/*.svg" % LETTERS_DIR)

for letter in letters:
    letter = letter.split("/")[-1].replace(".svg", "")
    print letter

    try:
        # Convert HTML entity to unicode name
        char = letter.replace("&#", "").replace(";", "")
        char = fontforge.nameFromUnicode(int(char))
        print char
        expand(char, WEIGHT)
    except TypeError:
        # In case it still doesn't work, it passes. i.e: €
        print "%s was not expanded." % char
        pass
    
# Gets space character from original font
font.createMappedChar("space")
font["space"].width = original["space"].width

font.familyname = "%s" % (BASE_NAME)
font.fontname = "%s-%s" % (BASE_NAME, WEIGHT)
font.fullname = "%s %s" % (BASE_NAME, WEIGHT)
font.weight = "%d" % WEIGHT
font.os2_width = int(sys.argv[4])

font.generate("%s-%s.otf" % (BASE_NAME, WEIGHT))
