import requests
import overpy


def elements_json_overpass(overpass_query):
    """
    This function gets the response of the Overpass
    API according to a query. It returns a json. It
    must be used when the overpy can not get specific
    elements from API response. Example: bound limits
    of a way from Open Street Map.

    :param overpass_query:      String

    :return:                    list
    """
    overpass_url = "http://overpass-api.de/api/interpreter"
    response = requests.get(overpass_url, params={'data': overpass_query})
    data = response.json()
    elements = data.get("elements")
    return elements


def overpy_response(overpy_query):
    """
    This function gets the response of the Python Overpass
    API, called Overpy, according to a query.

    Overpy documentation:
    https://python-overpy.readthedocs.io/en/latest/index.html

    :param overpy_query:        String

    :return:                    Overpy object
    """
    api = overpy.Overpass()
    response = api.query(overpy_query)
    return response


if __name__ == "__main__":
    overpass_query = "[out:json];is_in(-22.816008, -47.075614); out geom qt;"
    print("query: ", overpass_query)
    json_osm = elements_json_overpass(overpass_query)
    print(type(json_osm))

    iso = 'SP-BR'
    query_state = "relation['ISO3166-2'='" + iso + "']; (._;>;); out ids;"
    result_overpy = overpy_response(query_state)
    print(type(result_overpy))