import networkx as nx
from route import Heuristics
from route import Graph
import matplotlib.pyplot as plt
from classes import Route
import osmnx as ox
from Constants import *


def create_graph_route(nodes_and_coordinates, nodes_and_weights):

    # creating a complete graph
    H = nx.complete_graph(len(nodes_and_coordinates.keys()))

    # Modifying node names (id nodes of G = id nodes of H)
    node_names = list(nodes_and_weights.keys())
    mapping = {i:node_names for i, node_names in enumerate(node_names)}
    H = nx.relabel_nodes(H, mapping)

    # Add x, y and value of vehicle mass increment
    for i in nodes_and_coordinates:
        coord = nodes_and_coordinates.get(i)
        weight_node = nodes_and_weights.get(i)
        H.nodes[i]['x'] = coord[1]
        H.nodes[i]['y'] = coord[0]
        H.nodes[i]['mass'] = weight_node
    return H


def sum_costs(G, path):
    weight = Graph._weight(G, 'weight')
    sum_costs = 0

    for i in range(len(path)-1):
        e = G.adj[path[i]].get(path[i + 1])
        if e is None:
            print(path[i], path[i + 1])
        weight_edge = weight(path[i], path[i + 1], e)
        sum_costs += weight_edge
    return sum_costs


def get_weight(G, source, target, vehicle_mass):

    G = Graph.update_weight(G, vehicle_mass)
    path = Heuristics.shortest_path_faster(G, source, target, 'weight')
    return sum_costs(G, path)


def sum_costs_route(G, H, route, vehicle_mass):

    vehicle_mass += H.nodes[route[0]]['mass']
    cost_work = 0
    cost_work_all = 0

    for node in range(len(route)-1):
        vehicle_mass += H.nodes[route[node]]['mass']
        cost_work = get_weight(G, route[node], route[node+1], vehicle_mass)
        cost_work_all += cost_work

    return cost_work_all

if __name__ == '__main__':
    nodes_weight = {1000000002: 0, 1000000004: (50, 'Kg'), 1000000006: (30, 'Kg'), 1000000008: (15, 'Kg'), 994679386: (12, 'Kg'), 1000000012: 0}
    nodes_coord = {1000000002: (-22.816008, -47.075614), 1000000004: (-22.816639, -47.074891), 1000000006: (-22.818317, -47.083415), 1000000008: (-22.820244, -47.085422), 994679386: (-22.823953, -47.087718), 1000000012: (-22.816008, -47.075614)}
    H = create_graph_route(nodes_coord, nodes_weight)
    Heuristics._dfs(H, 1000000002, 1000000006, 10)