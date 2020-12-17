import requests


class GetJsonOsm:
    def __init__(self):
        self.overpass_url = "http://overpass-api.de/api/interpreter"

    def get_json_osm(self, overpass_query):
        response = requests.get(self.overpass_url, params={'data': overpass_query})
        data = response.json()
        return data
