import osmnx as ox
import pandas as pd
import networkx as nx
import inspect
from geography import GeoTiff, Coordinates
from Constants import *
import math
from scipy import constants
import haversine as hs
from haversine import Unit
from route import Scenario
import xml.dom.minidom
from collections import Counter
from simulation import Main, Map_Simulation


def set_node_elevation(G, name_file_geotiff):
    """
    Add `elevation` attribute to each node in meters.
    Uses elevation data by geotiff file by default

    :param G:           NetworkX graph
                        input graph

    :param directory:   str
                        Directory of the geotiff file

    :param geotiff:     str
                        file_name of the geotiff

    :return:            networkx.MultiDiGraph
                        graph with node elevation attributes
    """

    # create a dict with x coordinates of all nodes
    x = nx.get_node_attributes(G, "x")

    # create a list with the longitudes
    longitudes = list(x.values())

    # create a dict with y coordinates of all nodes
    y = nx.get_node_attributes(G, "y")

    # create a list with the latitudes
    latitudes = list(y.values())

    # create a list with the id of all nodes
    ids = list(y.keys())
    elevation = []

    # get elevation value from geotiff file,
    # based on x,y coordinate
    for i in range(0, len(x)):
        elevation.append(GeoTiff.coordinate_pixel(name_file_geotiff, longitudes[i], latitudes[i]))

    # create a pandas series with the id of the node and corresponding elevation values
    pd_elevation = pd.Series(elevation, index=ids)

    # add the elevation value in the node attributes
    nx.set_node_attributes(G, pd_elevation.to_dict(), name="elevation")

    return G


def set_node_elevation_simulation(G, file_name_net):

    nodes_dict = Map_Simulation.nodes_z_net(file_name_net)
    ids = list(G.nodes)
    elevation = []
    for i in ids:
        elevation.append(nodes_dict.get(str(i)))

    # create a pandas series with the id of the node and corresponding elevation values
    pd_elevation = pd.Series(elevation, index=ids)

    # add the elevation value in the node attributes
    nx.set_node_attributes(G, pd_elevation.to_dict(), name="elevation")

    return G


def edge_grades(G):
    """
    Adds the angle of the roads according to the elevation.
    :param G:   NetworkX graph
                input graph
    :return:    networkx.MultiDiGraph
                graph with edge grades attributes
    """
    G = ox.add_edge_grades(G)
    return G


def save_graph_file(G, name_file='map'):
    """
    Save the graph file

    :param G:           NetworkX graph
                        input graph

    :param name_file    String
                        Name of the file
    """
    name_len = len(name_file)

    # the length of extension
    if name_len > 7:
        file_extension = name_file[name_len - 8] + name_file[name_len - 7] + \
                         name_file[name_len - 6] + name_file[name_len - 5] + \
                         name_file[name_len - 4] + name_file[name_len - 3] + \
                         name_file[name_len - 2] + name_file[name_len - 1]
        if file_extension != '.graphml':
            name_file += '.graphml'
    else:
        name_file += '.graphml'

    ox.io.save_graphml(G, filepath=name_file)
    #ox.io.save_graph_shapefile(G, filepath= directory + 'shapefile')


def plot_graph(G):
    """
    Plot the scenario graph based on elevation colors

    :param G:           NetworkX graph.
                        input graph
    """
    nc = ox.plot.get_node_colors_by_attr(G, 'elevation', cmap='plasma')
    fig1, ax1 = ox.plot_graph(G, node_color=nc, node_size=5, edge_color='#333333', bgcolor='k')


