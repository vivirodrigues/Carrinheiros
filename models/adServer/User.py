try:
    from models.adServer import JsonDB
except:
    pass


class User:

    def __init__(self, json):
        self.json = json
        self.id = ''
        self.lat = ''
        self.lon = ''
        self.alt = ''
        self.name = ''
        self.email = ''
        self.orders_fulfilled = []
        self.lat_depot = ''
        self.lon_depot = ''
        self.alt_depot = ''
        self.main()

    def set_id(self):
        self.id = self.json.get("id")

    def set_lat(self):
        self.lat = self.json.get("latitude")

    def set_lon(self):
        self.lon = self.json.get("longitude")

    def set_alt(self):
        self.alt = self.json.get("altitude")

    def set_lat_depot(self):
        self.lat_depot = self.json.get("latitude_depot")

    def set_lon_depot(self):
        self.lon_depot = self.json.get("longitude_depot")

    def set_alt_depot(self):
        self.alt_depot = self.json.get("altitude_depot")

    def set_name(self):
        self.name = self.json.get("name")

    def set_email(self):
        self.email = self.json.get("email")

    def set_orders(self):
        self.orders_fulfilled = self.json.get("orders_fulfilled")

    def get_lat(self):
        return self.lat

    def get_alt(self):
        return self.alt

    def get_lon(self):
        return self.lon

    def get_lat_depot(self):
        return self.lat_depot

    def get_lon_depot(self):
        return self.lon_depot

    def get_alt_depot(self):
        return self.alt_depot

    def get_name(self):
        return self.name

    def get_email(self):
        return self.email

    def get_orders(self):
        return self.orders_fulfilled

    def main(self):
        self.set_lat()
        self.set_lon()
        self.set_alt()
        self.set_lat_depot()
        self.set_lon_depot()
        self.set_alt_depot()
        self.set_id()
        self.set_email()
        self.set_name()
        self.set_orders()


if __name__ == '__main__':
    id_user = "000"
    file = "User" + id_user
    file_user = JsonDB.JsonFile(file)
    json_user = file_user.get_file_content()
    carrinheiro = User(json_user)
    print("Test with user:", carrinheiro.get_name())
