import geopy.distance
from geopy.geocoders import Nominatim
from geography import Overpass
import statistics
import sys
import time


def _string_coordinate(coordinate):
    """
    Private function.

    It changes the type of coordinate data
    from tuple with float numbers to a string.


    :param coordinate:      tuple
                            (float, float) : lat, lon

    :return:                String
                            "lat, lon"
    """
    lat = str(coordinate[0])
    lon = str(coordinate[1])
    return lat + "," + lon


def _geolocator(coordinate, name_project):
    """
    Private function.

    This function gets the Open Street Map (OSM)
    information about the input coordinate using
    geopy.geocoders.Nominatim.


    :param coordinate:      String
                            The string must have the coordinates
                            Format: (lat, lon)
                            Example: "(00.00, 00.00)"

    :param name_project     String
                            The name of the current project

    :return:                geopy.geocoders.Nominatim.geolocator
                            This object has OSM information
                            about the input coordinate
    """
    # define Nominatim geocoder user
    geolocator = Nominatim(user_agent=name_project)

    while True:
        try:
            # search for the coordinate information

            location = geolocator.reverse(coordinate)
            if location.raw:
                return location
        except AttributeError:
            #print(
            #    "Error: The coordinates do not correspond to a valid location. It is necessary to be close to a road.")
            return None
        except:
            # print("Another exception")
            time.sleep(30)
            continue
        break


def _osm_type(location):
    """
    Private function.

    This function verifies the type of the location.
    The input could be an Open Street Map (OSM) node
    or a part of a way, an OSM type of data containing
    multiples nodes.


    :param location         geopy.geocoders.Nominatim.geolocator
                            This object has OSM information
                            about the input coordinate

    :return:                String
                            Open Street Map type
                            "node" or "way"
    """

    # get the osm type
    # (coordinate can correspond to a node or a way)
    osm_type = location.raw.get('osm_type')

    if osm_type is not None:
        return osm_type
    else:
        #print("Error: OSM Type does not exists")
        sys.exit()


def _id_osm(location):
    """
    Private function.

    This function gets the location id from the Open Street Map.


    :param location         geopy.geocoders.Nominatim.geolocator
                            This object has OSM information
                            about the input coordinate

    :return:                int
                            Open Street Map id
    """

    osm_id = location.raw.get('osm_id')
    if osm_id is not None:
        return osm_id
    else:
        #print("Error: OSM ID does not exists")
        sys.exit()


def coordinate_node(id_node):
    """
    This function verifies the coordinates
    of an Open Street Map (OSM) id of node.

    :param id_node:     int
                        OSM id of the node

    :return:            tuple
                        The function returns a tuple
                        with two float values, latitude
                        and longitude of the OSM node.
                        (lat, lon)
    """
    query_state = "node(" + str(id_node) + "); (._;>;); out qt;"
    result_overpass = Overpass.overpy_response(query_state)

    lat = float(result_overpass.nodes[0].lat)
    lon = float(result_overpass.nodes[0].lon)

    return lat, lon


def nodes_from_way_osm(osm_id):
    """
    This function gets all nodes inside a way of
    the Open Street Map. The nodes has latitude
    and longitude.


    :param osm_id:      int
                        Open Street Map id

    :return:            dict
                        {id_node: (lat, lon)}
    """

    # the Overpass query must get all nodes from a osm way
    query_state = "way(" + str(osm_id) + "); (._;>;); out qt;"
    result = Overpass.overpy_response(query_state)

    nodes = {}

    # in each node of the way, get the lat and lon
    for i in result.nodes:
        # nodes.update(id_node : (lat, lon))
        nodes.update([(i.id, (float(i.lat), float(i.lon)))])

    return nodes


def closest_node_id(coordinate, nodes):
    """
    This function gets the closest osm node from
    the input coordinate using geodesic distance.

    :param coordinate:      tuple
                            (float, float) : lat, lon

    :param nodes:           dict
                            {id_node: (lat, lon)}

    :return:                dict
                            {id_node: (lat, lon)}
                            osm id and coordinate of
                            the closest node
    """

    min_distance = float('inf')
    closest = {}

    for i in nodes:

        # coordinate of the current node
        node_coordinate = nodes.get(i)

        # distance between coordinate and the current node in meters
        distance = geopy.distance.geodesic(coordinate, node_coordinate).m
        if distance < min_distance:
            # it is necessary to empty the dictionary
            closest = {}
            closest.update([(i, node_coordinate)])
            min_distance = distance

    return closest


