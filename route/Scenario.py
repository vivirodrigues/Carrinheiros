from geography import Map
import Graph
import osmnx as ox
from Constants import *
import networkx as nx
from osmnx import utils_graph, utils
from shapely.geometry import Point


def add_collect_points(G, collect_points):

    id_node_collect_point = 1000000000

    nodes_collect_points = []

    for i in collect_points:

        id_node_collect_point += 1

        # get the adjacent nodes of the coordinate
        nodes_adjacent, location = Map.adjacent_nodes(i)
        # print("adjacents", nodes_adjacent)

        # it do not considers invalid coordinates
        if nodes_adjacent is None or location is None:
            pass

        # if len nodes_adjacent is 1, the collect point already is a node
        elif len(nodes_adjacent) == 1:

            id_node = list(nodes_adjacent.keys())[0]
            # print(id_node, "already is a node in OSM")

            # if the node is not in the Graph
            if id_node not in G:
                print(location.raw)
                G = _add_node(G, i, id_node)
                print(i)
                node1, node2, key, shapely, distance = get_nearest_edge(G, i, return_geom=True, return_dist=True)
                print("bounds", shapely.bounds) # (minx, miny, maxx, maxy)
                print("coords", shapely.coords[:])
                print(distance)


            nodes_collect_points.append(id_node)

        # if nodes_adjacent is a tuple, it must to create a node
        # between adjacent nodes
        elif len(nodes_adjacent) > 1:

            # id of the node
            keys = list(nodes_adjacent.keys())

            # create a node with collect point coordinates
            G = _add_node(G, i, id_node_collect_point)
            # G.add_node(id_node_collect_point, x=i[1], y=i[0])

            if keys[0] not in G:
                print(location.raw)
                G = _add_node(G, i, keys[0])

            if keys[1] not in G:
                print(location.raw)
                G = _add_node(G, i, keys[1])

            G = _add_edge(G, id_node_collect_point, keys[0])
            G = _add_edge(G, id_node_collect_point, keys[1])
            # G.add_edges_from([(id_node_collect_point, keys[0]), (id_node_collect_point, keys[1])])

            nodes_collect_points.append(id_node_collect_point)
        else:
            print("Error: tuple are supported.")

    print(nodes_collect_points)
    return G


def _add_node(G, tuple_coordinates, id_node):
    G.add_node(id_node, x=tuple_coordinates[1], y=tuple_coordinates[0])
    print("Add node: ", tuple_coordinates[1], tuple_coordinates[0])
    return G


def _add_edge(G, id_node_from, id_node_to):
    # create edges to adjacent nodes
    G.add_edges_from([(id_node_from, id_node_to)])
    print("Add edges:", id_node_from, id_node_to)
    return G


def get_nearest_edge(G, point, return_geom=False, return_dist=False):
    """
    Find the nearest edge to a point by minimum Euclidean distance.
    For best results, both G and point should be projected.
    Parameters
    ----------
    G : networkx.MultiDiGraph
        input graph
    point : tuple
        the (lat, lng) or (y, x) point for which we will find the nearest edge
        in the graph
    return_geom : bool
        Optionally return the geometry of the nearest edge
    return_dist : bool
        Optionally return the distance in graph's coordinates' units between
        the point and the nearest edge
    Returns
    -------
    tuple
        Graph edge unique identifier as a tuple of (u, v, key).
        Or a tuple of (u, v, key, geom) if return_geom is True.
        Or a tuple of (u, v, key, dist) if return_dist is True.
        Or a tuple of (u, v, key, geom, dist) if return_geom and return_dist are True.
    """
    # convert lat,lng (y,x) point to x,y for shapely distance operation
    xy_point = Point(reversed(point))

    # calculate euclidean distance from each edge's geometry to this point
    gs_edges = utils_graph.graph_to_gdfs(G, nodes=False)["geometry"]
    uvk_geoms = zip(gs_edges.index, gs_edges.values)
    distances = ((uvk, geom, xy_point.distance(geom)) for uvk, geom in uvk_geoms)

    object_methods = [method_name for method_name in dir(distances)
                      if callable(getattr(distances, method_name))]
    print(gs_edges.to_dict())

    # the nearest edge minimizes the distance to the point
    (u, v, key), geom, dist = min(distances, key=lambda x: x[2])
    utils.log(f"Found nearest edge ({u, v, key}) to point {point}")

    # return results requested by caller
    if return_dist and return_geom:
        return u, v, key, geom, dist
    elif return_dist:
        return u, v, key, dist
    elif return_geom:
        return u, v, key, geom
    else:
        return u, v, key


if __name__ == '__main__':
    G = ox.graph_from_bbox(-22.796008, -22.843953, -47.054891, -47.107718000000006, network_type='all')
    stop_points = [(-22.820204, -47.085525), (-22.825029, -47.068495),
                   (-22.824376, -47.070952), (-22.82503, -47.07410),
                   (-22.82504, -47.07730), (-24.992554, -47.069115)]# (-22.816008, -47.075614)]
    # fig1, ax1 = ox.plot_graph(G, node_size=5, edge_color='#333333', bgcolor='k')
    Graph.save_graph_file(G, '../' + MAPS_DIRECTORY, 'test1')
    G = add_collect_points(G, stop_points)
    G = Graph.set_node_elevation(G, '../' + MAPS_DIRECTORY, '22S48_ZN.tif')
    Graph.save_graph_file(G, '../' + MAPS_DIRECTORY, 'test.graphml')
    Graph.plot_graph(G)
