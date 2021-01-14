from models.mapsServer import DownloadGeo


class ScenarioGeo:
    # reading the GeoTiff file
    def __init__(self, geo_directory, coordinates_stop_points):
        self.dir_geo = geo_directory
        self.coordinates_list = coordinates_stop_points
        self.file_name = ''
        self.scenario_geotiff = ''
        self.main()

    def set_name_geo(self):
        self.file_name = '22S48_ZN'  # create a function to find it name

    def set_geotiff(self):
        # it checks if the file exists
        try:
            with open(self.dir_geo + self.file_name, 'r') as f:
                # self.scenario_geotiff = f.read()
                print("File exists")
        except IOError:
            # if not exists, it downloads the file
            download_file = DownloadGeo.DownloadGeo(self.file_name, self.dir_geo)
            self.set_geotiff()

    def join_geo(self):
        # it sticks the files according to the coordinates
        pass

    def main(self):
        self.set_name_geo()
        self.set_geotiff()


if __name__ == "__main__":
    coordinates_path = [(-22.816008, -47.075614, 606.0), (-22.816639, -47.074891, 602.0),
                        (-22.818317, -47.083415, 602.0), (-22.820244, -47.085422, 602.0),
                        (-22.816008, -47.075614, 606.0), (-22.823953, -47.087718, 602.0)]
    dir_geo = '../maps/'
    ScenarioGeo(dir_geo, coordinates_path)