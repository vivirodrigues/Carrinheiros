from route import Graph
import networkx as nx
import osmnx as ox
from collections import deque
from Constants import *
from route import Graph_Collect
import random
import more_itertools


def bellman_ford(G, initial_node, target_node, weight):
    weight = Graph._weight(G, weight)
    distance, route = nx.single_source_bellman_ford(G, initial_node, target_node, weight)
    return distance, route


def bidirectional_dijkstra(G, initial_node, target_node, weight):
    weight = Graph._weight(G, weight)
    distance, route = nx.bidirectional_dijkstra(G, initial_node, target_node, weight)
    return distance, route


def _shortest_path_faster(G, source, weight):
    """
    This function returns the single-source shortest path in
    weighted directed graph based on Shortest Path Faster
    Algorithm (SPFA). It is an improvement of the Bellman–
    Ford algorithm.

    The pseudocode of the SPFA:
    https://en.wikipedia.org/wiki/Shortest_Path_Faster_Algorithm

    :param G:           NetworkX graph.
                        input graph

    :param source:      Float
                        Id of the start node

    :param target:      Float
                        Id of the goal node

    :param weight:      Function

    :return:            List
                        List with all nodes of the
                        shortest path
    """

    weight = Graph._weight(G, weight)
    last_edge = {source: (None, None)}
    pred_edge = {source: None}
    source = [source]
    q = deque(source)
    G_adjacents = G.succ if G.is_directed() else G.adj
    n_G = len(G_adjacents)

    count = {}
    dist = {}
    parent = {}

    inf = float("inf")

    # Initialization
    for i in G.nodes:
        dist.update([(i, inf)])
        parent.update([(i, None)])

    dist.update([(source[0], 0)])

    while q:
        u = q.popleft()

        # for each edge between the node u and their adjacent nodes
        for v, e in G_adjacents[u].items():

            # Relaxing
            new_dist_v = dist.get(u) + weight(u, v, e)

            if new_dist_v < dist.get(v):

                if v in last_edge[u]:
                    print("Error: Negative cost cycle.")
                    return False

                if v in pred_edge and pred_edge[v] == u:
                    last_edge[v] = last_edge[u]
                else:
                    last_edge[v] = (u, v)

                dist.update([(v, new_dist_v)])
                parent.update([(v, u)])

                if v not in q:

                    q.append(v)
                    count_v = count.get(v, 0) + 1
                    if count_v == n_G:
                        print("Error: Negative cost cycle")
                        return False
                    count[v] = count_v
                    pred_edge[v] = u

    return dist, parent


def verifying_nodes(path, nodes):
    for i in nodes:
        if i not in list(path):
            return True
    return False


def _nearest_neighbor(G, H, source, target, vehicle_mass):
    """
    This function returns the single-source shortest path in
    weighted directed graph based on Shortest Path Faster
    Algorithm (SPFA). It is an improvement of the Bellman–
    Ford algorithm.

    The pseudocode of the SPFA:
    https://en.wikipedia.org/wiki/Shortest_Path_Faster_Algorithm

    :param G:           NetworkX graph.
                        input graph

    :param source:      Float
                        Id of the start node

    :param target:      Float
                        Id of the goal node

    :param weight:      Function

    :return:            List
                        List with all nodes of the
                        shortest path
    """
    if source not in H:
        print("Error")
        return False

    open = [source]
    closed = []
    current_vehicle_mass = vehicle_mass
    nodes_graph = list(H.nodes)
    nodes_graph.remove(target)

    while len(open) > 0:
        dist = {}
        node = open.pop(0)
        closed.append(node)
        missing = verifying_nodes(closed, nodes_graph)

        # if current node is the target (objective) and
        # there is not nodes missing to be visited
        if node == target and missing is False:
            return closed
        else:

            # checks nodes that have not yet been added in closed
            possibilities = set(H.adj[node]) - set(closed)

            for u in possibilities:
                # checks the edge weight according to the vehicle's mass +
                # mass increase at the current vertex
                edge_cost = Graph_Collect.cost_path(G, node, u, current_vehicle_mass)
                dist.update([(u, edge_cost)])

            # sorting the dict according to edge weights
            dist = dict(sorted(dist.items(), key=lambda item: item[1]))

            if len(dist) < 1 and source == target:
                new_node = target
            else:
                new_node = list(dist.keys())[0]
                if len(dist) > 1 and new_node == target:
                    new_node = list(dist.keys())[1]

            open.append(new_node)
            current_vehicle_mass += H.nodes[new_node]['mass']


def _path(source, target, parent, path):
    """
    This function finds the path from source to the target
    according to the parent dictionary. It must be used for
    shortest_path_faster function.

    :param source:      Float
                        Id of the start node

    :param target:      Float
                        Id of the goal node

    :param parent:      Dictionary
                        The value of each key is the parent
                        node (predecessor node).

    :param path:        list
                        The list contains the id of the nodes
                        of the path from source to the target.

    :return:            list
                        The list contains the id of the nodes
                        of the path from source to the target.
    """

    if len(path) == 0:
        path.append(target)

    if target == source:
        pass

    elif parent.get(target) is None:
        print("Target cannot be reached")
        return False
    else:
        path.append(parent.get(target))
        _path(source, parent.get(target), parent, path)

    return path[::-1]


def shortest_path_faster(G, source, target, weight):
    dist, parent = _shortest_path_faster(G, source, weight)
    path = []
    route = _path(source, target, parent, path)
    return route


def exact_method(G, H, source, target):
    nodes_graph = list(H.nodes)
    nodes_graph.remove(source)
    if source != target:
        nodes_graph.remove(target)

    permutations = list(more_itertools.distinct_permutations(nodes_graph, 5))

    costs = []
    all_permutations = []
    for i in permutations:
        i = list(i)
        i.insert(0, source)
        i.append(target)
        all_permutations.append(i)
        sum_costs = Graph_Collect.sum_costs_route(G, H, i, 110)
        costs.append(sum_costs)
    minimum = min(costs)
    index_minimum = costs.index(minimum)

    return all_permutations[index_minimum]


def comparar_paths(G):
    nodes = list(G.nodes)
    source = 1000000006 # random.choice(nodes)
    target = 1000000002 # random.choice(nodes)
    print(G.succ)

    dist_mine, rota_mine = shortest_path_faster(G, source, target, 'weight')
    dist1, rota_bellman = bellman_ford(G, source, target, 'weight')

    print(rota_bellman)
    print(rota_mine[::-1])
    if rota_bellman == rota_mine[::-1]:
        print("Ok")
    else:
        print("Errooooo")


if __name__ == '__main__':
    G = ox.graph_from_bbox(-22.796008, -22.843953, -47.054891, -47.107718000000006, network_type='all')
    G = Graph.set_node_elevation(G, '../' + MAPS_DIRECTORY, '22S48_ZN.tif')
    G = Graph.edge_grades(G)
    G = Graph.surface(G, '../' + MAPS_DIRECTORY, FILE_NAME_OSM)
    G = Graph.hypotenuse(G)
    G = Graph.maxspeed(G)
    G = Graph.update_weight(G, 10)


    # dist1, route1 = bellman_ford(G, 505388658, 505388842, Graph.update_weight())

    #dist2, route2 = bidirectional_dijkstra(G, nodes[1], nodes[5], Graph.impedance)
    # fig, ax = ox.plot_graph_route(G, route1, node_size=0)
    # fig, ax = ox.plot_graph_route(G, route2, node_size=0)
    #for i in range(1):
    #   comparar_paths(G)