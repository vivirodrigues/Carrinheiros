from classes import User, Path
from geography import Coordinates, OpenSteetMap, GeoTiff
import osmnx as ox
from Constants import *
from route import Graph
from route import Graph_Collect
from route import Heuristics


class Carrinheiro:
    def __init__(self, id_user, date, vehicle_mass):
        self.id_user = id_user
        self.collection_day = date
        self.vehicle_mass = vehicle_mass  # Kg
        self.carrinheiro = User.get_user(id_user, DATABASE_DIRECTORY)
        self.path = Path.Path(self.carrinheiro, date, DATABASE_DIRECTORY)
        self.ad_weights = self.path.get_weight()
        self.id_node_start = ''
        self.id_node_end = ''

    def main(self):

        # get user stop points
        stop_points = self.path.get_stop_points()

        # download the osm file (scenario)
        osm_scenario = OpenSteetMap.file_osm(MAPS_DIRECTORY, FILE_NAME_OSM, stop_points)

        # download the GeoTiff file (scenario)
        geotiff_name = GeoTiff.geotiff(MAPS_DIRECTORY, stop_points)

        max_lat, min_lat, max_lon, min_lon = Coordinates.create_osmnx(stop_points)

        # Scenario graph (paths are edges and junctions are nodes)
        G = ox.graph_from_bbox(max_lat, min_lat, max_lon, min_lon, network_type='all')
        G, nodes_and_coordinates, nodes_and_weights = Graph.configure_graph(G, geotiff_name, stop_points, self.vehicle_mass, self.ad_weights)

        # Graph with all collect points
        H = Graph_Collect.create_graph_route(nodes_and_coordinates, nodes_and_weights)

        index_coordinate_start = list(nodes_and_coordinates.values()).index(self.path.start_point)
        self.id_node_start = list(nodes_and_coordinates.keys())[index_coordinate_start]
        index_coordinate_end = list(nodes_and_coordinates.values()).index(self.path.end_point)
        self.id_node_end = list(nodes_and_coordinates.keys())[index_coordinate_end]

        print("From", self.id_node_start, "to", self.id_node_end)
        route = Heuristics._best_first_search(G, H, self.id_node_start, self.id_node_end, self.vehicle_mass)


if __name__ == '__main__':
    id_user1 = "000"
    date = "25 01 2021"
    scenario = Carrinheiro(id_user1, date, 110)
    scenario.main()


