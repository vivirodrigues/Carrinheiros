from classes import User, Path
from geography import Coordinates, OpenSteetMap, GeoTiff
import osmnx as ox
from Constants import *
from route import Graph
from route import Scenario


class Carrinheiros:
    def __init__(self, id_user, date):
        self.id_user = id_user
        self.collection_day = date
        self.directory_json = DATABASE_DIRECTORY
        self.directory_maps = MAPS_DIRECTORY
        self.carrinheiro = User.get_user(id_user, self.directory_json)
        self.path = Path.Path(self.carrinheiro, date, self.directory_json)

    def main(self):

        # get user stop points
        stop_points = self.path.get_stop_points()

        # download the osm file (scenario)
        osm_scenario = OpenSteetMap.file_osm(self.directory_maps, FILE_NAME_OSM, stop_points)

        # download the GeoTiff file (scenario)
        geotiff_name = GeoTiff.geotiff(self.directory_maps, stop_points)

        max_lat, min_lat, max_lon, min_lon = Coordinates.create_osmnx(stop_points)

        # graph
        G = ox.graph_from_bbox(max_lat, min_lat, max_lon, min_lon, network_type='all')
        G = Scenario.add_collect_points(G, stop_points)
        G = Graph.set_node_elevation(G, MAPS_DIRECTORY, geotiff_name)
        Graph.save_graph_file(G, MAPS_DIRECTORY, GRAPH_NAME)
        G = Graph.edge_grades(G)
        Graph.plot_graph(G)


if __name__ == '__main__':
    id_user1 = "000"
    date = "25 01 2021"
    scenario = Carrinheiros(id_user1, date)
    scenario.main()

