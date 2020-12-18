import requests
import urllib.request
import zipfile


class Download:
    def __init__(self, coordinates, file_name):
        self.coordinates_osm = coordinates
        self.file_name_osm = file_name
        self.file_name_geotiff = "22S48_ZN"
        self.directory = '../maps/'

    def download_osm(self):
        url = "http://overpass.openstreetmap.ru/cgi/xapi_meta?*[bbox={}]".format(self.coordinates_osm)
        r = requests.get(url, allow_redirects=True)
        with open(self.directory + self.file_name_osm, 'w') as fd:
            fd.write(r.text)
        print("Downloaded File:", self.file_name_osm, "\nCoordinates", self.coordinates_osm)

    def download_geotiff(self):
        url = "http://www.dsr.inpe.br/topodata/data/geotiff/" + self.file_name_geotiff
        with urllib.request.urlopen(url) as dl_file:
            with open(self.directory + self.file_name_geotiff, 'wb') as out_file:
                out_file.write(dl_file.read())
        with zipfile.ZipFile(self.directory + self.file_name_geotiff, 'r') as zip_ref:
            zip_ref.extractall(self.directory)


if __name__ == "__main__":
    coordinates_osm = str(-47.246313) + "," + str(-23.0612161) + "," + str(-47.239999) + "," + str(-23.0609999)
    name_file = "map.osm"
    download_test = Download(coordinates_osm, name_file)
    # download_test.download_osm()
    download_test.download_geotiff()
