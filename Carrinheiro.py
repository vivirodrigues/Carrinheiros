from classes import User, Path
from geography import Coordinates, OpenSteetMap, GeoTiff
import osmnx as ox
from Constants import *
from route import Graph
from route import Graph_Collect
from route import Heuristics, GA
import time


def scenario_stop_points(path):

    # get user stop points
    stop_points = path.get_stop_points()

    # download the osm file (scenario)
    stop_points = OpenSteetMap.file_osm(MAPS_DIRECTORY, FILE_NAME_OSM, stop_points)

    return stop_points


def graph_scenario(stop_points, geotiff_name, ad_weights):

    max_lat, min_lat, max_lon, min_lon = Coordinates.create_osmnx(stop_points)

    # Scenario graph (paths are edges and junctions are nodes)
    G = ox.graph_from_bbox(max_lat, min_lat, max_lon, min_lon, network_type='all')
    G, nodes_coordinates, nodes_mass_increment = Graph.configure_graph(G, geotiff_name, stop_points, VEHICLE_MASS,
                                                                        ad_weights)
    # print(nodes_and_coordinates, nodes_and_weights)
    return G, nodes_coordinates, nodes_mass_increment


def nearest_neighbor_path(G, H, node_source, node_target):

    start = time.time()
    route = Heuristics.nearest_neighbor(G, H, node_source, node_target, VEHICLE_MASS)
    cost_total, paths = Graph_Collect.sum_costs_route(G, H, route, VEHICLE_MASS)
    end = time.time()
    print("Total cost route nearest", route, cost_total)
    print("time nearest (s)", end - start)

    return cost_total, paths


def closest_insertion_path(G, H, node_source, node_target):
    start = time.time()
    route = Heuristics.closest_insertion(G, H, node_source, node_target)
    cost_total, paths = Graph_Collect.sum_costs_route(G, H, route, VEHICLE_MASS)
    end = time.time()
    print("Total cost route closest insertion", route, cost_total)
    print("time closest insertion (s)", end - start)

    return cost_total, paths


def genetic_algorithm(G, H, node_source, node_target, nodes_coordinates):
    nodes_h = list(nodes_coordinates.keys())
    start = time.time()
    route = GA.GA(G, H, node_source, node_target, nodes_h)
    end = time.time()
    cost_total, paths = Graph_Collect.sum_costs_route(G, H, route, VEHICLE_MASS)
    print("Total cost route GA", route, cost_total)
    print("Time GA", end - start)

    return cost_total, paths


def exact_method_path(G, H, node_source, node_target, nodes_coordinates):
    start = time.time()
    cost_total, route, paths = Heuristics.exact_method(G, H, node_source, node_target)
    end = time.time()
    print("Total cost route exact method", route, cost_total)
    print("time exact method", end - start)
    return cost_total, paths


def carrinheiro(id_user, date):
    user_carrinheiro = User.get_user(id_user, DATABASE_DIRECTORY)
    path = Path.Path(user_carrinheiro, date, DATABASE_DIRECTORY)

    stop_points = scenario_stop_points(path)

    # download the GeoTiff file (scenario)
    geotiff_name = GeoTiff.geotiff(MAPS_DIRECTORY, stop_points)

    G, nodes_coordinates, nodes_mass_increment = graph_scenario(stop_points, geotiff_name, path.material_weights)

    H = Graph_Collect.create_graph_route(nodes_coordinates, nodes_mass_increment)

    index_coordinate_start = list(nodes_coordinates.values()).index(path.start_point)
    node_source = list(nodes_coordinates.keys())[index_coordinate_start]
    index_coordinate_end = list(nodes_coordinates.values()).index(path.end_point)
    node_target = list(nodes_coordinates.keys())[index_coordinate_end]

    cost_total, paths = closest_insertion_path(G, H, node_source, node_target)

    for i in paths:
        fig, ax = ox.plot_graph_route(G, i, route_linewidth=6, node_size=0, bgcolor='w')


if __name__ == '__main__':
    id_user1 = "000"
    date = "25 01 2021"
    carrinheiro(id_user1, date)



