from geography import Map
import Graph
import osmnx as ox


def add_collect_points(collect_points):

    id_node_collect_point = 1000000000

    nodes_collect_points = []

    for i in collect_points:

        id_node_collect_point += 1

        # get the adjacent nodes of the coordinate
        nodes_adjacent = Map.adjacent_nodes(i)

        # if len nodes_adjacent is 1, the collect point already is a node
        if len(nodes_adjacent) == 1:
            id_node = list(nodes_adjacent.keys())[0]
            print(id_node, " already is a node")
            nodes_collect_points.append(id_node)

        # if nodes_adjacent is a tuple, it must to create a node
        # between adjacent nodes
        elif len(nodes_adjacent) > 1:

            # id
            keys = list(nodes_adjacent.keys())

            # create a node with collect point coordinates
            G.add_node(id_node_collect_point, x=i[1], y=i[0])
            print("Add node: ", i[1], i[0])

            # create edges to adjacent nodes
            G.add_edges_from([(id_node_collect_point, keys[0]), (id_node_collect_point, keys[1])])
            print("Add edges:", id_node_collect_point, keys[0], "and", id_node_collect_point, keys[1])

            nodes_collect_points.append(id_node_collect_point)
        else:
            print("Error: tuple are supported.")

    print(nodes_collect_points)
    return G


if __name__ == '__main__':
    G = ox.graph_from_bbox(-22.796008, -22.843953, -47.054891, -47.107718000000006, network_type='all')
    stop_points = [(-22.816008, -47.075614), (-22.816639, -47.074891),
                   (-22.817423, -47.082436), (-22.820244, -47.085422),
                   (-22.823953, -47.087718), (-22.816008, -47.075614)]
    Graph.plot_graph(G)
    G = add_collect_points(stop_points)
    Graph.plot_graph(G)
    Graph.save_graph_file(G, 'test.graphml')
