import osmnx as ox
import pandas as pd
import networkx as nx
import inspect
from geography import GeoTiff
from Constants import *


def set_node_elevation(G, directory, name_file_geotiff):
    """
    Add `elevation` attribute to each node in meters.
    Uses elevation data by geotiff file by default

    :param G:       NetworkX graph
                    input graph
    :param geotiff: str
                    path + file_name of the geotiff
    :return:        networkx.MultiDiGraph
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
        elevation.append(GeoTiff.coordinate_pixel(directory + name_file_geotiff, longitudes[i], latitudes[i]))

    # create a pandas series with the id of the node and corresponding elevation values
    pd_elevation = pd.Series(elevation, index=ids)

    # add the elevation value in the node attributes
    nx.set_node_attributes(G, pd_elevation.to_dict(), name="elevation")

    return G


#def add_surface(G):


def edge_grades(G):
    """

    :param G:   NetworkX graph
                input graph
    :return:    networkx.MultiDiGraph
                graph with edge grades attributes
    """
    G = ox.add_edge_grades(G)
    return G


def save_graph_file(G, directory='', name_file='map'):
    """
    Save the graph file

    :param G:           NetworkX graph
                        input graph

    :param directory:   String
                        path to save the file

    :param name_file    String
                        Name of the file
    """
    name_len = len(name_file)

    # the length of extension
    if name_len > 7:
        file_extension = name_file[name_len - 8] + name_file[name_len - 7] +\
                         name_file[name_len - 6] + name_file[name_len - 5] +\
                         name_file[name_len - 4] + name_file[name_len - 3] +\
                         name_file[name_len - 2] + name_file[name_len - 1]
        if file_extension != '.graphml':
            name_file += '.graphml'
    else:
        name_file += '.graphml'

    ox.io.save_graphml(G, filepath=directory + name_file)


def plot_graph(G):
    """
    Plot the scenario graph based on elevation colors

    :param G:           NetworkX graph.
                        input graph
    """
    nc = ox.plot.get_node_colors_by_attr(G, 'elevation', cmap='plasma')
    fig1, ax1 = ox.plot_graph(G, node_color=nc, node_size=5, edge_color='#333333', bgcolor='k')


# define some edge impedance function here
def impedance(length, grade):
    penalty = grade ** 2
    name = inspect.currentframe().f_code.co_name
    return name, length * penalty


def update_weight(G, function):
    """
    Update edge weight.

    :param G:           NetworkX graph.
                        input graph

    :param function:    A function to update edge weight

    :return:            function
                        it returns a function that verifies an edge weight
    """
    for u, v, k, data in G.edges(keys=True, data=True):
        name, data[name] = function(data['length'], data['grade'])
    return lambda u, v, d: min(attr.get(name, 1) for attr in d.values())


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
        weight_function = update_weight(G, weight)
        return weight_function

    if G.is_multigraph():
        return lambda u, v, d: min(attr.get(weight, 1) for attr in d.values())
    return lambda u, v, data: data.get(weight, 1)


def displacement(G):
    name = inspect.currentframe().f_code.co_name
    all_items = G.succ
    coord_x = nx.get_node_attributes(G, "x")
    coord_y = nx.get_node_attributes(G, "y")
    for u, v, k, data in G.edges(keys=True, data=True):
        node_1 = all_items.get(u)
        node_2 = all_items.get(v)
        coord_x_1 = coord_x.get(node_1)
        coord_y_1 = coord_x.get(node_1)
        #name, data[name] = value


def motriz_force(G, id_edge, vehicle_mass, angle_inclination):
    force_px = vehicle_mass * constants.g * math.sin(angle_inclination)
    # force = (vehicle_mass * accel) + force_px
    # work = force *


if __name__ == '__main__':
    G = ox.graph_from_bbox(-22.796008, -22.843953, -47.054891, -47.107718000000006, network_type='all')
    G = set_node_elevation(G, '../' + MAPS_DIRECTORY, '22S48_ZN.tif')
    G = edge_grades(G)
    nodes = list(G.nodes)
    function_weight = _weight(G, impedance)
    save_graph_file(G, '../' + MAPS_DIRECTORY, 'map')
