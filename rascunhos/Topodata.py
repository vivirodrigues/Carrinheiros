def set_lon(lon, longitudes):
    # it is defined according to the topodata model in Brazil
    # http://www.webmapit.com.br/inpe/topodata/

    if int(lon) not in longitudes:
        lon += 1
        return str(int(lon)) + '_'
    elif int(lon) in longitudes and int(lon) % 3 == 0:
        lon += 1
        return str(int(lon)) + '5'
    else:
        if lon > int(lon) + 0.5:
            lon += 2
            return str(int(lon)) + '_'

    return str(int(lon)) + '5'


class Topodata:
    def __init__(self, osm_coordinates):
        self.coordinates_osm = osm_coordinates
        self.hemisphere_min_lat = ''
        self.hemisphere_max_lat = ''
        self.min_lat = float('inf')
        self.min_lon = float('inf')
        self.max_lat = float('-inf')
        self.max_lon = float('-inf')
        self.data_type = 'ZN'  # altitude
        self.name = []
        # longitudes is defined according to the topodata model in Brazil
        self.longitudes = (75, 73, 72, 70, 69, 67, 66, 64, 63,
                           61, 60, 58, 57, 55, 54, 52, 51, 49,
                           48, 46, 45, 43, 42, 40, 39, 37, 36)
        self.main()

    def set_hemisphere(self):
        # it defines the hemisphere from latitude
        if self.coordinates_osm[1] > 0:  # min_max
            self.hemisphere_min_lat = 'N'  # North
        else:
            self.hemisphere_min_lat = 'S'  # South

        if self.coordinates_osm[3] > 0:  # max_lat
            self.hemisphere_max_lat = 'N'  # North
        else:
            self.hemisphere_max_lat = 'S'  # South

    def set_lat_min(self):
        self.min_lat = str(abs(int(self.coordinates_osm[1])))

    def set_lat_max(self):
        self.max_lat = str(abs(int(self.coordinates_osm[3])))

    def set_lon_min(self):
        self.min_lon = set_lon(abs(self.coordinates_osm[0]), self.longitudes)

    def set_lon_max(self):
        self.max_lon = set_lon(abs(self.coordinates_osm[2]), self.longitudes)

    def set_file_names(self):
        ###
        # topodata file name: Latitude_min (left) + Hemisphere (S or N) + Longitude

        if self.max_lat == self.min_lat and self.max_lon == self.min_lon:
            name = str(self.max_lat) + self.hemisphere_max_lat + str(self.max_lon) + self.data_type
            self.name.append(name)
        elif self.max_lon == self.min_lon or self.max_lat == self.min_lat:
            # 2 geotiff files with same longitude or same longitude
            name_1 = str(self.min_lat) + self.hemisphere_min_lat + str(self.min_lon) + self.data_type
            name_2 = str(self.max_lat) + self.hemisphere_max_lat + str(self.max_lon) + self.data_type
            self.name = [name_1, name_2]
        else:
            # 4 geotiffs
            name_1 = str(self.min_lat) + self.hemisphere_min_lat + str(self.min_lon) + self.data_type
            name_2 = str(self.min_lat) + self.hemisphere_max_lat + str(self.max_lon) + self.data_type
            name_3 = str(self.max_lat) + self.hemisphere_max_lat + str(self.min_lon) + self.data_type
            name_4 = str(self.max_lat) + self.hemisphere_max_lat + str(self.max_lon) + self.data_type
            self.name = [name_1, name_2, name_3, name_4]

    def get_file_names(self):
        return self.name

    def main(self):
        self.set_lat_min()
        self.set_lat_max()
        self.set_lon_min()
        self.set_lon_max()
        self.set_hemisphere()
        self.set_file_names()


if __name__ == '__main__':
    # min_lon, min_lat, max_lon, max_lat
    coordinates = [-47.087718, -22.823953, -47.074891, -22.816008]
    #Topodata(coordinates)
    print(Topodata(coordinates).get_file_names())
