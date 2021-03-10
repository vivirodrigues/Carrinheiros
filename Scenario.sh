#!/bin/bash

id="000"
date="25 01 2021"
dirMaps="data/maps"

echo "............script started............"

# shellcheck disable=SC2207
result=$(python3 Carrinheiro.py --idUser=$id --date="$date")

echo "---------------"

# shellcheck disable=SC1073
echo "$result"

#gdal_translate -of GTiff -ot Int16 -co TFW=YES $dirMaps/22S48_ZN.tif $dirMaps/map.tif

#netconvert --osm-files $dirMaps/map.osm --heightmap.geotiff $dirMaps/map.tif -o $dirMaps/map.net.xml
