#!/bin/bash

directoryGeoTiff="../maps"
directoryData="../data"

python3 Scenario.py --dirData=$directoryData --dirGeoTiff=$directoryGeoTiff

gdal_translate -of GTiff -ot Int16 -co TFW=YES $directoryGeoTiff/22S48_ZN.tif ../maps/map.tif

netconvert --osm-files ../maps/map.osm --heightmap.geotiff ../maps/map.tif -o ../maps/map.net.xml
