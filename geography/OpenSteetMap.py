from geography import Download, Coordinates, Overpass


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
    :param osm_relation:
    :return:
    """

    iso = define_iso(search_coordinate)
    query_state = "relation['ISO3166-2'='" + iso + "']; (._;>;); out ids;"
    result_overpy = Overpass.overpy_response(query_state)
    id_area = result_overpy.relations[0].id + osm_relation
    return id_area


def _search_coordinate(coordinates_list):
    # it is used in queries to search overpass
    osm_lat = coordinates_list[0]
    osm_lon = coordinates_list[0]
    search_coordinate = (osm_lat, osm_lon)
    return search_coordinate


def _osm(coordinates_osm, directory, file_name):
    # it checks if file exists
    try:
        with open(directory + file_name, 'r') as f:
            scenario_osm = f.read()
            print("file exists")
    except IOError:
        print(directory + file_name)
        download_file = Download.download_osm(coordinates_osm, file_name, directory)
        _osm(coordinates_osm, file_name, directory)


def file_osm(directory, file_name, coordinates_stop_points):

    coordinates_list = Coordinates.coordinates_list_bbox(coordinates_stop_points)
    coordinates_osm = Coordinates.coordinates_string(coordinates_list)
    _osm(coordinates_osm, directory, file_name)


if __name__ == "__main__":
    coordinates_path = [(-22.816008, -47.075614), (-22.816639, -47.074891),
                        (-22.818317, -47.083415), (-22.820244, -47.085422),
                        (-22.816008, -47.075614), (-22.823953, -47.087718)]
    dir_osm = '../data/maps/'
    file_osm(dir_osm, 'map.osm', coordinates_path)