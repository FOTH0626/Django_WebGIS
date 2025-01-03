#!/bin/sh
for f in static/Resources/GeoTiff/*.tif; do
    gdalwarp -of png -dstalpha $f $f.png
done
