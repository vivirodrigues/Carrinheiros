from models.mapsServer import Map
import Graph
import osmnx as ox


def nodes_collect_points(collect_points):

    aux = 1

    nodes_collect_points = []

    for i in collect_points:
        aux += 1
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
            keys = list(nodes_adjacent.keys())
            values = list(nodes_adjacent.values())
            print("Add node: ", values[0][1], values[0][0])
            # create the node
            # G.add_node(aux, x=i[1], y=i[0])
            # create the edges
            nodes_collect_points.append(aux)
        else:
            print("Error: only int or tuple are supported.")

    print(nodes_collect_points)
    return G


if __name__ == '__main__':
    G = ox.graph_from_bbox(-22.796008, -22.843953, -47.054891, -47.107718000000006, network_type='all')
    stop_points = [(-22.816008, -47.075614), (-22.816639, -47.074891),
                   (-22.817423, -47.082436), (-22.820244, -47.085422),
                   (-22.823953, -47.087718), (-22.816008, -47.075614)]
    Graph.save_graph_file(G, 'test1.graphml')
    G = nodes_collect_points(stop_points)
    Graph.save_graph_file(G, 'test.graphml')
