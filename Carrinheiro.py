import haversine as hs
from haversine import Unit
from geography import Coordinates
import osmnx as ox
from Constants import *
from route import Graph
from route import Graph_Collect
from route import Heuristics, GA
import time


def scenario_stop_points(path):

    # get user stop points
    stop_points = path.get_stop_points()

    stop_points = coverage_area(stop_points)

    return stop_points


def coverage_area(stop_points):

    # validate coordinates points
    # according to coverage area
    coordinate_initial = (stop_points[0][1], stop_points[0][0])
    for i in stop_points:
        distance_node_initial = hs.haversine((i[1], i[0]), coordinate_initial, unit=Unit.METERS)
        if distance_node_initial > COVERAGE_AREA:
            stop_points.remove(i)

    return stop_points


def graph_scenario(stop_points, geotiff_name, ad_weights, file_name_osm):

    max_lat, min_lat, max_lon, min_lon = Coordinates.create_osmnx(stop_points)

    # Scenario graph (paths are edges and junctions are nodes)
    G = ox.graph_from_bbox(max_lat, min_lat, max_lon, min_lon, network_type='all')
    G, nodes_coordinates, nodes_mass_increment = Graph.configure_graph(G, geotiff_name, stop_points, ad_weights, file_name_osm)
    return G, nodes_coordinates, nodes_mass_increment


def nearest_neighbor_path(G, H, node_source, node_target, impedance):

    route = Heuristics.nearest_neighbor(G, H, node_source, node_target, VEHICLE_MASS, impedance)
    cost_total, paths = Graph_Collect.sum_costs_route(G, H, route, VEHICLE_MASS, impedance)

    return cost_total, paths


def closest_insertion_path(G, H, node_source, node_target, impedance):

    # order the visit of the stop points
    route = Heuristics.closest_insertion(G, H, node_source, node_target, impedance)

    # create the path to visit all stop points
    cost_total, paths = Graph_Collect.sum_costs_route(G, H, route, VEHICLE_MASS, impedance)

    return cost_total, paths


def further_insertion_path(G, H, node_source, node_target, impedance):

    # order the visit of the stop points
    route = Heuristics.further_insertion(G, H, node_source, node_target, impedance)

    # create the path to visit all stop points
    cost_total, paths = Graph_Collect.sum_costs_route(G, H, route, VEHICLE_MASS, impedance)

    return cost_total, paths


def genetic_algorithm(G, H, node_source, node_target, nodes_coordinates, impedance):

    nodes_h = list(nodes_coordinates.keys())
    route = GA.GA(G, H, node_source, node_target, nodes_h, impedance)
    cost_total, paths = Graph_Collect.sum_costs_route(G, H, route, VEHICLE_MASS, impedance)

    return cost_total, paths


def exact_method_path(G, H, node_source, node_target, nodes_coordinates):
    cost_total, route, paths = Heuristics.exact_method(G, H, node_source, node_target)
    return cost_total, paths


