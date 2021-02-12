import requests


class DownloadOsm:
    # Download osm file in Overpass API using xapi_meta for large files
    def __init__(self, coordinates, file_name, directory_file):
        self.coordinates_osm = coordinates  # scenario rectangle area
        self.file_name_osm = file_name
        self.directory = directory_file
        self.download()

    def download(self):
        print(self.coordinates_osm)
        url = "http://overpass.openstreetmap.ru/cgi/xapi_meta?*[bbox={}]".format(self.coordinates_osm)
        r = requests.get(url, allow_redirects=True)
        with open(self.directory + self.file_name_osm, 'w') as fd:
            fd.write(r.text)
        print("Downloaded File:", self.file_name_osm, "\nCoordinates", self.coordinates_osm)


if __name__ == "__main__":
    coordinates_osm = str(-47.246313) + "," + str(-23.0612161) + "," + str(-47.239999) + "," + str(-23.0609999)
    name_file = "map.osm"
    directory = '../geography/'
    download_test = DownloadOsm(coordinates_osm, name_file, directory)
