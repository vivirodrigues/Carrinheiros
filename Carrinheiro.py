import argparse
import haversine as hs
from haversine import Unit
from classes import User, Path
from geography import Coordinates, OpenSteetMap, GeoTiff
import osmnx as ox
from Constants import *
from route import Graph
from route import Graph_Collect
from route import Heuristics, GA
import time
import sys
from simulation import Map_Simulation


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
            # print("The ad available in the", i, "coordinate is outside the coverage area.")
            stop_points.remove(i)

    return stop_points


def graph_scenario(stop_points, geotiff_name, ad_weights, file_name_osm):

    max_lat, min_lat, max_lon, min_lon = Coordinates.create_osmnx(stop_points)

    # Scenario graph (paths are edges and junctions are nodes)
    G = ox.graph_from_bbox(max_lat, min_lat, max_lon, min_lon, network_type='all')
    # ox.plot_graph(G)
    G, nodes_coordinates, nodes_mass_increment = Graph.configure_graph(G, geotiff_name, stop_points, ad_weights, file_name_osm)
    # print(nodes_and_coordinates, nodes_and_weights)
    return G, nodes_coordinates, nodes_mass_increment


#def nearest_neighbor_path(G, H, node_source, node_target, impedance=IMPEDANCE):
def nearest_neighbor_path(G, H, node_source, node_target, impedance):

    #start = time.time()
    route = Heuristics.nearest_neighbor(G, H, node_source, node_target, VEHICLE_MASS, impedance)
    cost_total, paths = Graph_Collect.sum_costs_route(G, H, route, VEHICLE_MASS, impedance)
    #end = time.time()
    #print("Total cost route nearest", route, cost_total)
    #print("time nearest (s)", end - start)

    return cost_total, paths


#def closest_insertion_path(G, H, node_source, node_target, impedance = IMPEDANCE):
def closest_insertion_path(G, H, node_source, node_target, impedance):

    #start = time.time()

    # order the visit of the stop points
    route = Heuristics.closest_insertion(G, H, node_source, node_target, impedance)

    # create the path to visit all stop points
    cost_total, paths = Graph_Collect.sum_costs_route(G, H, route, VEHICLE_MASS, impedance)

    #end = time.time()
    #print("Total cost route closest insertion", route, cost_total)
    #print("time closest insertion (s)", end - start)

    return cost_total, paths


def further_insertion_path(G, H, node_source, node_target, impedance):

    #start = time.time()

    # order the visit of the stop points
    route = Heuristics.further_insertion(G, H, node_source, node_target, impedance)

    # create the path to visit all stop points
    cost_total, paths = Graph_Collect.sum_costs_route(G, H, route, VEHICLE_MASS, impedance)

    #end = time.time()
    #print("Total cost route closest insertion", route, cost_total)
    #print("time closest insertion (s)", end - start)

    return cost_total, paths


#def genetic_algorithm(G, H, node_source, node_target, nodes_coordinates, impedance=IMPEDANCE):
def genetic_algorithm(G, H, node_source, node_target, nodes_coordinates, impedance):

    nodes_h = list(nodes_coordinates.keys())
    start = time.time()
    route = GA.GA(G, H, node_source, node_target, nodes_h, impedance)
    end = time.time()
    cost_total, paths = Graph_Collect.sum_costs_route(G, H, route, VEHICLE_MASS, impedance)
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

    # download the osm file (scenario)
    file_name_osm = OpenSteetMap.file_osm(MAPS_DIRECTORY, stop_points)

    # download the GeoTiff file (scenario)
    geotiff_name = GeoTiff.geotiff(MAPS_DIRECTORY, stop_points)

    G, nodes_coordinates, nodes_mass_increment = graph_scenario(stop_points, geotiff_name, path.material_weights, file_name_osm)

    H = Graph_Collect.create_graph_route(nodes_coordinates, nodes_mass_increment)

    index_coordinate_start = list(nodes_coordinates.values()).index(path.start_point)
    node_source = list(nodes_coordinates.keys())[index_coordinate_start]
    index_coordinate_end = list(nodes_coordinates.values()).index(path.end_point)
    node_target = list(nodes_coordinates.keys())[index_coordinate_end]

    cost_total, paths = closest_insertion_path(G, H, node_source, node_target)

    for i in paths:
        fig, ax = ox.plot_graph_route(G, i, route_linewidth=6, node_size=0, bgcolor='w')

    return paths


if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Execution parameters')

    parser.add_argument('--idUser', metavar='t', type=str, nargs=1, default=["000"], action='store',
                        help='id of the user \"carrinheiro\"')
    parser.add_argument('--date', metavar='t', type=str, nargs=1, default=["25 01 2021"], action='store',
                        help='Collection date \"DD MM YYYY\"')

    args = parser.parse_args()

    # dirGeo = args.dirGeo[0].split('/')[0]
    id_user = args.idUser[0]
    date = args.date[0]

    #id_user = "000"
    #date = "25 01 2021"
    paths = carrinheiro(id_user, date)