def hypotenuse(G):

    """
    This function calculates the hypotenuse (distance)
    considering latitude, longitude and altitude (x, y, z).
    Also, it uses the pythagorean triangle, where 'a' is
    the hypotenuse, 'b' is the distance between the x and y
    coordinates, and c is the altitude (z).

    :param G:       NetworkX graph.
                    input graph

    :return:        NetworkX graph.
                    Graph with the hypotenuse data
                    in each edge.
    """

    #edges_G = [(u, v, k, data) for u, v, k, data in G.edges(keys=True, data=True) if
    #               data['length'] is None]
    edges_G = [(u, v, k, data) for u, v, k, data in G.edges(keys=True, data=True)]
    if len(edges_G) > 0:
        coord_x = nx.get_node_attributes(G, "x")
        coord_y = nx.get_node_attributes(G, "y")
        coord_z = nx.get_node_attributes(G, "elevation")
        for u, v, k, data in edges_G:  # G.edges(keys=True, data=True):
            coord_x_1 = coord_x.get(u)
            coord_y_1 = coord_y.get(u)
            coord_z_1 = coord_z.get(u)
            coord_1 = (coord_x_1, coord_y_1)
            coord_x_2 = coord_x.get(v)
            coord_y_2 = coord_y.get(v)
            coord_z_2 = coord_z.get(v)
            coord_2 = (coord_x_2, coord_y_2)
            # b = hs.haversine(coord_1, coord_2, unit=Unit.METERS)
            d = coord_x_2 - coord_x_1
            b = coord_y_2 - coord_y_1
            c = coord_z_2 - coord_z_1
            a = ((d ** 2) + (b ** 2) + (c ** 2)) ** (1 / 2)
            ########################
            data['hypotenuse'] = float(a)
    return G


def define_surface(file_osm):
    """
    This function creates a vector with edge surfaces and
    the nodes that the edge contains.

    :param file_osm:    String
                        directory + name of osm file
                        saved in the disk

    :return:            vector
                        It returns a vector with tuples
                        The first item of the tuple has
                        a list with the ids of the nodes
                        within an edge. The second item
                        of the tuple is the surface of
                        the edge. (asphalt, unpaved,
                        paved, etc.)
                        Ex: [([1, 2, 3],'asphalt'),
                            ([4, 5, 6],'unpaved')]
    """

    le = len(file_osm)
    if file_osm[le-4] + file_osm[le-3] + file_osm[le-2] + file_osm[le-1] != '.osm':
        file_osm += '.osm'

    # get the surface of an edge
    x = xml.dom.minidom.parse(file_osm)
    osm = x.documentElement
    all_items = []
    child = [i for i in osm.childNodes if i.nodeType == x.ELEMENT_NODE]

    for i in child:
        if i.nodeName == "way":
            way = [cont for cont in i.childNodes if cont.nodeType == x.ELEMENT_NODE]
            nd = []
            surface_floor = ''
            for tags in way:
                if tags.nodeName == 'nd':
                    nd.append(tags.getAttribute('ref'))
                if tags.getAttribute('k') == 'surface':
                    surface_floor = tags.getAttribute('v')
            if len(surface_floor) > 1:
                all_items.append((nd, surface_floor))

    return all_items


def _surface(u, v, surface_vector):
    """

    :param u:               float/string
                            id of the source node

    :param v:               float/string
                            id of the target node

    :param surface_vector:  vector
                            The vector must have tuples.
                            The first item of the tuple has
                            a list with the ids of the nodes
                            within an edge. The second item
                            of the tuple is the surface of
                            the edge. Created by the
                            'define_surface' function.

    :return:                Surface of edge that contains the
                            input nodes u and v.
    """
    for i in surface_vector:
        if str(u) in i[0] and str(v) in i[0]:
            return i[1]


def surface(G, file_name):
    """
    This function configures the surface of the graph edges.

    :param G:           NetworkX graph.
                        input graph

    :param directory:   String
                        directory of the '.osm' file.

    :param file_name:   String
                        name file '.osm', included
                        file extension. It can be obtained
                        in Open Street Map.

    :return G:          NetworkX graph
                        Graph with surface information in
                        each edge.
    """
    surface_vector = define_surface(file_name)
    function_name = inspect.currentframe().f_code.co_name
    for u, v, k, data in G.edges(keys=True, data=True):
        surface_name = _surface(u, v, surface_vector)
        if surface_name is not None:
            data[function_name] = surface_name
        else:
            data[function_name] = 'paved'
    return G