def is_horizontal_way(list_nodes_values):
    """
    This function verifies if the way has more variance
    horizontally (longitude) or vertically (latitude).

    :param list_nodes_values:       list
                                    it contains tuples with lat and lon
                                    [(lat, lon)]

    :return: boolean                True if is a horizontal way, false
                                    if is not.
    """
    # create a list with all nodes latitudes
    lat = []
    for i in list_nodes_values:
        lat.append(i[1])

    # create a list with all nodes longitudes
    lon = []
    for i in list_nodes_values:
        lon.append(i[0])

    # verify the variance in latitude list
    variance_lat = statistics.variance(lat)

    # verify the variance in longitude list
    variance_lon = statistics.variance(lon)

    # if longitude has more variance, it is
    # a horizontal way
    if variance_lon > variance_lat:
        return True
    else:
        return False


def quadrants(coordinate, nodes):
    """
    Separate the nodes adjacent to the input coordinate
    into quadrants:

    :param coordinate:          tuple
                                (float, float) : lat, lon

    :param nodes:               dict
                                {id_node: (lat, lon)}

    :return:                    list, list, list, list
                                left, right, bottom, top
    """

    list_nodes_values = list(nodes.values())
    list_nodes_keys = list(nodes.keys())

    left = {}
    right = {}
    top = {}
    bottom = {}

    for i in range(0, len(list_nodes_values)):

        # if latitude of the current node <= latitude of the input coordinate
        if list_nodes_values[i][0] <= coordinate[0]:

            # bottom nodes dict = {id of the node: (lat, lon)}
            bottom.update([(list_nodes_keys[i], list_nodes_values[i])])
        else:

            # top nodes dict = {id of the node: (lat, lon)}
            top.update([(list_nodes_keys[i], list_nodes_values[i])])

        # if longitude of the current node <= longitude of the input coordinate
        if list_nodes_values[i][1] <= coordinate[1]:

            # left nodes dict = {id of the node: (lat, lon)}
            left.update([(list_nodes_keys[i], list_nodes_values[i])])

        else:

            # right nodes dict = {id of the node: (lat, lon)}
            right.update([(list_nodes_keys[i], list_nodes_values[i])])

    return left, right, bottom, top


def _adjacent_nodes(coordinate, nodes):
    """

    :param coordinate:      tuple
                            (float, float) : lat, lon

    :param nodes:           dict
                            {id_node: (lat, lon)}

    :return:                tuple
                            (int, int)
                            Open Street Map ids of closest
                            adjacent nodes (id, id)
    """

    left, right, bottom, top = quadrants(coordinate, nodes)

    between_nodes = {}

    # True if the longitudinal variation is greater than the latitudinal variation
    horizontal_way = is_horizontal_way(list(nodes.values()))

    if horizontal_way:

        # if there is nodes in both sides (left and right)
        if len(left) > 0 and len(right) > 0:

            # closest node in the left side of coordinate
            first_closest = closest_node_id(coordinate, left)

            # closest node in the right side of coordinate
            second_closest = closest_node_id(coordinate, right)

        # if there is not nodes in left and/or right
        # and there is nodes in top and bottom sides
        elif len(top) > 0 and len(bottom) > 0:

            first_closest = closest_node_id(coordinate, top)
            second_closest = closest_node_id(coordinate, bottom)

        else:

            # if there is not node in one of the sides
            first_closest, second_closest = _nodes_around(coordinate)

    # if is not a horizontal way
    else:

        # if there is nodes on both sides (bottom and top)
        if len(top) > 0 and len(bottom) > 0:

            # closest node on the top side of coordinate
            first_closest = closest_node_id(coordinate, top)

            # closest node on the bottom side of coordinate
            second_closest = closest_node_id(coordinate, bottom)

        # if there is not nodes in top and/or bottom
        # and there is nodes in left and right sides
        elif len(left) > 0 and len(right) > 0:

            first_closest = closest_node_id(coordinate, left)
            second_closest = closest_node_id(coordinate, right)
        else:

            # if there is not node on one of the sides
            first_closest, second_closest = _nodes_around(coordinate)

    between_nodes.update(first_closest)
    between_nodes.update(second_closest)

    return between_nodes


