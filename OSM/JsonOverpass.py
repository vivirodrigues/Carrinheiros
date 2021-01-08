import requests


class JsonFile:
    def __init__(self, query):
        self.overpass_url = "http://overpass-api.de/api/interpreter"
        self.json_osm = {}
        self.elements = ''
        self.overpass_query = query
        self.set_response()
        self.set_elements()

    def set_query(self, query):
        self.overpass_query = query

    def get_query(self):
        return self.overpass_query

    def set_response(self):
        response = requests.get(self.overpass_url, params={'data': self.overpass_query})
        data = response.json()
        self.json_osm = data

    def get_response(self):
        return self.json_osm

    def set_elements(self):
        elements = self.json_osm.get("elements")
        self.elements = elements

    def get_elements(self):
        return self.elements