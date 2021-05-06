import geopy.distance
import networkx as nx
from geography import Map
import osmnx as ox
from Constants import *
from shapely.geometry import Point, LineString
from simulation.Map_Simulation import create_node, create_way, parse_file_tree, node_coordinates, \
    get_nodes, edges_net, adjacent_nodes, edges_type


def add_collect_points(G, collect_points, ad_weights, file_name_osm):
    id_nearest_node = 300000000000

    id_node_collect = 100000000000

    id_1adjacent_street1 = 40000000000
    id_1adjacent_street2 = 50000000000
    id_2adjacent_street1 = 60000000000
    id_2adjacent_street2 = 70000000000

    node1_added = id_nearest_node + 1

    nodes_mass_increment = {}
    nodes_collect_coordinates = {}

    tree = parse_file_tree(file_name_osm)
    osm_tag = tree.getroot()
    dict_nodes_coords = node_coordinates(tree)

    for i in collect_points:

        id_nearest_node += 1
        id_node_collect += 1

        id_1adjacent_street1 += 1
        id_1adjacent_street2 += 1
        id_2adjacent_street1 += 1
        id_2adjacent_street2 += 1

        weight = 0
        nodes_adjacent = {}

        try:
            # get the adjacent nodes of the coordinate
            nodes_adjacent, location = Map.adjacent_nodes(i)

        except:
            print("The ad on the", i, "coordinate is in an invalid area.")

        # the dict must have 2 items (2 adjacent nodes)
        if len(nodes_adjacent) > 1:
            # id of the adjacent nodes
            keys = list(nodes_adjacent.keys())

            # coordinates of the adjacent nodes
            coordinates = list(nodes_adjacent.values())

            e1 = (keys[0], keys[1])
            e2 = (keys[1], keys[0])

            # if the adjacent nodes are not in the graph
            if keys[0] not in G or keys[1] not in G:
                coordinates, keys = nearest_edge(G, i)

            elif G.has_edge(*e1) or G.has_edge(*e2) is False:
                coordinates, keys = nearest_edge(G, i)

            line = LineString(coordinates)
            point = Point(i)
            distance = line.project(point)
            edge_split = cut(line, distance)

            if len(edge_split) > 1:

                first_edge = edge_split[0].coords[:]
                second_edge = edge_split[1].coords[:]

                nearest_node = first_edge[1]

                # create the closest node inside the way
                G = _add_node(G, nearest_node, id_nearest_node)

                G = _add_node(G, i, id_node_collect)

                len_first_edge = calculate_distance(first_edge[0], first_edge[1])
                len_second_edge = calculate_distance(second_edge[0], second_edge[1])

                if first_edge[0] == coordinates[0]:
                    first_node = keys[0]
                    second_node = keys[1]
                else:
                    first_node = keys[1]
                    second_node = keys[0]

                highway = define_highway(G, first_node, second_node)

                # edge between node collect to nearest node dividing the adjacent street
                len_edge = calculate_distance(i, nearest_node)
                G.add_edge(id_node_collect, id_nearest_node, length=len_edge, highway='service', oneway='false')
                G.add_edge(id_nearest_node, id_node_collect, length=len_edge, highway='service', oneway='false')

                # create the edge of the first adjacent node
                # to the closest node inside the way
                G.add_edge(id_nearest_node, first_node, length=len_first_edge, highway=highway, oneway='false')
                G.add_edge(first_node, id_nearest_node, length=len_first_edge, highway=highway, oneway='false')

                # create the edge of the second adjacent node
                # to the closest node inside the way
                G.add_edge(id_nearest_node, second_node, length=len_second_edge, highway=highway, oneway='false')
                G.add_edge(second_node, id_nearest_node, length=len_second_edge, highway=highway, oneway='false')

                G = delete_edge(G, first_node, second_node)

                # it is necessary because every first node id is zero (?)
                # if str(id_node_collect) == str(node1_added):
                if str(id_nearest_node) == str(node1_added):
                    osm_tag = create_node(osm_tag, str(0), str(0), str(0))

                osm_tag = create_node(osm_tag, str(id_nearest_node), str(nearest_node[0]), str(nearest_node[1]))

                # edges between nearest node and first id node
                osm_tag = create_way(osm_tag, str(id_1adjacent_street1), str(first_node), str(id_nearest_node))
                osm_tag = create_way(osm_tag, str(id_1adjacent_street2), str(id_nearest_node), str(first_node))

                # edges between nearest node and second id node
                osm_tag = create_way(osm_tag, str(id_2adjacent_street1), str(id_nearest_node), str(second_node))
                osm_tag = create_way(osm_tag, str(id_2adjacent_street2), str(second_node), str(id_nearest_node))

                if i in ad_weights:
                    weight = ad_weights.get(i)[0]

                nodes_mass_increment.update([(id_nearest_node, weight)])
                nodes_collect_coordinates.update([(id_nearest_node, i)])

                # the distance between edge and the collect point is 0
                # so we get the nearest node to be the point
            else:

                # get the id of the nearest node
                # id_node = list(Map.closest_node_id(i, nodes_adjacent).keys())[0]
                id_node, dist = ox.get_nearest_node(G, i, return_dist=True)

                if i in ad_weights:
                    weight = ad_weights.get(i)[0]
                nodes_mass_increment.update([(id_node, weight)])
                nodes_collect_coordinates.update([(id_node, i)])

        else:
            print("Error: only tuple are supported.")

    tree.write(file_name_osm, xml_declaration=True)
    return G, nodes_collect_coordinates, nodes_mass_increment