def define_max_speed(highway):
    """
    This function defines the speed limit from the type of way;
    Ex: the 'motorway' input returns 110 (Km/h)

    :param highway:     String
                        Open Street Map type of a way.

    :return:            int
                        Speed limit estimate of the way in
                        Brazil.
    """

    # the dict contains the speed limit of each way type in 'Km/h'.
    maxspeed = {'motorway': 110, 'trunk': 80, 'primary': 80,
                'secondary': 60, 'tertiary': 40, 'residential': 30,
                'unclassified': 60, 'motorway_link': 80, 'trunk_link': 80,
                'primary_link': 60, 'secondary_link': 40, 'tertiary_link': 40,
                'living_street': 30, 'service': 30, 'pedestrian': 10,
                'track': 60, 'sidewalk': 10, 'footway': 10, 'crossing': 10,
                'steps': 1000, 'cycleway': 80}

    max_speed = maxspeed.get(highway)

    # if the way type is not in the dict, it assumes 60 km/h
    if max_speed is None:
        return 60
    else:
        return max_speed


def maxspeed(G):
    """
    This function defines the maximum speed of the edges.

    :param G:       NetworkX graph.
                    input graph

    :return:        NetworkX graph.
                    graph with max speed attribute
                    in all edges
    """

    # number of edges connecting two points
    width_dict = Counter(G.edges())
    edge_width = {}
    for ((u, v), value) in width_dict.items():
        edge_width.update([((u,v), value)])

    # for each edge considering maxspeed attribute
    for (u, v, wt) in G.edges.data('maxspeed'):

        # if maxspeed attribute is not None,
        # it does not need to do anything.
        # if it is None, it defines the maxspeed.
        if wt is None:
            number_edges = edge_width.get((u, v))

            # if there is just one edge between two nodes,
            # the for loop will have one iteration
            for i in range(number_edges):

                # it gets the type of the way
                type_highway = G.edges[u, v, i]['highway']

                # if there is more than one
                # type of highway in a list
                if type(type_highway) == list:

                    # it gets the max speed in the list
                    # of the way types
                    max_speed_highway = 0
                    for j in type_highway:
                        max_speed = define_max_speed(j)
                        if max_speed > max_speed_highway:
                            max_speed_highway = max_speed

                    G.edges[u, v, i]['maxspeed'] = max_speed_highway
                else:
                    max_speed = define_max_speed(type_highway)
                    G.edges[u, v, i]['maxspeed'] = max_speed

    return G


def travel_time(G):

    hwy_speeds = {'motorway': 110, 'trunk': 80, 'primary': 80,
                  'secondary': 60, 'tertiary': 40, 'residential': 30,
                  'unclassified': 60, 'motorway_link': 80, 'trunk_link': 80,
                  'primary_link': 60, 'secondary_link': 40, 'tertiary_link': 40,
                  'living_street': 30, 'service': 30, 'pedestrian': 10,
                  'track': 60, 'sidewalk': 10, 'footway': 10, 'crossing': 10,
                  'cycleway': 20}

    G = ox.add_edge_speeds(G, hwy_speeds)
    G = ox.add_edge_travel_times(G)

    return G


def max_speed_factor(weight, speed):
    """
    This function multiplies the weight of the edge by a factor,
    according to the maximum speed of the way. The higher the
    speed limit, the more dangerous.

    :param weight:      float
                        Edge weight

    :param speed:       float
                        Speed limit of the way

    :return:            float
    """
    if type(speed) == list:
        speed = max(speed)
    speed = float(speed)

    if speed < 21:
        factor = 0
    elif speed < 41:
        factor = 20
    elif speed < 61:
        factor = 30
    elif speed < 81:
        factor = 40
    elif speed < 91:
        factor = 50
    else:
        factor = 5

    weight = weight + (weight * (factor/100))
    return weight


