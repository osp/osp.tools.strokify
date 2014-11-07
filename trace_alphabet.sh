#!/bin/bash

FONTFAMILY=$(python2 getFontName.py ${1}  2> /dev/null)

echo "FONT FAMILY: " + ${FONTFAMILY}

 #FONTFAMILY="Ume P Gothic Balsa"
  #FONTFAMILY="Ume P Mincho"

  TRACEWIDTH=4000 

  OUTPUTDIR=o


  #WNAME=`echo 00$WEIGHT | rev | cut -c 1-2 | rev`
  #NAME=Umetra-P_`echo $FONTFAMILY | rev | cut -d " " -f 1 | rev`-stroke

# --------------------------------------------------------------------------- # 
  TMPDIR=tmp
  mkdir -p ${TMPDIR}

  SHIFT=`expr 35`
  e() { echo $1 >> ${DUMP}; }
 
 
for LETTER in "&#64;" "&#65;"  
#for LETTER in "&#33;" "&#34;" "&#35;" "&#36;" "&#37;" "&#38;" "&#39;" "&#40;" "&#41;" "&#42;" "&#43;" "&#44;" "&#45;" "&#46;" "&#47;" "&#48;" "&#49;" "&#50;" "&#51;" "&#52;" "&#53;" "&#54;" "&#55;" "&#56;" "&#57;" "&#58;" "&#59;" "&#60;" "&#61;" "&#62;" "&#63;" "&#64;" "&#65;" "&#66;" "&#67;" "&#68;" "&#69;" "&#70;" "&#71;" "&#72;" "&#73;" "&#74;" "&#75;" "&#76;" "&#77;" "&#78;" "&#79;" "&#80;" "&#81;" "&#82;" "&#83;" "&#84;" "&#85;" "&#86;" "&#87;" "&#88;" "&#89;" "&#90;" "&#91;" "&#92;" "&#93;" "&#94;" "&#95;" "&#96;" "&#97;" "&#98;" "&#99;" "&#100;" "&#101;" "&#102;" "&#103;" "&#104;" "&#105;" "&#106;" "&#107;" "&#108;" "&#109;" "&#110;" "&#111;" "&#112;" "&#113;" "&#114;" "&#115;" "&#116;" "&#117;" "&#118;" "&#119;" "&#120;" "&#121;" "&#122;" "&#123;" "&#124;" "&#125;" "&#126;" "&#127;" "&#128;" "&#129;" "&#130;" "&#131;" "&#132;" "&#133;" "&#134;" "&#135;" "&#136;" "&#137;" "&#138;" "&#139;" "&#140;" "&#141;" "&#142;" "&#143;" "&#144;" "&#145;" "&#146;" "&#147;" "&#148;" "&#149;" "&#150;" "&#151;" "&#152;" "&#153;" "&#154;" "&#155;" "&#156;" "&#157;" "&#158;" "&#159;" "&#160;" "&#161;" "&#162;" "&#163;" "&#164;" "&#165;" "&#166;" "&#167;" "&#168;" "&#169;" "&#170;" "&#171;" "&#172;" "&#173;" "&#174;" "&#175;" "&#176;" "&#177;" "&#178;" "&#179;" "&#180;" "&#181;" "&#182;" "&#183;" "&#184;" "&#185;" "&#186;" "&#187;" "&#188;" "&#189;" "&#190;" "&#191;" "&#192;" "&#193;" "&#194;" "&#195;" "&#196;" "&#197;" "&#198;" "&#199;" "&#200;" "&#201;" "&#202;" "&#203;" "&#204;" "&#205;" "&#206;" "&#207;" "&#208;" "&#209;" "&#210;" "&#211;" "&#212;" "&#213;" "&#214;" "&#215;" "&#216;" "&#217;" "&#218;" "&#219;" "&#220;" "&#221;" "&#222;" "&#223;" "&#224;" "&#225;" "&#226;" "&#227;" "&#228;" "&#229;" "&#230;" "&#231;" "&#232;" "&#233;" "&#234;" "&#235;" "&#236;" "&#237;" "&#238;" "&#239;" "&#240;" "&#241;" "&#242;" "&#243;" "&#244;" "&#245;" "&#246;" "&#247;" "&#248;" "&#249;" "&#250;" "&#251;" "&#252;" "&#253;" "&#254;" "&#8364;" \
#"&#338;" "&#339;" "&#8230;" "&#8211;" "&#8212;" "&#8216;" "&#8217;" "&#8220;" "&#8221;" "&#8544;" "&#8545;" "&#8546;" "&#8547;" "&#8548;" "&#8549;" "&#8550;" "&#8551;" "&#8552;" "&#8553;" "&#8554;" "&#8555;" "&#8556;" "&#8557;" "&#8558;" "&#8559;" "&#8592;" "&#8593;" "&#8594;" "&#8595;" "&#9450;" "&#9312;" "&#9313;" "&#9314;" "&#9315;" "&#9316;" "&#9317;" "&#9318;" "&#9319;" "&#9320;" "&#9833;" "&#9834;" "&#9835;" "&#9836;" "&#9837;" "&#9838;" "&#9839;" \
#"&#8242;" "&#8243;" "&#8738;"
   do
 
      DUMP=$TMPDIR/${LETTER}.svg
 
      e '<?xml version="1.0" encoding="UTF-8" standalone="no"?>'
      e '<svg width="4000" height="4500" id="svg" version="1.1"'
      e 'xmlns:inkscape="http://www.inkscape.org/namespaces/inkscape"'
      e '>'
      e '<g inkscape:label="letter" inkscape:groupmode="layer" id="X">'
      e '<flowRoot xml:space="preserve" id="flowRoot"'
 
      e "style=\"font-size:4000px;\
                 font-style:normal;\
                 font-variant:normal;\
                 font-weight:normal;\
                 font-stretch:normal;\
                 text-align:center;\
                 line-height:100%;\
                 letter-spacing:0px;\
                 word-spacing:0px;\
                 writing-mode:lr-tb;\
                 text-anchor:middle;\
                 fill:#000000;\
                 fill-opacity:1;\
                 stroke:none;\
                 font-family:$FONTFAMILY;\
                -inkscape-font-specification:$FONTFAMILY\""
      e '><flowRegion id="flowRegion">'
      e "<rect id=\"rect\" width=\"4000\" height=\"4500\" x=\"0\" y=\"-$SHIFT\" />"
      e "</flowRegion><flowPara id=\"flowPara\">$LETTER</flowPara></flowRoot>"
      e '</g>'
      e '</svg>'
 
      # Export SVG into PNG
      inkscape --export-png=${DUMP%%.*}.png \
               --export-background=#ffffff \
               --export-width=$TRACEWIDTH \
              $DUMP
        
      # This is only for Steph's machine which fails on autotracing png, but it makes the script super slow
      convert ${DUMP%%.*}.png ${DUMP%%.*}.gif

      # Vectorize bitmap with stroke
      autotrace -centerline \
                -color-count=2 \
                -background-color=ffffff \
                -output-file=$DUMP \
                ${DUMP%%.*}.gif

      # Setting "stroke" to "none" forces stroke import in Fontforge
      STYLE="style=\"stroke:none;fill:none;\""

      # Apply stroke style
      sed -i "s/style=\"[^\"]*\"/$STYLE/g" $DUMP

      # Removes png files
      #rm ${DUMP%%.*}.png

    done


    echo "Launching svg2ttf"
    # Launches Ana and Ricardo's script (takes a set of SVG files and puts it into an sfd file)
    python2 svg2ufo.py ${1}

    python2 ufo_clean.py ${1}-stroke.ufo

    # Moves "output.ttf" into "o" folder
    #mv output.ttf ${OUTPUTDIR}/${NAME}.ttf


    # Clean the "tmp" folder
    #rm $TMPDIR/*.*



exit 0;



