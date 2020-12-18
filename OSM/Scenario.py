import Coordinates
import Overpass
import Download
import argparse


class Scenario:
    def __init__(self, city, state, country):
        self.city = city
        self.state = state
        self.country = country
        self.file_name_osm = 'map.osm'
        self.file_name_geotiff = '22S48_ZN.tif'
        self.directory = '../maps/'
        self.id_state_area = 0.0
        self.coordinates_osm = ''
        self.scenario_osm = ''
        self.scenario_geotiff = ''
        self.osm_relation = 3600000000
        self.main()

    def set_state_area(self):
        iso = self.country + '-' + self.state
        # OSM pattern : 3600000000 for relation, 2400000000 for way
        query_state = "relation['ISO3166-2'='" + iso + "']; (._;>;); out ids;"
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

    def main(self):
        self.set_state_area()
        self.set_coordinates_osm()
        self.set_osm()
        self.set_geotiff()


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='Execution parameters')
    parser.add_argument('--city', metavar='t', type=str, nargs=1, default=['Campinas'], action='store', help='Scenario City')
    parser.add_argument('--state', metavar='t', type=str, nargs=1, default=['SP'], action='store', help='Scenario State')
    parser.add_argument('--country', metavar='t', type=str, nargs=1, default=['BR'], action='store', help='Scenario Country')

    args = parser.parse_args()

    city = args.city[0].split('/')[-1]
    state = args.state[0].split('/')[-1]
    country = args.country[0].split('/')[-1]

    Scenario(city, state, country)
