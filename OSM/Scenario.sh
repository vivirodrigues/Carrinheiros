#!/bin/bash

directory="../maps"
coordinates_scenario="[(-22.816008,-47.075614),(-22.816639,-47.074891),(-22.818317,-47.083415),(-22.820244,-47.085422),(-22.823953,-47.087718)]"

python3 Scenario.py --coord=$coordinates_scenario --directory=$directory

gdal_translate -of GTiff -ot Int16 -co TFW=YES $directory/22S48_ZN.tif ../maps/map.tif

netconvert --osm-files ../maps/map.osm --heightmap.geotiff ../maps/map.tif -o ../maps/map.net.xml