def _nodes_around(coordinate):
    """
    This function is used when is not possible to get
    adjacent nodes on the same osm "way" of the input
    coordinate.

    :param coordinate:      tuple
                            (float, float) : lat, lon

    :return:                int, int
                            Open Street Map ids of closest
                            adjacent nodes around the input
                            coordinate(id, id)
    """

    coord = _string_coordinate(coordinate)
    flag = True
    limit = 0
    around_nodes = {}
    result_overpass = ''

    while flag:

        # meters around the coordinate to search nodes
        limit += 50

        # the query search nodes around the coordinate within the limit
        query_state = "node(around:" + str(limit) + ", " + coord + "); (._;>;); out;"
        result_overpass = Overpass.overpy_response(query_state)

        # if there is more than one node around the coordinate
        if len(result_overpass.nodes) > 1:
            flag = False

    for i in result_overpass.nodes:
        # update the dict with around nodes
        # around nodes dict = {id of the node: (lat, lon)}
        around_nodes.update([(float(i.id), (float(i.lat), float(i.lon)))])

    # get the first closest node from the coordinate
    first_closest = closest_node_id(coordinate, around_nodes)

    # remove the first closest node of the dict with all nodes
    around_nodes.pop(list(first_closest.keys())[0])

    # get the second closest node from the coordinate
    second_closest = closest_node_id(coordinate, around_nodes)
    return first_closest, second_closest


def adjacent_nodes(coordinate):
    """

    If the input coordinate is inside a Open Street Map
    (OSM) way and is not a node, this function finds the
    adjacent nodes of the input coordinate. If the input
    coordinate is a node, it returns the id of the node.

    :param coordinate:      tuple
                            (float, float) : lat, lon

    :return:                dict, geopy.location.Location

                            If the input coordinate is a
                            way:
                            It returns a dict with the id
                            of adjacent nodes as key, and
                            a tuple with the coordinate of
                            the node.

                            If the input coordinate is a
                            node:
                            It returns a int if the input
                            coordinate is a OSM node. The
                            int output corresponds the OSM id
                            of the node.

                            Also returns an object
                            geopy.location corresponding to
                            the input coordinate geolocation
                            data.

    """
    # string of the input coordinate
    coordinate_str = _string_coordinate(coordinate)

    # gets the Open Street Map (OSM)
    # information about the input coordinate
    location = _geolocator(coordinate_str, 'DS')

    if location is not None:

        # verifies the type of the location
        type_osm = _osm_type(location)

        # verifies the OSM id of the location
        id_osm = _id_osm(location)

        # if the type of location is a OSM way
        if type_osm == 'way':

            # get all nodes of the OSM way
            nodes = nodes_from_way_osm(id_osm)

            # get the adjacent nodes of the input coordinate
            nodes_between = _adjacent_nodes(coordinate, nodes)

            # returns a tuple with the ids of the adjacent nodes
            return nodes_between, location

        # if the type of location is a OSM node
        elif type_osm == 'node' or type_osm == 'relation':

            road = location.raw.get('address').get('road')
            city = location.raw.get('address').get('city')
            search = road + ',' + city
            geolocator = Nominatim(user_agent='DS')

            while True:
                try:
                    location_1 = geolocator.geocode(search)
                    osm_id = location_1.raw.get('osm_id')

                except:
                    time.sleep(30)
                    continue
                break

            # get all nodes of the OSM way
            nodes = nodes_from_way_osm(osm_id)

            # get the adjacent nodes of the input coordinate
            nodes_between = _adjacent_nodes(coordinate, nodes)

            # returns a tuple with the ids of the adjacent nodes
            return nodes_between, location_1

        elif type_osm == 'node':

            node_osm = {id_osm: (float(location.raw.get('lat')), float(location.raw.get('lon')))}

            # returns the id of the OSM node
            return node_osm, location

        # else:
            # print("Error: only Open Street Map \'way\' and \'nodes\' are supported.")

    else:
        return None, None


if __name__ == '__main__':
    coordinate = (-22.82504, -47.0773)
    # coordinate = (-24.992554, -47.069115)
    # for i in range(2):
    location = _geolocator(_string_coordinate(coordinate), 'Carri')
    type_osm = _osm_type(location)
    id_osm = _id_osm(location)
    nodes = nodes_from_way_osm(id_osm)
    closest_node_inside_edge = closest_node_id(coordinate, nodes)
    nodes_between = _adjacent_nodes(coordinate, nodes)
    print(nodes_between)
    """
    if location is not None:
        type_osm = _osm_type(location)
        id_osm = _id_osm(location)
        nodes = nodes_from_way_osm(id_osm)
        closest_node_inside_edge = closest_node_id(coordinate, nodes)
        nodes_between = _adjacent_nodes(coordinate, nodes)
        print(nodes_between)
    """