def nearest_edge(G, i):
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
    keys = [0, 0]

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


def delete_edge(G, first_id, second_id):
    # removes the edge connecting the two adjacent nodes
    e = (first_id, second_id)
    e1 = (second_id, first_id)

    if G.has_edge(*e):
        G.remove_edge(first_id, second_id)
        """
        try:
            G.remove_edge(first_id, second_id)
        except:
            pass
        """
    elif G.has_edge(*e1):
        G.remove_edge(second_id, first_id)
    else:
        pass

    return G


def simulation_edit_graph(G, file_name_osm):
    dict_edges_net = edges_net(NET)
    dict_edges_type = edges_type(NET)

    nodes_adjacent_xml = adjacent_nodes(dict_edges_net)

    tree = parse_file_tree(file_name_osm)

    dict_nodes_coords = node_coordinates(tree)

    G_adjacents = G.succ if G.is_directed() else G.adj

    nodes_added = []

    nodes = get_nodes(NET)

    for i in nodes:
        try:
            adj = list(G_adjacents[int(i)].keys())
        except:
            # if the node does not exists in G
            coords = dict_nodes_coords.get(int(i))  # lat, lon
            G = _add_node(G, coords, int(i))
            nodes_added.append(int(i))

    # adding edges
    for i in nodes:
        if nodes_adjacent_xml.get(i) is not None and len(nodes_adjacent_xml.get(i)) > 0:
            for j in nodes_adjacent_xml.get(i):
                e = (i, j)
                e1 = (j, i)

                if G.has_edge(*e) is False:
                    len_edge = calculate_distance(dict_nodes_coords.get(i), dict_nodes_coords.get(j))
                    edge_type = dict_edges_type.get(e)
                    if edge_type != ['subway'] and edge_type != ['rail']:
                        G.add_edge(i, j, length=len_edge, highway=edge_type[0], oneway='true')

                if G.has_edge(*e1) is False and BIDIRECTIONAL is True:
                    len_edge = calculate_distance(dict_nodes_coords.get(j), dict_nodes_coords.get(i))
                    edge_type = dict_edges_type.get(e)
                    if edge_type != ['subway'] and edge_type != ['rail']:
                        G.add_edge(j, i, length=len_edge, highway=edge_type[0], oneway='true')

    # deleting edges
    for i in nodes:
        if G_adjacents[int(i)].keys() is not None:
            adj_G = set(G_adjacents[int(i)].keys())
        else:
            adj_G = set()
        if nodes_adjacent_xml.get(int(i)) is not None:
            adj_net = set(nodes_adjacent_xml.get(int(i)))
        else:
            adj_net = set()

        edges_to_delete = adj_G - adj_net
        if not None and len(edges_to_delete) > 0:
            for j in edges_to_delete:
                G = delete_edge(G, i, j)

    dead_ends = [(u, v) for u, v, k, data in G.edges(keys=True, data=True) if data['highway'] == 'steps']
    for i, j in dead_ends:
        G = delete_edge(G, i, j)

    return G


def calculate_distance(coordinate_from, coordinate_to):
    return geopy.distance.geodesic(coordinate_from, coordinate_to).m


def _add_node(G, tuple_coordinates, id_node):
    G.add_node(id_node, x=tuple_coordinates[1], y=tuple_coordinates[0])
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
                LineString(coords[:i + 1]),
                LineString(coords[i:])]
        if pd > distance:
            cp = line.interpolate(distance)
            return [
                LineString(coords[:i] + [(cp.x, cp.y)]),
                LineString([(cp.x, cp.y)] + coords[i:])]
