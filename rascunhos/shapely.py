import osmnx as ox
from shapely.geometry import Point, LineString


def order(coordinate):
    lon = coordinate[0]
    lat = coordinate[1]
    new_coordinate = (lat, lon)
    return new_coordinate


def cut(line, distance):
    # Cuts a line in two at a distance from its starting point
    print("distance", distance)
    print("len", line.length)
    if distance <= 0.000 or distance >= line.length:
        print("entrou aqui")
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


G = ox.graph_from_bbox(-22.796008, -22.843953, -47.054891, -47.107718000000006, network_type='all')
i = (-22.82504, -47.07730)
node1, node2, key, shapely, distance = ox.get_nearest_edge(G, i, return_geom=True, return_dist=True)

coords = shapely.coords[:]
point = Point(i)

b = []
for i in coords:
    b.append(order(i))

line = LineString(b)
print("line", LineString(line))
d = line.project(point)
print("d", d)
a = cut(line, d)
print("tamanho", len(a))
print("primeira coord", a[0].coords[:])

print("boundary", list(line.boundary.boundary))
print("distance", point.distance(line))
print("bounds", shapely.bounds) # (minx, miny, maxx, maxy)

# G.add_edges_from([(id_node_collect_point, keys[0]), (id_node_collect_point, keys[1])])
# G.add_node(id_node_collect_point, x=i[1], y=i[0])
# G.add_edges_from([(id_node_from, id_node_to)])