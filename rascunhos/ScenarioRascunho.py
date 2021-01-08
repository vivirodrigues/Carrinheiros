from models.mapsServer import Coordinates, DownloadOsm, JsonOverpass, Overpass
from models.adServer import Path, JsonDB, DateTime
import argparse


# OSM and GeoTiff
class Scenario:
    def __init__(self, dirOSM, dirGeo, dirModels, dirDB):
        self.iso = ''
        self.search_coordinate = ()
        self.coordinates_list = []
        self.file_name_osm = 'map.osm'
        self.file_name_geotiff = '22S48_ZN.tif'  # create a function to find it name
        self.dir_osm = dirOSM
        self.dir_geo = dirGeo
        self.dir_models = dirModels
        self.dir_db = dirDB
        self.id_state_area = 0.0
        self.coordinates_osm = ''
        self.scenario_osm = ''
        self.scenario_geotiff = ''
        self.osm_relation = 3600000000
        self.main()

    def set_city(self):
        overpass_query = "[out:json];is_in" + str(self.search_coordinate) + "; out geom qt; "
        json_osm = JsonOverpass.JsonFile(overpass_query)
        response_json = json_osm.get_elements()
        iso = ''
        for i in response_json:
            tags = i.get("tags")
            if tags.get("ISO3166-2") is not None:
                iso = tags.get("ISO3166-2")
        self.iso = iso

    def set_state_area(self):
        # iso = country + '-' + state : BR-SP
        # OSM pattern : 3600000000 for relation, 2400000000 for way
        query_state = "relation['ISO3166-2'='" + self.iso + "']; (._;>;); out ids;"
        api_overpass = Overpass.Overpass(query_state)
        result = api_overpass.get_response()
        self.id_state_area = result.relations[0].id + self.osm_relation
        print("State area", self.id_state_area)

    def set_coordinates_osm(self):
        path = Path.Path("000")
        self.coordinates_list = path.get_coordinates_path()
        osm_lat = self.coordinates_list[0][0]
        osm_lon = self.coordinates_list[0][1]
        self.search_coordinate = (osm_lat, osm_lon)
        coordinates = Coordinates.Coordinates(path.get_coordinates_path())
        self.coordinates_osm = coordinates.get_coordinates()

    def set_osm(self):
        # it checks if file exists
        try:
            with open(self.dir_osm + self.file_name_osm, 'r') as f:
                self.scenario_osm = f.read()
        except IOError:
            download_file = DownloadOsm.Download(self.coordinates_osm, self.file_name_osm, self.dir_osm)
            download_file.download_osm()
            self.set_osm()

    def set_geotiff(self):
        # it checks if file exists
        try:
            print(self.dir_geo + self.file_name_geotiff)
            with open(self.dir_geo + self.file_name_geotiff, 'r') as f:
                # self.scenario_geotiff = f.read()
                print("File exists")
        except IOError:
            download_file = DownloadOsm.Download(self.coordinates_osm, self.file_name_geotiff, self.dir_geo)
            download_file.download_geotiff()
            self.set_geotiff()

    def main(self):
        self.set_coordinates_osm()
        self.set_city()
        self.set_state_area()
        self.set_osm()
        self.set_geotiff()


if __name__ == "__main__":
    # default_coord = [(-22.816008,-47.075614),(-22.816639,-47.074891),(-22.818317,-47.083415),(-22.820244,-47.085422),(-22.823953,-47.087718)]
    parser = argparse.ArgumentParser(description='Execution parameters')
    parser.add_argument('--dirOSM', metavar='t', type=str, nargs=1, default=["../maps/"], action='store',
                        help='GeoTiff Directory')
    parser.add_argument('--dirGeo', metavar='t', type=str, nargs=1, default=["../GEOTIFF/"], action='store',
                        help='OSM Directory')
    parser.add_argument("--dirModels", metavar='t', type=str, nargs=1, default=["../models/"], action='store',
                        help='Data directory')
    parser.add_argument("--dirDB", metavar='t', type=str, nargs=1, default=["../models/DB/"], action='store',
                        help='DataBase directory')

    args = parser.parse_args()

    # dirGeo = args.dirGeo[0].split('/')[0]
    dirGeo = args.dirGeo[0]
    dirOSM = args.dirOSM[0]
    dirModels = args.dirModels[0]
    dirDB = args.dirDB[0]

    Scenario(dirOSM, dirGeo, dirModels, dirDB)
