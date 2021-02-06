from models.route.Graph import _weight
from models.route import Graph
import networkx as nx
import osmnx as ox


def bellman_ford(G, initial_node, target_node, weight):
    weight = _weight(G, weight)
    distance, route = nx.single_source_bellman_ford(G, initial_node, target_node, weight)
    return distance, route


def bidirectional_dijkstra(G, initial_node, target_node, weight):
    weight = _weight(G, weight)
    distance, route = nx.bidirectional_dijkstra(G, initial_node, target_node, weight)
    return distance, route


if __name__ == '__main__':
    G = ox.graph_from_bbox(-22.796008, -22.843953, -47.054891, -47.107718000000006, network_type='all')
    G = Graph.set_node_elevation(G, '../maps/22S48_ZN.tif')
    G = Graph.set_edge_grades(G)
    Graph.save_graph_file(G, '../maps/map.graphml')
    nodes = list(G.nodes)
    dist1, route1 = bellman_ford(G, nodes[1], nodes[5], Graph.impedance)
    dist2, route2 = bidirectional_dijkstra(G, nodes[1], nodes[5], Graph.impedance)
    fig, ax = ox.plot_graph_route(G, route1, node_size=0)
    fig, ax = ox.plot_graph_route(G, route2, node_size=0)