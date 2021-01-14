import overpy


class Overpass:
    # it connects with Overpass API based on the input query
    def __init__(self, query):
        self.api = overpy.Overpass()
        self.query = query
        self.response = ''
        self.set_response()

    def set_query(self, query):
        self.query = query

    def get_query(self):
        return self.query

    def set_response(self):
        response = self.api.query(self.query)
        self.response = response

    def get_response(self):
        # returns the response from Overpass API based on the input query
        return self.response
