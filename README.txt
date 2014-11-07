# STROKIFY

## svg2ufo.py

Called in trace_alphabet. Used to import SVG files into a .ufo font.



## traceAlphabet.py

Produces a stroke .ufo font file from an outline font file.

Usage:

    trace_alphabet.sh "TeX Gyre Termes"

Where "TeX Gyre Termes" is the font family name.


## openClosedPaths.py

When importing a stroke from Inkscape, Fontforge automatically closes the shape. This script is trying to reopen the shape. It does not work 100% of times, but maybe 90% of the time, which is already time-saving!


## expand_stroke.py

Once your strokes are clean, you can launch this script to expand the stroke with the width and parameters you want.

Usage:

    python expand_stroke.py  "Spacing Font" "New font"  30 1

Where:
- "Spacing Font" is the original font from which we get the spacing info back.
- "New Font" is the name of the produced font
- "30" is the width of the stroke
- "1" is the variant of the font (we use this to put all fonts in the same font family but still be able to use them in software like Inkscape)
    - 1: Ultra-Condensed
    - 2: Extra-Condensed
    - 3: Condensed
    - 4: Semi-Condensed
    - 5: Normal
    - 6: Semi-Expanded
    - 7: Expanded
    - 8: Extra-Expanded
    - 9: Ultra-Expanded
