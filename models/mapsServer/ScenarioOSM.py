from models.mapsServer import Overpass, Coordinates, DownloadOsm, JsonOverpass


class ScenarioOsm:
    def __init__(self, dir_osm, coordinates_path):
        self.iso = ''
        self.search_coordinate = ()
        self.coordinates_list = coordinates_path
        self.file_name_osm = 'map.osm'
        self.dir_osm = dir_osm
        self.id_state_area = 0.0
        self.coordinates_osm = ''
        self.scenario_osm = ''
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
        coordinates = Coordinates.Coordinates(self.coordinates_list)
        self.coordinates_osm = coordinates.get_coordinates()

    def set_search_coordinate(self):
        osm_lat = self.coordinates_list[0][0]
        osm_lon = self.coordinates_list[0][1]
        self.search_coordinate = (osm_lat, osm_lon)

    def set_osm(self):
        # it checks if file exists
        try:
            with open(self.dir_osm + self.file_name_osm, 'r') as f:
                self.scenario_osm = f.read()
        except IOError:
            download_file = DownloadOsm.DownloadOsm(self.coordinates_osm, self.file_name_osm, self.dir_osm)
            self.set_osm()

    def main(self):
        self.set_search_coordinate()
        self.set_coordinates_osm()
        # self.set_city()
        # self.set_state_area()
        self.set_osm()


if __name__ == "__main__":
    coordinates_path = [(-22.816008, -47.075614, 606.0), (-22.816639, -47.074891, 602.0),
                        (-22.818317, -47.083415, 602.0), (-22.820244, -47.085422, 602.0),
                        (-22.816008, -47.075614, 606.0), (-22.823953, -47.087718, 602.0)]
    dir_osm = '../maps/'
    ScenarioOsm(dir_osm, coordinates_path)