import rasterio
from rasterio.merge import merge
from rasterio.plot import show
import glob
import os


dirpath = r"../models/maps/"
out_fp = r"../models/maps/out.tif"
# Make a search criteria to select the DEM DB
search_criteria = "*.tif"
tif1 = '25S495ZN.tif'
tif2 = '26S495ZN.tif'
q = os.path.join(dirpath, search_criteria)
print("q", q)
# dem_fps = glob.glob(q)
dem_fps = [dirpath + tif1, dirpath + tif2]
src_files_to_mosaic = []
for fp in dem_fps:
    src = rasterio.open(fp)
    src_files_to_mosaic.append(src)
mosaic, out_trans = merge(src_files_to_mosaic)
show(mosaic, cmap='terrain')
out_meta = src.meta.copy()
out_meta.update({"driver": "GTiff",
                 "height": mosaic.shape[1],
                 "width": mosaic.shape[2],
                 "transform": out_trans,
                 "crs": "+proj=utm +zone=35 +ellps=GRS80 +units=m +no_defs "
                 }
                )
with rasterio.open(out_fp, "w", **out_meta) as dest:
    dest.write(mosaic)
