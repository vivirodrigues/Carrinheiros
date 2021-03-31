import urllib.request
import zipfile
import requests


def download_geotiff(directory, file_name):
    """
    This function downloads the GeoTiff file according to file_name.
    The file name should be defined in Topodata.py
    Ex:
    coordinates = [-00.00, -00.00, -00.00, -00.00]
    file_name = Topodata.file_names_topodata(coordinates)
    directory = '../folder'
    Download.download_geotiff(file_name, directory)


    :param file_name:       String
                            Name of the file that must be downloaded.
                            It is according to the data model of Topodata.
                            Ex: 22S48_ZN
                            latitude + hemisphere + longitude +
                            + '_' or '5' + type of data

    :param directory:       folder that must be used to save the
                            downloaded file.
    """
    # In Brazil, geomorphometric data is on the INPE website (topodata)
    url = "http://www.dsr.inpe.br/topodata/data/geotiff/" + file_name
    with urllib.request.urlopen(url) as dl_file:
        with open(directory + file_name, 'wb') as out_file:
            out_file.write(dl_file.read())
    with zipfile.ZipFile(directory + file_name, 'r') as zip_ref:
        zip_ref.extractall(directory)


def download_osm(coordinates_osm, file_name):
    """
    :param coordinates_osm  Sting
                            bbox=left,bottom,right,top
                            left: minLon
                            bottom: minLat
                            right: maxLon
                            top: maxLat

    :param file_name:       String
                            Name of the file that must be downloaded.
                            Ex: 'map.osm' or 'map'

    """
    name_len = len(file_name)
    file_extension = file_name[name_len-4] + file_name[name_len-3] + file_name[name_len-2] + file_name[name_len-1]

    print("Downloading: ", coordinates_osm)
    url = "http://overpass.openstreetmap.ru/cgi/xapi_meta?*[bbox={}]".format(coordinates_osm)
    r = requests.get(url, allow_redirects=True)
    if file_extension == '.osm':
        with open(file_name, 'w') as fd:
            fd.write(r.text)
    else:
        with open(file_name + '.osm', 'w') as fd:
            fd.write(r.text)
    # print("Downloaded File:", file_name, "\nCoordinates", coordinates_osm)


if __name__ == "__main__":
    coordinates_osm = str(-47.246313) + "," + str(-23.0612161) + "," + str(-47.239999) + "," + str(-23.0609999)
    # name_file = "map.osm"
    # directory = '../geography/'
    #download_osm(coordinates_osm, directory + name_file)

    name_file = "01S495ZN"
    directory = '../data/maps/'
    download_geotiff(directory, name_file)