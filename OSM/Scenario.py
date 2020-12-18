from OSM import JsonFile
from OSM import Coordinates
from OSM import Overpass
from OSM import Download


class Scenario:
    def __init__(self, city, state, country):
        self.city = city
        self.state = state
        self.country = country
        self.file_name = 'map.osm'
        self.id_state_area = 0.0
        self.coordinates_osm = ''
        self.scenario = ''
        self.osm_relation = 3600000000
        self.main()

    def set_state_area(self):
        iso = self.country + '-' + self.state
        # OSM pattern : 3600000000 for relation, 2400000000 for way
        query_state = "relation['ISO3166-2'='" + iso + "']; (._;>;); out ids;"
        api_overpass = Overpass.Overpass(query_state)
        result = api_overpass.get_response()
        self.id_state_area = result.relations[0].id + self.osm_relation

    def set_coordinates_osm(self):
        coordinates = Coordinates.Coordinates(self.city, self.id_state_area)
        self.coordinates_osm = coordinates.get_coordinates()

    def set_scenario(self):
        # it checks if file exists
        try:
            with open(self.file_name, 'r') as f:
                self.scenario = f.read()
                print(self.scenario)
        except IOError:
            download_file = Download.Download(self.coordinates_osm, self.file_name)
            download_file.download()
            self.set_scenario()

    def main(self):
        self.set_state_area()
        self.set_coordinates_osm()
        self.set_scenario()


if __name__ == "__main__":
    Scenario("Campinas", "SP", "BR")
