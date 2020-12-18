import requests


class Download:
    def __init__(self, coordinates, file_name):
        self.coordinates_osm = coordinates
        self.file_name = file_name

    def download(self):
        url = "http://overpass.openstreetmap.ru/cgi/xapi_meta?*[bbox={}]".format(self.coordinates_osm)
        r = requests.get(url, allow_redirects=True)
        with open('maps/' + self.file_name, 'w') as fd:
            fd.write(r.text)
        print("Downloaded File:", self.file_name, "\nCoordinates", self.coordinates_osm)


if __name__ == "__main__":
    coordinates_osm = str(-47.246313) + "," + str(-23.0612161) + "," + str(-47.239999) + "," + str(-23.0609999)
    name_file = "map.osm"
    download_test = Download(coordinates_osm, name_file)
    download_test.download()
