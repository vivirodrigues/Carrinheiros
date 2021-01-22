class Coordinates:
    ###
    # It defines the minimum and maximum latitudes and longitudes of a coordinates list
    # The resulting coordinates can be used to make a scenery rectangle
    # The scenery rectangle can be downloaded in osm
    ###
    def __init__(self, coordinates_vector):
        self.vector = coordinates_vector  # a list of tuples with coordinates (stop_points)
        self.limit = 0.02 # margin in the scenario rectangle area
        self.coordinates = ''
        self.coordinates_list = []
        self.min_lat = float('inf')
        self.min_lon = float('inf')
        self.max_lat = float('-inf')
        self.max_lon = float('-inf')
        self.main()

    def set_min_lat(self):
        self.min_lat = min(self.vector, key=lambda t: t[0])[0]

    def get_min_lat(self):
        return self.min_lat

    def set_min_lon(self):
        self.min_lon = min(self.vector, key=lambda t: t[1])[1]

    def get_min_lon(self):
        return self.min_lon

    def set_max_lon(self):
        self.max_lon = max(self.vector, key=lambda t: t[1])[1]

    def get_max_lon(self):
        return self.max_lon

    def set_max_lat(self):
        self.max_lat = max(self.vector, key=lambda t: t[0])[0]

    def get_max_lat(self):
        return self.max_lat

    def set_coordinates(self):
        # it transforms the list of rectangle area in string
        # min_lon, min_lat, max_lon, max_lat
        self.coordinates_list = [self.min_lon, self.min_lat, self.max_lon, self.max_lat]
        new_coordinates = str(self.coordinates_list[0])
        for i, item in enumerate(self.coordinates_list[1:]):
            new_coordinates += ",{0}".format(str(item))
        self.coordinates = new_coordinates

    def get_coordinates(self):
        return self.coordinates

    def get_coordinates_list(self):
        return self.coordinates_list

    def set_limits(self):
        # add a margin in the scenario rectangle area
        self.min_lat -= self.limit
        self.min_lon -= self.limit
        self.max_lon += self.limit
        self.max_lat += self.limit

    def main(self):
        self.set_min_lat()
        self.set_min_lon()
        self.set_max_lat()
        self.set_max_lon()
        self.set_limits()
        self.set_coordinates()


if __name__ == "__main__":
    coordinates = Coordinates(
        [(-22.816008, -47.075614, 606.0), (-22.816639, -47.074891, 602.0), (-22.818317, -47.083415, 602.0),
         (-22.820244, -47.085422, 602.0), (-22.823953, -47.087718, 602.0), (-22.816008, -47.075614, 606.0)])
    # -47.087718,-22.823953,-47.074891,-22.816008
    print("Coordinates:", coordinates.get_coordinates())
