import overpy
from OSM import GetJsonOSM
import json


class OsmDownload:
    def __init__(self, city, state):
        self.api = overpy.Overpass()
        self.latMin = 0.0
        self.lonMin = 0.0
        self.latMax = 0.0
        self.lonMax = 0.0
        self.id_state_area = 0.0
        self.areas = []
        self.city = city
        self.state = state
        self.state_name = 'São Paulo'
        self.country = 'BR'
        self.get_dict_osm = GetJsonOSM.GetJsonOsm()
        self.main()

    def set_areas(self):
        result = self.api.query(
            "node[name=\"" + self.city + "\"][\"is_in:state\"~\"" + self.state_name + "\"];foreach(out;is_in;out;);")
        self.areas = result.area_ids

    def set_state_area(self):
        iso = self.country + '-' + self.state
        # OSM pattern : 3600000000 for relation, 2400000000 for way
        query_state = "relation['ISO3166-2'='" + iso + "']; (._;>;); out ids;"
        result = self.api.query(query_state)
        value_osm_relation = 3600000000
        self.id_state_area = result.relations[0].id + value_osm_relation

    def set_coordinates(self):
        result = self.api.query(
            "[out:json]; relation[\'type\' = \'boundary\']"
            + "[\'boundary\' = \'administrative\']"
            + "[\'name\' = \'" + self.city + "\'](area:" + str(self.id_state_area) + ");"
            + "way(r);"
            + "(._; >;); out geom qt;")
        for way in result.ways:
            nodes = way.get_nodes(resolve_missing=True)
            self.latMin = nodes[0].lat
            self.latMax = nodes[-1].lat
            self.lonMax = nodes[0].lon
            self.lonMin = nodes[-1].lon
        print(result.ways[0])
        print(self.lonMin)

    def main(self):
        self.set_state_area()
        # self.set_coordinates()
        overpass_query = "[out:json];" \
                         "relation['type'='boundary']['boundary'='administrative']['name'=" + self.city + "]" \
                         "(area:" + str(self.id_state_area) + ");way(r);(._;>;);out geom qt;"
        result = self.get_dict_osm.get_json_osm(overpass_query)
        print(result)


if __name__ == "__main__":
    OsmDownload("Campinas", "SP")
