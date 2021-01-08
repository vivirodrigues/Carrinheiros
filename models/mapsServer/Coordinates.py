# import Json


class Coordinates:
    def __init__(self, coordinates_vector):
        self.vector = coordinates_vector
        self.limit = 0.1
        self.coordinates = ''
        self.min_lat = float('inf')
        self.min_lon = float('inf')
        self.max_lat = float('-inf')
        self.max_lon = float('-inf')
        self.set_min_lat()
        self.set_min_lon()
        self.set_max_lat()
        self.set_max_lon()
        self.set_limits()
        self.set_coordinates()

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
        coordinates_osm = [self.min_lon, self.min_lat, self.max_lon, self.max_lat]
        new_coordinates = str(coordinates_osm[0])
        for i, item in enumerate(coordinates_osm[1:]):
            new_coordinates += ",{0}".format(str(item))
        self.coordinates = new_coordinates

    def get_coordinates(self):
        return self.coordinates

    def set_limits(self):
        self.min_lat -= 0.02
        self.min_lon -= 0.02
        self.max_lon += 0.02
        self.max_lat += 0.02


if __name__ == "__main__":
    coordinates = Coordinates([(-22.816008, -47.075614, 0), (-22.816639, -47.074891, 0), (-22.818317, -47.083415, 0), (-22.820244, -47.085422, 0), (-22.823953, -47.087718, 0)])
    coordinates = Coordinates([(-22.816008, -47.075614, 606.0), (-22.816639, -47.074891, 602.0), (-22.818317, -47.083415, 602.0), (-22.820244, -47.085422, 602.0), [], (-22.823953, -47.087718, 602.0)])
    # -47.087718,-22.823953,-47.074891,-22.816008
    print("Coordinates:", coordinates.get_coordinates())
