from OSM import Coordinates
from OSM import Overpass
from OSM import Download
import Path
import argparse
from OSM import JsonOverpass


class Scenario:
    def __init__(self, dirGeo, dirData):
        self.city = 'Campinas'
        self.state = 'SP'
        self.country = 'BR'
        self.iso = ''
        self.osm_coordinate = ()
        self.coordinates_list = []
        self.file_name_osm = 'map.osm'
        self.file_name_geotiff = '22S48_ZN.tif'
        self.dir_geotiff = dirGeo
        self.dir_data = dirData
        self.id_state_area = 0.0
        self.coordinates_osm = ''
        self.scenario_osm = ''
        self.scenario_geotiff = ''
        self.osm_relation = 3600000000
        self.set_coordinates_osm()
        self.set_city()
        self.set_state_area()
        self.set_osm()
        self.set_geotiff()

    def set_city(self):
        overpass_query = "[out:json];is_in" + str(self.osm_coordinate) + "; out geom qt; "
        print("query:", overpass_query)
        json_osm = JsonOverpass.JsonFile(overpass_query)
        print("json:", json_osm)
        response_json = json_osm.get_elements()
        print("response:", response_json)
        for i in response_json:
            tags = i.get("tags")
            if tags.get("ISO3166-2") is not None:
                iso = tags.get("ISO3166-2")
        self.iso = iso
        print(self.iso)

    def set_state_area(self):
        # iso = self.country + '-' + self.state
        # OSM pattern : 3600000000 for relation, 2400000000 for way
        query_state = "relation['ISO3166-2'='" + self.iso + "']; (._;>;); out ids;"
        api_overpass = Overpass.Overpass(query_state)
        result = api_overpass.get_response()
        self.id_state_area = result.relations[0].id + self.osm_relation
        print("State area", self.id_state_area)

    def set_coordinates_osm(self):
        # coordinates = CityCoordinates.Coordinates(self.city, self.id_state_area)
        path = Path.Path("000")
        self.coordinates_list = path.get_coordinates_path()
        print(self.coordinates_list)
        osm_lat = self.coordinates_list[0][0]
        osm_lon = self.coordinates_list[0][1]
        self.osm_coordinate = (osm_lat, osm_lon)
        coordinates = Coordinates.Coordinates(path.get_coordinates_path())
        self.coordinates_osm = coordinates.get_coordinates()

    def set_osm(self):
        # it checks if file exists
        try:
            with open('../maps/' + self.file_name_osm, 'r') as f:
                self.scenario_osm = f.read()
        except IOError:
            download_file = Download.Download(self.coordinates_osm, self.file_name_osm)
            download_file.download_osm()
            self.set_osm()

    def set_geotiff(self):
        # it checks if file exists
        try:
            with open(self.dir_geotiff + self.file_name_geotiff, 'r') as f:
                # self.scenario_geotiff = f.read()
                print("File exists")
        except IOError:
            download_file = Download.Download(self.coordinates_osm, self.file_name_geotiff)
            download_file.download_geotiff()
            self.set_geotiff()


if __name__ == "__main__":
    # default_coord = [(-22.816008,-47.075614),(-22.816639,-47.074891),(-22.818317,-47.083415),(-22.820244,-47.085422),(-22.823953,-47.087718)]
    parser = argparse.ArgumentParser(description='Execution parameters')
    parser.add_argument('--dirGeoTiff', metavar='t', type=str, nargs=1, default=["../maps/"], action='store', help='File Directory')
    parser.add_argument("--dirData", metavar='t', type=str, nargs=1, default=["../data"], action='store', help= 'Data directory')

    args = parser.parse_args()

    dirGeo = args.dirGeoTiff[0].split('/')[-1]
    dirData = args.dirData[0].split('/')[-1]

    print("dirGeo", dirGeo)
    print("dirData", dirData)
    Scenario(dirGeo, dirData)
