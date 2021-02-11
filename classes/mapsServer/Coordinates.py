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


def _add_margin(coordinates_list, margin_value_coordinate=0.02):
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
    # margin in the scenario rectangle area
    # add a margin in the scenario rectangle area
    coordinates_list[0] -= margin_value_coordinate
    coordinates_list[1] -= margin_value_coordinate
    coordinates_list[2] += margin_value_coordinate
    coordinates_list[3] += margin_value_coordinate
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


def coordinates_list_bbox(coordinates, margin_value_coordinate=0.02):
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


if __name__ == "__main__":
    coordinates = ([(-22.816008, -47.075614, 606.0),
                    (-22.816639, -47.074891, 602.0),
                    (-22.818317, -47.083415, 602.0),
                    (-22.820244, -47.085422, 602.0),
                    (-22.823953, -47.087718, 602.0),
                    (-22.816008, -47.075614, 606.0)])
    # -47.087718,-22.823953,-47.074891,-22.816008
    # -47.246313,-23.0612161,-47.239999,-23.0609999
    test = coordinates_list_bbox(coordinates)
    print("Coordinates:", test)
    print("string", coordinates_string(test))
