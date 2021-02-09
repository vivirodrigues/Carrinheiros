import geopy.distance
from geopy.geocoders import Nominatim
from models.mapsServer.Overpass import Overpass
import statistics


def string_coordinate(coordinate):
    lat = str(coordinate[0])
    lon = str(coordinate[1])
    return lat + "," + lon


def get_id_edge_from_coordinate(coordinate):
    # get the way of a node
    geolocator = Nominatim(user_agent="DS")
    location = geolocator.reverse(coordinate)
    osm_id = location.raw.get('osm_id')
    osm_type = location.raw.get('osm_type')
    if osm_type == 'way':
        return osm_id
    elif osm_type == 'node':
        # create an option to make a route until de node directly
        road = location.raw.get('address').get('road')
        city_district = location.raw.get('address').get('city_district')
        city = location.raw.get('address').get('city')
        country = location.raw.get('address').get('country')
        search = road + ',' + city_district + ',' + city + ',' + country
        try:
            location = geolocator.geocode(search)
            test = location.raw
        except:
            # if the search fail
            search = road + ',' + city
            location = geolocator.geocode(search)
        osm_id = location.raw.get('osm_id')
        return osm_id


def get_nodes_from_edge(edge_id):
    # pegar todos os nodes e as respectivas lon, lat de dentro de uma aresta
    query_state = "way(" + str(edge_id) + "); (._;>;); out qt;"
    api_overpass = Overpass(query_state)
    result = api_overpass.get_response()
    nodes = {}
    for i in result.nodes:
        nodes.update([(i.id, (float(i.lon), float(i.lat)))])
    return nodes


def order(coordinate):
    lon = coordinate[0]
    lat = coordinate[1]
    new_coordinate = (lat, lon)
    return new_coordinate


def get_closest_node_id(coordinate, nodes):
    min_distance = float('inf')
    closest = ''
    for i in nodes:
        node_coordinate = order(nodes.get(i))
        distance = geopy.distance.geodesic(coordinate, node_coordinate).m
        if distance < min_distance:
            closest = i
            min_distance = distance
    return closest


def _between_nodes_rascunho(coordinate, nodes, closest):
    first_node = closest
    list_keys = list(nodes.keys())
    index_closest = list_keys.index(first_node)
    new_nodes = {}
    if index_closest > 0:
        key_before = list_keys[index_closest - 1]
        new_nodes.update([(key_before, nodes.get(key_before))])
    if index_closest < len(nodes) - 1:
        key_after = list_keys[index_closest + 1]
        new_nodes.update([(key_after, nodes.get(key_after))])
    second_node = get_closest_node_id(coordinate, new_nodes)
    # between_nodes = ()
    if first_node == second_node:
        between_nodes = tuple(first_node)
    else:
        between_nodes = (first_node, second_node)
    return between_nodes
    # closest_node_inside_edge = get_closest_node_id(coordinate, nodes)
    # nodes_between = _between_nodes(coordinate, nodes, closest_node_inside_edge)


def _is_horizontal_way(list_nodes_values):
    """

    :param list_nodes_values: list
    :return: boolean
    """
    lat = []
    for i in list_nodes_values:
        lat.append(i[1])
    lon = []
    for i in list_nodes_values:
        lon.append(i[0])
    variance_lat = statistics.variance(lat)
    variance_lon = statistics.variance(lon)
    if variance_lon > variance_lat:
        return True
    else:
        return False


def _quadrants(coordinate, list_nodes_values, list_nodes_keys):

    coordinate = order(coordinate)

    left = {}
    right = {}
    bottom = {}
    top = {}

    for i in range(0, len(list_nodes_values)):
        if list_nodes_values[i][0] <= coordinate[0]:
            left.update([(list_nodes_keys[i], list_nodes_values[i])])
        else:
            right.update([(list_nodes_keys[i], list_nodes_values[i])])
        if list_nodes_values[i][1] <= coordinate[1]:
            bottom.update([(list_nodes_keys[i], list_nodes_values[i])])
        else:
            top.update([(list_nodes_keys[i], list_nodes_values[i])])

    return left, right, bottom, top


def _between_nodes(coordinate, nodes):

    list_nodes_values = list(nodes.values())
    list_nodes_keys = list(nodes.keys())

    left, right, bottom, top = _quadrants(coordinate, list_nodes_values, list_nodes_keys)

    # if the longitudinal variation is greater than the latitudinal variation
    is_horizontal_way = _is_horizontal_way(list_nodes_values)

    if is_horizontal_way:
        if len(left) > 0 and len(right) > 0:
            first_closest = get_closest_node_id(coordinate, left)
            second_closest = get_closest_node_id(coordinate, right)
        else:
            # if there is not node in one of the sides
            print("Error")
            first_closest = get_closest_node_id(coordinate, top)
            second_closest = get_closest_node_id(coordinate, bottom)
    else:
        if len(top) > 0 and len(bottom) > 0:
            first_closest = get_closest_node_id(coordinate, top)
            second_closest = get_closest_node_id(coordinate, bottom)
        else:
            # if there is not node in one of the sides
            print("Error")
            first_closest = get_closest_node_id(coordinate, left)
            second_closest = get_closest_node_id(coordinate, right)
    between_nodes = (first_closest, second_closest)
    return between_nodes

def between_nodes(coordinate_float):
    coordinate = string_coordinate(coordinate_float)
    id_edge = get_id_edge_from_coordinate(str(coordinate))
    nodes = get_nodes_from_edge(id_edge)
    nodes_between = _between_nodes(coordinate_float, nodes)
    return nodes_between


if __name__ == '__main__':
    coordinate = (-22.816008, -47.075614)
    #coordinate = string_coordinate(coordinate)
    id_edge = get_id_edge_from_coordinate(string_coordinate(coordinate))
    nodes = get_nodes_from_edge(id_edge)
    closest_node_inside_edge = get_closest_node_id(coordinate, nodes)
    nodes_between = _between_nodes(coordinate, nodes)
    print(nodes_between)
