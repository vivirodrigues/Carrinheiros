def set_areas(self):
    state_name = 'São Paulo'
    city = 'Campinas'
    result = self.api.query(
        "node[name=\"" + city + "\"][\"is_in:state\"~\"" + state_name + "\"];foreach(out;is_in;out;);")
    return result.area_ids


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
