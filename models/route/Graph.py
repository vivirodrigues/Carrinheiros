import osmnx as ox
import pandas as pd
import networkx as nx
import inspect
from models.mapsServer import ScenarioGeo


def set_node_elevation(G, geotiff):
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
        elevation.append(ScenarioGeo.get_coordinate_pixel(geotiff, longitudes[i], latitudes[i]))

    # create a pandas series with the id of the node and corresponding elevation values
    pd_elevation = pd.Series(elevation, index=ids)

    # add the elevation value in the node attributes
    nx.set_node_attributes(G, pd_elevation.to_dict(), name="elevation")

    return G


def set_edge_grades(G):
    """

    :param G:   NetworkX graph
                input graph
    :return:    networkx.MultiDiGraph
                graph with edge grades attributes
    """
    G = ox.add_edge_grades(G)
    return G


def save_graph_file(G, file_path):
    """
    Save the graph file

    :param G:           NetworkX graph
                        input graph
    :param file_path:   str
                        path + file_name to save
    """
    ox.io.save_graphml(G, filepath=file_path)


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


if __name__ == '__main__':
    G = ox.graph_from_bbox(-22.796008, -22.843953, -47.054891, -47.107718000000006, network_type='all')
    G = set_node_elevation(G, '../maps/22S48_ZN.tif')
    G = set_edge_grades(G)
    nodes = list(G.nodes)
    function_weight = _weight(G, impedance)
    save_graph_file(G, '../maps/map.graphml')
