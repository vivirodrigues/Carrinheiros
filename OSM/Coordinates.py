import JsonFile


class Coordinates:
    def __init__(self, city, id_state_area):
        self.city = city
        self.id_state_area = id_state_area
        self.response_json = {}
        self.coordinates = ''
        self.min_lat = float('inf')
        self.min_lon = float('inf')
        self.max_lat = float('-inf')
        self.max_lon = float('-inf')
        self.main()

    def set_response_json(self):
        overpass_query = "[out:json];" \
                         "relation['type'='boundary']['boundary'='administrative']['name'=" + self.city + "]" \
                         "(area:" + str(self.id_state_area) + ");way(r);(._;>;);out geom qt;"
        json_osm = JsonFile.JsonFile(overpass_query)
        self.response_json = json_osm.get_elements()

    def get_response_json(self):
        return self.response_json

    def set_min_lat(self):
        lat = []
        for i in self.response_json:
            if i.get("type") == "way":
                bounds = i.get("bounds")
                lat.append(bounds.get('minlat'))
        self.min_lat = min(lat)

    def get_min_lat(self):
        return self.min_lat

    def set_min_lon(self):
        lon = []
        for i in self.response_json:
            if i.get("type") == "way":
                bounds = i.get("bounds")
                lon.append(bounds.get('minlon'))
        self.min_lon = min(lon)

    def get_min_lon(self):
        return self.min_lon

    def set_max_lon(self):
        lon = []
        for i in self.response_json:
            if i.get("type") == "way":
                bounds = i.get("bounds")
                lon.append(bounds.get('maxlon'))
        self.max_lon = max(lon)

    def get_max_lon(self):
        return self.max_lon

    def set_max_lat(self):
        lat = []
        for i in self.response_json:
            if i.get("type") == "way":
                bounds = i.get("bounds")
                lat.append(bounds.get('maxlat'))
        self.max_lat = max(lat)

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

    def main(self):
        self.set_response_json()
        self.set_min_lat()
        self.set_min_lon()
        self.set_max_lat()
        self.set_max_lon()
        self.set_coordinates()


if __name__ == "__main__":
    coordinates = Coordinates("Campinas", "3600298204")
    print("Coordinates:", coordinates.get_coordinates())
