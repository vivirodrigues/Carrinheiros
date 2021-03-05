def _set_longitude(longitude):
    longitudes = (75, 73, 72, 70, 69, 67, 66, 64, 63,
                  61, 60, 58, 57, 55, 54, 52, 51, 49,
                  48, 46, 45, 43, 42, 40, 39, 37, 36)

    # it is defined according to the topodata model in Brazil
    # http://www.webmapit.com.br/inpe/topodata/

    if int(longitude) not in longitudes:
        longitude += 1
        return str(int(longitude)) + '_'
    elif int(longitude) in longitudes and int(longitude) % 3 == 0:
        longitude += 1
        return str(int(longitude)) + '5'
    else:
        if longitude > int(longitude) + 0.5:
            longitude += 2
            return str(int(longitude)) + '_'

    return str(int(longitude)) + '5'


def _hemisphere(latitude):
    """
    This function defines the hemisphere from latitude

    :param latitude:    float

    :return:            String
                        'S' is South
                        'N' is North
    """
    #
    if latitude > 0:  # min_max
        hemisphere_lat = 'N'  # North
    else:
        hemisphere_lat = 'S'  # South

    hemisphere = hemisphere_lat

    return hemisphere


def hemisphere_max_min(osm_coordinates):
    """
    Returns the hemispheres of the maximum and minimum
    latitudes of the bbox.

    :param osm_coordinates:     list
                                list with float values of coordinates
                                min_lon, min_lat, max_lon, max_lat

    :return:                    String, String
                                minimum latitude hemisphere,
                                maximum latitude hemisphere
    """

    min_lat = osm_coordinates[1]
    max_lat = osm_coordinates[3]

    hemisphere_min_lat = _hemisphere(min_lat)
    hemisphere_max_lat = _hemisphere(max_lat)

    return hemisphere_min_lat, hemisphere_max_lat


def file_names_topodata(coordinates_osm):
    """
    This function returns the Topodata file(s) according to
    Open Street Map (OSM) coordinates of a bounding box (bbox).
    The model of topodata file name is:
    Minimum latitude (left) + Hemisphere ('S' or 'N') + Longitude

    :param coordinates_osm:     list
                                list with float values of coordinates
                                min_lon, min_lat, max_lon, max_lat
    :return:
    """

    # Transforms the float values within the list of input
    # coordinates into integers, then, strings.

    # Latitude must be the string of integer positive
    # (number rounding)
    min_lat = abs(int(coordinates_osm[1]))
    max_lat = abs(int(coordinates_osm[3]))

    # Longitudes are adapted according to the
    # Topodata data model: http://www.dsr.inpe.br/topodata/
    min_lon = _set_longitude(abs(coordinates_osm[0]))
    max_lon = _set_longitude(abs(coordinates_osm[2]))

    # the data type of altitude files in Topodata is 'ZN'
    data_type = 'ZN'

    hemisphere_min_lat, hemisphere_max_lat = hemisphere_max_min(coordinates_osm)

    # 1 GeoTiff file: same longitude and same latitude
    if max_lat == min_lat and max_lon == min_lon:
        # name = str(max_lat) + hemisphere_max_lat + str(max_lon) + data_type
        name = "{:02d}".format(max_lat) + hemisphere_max_lat + str(max_lon) + data_type
        return [name]

    # 2 GeoTiff files: same longitude or same latitude
    elif max_lon == min_lon or max_lat == min_lat:
        name_1 = "{:02d}".format(min_lat) + hemisphere_min_lat + str(min_lon) + data_type
        name_2 = "{:02d}".format(max_lat) + hemisphere_max_lat + str(max_lon) + data_type
        return [name_1, name_2]

    # 4 GeoTiffs files: different longitudes and latitudes
    else:
        name_1 = "{:02d}".format(min_lat) + hemisphere_min_lat + str(min_lon) + data_type
        name_2 = "{:02d}".format(min_lat) + hemisphere_max_lat + str(max_lon) + data_type
        name_3 = "{:02d}".format(max_lat) + hemisphere_max_lat + str(min_lon) + data_type
        name_4 = "{:02d}".format(max_lat) + hemisphere_max_lat + str(max_lon) + data_type
        return [name_1, name_2, name_3, name_4]


if __name__ == '__main__':
    # min_lon, min_lat, max_lon, max_lat
    coordinates = [-47.087718, -22.823953, -47.074891, -22.816008]
    print(file_names_topodata(coordinates))
