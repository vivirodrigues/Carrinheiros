from geography import Download, Topodata, Coordinates
from osgeo import gdal
import rasterio
from rasterio.merge import merge
from rasterio.plot import show


def coordinate_pixel(geotiff, lon, lat):
    """

    :param geotiff: str
                    path + file_name of the geotiff

    :param lon:     float
                    longitude value

    :param lat:     float
                    latitude value

    :return:        <class 'numpy.float32'>
                    value of lon,lat pixel in geotiff
    """

    name_len = len(geotiff)
    file_extension = geotiff[name_len - 4] + geotiff[name_len - 3] +\
                     geotiff[name_len - 2] + geotiff[name_len - 1]

    if file_extension != '.tif':
        geotiff += '.tif'

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


def set_tif_names(directory, file_names):
    """
    This function returns the directory + file_name
    of the inputs.

    In general, it is used to do mosaic with many
    geotiff files.

    :param directory:       String
    :param file_names:      String
    :return:                list
                            It returns a list with
                            Strings. Each string
                            has the merge of
                            the directory and file
                            name.
    """
    tif_names = []
    for i in file_names:
        tif_names.append(directory + i + '.tif')
    return tif_names


def _geotiff(directory, file_names):
    """
    This function verifies if the GeoTiff file
    exists in a directory. If it not exists,
    the function downloads the GeoTiff file.

    :param directory:   String

    :param file_names:  list
                        The list should have
                        Strings that corresponds
                        to the name files of geotiffs.
    """
    number_of_files = len(file_names)

    for i in range(0, number_of_files):
        try:

            # it checks if the file exists
            with open(directory + file_names[i], 'r') as f:
                pass
                # self.scenario_geotiff = f.read()
                print(file_names[i], " file exists")
        except IOError:
            # if it does not exist, it downloads the file
            print(file_names[i])
            download_file = Download.download_geotiff(directory, file_names[i])


def join_geo(directory, geo_directory_and_file_names, name_mosaic_file='out.tif'):
    """
    This function does a mosaic with geotiff files according
    to the geographic position.

    :param directory:                       String

    :param geo_directory_and_file_names:    list
                                            list of Strings
                                            Each string:
                                            directory + file_name

    :param name_mosaic_file:                String
                                            Name of the output file
                                            (mosaic)
    """
    # output geotiff file
    out_fp = directory + name_mosaic_file
    dem_fps = geo_directory_and_file_names
    src_files_to_mosaic = []
    for fp in dem_fps:
        src = rasterio.open(fp)
        src_files_to_mosaic.append(src)
    mosaic, out_trans = merge(src_files_to_mosaic)
    #show(mosaic, cmap='terrain')
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


def verify_geo_file_coordinates(directory, file_name):
    """
    This function gets the coordinates limit of a GeoTiff
    file. It returns a list with the same format of a
    bounding box (bbox) of the Open Street Map.

    :param directory:       String

    :param file_name:       String
                            The name of the GeoTiff


    :return:                list
                            [minimum longitude,
                            minimum latitude,
                            maximum longitude,
                            maximum latitude]
    """

    path_dir = str(directory) + str(file_name) + '.tif'
    ds = gdal.Open(path_dir, gdal.GA_ReadOnly)
    if not ds:
        pass
        #print("Error: GeoTiff not found")
    else:
        width = ds.RasterXSize
        height = ds.RasterYSize
        gt = ds.GetGeoTransform()
        min_lon = gt[0] # min_x
        min_lat = gt[3] + width * gt[4] + height * gt[5] # min_y
        max_lon = gt[0] + width * gt[1] + height * gt[2] # max_x
        max_lat = gt[3] # max_y
        # min_lon, min_lat, max_lon, max_lat
        geo_file_coordinates = [min_lon, min_lat, max_lon, max_lat]
        return geo_file_coordinates


def geotiff(directory, coordinates_stop_points):
    """
    This function downloads the GeoTiff file in
    the Topodata database, according to the input
    coordinates. In other words, it checks which
    geotiff files contain a bounding box, defined
    by the input coordinates.

    The function also verifies if the GeoTiff file
    exists in a directory before download it. If it
    not exists, the function downloads the GeoTiff file.

    :param directory:                   String

    :param coordinates_stop_points:     list
                                        The list should
                                        have tuples with
                                        coordinates of the
                                        points.

    :return:                            String
                                        The name of the GeoTiff
                                        file

    Example of coordinates_stop_points:
    coordinates = [(-22.816008, -47.075614), (-22.816639, -47.074891),
                   (-22.818317, -47.083415), (-22.820244, -47.085422),
                   (-22.816008, -47.075614), (-22.823953, -47.087718)]

    """

    coordinates_osm = Coordinates.coordinates_list_bbox(coordinates_stop_points)
    file_names = Topodata.file_names_topodata(coordinates_osm)

    number_of_files = len(file_names)

    geo_directory_and_file_names = set_tif_names(directory, file_names)

    _geotiff(directory, file_names)

    if number_of_files > 1:
        mosaic_name = 'out.tif'
        join_geo(directory, geo_directory_and_file_names, mosaic_name)
        return mosaic_name
    else:
        tif_name = file_names[0]
        return tif_name


if __name__ == "__main__":
    coordinates_path = [(-22.816008, -47.075614, 606.0), (-22.816639, -47.074891, 602.0),
                        (-22.818317, -47.083415, 602.0), (-22.820244, -47.085422, 602.0),
                        (-22.816008, -47.075614, 606.0), (-22.823953, -47.087718, 602.0)]

    coordinates_1 = [(-25.977999, -49.575614, 606.0), (-25.877999, -49.585614, 602.0),
                     (-26.011199, -49.515614, 602.0), (-26.101199, -49.595614, 602.0),
                     (-26.021199, -49.075614, 606.0), (-26.051100, -49.071614, 602.0)]

    dir_geo = '../data/maps/'
    geotiff(dir_geo, coordinates_1)
    # file_name = '22S48_ZN'
    ###
    # Host:
    # sudo apt-get install gdal-bin
    # sudo apt-get install libgdal-dev libgdal1h
    # enviroment:
    # pip install GDAL==$(gdal-config --version) --global-option=build_ext --global-option="-I/usr/include/gdal"