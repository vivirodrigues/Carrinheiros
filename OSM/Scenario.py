import Coordinates
import Overpass
import Download
import argparse
import JsonFile


class Scenario:
    def __init__(self, coord, directory):
        self.city = 'Campinas'
        self.state = 'SP'
        self.country = 'BR'
        self.iso = ''
        self.coordinates_list = coord
        self.file_name_osm = 'map.osm'
        self.file_name_geotiff = '22S48_ZN.tif'
        self.directory = directory
        self.id_state_area = 0.0
        self.coordinates_osm = ''
        self.scenario_osm = ''
        self.scenario_geotiff = ''
        self.osm_relation = 3600000000
        self.set_city()
        self.set_state_area()
        self.set_coordinates_osm()
        self.set_osm()
        self.set_geotiff()

    def set_city(self):
        overpass_query = "[out:json];is_in" + str(self.coordinates_list[0]) + "; out geom qt; "
        json_osm = JsonFile.JsonFile(overpass_query)
        response_json = json_osm.get_elements()
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
        coordinates = Coordinates.Coordinates(self.city, self.id_state_area)
        self.coordinates_osm = coordinates.get_coordinates()

    def set_osm(self):
        # it checks if file exists
        try:
            with open(self.directory + self.file_name_osm, 'r') as f:
                self.scenario_osm = f.read()
        except IOError:
            download_file = Download.Download(self.coordinates_osm, self.file_name_osm)
            download_file.download_osm()
            self.set_osm()

    def set_geotiff(self):
        # it checks if file exists
        try:
            with open(self.directory + self.file_name_geotiff, 'r') as f:
                # self.scenario_geotiff = f.read()
                print("File exists")
        except IOError:
            download_file = Download.Download(self.coordinates_osm, self.file_name_geotiff)
            download_file.download_geotiff()
            self.set_geotiff()


if __name__ == "__main__":
    default_coord = "[(-22.816008,-47.075614),(-22.816639,-47.074891),(-22.818317,-47.083415),(-22.820244,-47.085422),(-22.823953,-47.087718)]"
    parser = argparse.ArgumentParser(description='Execution parameters')
    parser.add_argument('--directory', metavar='t', type=str, nargs=1, default=["../maps/"], action='store', help='File Directory')
    parser.add_argument("--coord", metavar='t', type=str, nargs=1, default=[default_coord], action='store', help= 'Coord')

    args = parser.parse_args()

    directory = args.directory[0].split('/')[-1]
    coord = args.coord[0]

    print("a", directory)
    print(coord)
    Scenario(coord, directory)
