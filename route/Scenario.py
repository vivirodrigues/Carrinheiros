import geopy.distance
import networkx as nx
from geography import Map
from route import Graph
import osmnx as ox
from Constants import *
from shapely.geometry import Point, LineString
from simulation import Map_osm


def add_collect_points(G, collect_points, ad_weights):

    id_new_node = 100000000000
    id_new_edge = 100000
    node1_added = id_new_node + 2

    nodes_mass_increment = {}
    nodes_collect_coordinates = {}

    tree = Map_osm.parse_file_tree(MAPS_DIRECTORY + FILE_NAME_OSM)
    osm_tag = tree.getroot()

    for i in collect_points:

        id_new_node += 2
        id_new_edge += 6

        weight = 0

        try:
            # get the adjacent nodes of the coordinate
            nodes_adjacent, location = Map.adjacent_nodes(i)
        except:
            print("The ad on the", i, "coordinate is in an invalid area.")

        # it do not considers invalid coordinates
        if nodes_adjacent is None or location is None:
            print("The ad on the", i, "coordinate is in an invalid area.")
            pass

        # the dict must have 2 items (2 adjacent nodes)
        elif len(nodes_adjacent) > 1:

            # id of the adjacent nodes
            keys = list(nodes_adjacent.keys())

            # coordinates of the adjacent nodes
            coordinates = list(nodes_adjacent.values())

            # if the adjacent nodes are not in the graph
            if keys[0] not in G or keys[1] not in G:

                coordinates, keys = nearest_edge(G, i, keys)

            line = LineString(coordinates)
            point = Point(i)
            distance = line.project(point)
            edge_split = cut(line, distance)

            if len(edge_split) > 1:
                first_edge = edge_split[0].coords[:]
                second_edge = edge_split[1].coords[:]

                nearest_node = first_edge[1]

                # create a node with collect point coordinates
                G = _add_node(G, i, id_new_node)

                # create the closest node inside the way
                G = _add_node(G, nearest_node, id_new_node + 1)

                len_first_edge = calculate_distance(first_edge[0], first_edge[1])
                len_second_edge = calculate_distance(second_edge[0], second_edge[1])

                if first_edge[0] == coordinates[0]:
                    first_node = keys[0]
                    second_node = keys[1]
                else:
                    first_node = keys[1]
                    second_node = keys[0]

                highway = define_highway(G, first_node, second_node)
                G = add_edges(G, i, first_node, second_node, id_new_node, len_first_edge, len_second_edge, nearest_node, highway)
                G = delete_edge(G, first_node, second_node)
                osm_tag = simulation_edit_map(osm_tag, i, id_new_node, node1_added, id_new_edge, first_node, second_node,
                                              nearest_node)
                if i in ad_weights:
                    weight = ad_weights.get(i)[0]
                nodes_mass_increment.update([(id_new_node, weight)])
                nodes_collect_coordinates.update([(id_new_node, i)])

            # the distance between edge and the collect point is 0
            # so we get the nearest node to be the point
            else:

                # get the id of the nearest node
                id_node = list(Map.closest_node_id(i, nodes_adjacent).keys())[0]
                if i in ad_weights:
                    weight = ad_weights.get(i)[0]
                nodes_mass_increment.update([(id_node, weight)])
                nodes_collect_coordinates.update([(id_node, i)])

        else:
            print("Error: only tuple are supported.")

    tree.write(MAPS_DIRECTORY + FILE_NAME_OSM, xml_declaration=True)
    return G, nodes_collect_coordinates, nodes_mass_increment


def nearest_edge(G, i, keys):
    """

    :param G:       NetworkX graph.
                    Geographic scenario

    :param i:       tuple
                    collect point coordinates

    :param keys:    list
                    list with id of adjacent nodes

    :return:        tuple, list
                    tuple with coordinates of adjacent nodes
                    list with id of adjacent nodes
    """

    keys[0], keys[1], key, shapely, distance_ = ox.get_nearest_edge(G, i, return_geom=True, return_dist=True)

    attribute_x = nx.get_node_attributes(G, 'x')
    attribute_y = nx.get_node_attributes(G, 'y')

    lon_node1 = attribute_x.get(keys[0])
    lat_node1 = attribute_y.get(keys[0])
    lon_node2 = attribute_x.get(keys[1])
    lat_node2 = attribute_y.get(keys[1])

    coordinates = [(lat_node1, lon_node1), (lat_node2, lon_node2)]

    return coordinates, keys


def define_highway(G, first_node, second_node):
    """

    :param G:           NetworkX graph.
                        Geographic scenario

    :param first_id:
                        id of the first adjacent node

    :param second_id:
                        id of the second adjacent node

    :return:            String
    """

    # define the type of highway based on OSM
    try:
        highway = G.edges[first_node, second_node, 0]['highway']
    except:
        highway = G.edges[second_node, first_node, 0]['highway']

    if highway is None:
        highway = 'residential'

    return highway


