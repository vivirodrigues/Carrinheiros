from general import Json


class User:

    def __init__(self, json):
        self.json = json
        self.id = ''
        self.type = ''
        self.name = ''
        self.email = ''
        self.interest = ''
        self.attended_ads = []
        self.coordinates = ()
        self.coordinates_depot = ()
        self.lat = ''
        self.lon = ''
        self.lat_depot = ''
        self.lon_depot = ''
        self.main()

    def set_id(self):
        # user id
        self.id = self.json.get("id")

    def set_type(self):
        ###
        # the user can be a waste collector, artisan or anyone who wants to participate
        # Strings: ("collector, "artisan", "collaborator")
        ###
        self.type = self.json.get("type")

    def set_name(self):
        # full name
        self.name = self.json.get("name")

    def set_email(self):
        self.email = self.json.get("email")

    def set_interest(self):
        ###
        # the interest can be in materials dispose, collect or both
        # Strings : ("dispose", "collect", "both")
        ###
        self.interest = self.json.get("interest")

    def set_attended_ads(self):
        ###
        # list of attended advertisements by the user
        ###
        self.attended_ads = self.json.get("attended_ads")

    def set_coordinates(self):
        ###
        # a list with user instant geographic coordinates
        # list -> tuple (latitude, longitude)
        ###
        self.coordinates = tuple(self.json.get("coordinates"))

    def set_coordinates_depot(self):
        ###
        # a list with waste depot geographic coordinates
        # list -> tuple (latitude, longitude)
        ###
        self.coordinates_depot = tuple(self.json.get("coordinates_depot"))

    def set_lat(self):
        self.lat = self.json.get("latitude")

    def set_lon(self):
        self.lon = self.json.get("longitude")

    def set_lat_depot(self):
        self.lat_depot = self.json.get("latitude_depot")

    def set_lon_depot(self):
        self.lon_depot = self.json.get("longitude_depot")

    def get_id(self):
        return self.id

    def get_type(self):
        return self.type

    def get_name(self):
        return self.name

    def get_email(self):
        return self.email

    def get_interest(self):
        return self.interest

    def get_attended_ads(self):
        return self.attended_ads

    def get_coordinates(self):
        return self.coordinates

    def get_coordinates_depot(self):
        return self.coordinates_depot

    def get_lat(self):
        return self.lat

    def get_lon(self):
        return self.lon

    def get_lat_depot(self):
        return self.lat_depot

    def get_lon_depot(self):
        return self.lon_depot

    def main(self):
        self.set_id()
        self.set_type()
        self.set_name()
        self.set_email()
        self.set_interest()
        self.set_attended_ads()
        self.set_coordinates()
        self.set_coordinates_depot()
        self.set_lat()
        self.set_lon()
        self.set_lat_depot()
        self.set_lon_depot()


def get_user(user_id, directory_json):
    file_name = get_file_user(user_id)
    json = Json.json_content(directory_json, file_name)
    user = User(json)
    return user


def get_file_user(user_id):
    file_name = "User" + str(user_id)
    return file_name


if __name__ == '__main__':
    id_user = "000"
    file = "User" + id_user
    json_user = Json.json_content('../data/DB/', file)
    carrinheiro = User(json_user)
    print("Test with user:", carrinheiro.get_type())
    #################################################
    directory_file_json = '../data/DB/'
    user_new = get_user(id_user, directory_file_json)
    print("Test 2", user_new.get_coordinates())
