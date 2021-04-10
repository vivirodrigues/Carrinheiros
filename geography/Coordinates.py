import haversine as hs
import osmnx as ox


def min_latitude(coordinates):
    """
    This function returns the minimum value of latitude
    of a list with tuples [(lat, lon), (lat, lon)].

    :param coordinates:     list
                            list with tuples. Each tuple
                            has coordinates float values.
                            [(lat, lon), (lat, lon)]
                            Ex:
                            [(-00.00, -00.00), (00.00, 00.00)]

    :return:                float
                            minimum latitude value
    """
    min_lat = min(coordinates, key=lambda t: t[0])[0]
    return min_lat


def min_longitude(coordinates):
    """
    This function returns the minimum value of longitude
    of a list with tuples [(lat, lon), (lat, lon)].

    :param coordinates:     list
                            list with tuples. Each tuple
                            has coordinates float values.
                            [(lat, lon), (lat, lon)]
                            Ex:
                            [(-00.00, -00.00), (00.00, 00.00)]

    :return:                float
                            minimum longitude value
    """
    min_lon = min(coordinates, key=lambda t: t[1])[1]
    return min_lon


def max_longitude(coordinates):
    """
    This function returns the maximum value of longitude
    of a list with tuples [(lat, lon), (lat, lon)].

    :param coordinates:     list
                            list with tuples. Each tuple
                            has coordinates float values.
                            [(lat, lon), (lat, lon)]
                            Ex:
                            [(-00.00, -00.00), (00.00, 00.00)]

    :return:                maximum longitude value
    """
    max_lon = max(coordinates, key=lambda t: t[1])[1]
    return max_lon


def max_latitude(coordinates):
    """
    This function returns the maximum value of latitude
    of a list with tuples [(lat, lon), (lat, lon)].

    :param coordinates:     list
                            list with tuples. Each tuple
                            has coordinates float values.
                            [(lat, lon), (lat, lon)]
                            Ex:
                            [(-00.00, -00.00), (00.00, 00.00)]

    :return:                maximum latitude value
    """
    max_lat = max(coordinates, key=lambda t: t[0])[0]
    return max_lat


def _add_margin(coordinates_list, margin_value_coordinate=0.01):
    """
    This function add a margin in the bound box (bbox) according to
    coordinate margin value.

    :param coordinates_list:        list
                                    the list has float coordinate values
                                    in this order:
                                    [min_lon, min_lat, max_lon, max_lat]

    :param margin_value_coordinate: float
                                    this value will be added to each
                                    coordinate to create a margin

    :return:                        list
                                    the list has float coordinate values
                                    with margin, in this order:
                                    [min_lon, min_lat, max_lon, max_lat]
    """

    base = hs.haversine((coordinates_list[1], coordinates_list[0]), (coordinates_list[3], coordinates_list[0]))
    altura = hs.haversine((coordinates_list[1], coordinates_list[0]), (coordinates_list[1], coordinates_list[2]))
    area_original = base * altura

    # margin in the scenario rectangle area
    # add a margin in the scenario rectangle area
    coordinates_list[0] -= margin_value_coordinate
    coordinates_list[1] -= margin_value_coordinate
    coordinates_list[2] += margin_value_coordinate
    coordinates_list[3] += margin_value_coordinate

    base = hs.haversine((coordinates_list[1], coordinates_list[0]), (coordinates_list[3], coordinates_list[0]))
    altura = hs.haversine((coordinates_list[1], coordinates_list[0]), (coordinates_list[1], coordinates_list[2]))
    area_nova = base * altura
    print("Área adicionada", area_nova - area_original)

    return coordinates_list


def coordinates_string(coordinates_list):
    """
    This function transforms the list of coordinates to string.

    :param coordinates_list:    list
                                the list has float coordinate values
                                in this order:
                                [min_lon, min_lat, max_lon, max_lat]

    :return:                    String
                                "min_lon, min_lat, max_lon, max_lat"
    """
    string_coordinates = str(coordinates_list[0])
    for i, item in enumerate(coordinates_list[1:]):
        string_coordinates += ",{0}".format(str(item))
    return string_coordinates


def coordinates_list_bbox(coordinates, margin_value_coordinate=0.01):
    """
    This function transforms a list with geographic points in a list
    of bound box (bbox). The list contains the minimum longitude and
    latitude, and the maximum longitude and latitude. The order of
    elements is: [min_lon, min_lat, max_lon, max_lat].

    Besides, this function adds a margin in the bound box (bbox),
    according to coordinate margin value.

    :param coordinates:                 list
                                        list with tuples. Each tuple
                                        has coordinates float values.
                                        [(lat, lon), (lat, lon)]
                                        Ex:
                                        [(-00.00, -00.00), (00.00, 00.00)]

    :param margin_value_coordinate:     float
                                        this value will be added to each
                                        coordinate to create a margin

    :return:                            list
                                        the list has float coordinate values
                                        with margin, in this order:
                                        [min_lon, min_lat, max_lon, max_lat]
    """
    min_lon = min_longitude(coordinates)
    min_lat = min_latitude(coordinates)
    max_lon = max_longitude(coordinates)
    max_lat = max_latitude(coordinates)
    # it transforms the list of rectangle area in string

    # min_lon, min_lat, max_lon, max_lat
    coordinates_list = [min_lon, min_lat, max_lon, max_lat]
    coordinates_list = _add_margin(coordinates_list, margin_value_coordinate)

    return coordinates_list


def create_osmnx(coordinates, margin_value_coordinate = 0.01):
    max_lon = max_longitude(coordinates) + margin_value_coordinate
    min_lon = min_longitude(coordinates) - margin_value_coordinate
    max_lat = max_latitude(coordinates) + margin_value_coordinate
    min_lat = min_latitude(coordinates) - margin_value_coordinate

    osmnx_list = [max_lat, min_lat, max_lon, min_lon]

    return osmnx_list[0], osmnx_list[1], osmnx_list[2], osmnx_list[3]


def add_m(coordinate):
    if coordinate < 0:
        new_coord = 'm' + str(abs(coordinate))
    else:
        new_coord = str(abs(coordinate))
    return new_coord


def def_file_name(coordinates_list):

    n1 = add_m(coordinates_list[0])
    n2 = add_m(coordinates_list[1])
    n3 = add_m(coordinates_list[2])
    n4 = add_m(coordinates_list[3])

    name = n1 + '_' + n2 + '_' + n3 + '_' + n4

    return name


if __name__ == "__main__":
    coordinates = ([(-1.4669727715675633, -48.47476438242888),
                    (-1.4617914926718831, -48.48735602308006),
                    (-1.4552257213149151, -48.476854602085865),
                    (-1.4570295065392669, -48.46451272534284),
                    (-1.473840715457675, -48.4597131060169)])
    # -47.087718,-22.823953,-47.074891,-22.816008
    # -47.087718,-22.823953,-47.074891,-22.816008
    # -47.246313,-23.0612161,-47.239999,-23.0609999
    test = coordinates_list_bbox(coordinates)
    a, b, c , d = create_osmnx(coordinates)
    G = ox.graph_from_bbox(a, b, c, d, network_type='all')
    fig, ax = ox.plot_graph(G)
    print("Coordinates:", test)
    print("string", coordinates_string(test))
