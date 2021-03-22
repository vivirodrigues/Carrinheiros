from geography import Download, Coordinates, Overpass
from general import Saves
from Constants import *


def define_iso(search_coordinate):
    """
    This function returns a ISO of a place.
    It is used when you want to download a complete city,
    for example. ISO is a string formed by the values
    country + '-' + state
    example : 'BR-SP'

    :param search_coordinate:   tuple
                                The tuple must have the lat, lon
                                of a geographic point. It can be
                                done by _search_coordinate function.
                                Order of coordinates: (lat, lon)

    :return:                    String
                                country + '-' + state
    """

    overpass_query = "[out:json];is_in" + str(search_coordinate) + "; out geom qt; "
    elements_osm = Overpass.elements_json_overpass(overpass_query)
    iso = ''
    for i in elements_osm:
        tags = i.get("tags")
        if tags.get("ISO3166-2") is not None:
            iso = tags.get("ISO3166-2")
    return iso


def id_state_area(search_coordinate, osm_relation):
    """
    This function returns a state code.
    It is used when you want to download a complete city,
    for example.

    In Open Street Map, the OSM relation values must be:
    3600000000 for relation, 2400000000 for way

    :param search_coordinate:   tuple
                                (lat, lon)

    :param osm_relation:        int
                                3600000000 or 2400000000

    :return:                    int
                                The Open Street Map id of the
                                area which contains the input
                                search coordinate
    """

    # Country - State. Ex: 'BR-SP'
    iso = define_iso(search_coordinate)
    query_state = "relation['ISO3166-2'='" + iso + "']; (._;>;); out ids;"
    result_overpy = Overpass.overpy_response(query_state)
    id_area = result_overpy.relations[0].id + osm_relation
    return id_area


def _search_coordinate(coordinates_list):
    """
    This function gets a coordinate from a list to be used
    on searches of Open Street Map API.

    :param coordinates_list:    list
                                the list has float coordinate values
                                in this order:
                                [min_lon, min_lat, max_lon, max_lat]

    :return:                    tuple
                                The tuple must have the coordinates
                                Format: (lat, lon)
                                (lat, lon)
    """
    # it is used in queries to search overpass
    osm_lat = coordinates_list[1]
    osm_lon = coordinates_list[0]
    search_coordinate = (osm_lat, osm_lon)
    return search_coordinate


def _osm(coordinates_osm, file_name):
    """
    This function checks if a Open Street Map '.osm' file
    exists in a directory. If it not exists, this function
    downloads the file.

    :param coordinates_osm:         string
                                    the string has coordinate values
                                    in this order:
                                    min_lon, min_lat, max_lon, max_lat

    :param file_name:               String
    """

    # it checks if file exists
    try:
        with open(file_name, 'r') as f:
            scenario_osm = f.read()
            print("file exists")
    except IOError:
        print(file_name)
        download_file = Download.download_osm(coordinates_osm, file_name)
        _osm(coordinates_osm, file_name)


def file_osm(directory, coordinates_points):
    """
    This function gets a list with tuples corresponding a geographic
    points. Each tuple has the coordinates (lat, lon) of the point.
    Then, it creates a bounding box which contain all coordinates
    inside. Besides, it checks if exists a Open Street Map '.osm' file
    in a directory. If it not exists, this function
    downloads the file.

    :param file_name:                       String

    :param coordinates_points:              list
                                            the list contains tuples.
                                            Each tuple has the latitude
                                            and the longitude corresponding
                                            to the geographic point.
                                            [(lat, lon)]
    :return:
    """

    coordinates_list = Coordinates.coordinates_list_bbox(coordinates_points, margin_value_coordinate=0.0)
    file_name = directory + Coordinates.def_file_name(coordinates_list) + '.osm'

    file = Saves.verify_file_exists(coordinates_list, file_name)
    if file is not False:
        print("OSM exists in ", file)
        return MAPS_DIRECTORY + file

    coordinates_list = Coordinates.coordinates_list_bbox(coordinates_points)
    coordinates_osm = Coordinates.coordinates_string(coordinates_list)
    file_name = directory + Coordinates.def_file_name(coordinates_list) + '.osm'

    # it just download a new osm file if does not exists a file with
    # the current coordinates
    _osm(coordinates_osm, file_name)
    return file_name


if __name__ == "__main__":
    coordinates_path = [(-22.816008, -47.075614), (-22.816639, -47.074891),
                        (-22.818317, -47.083415), (-22.820244, -47.085422),
                        (-22.816008, -47.07614), (-22.823953, -47.086718)]
    dir_osm = '../data/maps/'
    file_osm(dir_osm, coordinates_path)

    #coordinates_list = Coordinates.coordinates_list_bbox(coordinates_path)
    #search_coord = _search_coordinate(coordinates_list)
    #id_area = id_state_area(search_coord, 3600000000)
    #print(id_area)