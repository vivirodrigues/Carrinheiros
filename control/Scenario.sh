#!/bin/bash

dirOSM="../maps/"
dirGeo="../GEOTIFF/"
dirModels="../models/"
dirDB="../models/DB/"

python3 Scenario.py --dirModels=$dirModels --dirGeo=$dirGeo --dirOSM=$dirOSM --dirDB=$dirDB

gdal_translate -of GTiff -ot Int16 -co TFW=YES $dirGeo/22S48_ZN.tif ../maps/map.tif

netconvert --osm-files ../maps/map.osm --heightmap.geotiff ../maps/map.tif -o ../maps/map.net.xml
