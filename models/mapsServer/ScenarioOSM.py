from models.mapsServer import Overpass, Coordinates, DownloadOsm, JsonOverpass
from models.mapsServer.Coordinates import Coordinates


def set_iso(search_coordinate):
    ###
    # iso = country + '-' + state
    # example : 'BR-SP'
    # it is used when you want to download a complete city
    ###
    overpass_query = "[out:json];is_in" + str(search_coordinate) + "; out geom qt; "
    json_osm = JsonOverpass.JsonOverpass(overpass_query)
    response_json = json_osm.get_elements()
    iso = ''
    for i in response_json:
        tags = i.get("tags")
        if tags.get("ISO3166-2") is not None:
            iso = tags.get("ISO3166-2")
    return iso


def set_state_area(search_coordinate, osm_relation):
    ###
    # return a state code
    # it is used when you want to download a complete city
    # OSM_relation : 3600000000 for relation, 2400000000 for way
    ###
    iso = set_iso(search_coordinate)
    query_state = "relation['ISO3166-2'='" + iso + "']; (._;>;); out ids;"
    api_overpass = Overpass.Overpass(query_state)
    result = api_overpass.get_response()
    id_state_area = result.relations[0].id + osm_relation
    return id_state_area


class ScenarioOsm:
    # reading the osm file
    def __init__(self, osm_dir, coordinates_stop_points):
        self.coordinates_osm = Coordinates(coordinates_stop_points).get_coordinates()
        self.coordinates_list = Coordinates(coordinates_stop_points).get_coordinates_list()
        self.iso = ''
        self.search_coordinate = ()
        self.file_name_osm = 'map.osm'
        self.dir_osm = osm_dir
        self.id_state_area = 0.0
        self.scenario_osm = ''
        self.osm_relation = 3600000000
        self.main()

    def set_search_coordinate(self):
        # it is used in queries to search overpass
        osm_lat = self.coordinates_list[0]
        osm_lon = self.coordinates_list[0]
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
        self.set_osm()


if __name__ == "__main__":
    coordinates_path = [(-22.816008, -47.075614, 606.0), (-22.816639, -47.074891, 602.0),
                        (-22.818317, -47.083415, 602.0), (-22.820244, -47.085422, 602.0),
                        (-22.816008, -47.075614, 606.0), (-22.823953, -47.087718, 602.0)]
    dir_osm = '../maps/'
    ScenarioOsm(dir_osm, coordinates_path)