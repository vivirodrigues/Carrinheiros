from classes import User, Path
from geography import Coordinates, OpenSteetMap, GeoTiff
import osmnx as ox
from Constants import *
from route import Graph
from route import Graph_Collect
from route import Heuristics, GA
import time


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
        self.nodes_h = []

    def main(self):

        # get user stop points
        stop_points = self.path.get_stop_points()

        # download the osm file (scenario)
        stop_points = OpenSteetMap.file_osm(MAPS_DIRECTORY, FILE_NAME_OSM, stop_points)

        # download the GeoTiff file (scenario)
        geotiff_name = GeoTiff.geotiff(MAPS_DIRECTORY, stop_points)

        max_lat, min_lat, max_lon, min_lon = Coordinates.create_osmnx(stop_points)

        # Scenario graph (paths are edges and junctions are nodes)
        G = ox.graph_from_bbox(max_lat, min_lat, max_lon, min_lon, network_type='all')
        G, nodes_and_coordinates, nodes_and_weights = Graph.configure_graph(G, geotiff_name, stop_points, self.vehicle_mass, self.ad_weights)
        # print(nodes_and_coordinates, nodes_and_weights)

        # Graph with all collect points
        H = Graph_Collect.create_graph_route(nodes_and_coordinates, nodes_and_weights)
        self.nodes_h = list(nodes_and_coordinates.keys())

        index_coordinate_start = list(nodes_and_coordinates.values()).index(self.path.start_point)
        self.id_node_start = list(nodes_and_coordinates.keys())[index_coordinate_start]
        index_coordinate_end = list(nodes_and_coordinates.values()).index(self.path.end_point)
        self.id_node_end = list(nodes_and_coordinates.keys())[index_coordinate_end]
        """
        inicio = time.time()
        route_1 = Heuristics.nearest_neighbor(G, H, 1000000006, 1000000006, self.vehicle_mass)
        cost_total_1, paths_1 = Graph_Collect.sum_costs_route(G, H, route_1, VEHICLE_MASS)
        fim = time.time()
        print("Total cost route BFS", route_1, cost_total_1)
        print("time BFS (s)", fim - inicio)
        """
        inicio = time.time()
        route_2 = Heuristics.closest_insertion(G, H, 1000000006, 1000000006)
        cost_total_2, paths_2 = Graph_Collect.sum_costs_route(G, H, route_2, VEHICLE_MASS)
        fim = time.time()
        print("Total cost route closest insertion", route_2, cost_total_2)
        print("time closest insertion (s)", fim - inicio)
        """
        inicio = time.time()
        cost_total_3, route_3, paths_3 = Heuristics.exact_method(G, H, 1000000006, 1000000006)
        fim = time.time()
        print("Total cost route exact method", route_3, cost_total_3)
        print("time exact method", fim - inicio)
        
        inicio = time.time()
        route_GA = GA.GA(G, H, 1000000006, 1000000006, self.nodes_h)
        fim = time.time()
        cost_GA, paths_4 = Graph_Collect.sum_costs_route(G, H, route_GA, VEHICLE_MASS)
        print("Total cost route GA", route_GA, cost_GA)
        print("Time GA", fim - inicio)
        """

if __name__ == '__main__':
    id_user1 = "000"
    date = "25 01 2021"
    scenario = Carrinheiro(id_user1, date, 110)
    scenario.main()


