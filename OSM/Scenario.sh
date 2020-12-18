#!/bin/bash
python3 Scenario.py --city="Campinas" --state="SP" --country="BR"

# directory = "../maps"

gdal_translate -of GTiff -ot Int16 -co TFW=YES ../maps/22S48_ZN.tif ../maps/map.tif

netconvert --osm-files ../maps/map.osm --heightmap.geotiff ../maps/map.tif -o ../maps/map.net.xml
