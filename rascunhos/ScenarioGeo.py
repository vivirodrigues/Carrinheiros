from geography import Topodata, Coordinates
from rascunhos import DownloadGeo
from osgeo import gdal
import rasterio
from rasterio.merge import merge
from rasterio.plot import show


def get_coordinate_pixel(geotiff, lon, lat):
    """

    :param geotiff: str
                    path + file_name of the geotiff

    :param lon:     float
                    longitude value

    :param lat:     float
                    latitude value

    :return:        value of lon,lat pixel in geotiff
    """

    # open geotiff
    dataset = rasterio.open(geotiff)

    # get pixel of the coordinate
    py, px = dataset.index(lon, lat)

    # create 1x1px window of the pixel
    window = rasterio.windows.Window(px - 1//2, py - 1//2, 1, 1)

    # read rgb values of the window
    clip = dataset.read(window=window)

    # return the value of pixel
    return clip[0][0][0]


class ScenarioGeo:
    # reading the GeoTiff file
    def __init__(self, geo_directory, coordinates_stop_points):
        self.dir_geo = geo_directory
        self.coordinates_osm = Coordinates.coordinates_list_bbox(coordinates_stop_points)
        self.file_names = Topodata.file_names_topodata(self.coordinates_osm)
        # self.file_names = self.topodata.get_file_names()
        self.tif_names = []
        self.tif_name = ''
        self.n_files = 0
        self.main()

    def set_geotiff(self):
        # it checks if the file exists
        for i in range(0, self.n_files):
            try:
                with open(self.dir_geo + self.file_names[i], 'r') as f:
                    print(self.dir_geo)
                    print(self.file_names[i])
                    # self.scenario_geotiff = f.read()
                    print(self.file_names[i], " file exists")
            except IOError:
                # if not exists, it downloads the file
                print(self.file_names[i])
                # download_file = Download.download_geotiff(self.file_names[i], self.dir_geo)
                DownloadGeo.DownloadGeo(self.file_names[i], self.dir_geo).download()
                # self.set_geotiff()

    def verify_geo_file_coordinates(self):
        path_dir = str(self.dir_geo) + str(self.file_names[1]) + '.tif'
        ds = gdal.Open(path_dir, gdal.GA_ReadOnly)
        if not ds:
            print("Error: GeoTiff not found")
        else:
            width = ds.RasterXSize
            height = ds.RasterYSize
            gt = ds.GetGeoTransform()
            min_lon = gt[0] # min_x
            min_lat = gt[3] + width * gt[4] + height * gt[5] # min_y
            max_lon = gt[0] + width * gt[1] + height * gt[2] # max_x
            max_lat = gt[3] # max_y
            # min_lon, min_lat, max_lon, max_lat
            geo_file_coordinates = (min_lon, min_lat, max_lon, max_lat)
            return geo_file_coordinates

    def set_n_files(self):
        self.n_files = len(self.file_names)

    def set_tif_names(self):
        new = []
        for i in self.file_names:
            new.append(self.dir_geo + i + '.tif')
        self.tif_names = new

    def join_geo(self):
        # it sticks the files according to the coordinates
        out_fp = self.dir_geo + 'out.tif'  # exit file
        self.tif_name = 'out.tif'
        dem_fps = self.tif_names
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

    def main(self):
        self.set_n_files()
        self.set_tif_names()
        self.set_geotiff()
        if self.n_files > 1:
            self.join_geo()
        else:
            self.tif_name = self.tif_names[0]


if __name__ == "__main__":
    coordinates_path = [(-22.816008, -47.075614, 606.0), (-22.816639, -47.074891, 602.0),
                        (-22.818317, -47.083415, 602.0), (-22.820244, -47.085422, 602.0),
                        (-22.816008, -47.075614, 606.0), (-22.823953, -47.087718, 602.0)]

    coordinates_1 = [(-25.977999, -49.575614, 606.0), (-25.877999, -49.585614, 602.0),
                     (-26.011199, -49.515614, 602.0), (-26.101199, -49.595614, 602.0),
                     (-26.021199, -49.075614, 606.0), (-26.051100, -49.071614, 602.0)]

    dir_geo = '../data/maps/'
    ScenarioGeo(dir_geo, coordinates_1)
    # file_name = '22S48_ZN'
    ###
    # Host:
    # sudo apt-get install gdal-bin
    # sudo apt-get install libgdal-dev libgdal1h
    # enviroment:
    # pip install GDAL==$(gdal-config --version) --global-option=build_ext --global-option="-I/usr/include/gdal"