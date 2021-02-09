from models.mapsServer import Map
import osmnx as ox


def create_collect_points(G, collect_points):
    for i in collect_points:
        nodes_between = Map.between_nodes(i)
        print(nodes_between)
        G.add_node("point1", x = i[0], y = i[1])


if __name__ == '__main__':
    G = ox.graph_from_bbox(-22.796008, -22.843953, -47.054891, -47.107718000000006, network_type='all')
    stop_points = [(-22.816008, -47.075614), (-22.816639, -47.074891),
                   (-22.817423, -47.082436), (-22.820244, -47.085422),
                   (-22.823953, -47.087718), (-22.816008, -47.075614)]
    create_collect_points(G, stop_points)