def force(vehicle_mass, surface_floor, angle_inclination, speed = SPEED):
    """
    This function calculates the work according to the resistance forces,
    It includes aerodynamic force, rolling resistance, and gravity (px).

    :param vehicle_mass:        float
                                Instant vehicle mass in Kg

    :param surface_floor:       String
                                Type of the floor surface in the way.
                                Ex: asphalt

    :param angle_inclination:   float
                                angle (slope) inclination of the way,
                                according to elevation, in radians

    :param speed:               float
                                m/s

    :return:                    float
                                The resultant work in Joules
    """

    rolling_coefficients = {"paved": 0.01, "asphalt": 0.01, "concrete": 0.01,
                            "concrete:lanes": 0.01, "concrete:plates": 0.015,
                            "paving_stones": 0.02, "sett": 0.02, "unhewn_cobblestone": 0.032,
                            "cobblestone": 0.032, "metal": 0.01, "stepping_stones":0.4,
                            "unpaved": 0.06, "compacted": 0.06, "fine_gravel": 0.06,
                            "gravel": 0.08, "rock": 0.08, "pebblestone": 0.08,
                            "ground": 0.1, "dirt": 0.2, "earth": 0.2, "grass": 0.05,
                            "grass_paver": 0.1, "snow": 0.2, "woodchips": 0.05,
                            "sand": 0.05, "mud": 0.05}

    rolling_coefficient = rolling_coefficients.get(surface_floor)
    if rolling_coefficient is None:
        rolling_coefficient = 0.01 * (1 + (0.001 * speed))

    normal = vehicle_mass * constants.g * math.cos(angle_inclination)

    rolling_resistance = rolling_coefficient * normal

    aerodynamic_force = (1 / 2) * AIR_DENSITY * AERODYNAMIC_COEFFICIENT \
                        * FRONTAL_VEHICLE_AREA * (speed ** 2)

    # print(aerodynamic_force)

    px = vehicle_mass * constants.g * math.sin(angle_inclination)

    # force to maintain a constant velocity
    resultant_force = aerodynamic_force + px + rolling_resistance

    return abs(resultant_force)


def work(vehicle_mass, surface_floor, angle_inclination, hypotenuse_length):
    """
        This function calculates the work according to the resistance forces,
        It includes aerodynamic force, rolling resistance, and gravity (px).

        :param vehicle_mass:        float
                                    Instant vehicle mass in Kg

        :param surface_floor:       String
                                    Type of the floor surface in the way.
                                    Ex: asphalt

        :param angle_inclination:   float
                                    angle (slope) inclination of the way,
                                    according to elevation, in radians

        :param hypotenuse_length:   float
                                    The displacement value calculated
                                    according to angle of the inclination

        :return:                    float
                                    The resultant work in Joules
        """

    hypotenuse_length = float(hypotenuse_length)

    resultant_force = force(vehicle_mass, surface_floor, angle_inclination, SPEED)

    resultant_work = resultant_force * hypotenuse_length

    return resultant_work


def max_grade_factor(weight_value, max_grade, grade, percentage=0.5):
    factor_grade = math.exp(grade)/math.exp(max_grade)
    weight_value = weight_value + (weight_value * factor_grade * percentage)
    return weight_value


def impedance(length, grade):
    if grade > 0:
        penalty = grade ** 2
    else:
        penalty = grade * (-1)
    return length * penalty


def update_weight(G, vehicle_mass, max_grade = None, speed_factor = SPEED_FACTOR):
    """
    Update all edge weights of the graph G,
    according to current vehicle mass.

    :param G:               NetworkX graph.
                            input graph

    :param vehicle_mass:    float
                            The instant mass of the vehicle

    :return:                function
                            it returns a function that verifies an edge weight
    """

    for u, v, k, data in G.edges(keys=True, data=True):

        weight_value = work(vehicle_mass, data['surface'], data['grade'], data['length']) # math.degrees()
        impedance_value = impedance(data['length'], data['grade'])
        # length_value = data['length']
        length_value = float(data['length'])

        # if GRADE_FACTOR is True:
        #    weight_value = max_grade_factor(weight_value, max_grade, data['grade'])

        if speed_factor is True:
            # avoid dangerous streets (high speeds)
            length_value = max_speed_factor(length_value, data['maxspeed'])
            weight_value = max_speed_factor(weight_value, data['maxspeed'])
            impedance_value = max_speed_factor(impedance_value, data['maxspeed'])

        data['weight'] = weight_value
        data['impedance'] = impedance_value
        data['distance'] = length_value

    return G