def add_edges(G, i, first_id, second_id, id_new_node, len_first_edge, len_second_edge, nearest_node, highway):

    # create the edge of the first adjacent node
    # to the closest node inside the way
    G.add_edge(id_new_node + 1, first_id, length=len_first_edge, highway=highway, oneway='false')
    G.add_edge(first_id, id_new_node + 1, length=len_first_edge, highway=highway, oneway='false')

    # create the edge of the second adjacent node
    # to the closest node inside the way
    G.add_edge(id_new_node + 1, second_id, length=len_second_edge, highway=highway, oneway='false')
    G.add_edge(second_id, id_new_node + 1, length=len_second_edge, highway=highway, oneway='false')

    len_edge = calculate_distance(i, nearest_node)
    G.add_edge(id_new_node, id_new_node + 1, length=len_edge, highway='footway', oneway='false')
    G.add_edge(id_new_node + 1, id_new_node, length=len_edge, highway='footway', oneway='false')

    return G


def delete_edge(G, first_id, second_id):

    # removes the edge connecting the two adjacent nodes
    e = (first_id, second_id)

    if G.has_edge(*e):
        G.remove_edge(first_id, second_id)
    else:
        G.remove_edge(second_id, first_id)

    return G


def simulation_edit_map(osm_tag, i, id_new_node, first_node, id_new_edge, first_id, second_id, nearest_node):

    # it is necessary because every first node id is zero (?)
    if str(id_new_node) == str(first_node):
        osm_tag = Map_osm.create_node(osm_tag, str(0), str(0), str(0))

    osm_tag = Map_osm.create_node(osm_tag, str(id_new_node), str(i[0]), str(i[1]))

    osm_tag = Map_osm.create_node(osm_tag, str(id_new_node + 1), str(nearest_node[0]), str(nearest_node[1]))

    osm_tag = Map_osm.create_way(osm_tag, str(id_new_edge + 1), str(first_id), str(id_new_node + 1))
    osm_tag = Map_osm.create_way(osm_tag, str(id_new_edge + 2), str(id_new_node + 1), str(second_id))
    osm_tag = Map_osm.create_way(osm_tag, str(id_new_edge + 3), str(second_id), str(id_new_node + 1))
    osm_tag = Map_osm.create_way(osm_tag, str(id_new_edge + 4), str(id_new_node), str(id_new_node + 1))
    osm_tag = Map_osm.create_way(osm_tag, str(id_new_edge + 5), str(id_new_node + 1), str(id_new_node))

    return osm_tag


def calculate_distance(coordinate_from, coordinate_to):
    return geopy.distance.geodesic(coordinate_from, coordinate_to).m


def _add_node(G, tuple_coordinates, id_node):
    G.add_node(id_node, x=tuple_coordinates[1], y=tuple_coordinates[0])
    # print("Add node: ", tuple_coordinates[1], tuple_coordinates[0])
    return G


def cut(line, distance):
    # Cuts a line in two at a distance from its starting point
    if distance <= 0.0 or distance >= line.length:
        return [LineString(line)]
    coords = list(line.coords)
    for i, p in enumerate(coords):
        pd = line.project(Point(p))
        if pd == distance:
            return [
                LineString(coords[:i+1]),
                LineString(coords[i:])]
        if pd > distance:
            cp = line.interpolate(distance)
            return [
                LineString(coords[:i] + [(cp.x, cp.y)]),
                LineString([(cp.x, cp.y)] + coords[i:])]


if __name__ == '__main__':
    G = ox.graph_from_bbox(-22.796008, -22.843953, -47.054891, -47.107718000000006, network_type='all')

    stop_points = [(-22.820204, -47.085525), (-22.825029, -47.068495),
                   (-22.824376, -47.070952), (-22.82503, -47.07410),
                   (-22.82504, -47.07730), (-24.992554, -47.069115)]# (-22.816008, -47.075614)]
    # fig1, ax1 = ox.plot_graph(G, node_size=5, edge_color='#333333', bgcolor='k')
    # Graph.save_graph_file(G, '../' + MAPS_DIRECTORY, 'test1')
    weigths = {(-22.816639, -47.074891): (50, 'Kg'), (-22.818317, -47.083415): (30, 'Kg'), (-22.820244, -47.085422): (15, 'Kg'), (-22.823953, -47.087718): (12, 'Kg')}
    G, nodes_collect_and_coordinates, nodes_collect_and_weights = add_collect_points(G, stop_points, weigths)
    G = Graph.set_node_elevation(G, '../' + MAPS_DIRECTORY, '22S48_ZN.tif')
    G = Graph.edge_grades(G)
    Graph.save_graph_file(G, '../' + MAPS_DIRECTORY, 'test.graphml')
    # Graph.plot_graph(G)

    weight = Graph._weight(G, 'weight')
    distance, route = nx.bidirectional_dijkstra(G, 1000000002, 1000000011, weight)
    print(route)
