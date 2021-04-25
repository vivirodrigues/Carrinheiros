import networkx as nx
from route import Heuristics
from route import Graph
from Constants import *
import networkx as nx
import matplotlib.pyplot as plt


def create_graph_route(nodes_coordinates, nodes_mass_increment):
    """
    This function creates a complete graph with all collect nodes.
    Each node of the graph is a collect point.

    :param nodes_coordinates:       dictionary
                                    The dictionary must have the
                                    id of nodes and their geographic
                                    coordinates.
                                    Example: {id_node:(x, y)}

    :param nodes_mass_increment:    dictionary
                                    The dictionary must have the
                                    id of nodes and a tuple with
                                    the vehicle mass increment
                                    value in this point.
                                    The first item of the tuple is
                                    the amount, and the second is
                                    the type of data, as kilograms,
                                    grams, etc.
                                    Example: {id_node:(50, 'Kg')}

    :return:                        NetworkX graph.
                                    Complete graph not directed.
    """

    # creating a complete graph
    H = nx.complete_graph(len(nodes_coordinates.keys()))

    """
    # nx.draw(H, pos=nx.spring_layout(H))
    colors = ['#c1c1c1' for i in range(len(H.edges()) - 1)]
    colors.insert(len(H.edges()), 'r')
    other_colors = ['#A0CBE2' for i in range(len(H.nodes()) - 2)]
    other_colors.append('r')
    other_colors.append('r')
    ids = [i for i in range(len(H.edges()))]
    mapping = {i: ids for i, ids in enumerate(ids)}
    H = nx.relabel_nodes(H, mapping)

    options = {
        "node_color": other_colors, #'#A0CBE2',
        "node_size": 800,
        "edge_color": colors,
        "width": 5,
        "with_labels": True,
        "font_weight": 'bold'
    }
    nx.draw(H, **options)
    plt.show()
    """

    # Modifying node names (id nodes of G = id nodes of H)
    node_names = list(nodes_mass_increment.keys())
    mapping = {i:node_names for i, node_names in enumerate(node_names)}
    H = nx.relabel_nodes(H, mapping)

    # Add x, y and value of vehicle mass increment
    for i in nodes_coordinates:
        coord = nodes_coordinates.get(i)
        weight_node = nodes_mass_increment.get(i)
        H.nodes[i]['x'] = coord[1]
        H.nodes[i]['y'] = coord[0]
        H.nodes[i]['mass'] = weight_node

    return H


#def sum_costs(G, path, impedance = IMPEDANCE):
def sum_costs(G, path, impedance):
    """
    This function calculates the sum of the costs
    of a path created according to the geographic
    scenario graph.

    :param G:       NetworkX graph.
                    Geographic scenario

    :param path:    list
                    The list must contains the id
                    of nodes of the path.

    :param weight:  String or function

    :return:        float
                    The sum of all cost (weight)
                    edges of the path.
    """
    weight = Graph._weight(G, impedance) #'weight')
    sum_costs = 0

    for i in range(len(path)-1):
        e = G.adj[path[i]].get(path[i + 1])
        weight_edge = weight(path[i], path[i + 1], e)
        sum_costs += weight_edge

    return sum_costs


#def cost_path(G, source, target, vehicle_mass, impedance=IMPEDANCE):
def cost_path(G, source, target, vehicle_mass, impedance):
    """
    This function calculates the path between source and
    target nodes, and returns it. Besides, calculates the
    sum of all edges weight of the path, and returns it.

    :param G:               NetworkX graph.
                            Geographic scenario

    :param source:
    :param target:
    :param vehicle_mass:
    :return:
    """

    # updates the weight of all edges of the scenario according
    # to the current weight of the vehicle
    max_grade = max(list(nx.get_edge_attributes(G, "grade").values()))
    G = Graph.update_weight(G, vehicle_mass, max_grade)

    # finds the shortest path to the destination in the scenario graph
    #path = Heuristics.shortest_path_faster(G, source, target, 'weight')
    distance, path = Heuristics.bellman_ford(G, source, target, weight=impedance) # 'weight')
    # distance, path = Heuristics.bidirectional_dijkstra(G, source, target, weight=IMPEDANCE)
    #path = nx.astar_path(G, source, target, weight=IMPEDANCE)

    # cost to get to the destination:
    # the sum of the weight of all the edges from the path
    sum_path_costs = sum_costs(G, path, impedance)

    # updates the weight of all edges of the scenario according
    # to the current weight of the vehicle
    max_grade = max(list(nx.get_edge_attributes(G, "grade").values()))
    G = Graph.update_weight(G, VEHICLE_MASS, max_grade)

    return sum_path_costs, path


def sum_costs_route(G, H, route, vehicle_mass, impedance):
#def sum_costs_route(G, H, route, vehicle_mass, impedance=IMPEDANCE):
    """
    This function calculates the total cost of a route,
    according to the collect points in the scenario, and
    the vehicle mass update in each H node (collect point).

    :param G:                   NetworkX graph.
                                Geographic scenario

    :param H:                   NetworkX graph.
                                Complete graph where each node
                                is acollect point
    :param route:
    :param vehicle_mass:
    :return:
    """
    vehicle_mass += H.nodes[route[0]]['mass']
    paths = []
    cost_work_all = 0

    for node in range(len(route)-1):

        # adds the current weight of the vehicle to the weight
        # of the materials being collected in this node
        vehicle_mass += H.nodes[route[node]]['mass']

        # checks the cost of going from one node to the next collection point
        cost_work, path = cost_path(G, route[node], route[node + 1], vehicle_mass, impedance)
        cost_work_all += cost_work
        paths.append(path)

    return cost_work_all, paths


if __name__ == '__main__':
    nodes_weight = {1000000002: 0, 1000000004: (50, 'Kg'), 1000000006: (30, 'Kg'), 1000000008: (15, 'Kg'), 994679386: (12, 'Kg'), 1000000013: 0, 1000000014: 0, 1000000015: 0, 1000000016: 0, 1000000017: 0}
    nodes_coord = {1000000002: (-22.816008, -47.075614), 1000000004: (-22.816639, -47.074891), 1000000006: (-22.818317, -47.083415), 1000000008: (-22.820244, -47.085422), 994679386: (-22.823953, -47.087718), 1000000012: (-22.816008, -47.075614), 1000000013: (-22.816080, -47.075616), 1000000014: (-22.816000, -47.075697), 1000000015: (-22.816081, -47.075677), 1000000016: (-22.816014, -47.075633)}
    H = create_graph_route(nodes_coord, nodes_weight)