def get_edge_weight(G, u, v, id_edge, impedance):
    """
    It gets the edge weight of the graph G.

    :param G:           NetworkX graph.
                        input graph

    :param u:           Source node of the edge

    :param v:           Target node of the edge

    :param id_edge:     Integer
                        Id of the edge

    :return:            float
                        The weight of the edge
    """
    weights = nx.get_edge_attributes(G, impedance)
    return weights.get((u, v, id_edge))


def _weight(G, weight):
    """
    Update edge weight and returns a function that
     returns the weight of an edge.

    :param G:           NetworkX graph.
                        input graph

    :param weight:      if it is a function, it updates
                        edge weight and returns a function
                        that verifies an edge weight.
                        If it is a string, it considers the
                        string as the name of weight attribute
                        and returns a function that verifies an
                        edge weight according to the name
                        of the attribute

    """
    if callable(weight):
        return weight

    if G.is_multigraph():
        return lambda u, v, d: min(attr.get(weight, 1) for attr in d.values())
    return lambda u, v, data: data.get(weight, 1)


def configure_graph(G, geotiff_name, stop_points, ad_weights, file_name_osm):

    G, nodes_and_coordinates, nodes_and_weights = Scenario.add_collect_points(G, stop_points, ad_weights, file_name_osm)
    G = set_node_elevation(G, MAPS_DIRECTORY + geotiff_name)
    G = edge_grades(G)
    G = surface(G, file_name_osm)
    G = hypotenuse(G)
    G = maxspeed(G)
    max_grade = max(list(nx.get_edge_attributes(G, "grade").values()))
    G = update_weight(G, VEHICLE_MASS, max_grade)

    save_graph_file(G, GRAPH_NAME)
    #plot_graph(G)

    return G, nodes_and_coordinates, nodes_and_weights


def configure_graph_simulation(G, geotiff_name, stop_points, ad_weights, file_name_osm, G_file):

    G, nodes_coordinates, nodes_weights = Scenario.add_collect_points(G, stop_points, ad_weights, file_name_osm)

    Main.netconvert_geotiff(file_name_osm, MAPS_DIRECTORY + 'out.tif', NET)

    G = Scenario.simulation_edit_graph(G, file_name_osm)

    G = set_node_elevation(G, geotiff_name)

    G = edge_grades(G)

    G = surface(G, file_name_osm)

    # G = hypotenuse(G)

    G = maxspeed(G)

    G = travel_time(G)

    max_grade = max(list(nx.get_edge_attributes(G, "grade").values()))
    G = update_weight(G, VEHICLE_MASS, max_grade)

    # it transforms some edges in two ways streets
    if BIDIRECTIONAL is True:
        add_edges_G = [(v, u, data) for u, v, k, data in G.edges(keys=True, data=True) if G.has_edge(*(v, u)) is False and data['highway'] in TWO_WAY]
        G.add_edges_from(add_edges_G)

    save_graph_file(G, G_file)

    return G, nodes_coordinates, nodes_weights


if __name__ == '__main__':
    G = ox.graph_from_bbox(-22.796008, -22.843953, -47.054891, -47.107718000000006, network_type='all')
    #name_osm = '../data/maps/47.107718000000006_22.843953_47.054891_22.796008.osm'
    #G = set_node_elevation(G, '../' + MAPS_DIRECTORY + '22S48_ZN.tif')
    #G = edge_grades(G)
    #nodes = list(G.nodes)
    #G = surface(G, '../' + MAPS_DIRECTORY, name_osm)
    #G = hypotenuse(G)
    G = maxspeed(G)
    G = travel_time(G)
    #G = update_weight(G, 10)

    #G2 = G.copy()
    fig, ax = ox.plot_graph(G)
    #deadends = [(u, v) for u, v, k, data in G.edges(keys=True, data=True) if data['highway'] == 'footway']
    #print(deadends)
    #G2.remove_nodes_from(deadends)
    #fig, ax = ox.plot_graph(G2)
    #G2.remove_nodes_from(deadends)
    #fig, ax = ox.plot_graph(G2)



