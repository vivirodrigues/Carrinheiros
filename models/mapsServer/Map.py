import geopy.distance
from geopy.geocoders import Nominatim
from models.mapsServer.Overpass import Overpass


def string_coordinate(coordinate):
    lat = str(coordinate[0])
    lon = str(coordinate[1])
    return lat + "," + lon


def get_id_edge_from_coordinate(coordinate):
    # pegar a aresta do node
    geolocator = Nominatim(user_agent="DS")
    location = geolocator.reverse(coordinate)
    edge_id = location.raw.get('osm_id')
    return edge_id


def get_nodes_from_edge(edge_id):
    # pegar todos os nodes e as respectivas lon, lat de dentro de uma aresta
    query_state = "way(" + str(edge_id) + "); (._;>;); out qt;"
    api_overpass = Overpass(query_state)
    result = api_overpass.get_response()
    nodes = {}
    for i in result.nodes:
        nodes.update([(i.id, (float(i.lon), float(i.lat)))])
    print("len", len(nodes))
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


def _between_nodes(coordinate, nodes, closest):
    first_node = closest
    list_keys = list(nodes.keys())
    index_closest = list_keys.index(first_node)
    new_nodes = {}
    if index_closest > 0:
        key_before = list_keys[index_closest - 1]
        new_nodes.update([(key_before, nodes.get(key_before))])
    if index_closest < len(nodes):
        key_after = list_keys[index_closest + 1]
        new_nodes.update([(key_after, nodes.get(key_after))])
    second_node = get_closest_node_id(coordinate, new_nodes)
    between_nodes = ()
    if first_node == second_node:
        between_nodes = tuple(first_node)
    else:
        between_nodes = (first_node, second_node)
    return between_nodes


def between_nodes(coordinate):
    coordinate = string_coordinate(coordinate)
    id_edge = get_id_edge_from_coordinate(str(coordinate))
    nodes = get_nodes_from_edge(id_edge)
    closest_node_inside_edge = get_closest_node_id(coordinate, nodes)
    nodes_between = _between_nodes(coordinate, nodes, closest_node_inside_edge)
    return nodes_between


if __name__ == '__main__':
    coordinate = (-22.816008, -47.075614)
    coordinate = string_coordinate(coordinate)
    id_edge = get_id_edge_from_coordinate(str(coordinate))
    nodes = get_nodes_from_edge(id_edge)
    closest_node_inside_edge = get_closest_node_id(coordinate, nodes)
    nodes_between = _between_nodes(coordinate, nodes, closest_node_inside_edge)
    print(nodes_between)


