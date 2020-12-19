import rasterio
from rasterio.merge import merge
from rasterio.plot import show
import glob
import os


dirpath = r"../maps/"
out_fp = r"../maps/out.tif"
# Make a search criteria to select the DEM files
search_criteria = "*.tif"
q = os.path.join(dirpath, search_criteria)
print(q)
dem_fps = glob.glob(q)
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
