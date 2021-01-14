import urllib.request
import zipfile


class DownloadGeo:
    # Download GeoTiff zip and unzips the file
    def __init__(self, file_name, directory_file):
        self.file_name = file_name
        self.directory = directory_file
        self.download()

    def download(self):
        # In Brazil, geomorphometric data is on the INPE website (topodata)
        url = "http://www.dsr.inpe.br/topodata/data/geotiff/" + self.file_name
        with urllib.request.urlopen(url) as dl_file:
            with open(self.directory + self.file_name, 'wb') as out_file:
                out_file.write(dl_file.read())
        with zipfile.ZipFile(self.directory + self.file_name, 'r') as zip_ref:
            zip_ref.extractall(self.directory)


if __name__ == "__main__":
    name_file = "22S48_ZN"
    directory = '../maps/'
    download_test = DownloadGeo(name_file, directory)
