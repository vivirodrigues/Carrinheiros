import geopy.distance
from geopy.geocoders import Nominatim

# define Nominatim geocoder user
geolocator = Nominatim(user_agent="DS")

# search for the coordinate information
location = geolocator.reverse(coordinate)
osm_type = location.raw.get('osm_type')
if osm_type == 'node':
    print("id", location.raw.get('osm_id'))
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


def order(coordinate):
    lon = coordinate[0]
    lat = coordinate[1]
    new_coordinate = (lat, lon)
    return new_coordinate

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

# verificar centro da aresta
query_state = "way(around:100.0, -22.816008, -47.075614); (._;>;); out center;"
api_overpass = Overpass(query_state)
result = api_overpass.get_response()
print(result.ways[0].id)
print(result.ways[0].center_lat)

# pegar a aresta do node
geolocator = Nominatim(user_agent="DS")
location = geolocator.reverse("-22.816008, -47.075614")
print(location.address)
print(location.raw.get('osm_id'))

# distance between 2 points (coordinates)
def closest(coord1, coord2):
    distance = geopy.distance.geodesic(coord1, coord2).m
    return distance

print(closest((-22.816008, -47.075614), (-22.816008, -47.075613)))

# pegar todos os nodes e as respectivas lon, lat de dentro de uma aresta
query_state = "way(around:100.0, -22.816008, -47.075614); (._;>;); out qt;"
api_overpass = Overpass(query_state)
result = api_overpass.get_response()
a = {}
for i in result.ways:
    di = {}
    for j in i.nodes:
        di.update([(j.id, (float(j.lon), float(j.lat)))])
    a.update([(i.id, di)])
print(a.get(70200192))