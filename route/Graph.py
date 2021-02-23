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


def hypotenuse(G):
    name = inspect.currentframe().f_code.co_name
    coord_x = nx.get_node_attributes(G, "x")
    coord_y = nx.get_node_attributes(G, "y")
    coord_z = nx.get_node_attributes(G, "elevation")
    for u, v, k, data in G.edges(keys=True, data=True):
        coord_x_1 = coord_x.get(u)
        coord_y_1 = coord_y.get(u)
        coord_z_1 = coord_z.get(u)
        coord_1 = (coord_x_1, coord_y_1)
        coord_x_2 = coord_x.get(v)
        coord_y_2 = coord_y.get(v)
        coord_z_2 = coord_z.get(v)
        coord_2 = (coord_x_2, coord_y_2)
        b = hs.haversine(coord_1, coord_2, unit=Unit.METERS)
        c = coord_z_2 - coord_z_1
        a = ((b ** 2) + (c ** 2)) ** (1/2)
        ########################
        data[name] = str(a)

def define_surface(file_osm):

    le = len(file_osm)
    if file_osm[le-4] + file_osm[le-3] + file_osm[le-2] + file_osm[le-1] != '.osm':
        file_osm += '.osm'

    # get the surface of an edge
    x = xml.dom.minidom.parse(file_osm)
    osm = x.documentElement
    all_items = []
    child = [i for i in osm.childNodes if i.nodeType == x.ELEMENT_NODE]
    surface = ''

    for i in child:
        if i.nodeName == "way":
            way = [cont for cont in i.childNodes if cont.nodeType == x.ELEMENT_NODE]
            nd = []
            for tags in way:
                if tags.nodeName == 'nd':
                    nd.append(tags.getAttribute('ref'))
                if tags.getAttribute('k') == 'surface':
                    surface = tags.getAttribute('v')
            if len(surface) > 1:
                all_items.append((nd, surface))
    print(all_items)
    return all_items


def _work(surface_floor, vehicle_mass, angle_inclination, displacement):

    # vehicle_mass in kg

    rolling_coefficients = {"paved": 0.01, "asphalt": 0.01, "concrete": 0.01,
                            "concrete:lanes": 0.01, "concrete:plates": 0.015,
                            "paving_stones": 0.02, "sett": 0.02, "unhewn_cobblestone": 0.032,
                            "cobblestone" :0.032, "metal":0.01, "stepping_stones":0.4,
                            "unpaved":0.06, "compacted":0.06, "fine_gravel": 0.06,
                            "gravel": 0.08, "rock": 0.08, "pebblestone": 0.08,
                            "ground": 0.1, "dirt":0.2, "earth": 0.2, "grass": 0.05,
                            "grass_paver": 0.1, "snow":0.2, "woodchips": 0.05,
                            "sand":0.05, "mud":0.05}

    rolling_coefficient = rolling_coefficients.get(surface_floor)
    air_density = 1.2  # km / m³
    aerodynamic_coefficient = 1  # flat surface
    frontal_vehicle_area = 1  # m²
    speed = 0.83  # m/s = 3 km/h
    if rolling_coefficient is None:
        rolling_coefficient = 0.01 * (1 + (0.001 * speed))

    displacement = float(displacement)
    normal = vehicle_mass * constants.g * math.cos(abs(angle_inclination))
    rolling_resistance = rolling_coefficient * normal
    aerodynamic_force = (1 / 2) * air_density * aerodynamic_coefficient \
                        * frontal_vehicle_area * (speed ** 2)
    px = vehicle_mass * constants.g * math.sin(abs(angle_inclination))

    # force to maintain a constant velocity
    force = aerodynamic_force + px + rolling_resistance

    resultant_work = force * displacement

    return resultant_work


def work(G, floor_type, vehicle_mass):
    function_name = inspect.currentframe().f_code.co_name
    hypotenuse(G)
    for u, v, k, data in G.edges(keys=True, data=True):
        data[function_name] = _work(floor_type, vehicle_mass, data['grade'], data['hypotenuse'])
    return lambda u, v, d: min(attr.get(function_name, 1) for attr in d.values())


if __name__ == '__main__':
    G = ox.graph_from_bbox(-22.796008, -22.843953, -47.054891, -47.107718000000006, network_type='all')
    G = set_node_elevation(G, '../' + MAPS_DIRECTORY, '22S48_ZN.tif')
    G = edge_grades(G)
    nodes = list(G.nodes)
    # work_f = work(G, 0.5, 10)
    # save_graph_file(G, '../' + MAPS_DIRECTORY, 'map1')
    define_surface('../'+ MAPS_DIRECTORY + FILE_NAME_OSM)
