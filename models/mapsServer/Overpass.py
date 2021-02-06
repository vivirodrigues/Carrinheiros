import overpy
import geopy.distance
from geopy.geocoders import Nominatim

class Overpass:
    # it connects with Overpass API based on the input query
    def __init__(self, query):
        self.api = overpy.Overpass()
        self.query = query
        self.response = ''
        self.set_response()

    def set_query(self, query):
        self.query = query

    def get_query(self):
        return self.query

    def set_response(self):
        response = self.api.query(self.query)
        self.response = response

    def get_response(self):
        # returns the response from Overpass API based on the input query
        return self.response


if __name__ == '__main__':
    """
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

    
    # verificar de qual node a coordenada esta mais perto
    flag = True
    cont = 0
    while flag == True:
        cont += 50  # meters
        query_state = "node(around:" + str(cont) + ", -22.816008, -47.075614); (._;>;); out;"
        api_overpass = Overpass(query_state)
        result = api_overpass.get_response()
        if len(result.nodes) > 1:
            flag = False
    
    # distance between 2 points (coordinates)
    def closest(coord1, coord2):
        distance = geopy.distance.geodesic(coord1, coord2).m
        return distance

    print(closest((-22.816008, -47.075614), (-22.816008, -47.075613)))
    
    # verificar centro da aresta
    query_state = "way(around:100.0, -22.816008, -47.075614); (._;>;); out center;"
    api_overpass = Overpass(query_state)
    result = api_overpass.get_response()
    print(result.ways[0].id)
    print(result.ways[0].center_lat)
    
    """

    # pegar a aresta do node
    geolocator = Nominatim(user_agent="DS")
    location = geolocator.reverse("-22.816008, -47.075614")
    print(location.address)
    print(location.raw.get('osm_id'))

    # pegar todos os nodes e as respectivas lon, lat de dentro de uma aresta
    query_state = "way(" + str(location.raw.get('osm_id')) + "); (._;>;); out qt;"
    api_overpass = Overpass(query_state)
    result = api_overpass.get_response()
    nodes = {}
    for i in result.nodes:
        nodes.update([(i.id, (float(i.lon), float(i.lat)))])
    #print(nodes)
    # nodes = dict(sorted(nodes.items(), key=lambda item: item[1]))
    # print(sorted(list(nodes.values()), key=lambda k: [k[1], k[0]]))

    # verificar qual node fica mais proximo
    def closest(coord1, coords):
        dist = 1000
        menor = 0
        for i in coords:
            print("avaliado", i)
            coord_new = invert(coords.get(i))
            distance = geopy.distance.geodesic(coord1, coord_new).m
            print("distance", distance, "between", coord1, coord_new)
            if distance < dist:
                menor = i
                dist = distance
        return menor

    def invert(coord):
        lon = coord[0]
        lat = coord[1]
        return (lat, lon)

    print(closest((-22.816008, -47.075614), nodes))


    index_closest = list(nodes.keys()).index(860793205)
    print(nodes[index_closest - 1])