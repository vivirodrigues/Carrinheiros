from classes.adServer import User, Path, JsonDB, DateTime
from classes.mapsServer import ScenarioOSM, ScenarioGeo, Coordinates
import osmnx as ox

from classes.route import Graph


class Scenario:
    def __init__(self, id_user, date):
        self.id_user = id_user
        self.collection_day = date
        self.directory_json = 'classes/DB/'
        self.directory_maps = 'classes/maps/'
        self.carrinheiro = User.get_user(id_user, self.directory_json)
        self.path = Path.Path(self.carrinheiro, date, self.directory_json)

    def main(self):

        # get user stop points
        stop_points = self.path.get_stop_points()
        print(stop_points)

        # download the osm file (scenario)
        osm_scenario = ScenarioOSM.ScenarioOsm(self.directory_maps, stop_points)

        # download the GeoTiff file (scenario)
        geo_scenario = ScenarioGeo.ScenarioGeo(self.directory_maps, stop_points)
        geotiff_name = geo_scenario.tif_name

        max_lon = Coordinates.max_longitude(stop_points)
        min_lon = Coordinates.min_longitude(stop_points)
        max_lat = Coordinates.max_latitude(stop_points)
        min_lat = Coordinates.min_latitude(stop_points)

        # graph
        G = ox.graph_from_bbox(max_lat, min_lat, max_lon, min_lon, network_type='all')
        G = Graph.set_node_elevation(G, geotiff_name)
        G = Graph.set_edge_grades(G)
        Graph.save_graph_file(G, '../classes/maps/map.graphml')
        # Graph.plot_graph(G)


if __name__ == '__main__':
    id_user1 = "000"
    date = "25 01 2021"
    scenario = Scenario(id_user1, date)
    scenario.main()


