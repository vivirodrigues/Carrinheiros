try:
    from models.adServer import JsonDB
except:
    pass


class Ads:
    def __init__(self, json):
        self.json = json
        self.id = ''
        self.user_id = ''
        self.type = ''
        self.material_type = ''
        self.material_subtype = ''
        self.amount = ''
        self.measure_unit = ''
        self.available_days = []
        self.user_attending = ''
        self.status = ''
        self.coordinates = ()
        self.lat = ''
        self.lon = ''
        self.alt = ''
        self.main()

    def set_id(self):
        # ad id
        self.id = self.json.get("id")

    def set_user_id(self):
        # id of the user who made the ad
        self.user_id = self.json.get("user_id")

    def set_material_type(self):
        # String("paper", "metal", "glass", "plastic", etc)
        self.material_type = self.json.get("material_type")

    def set_material_subtype(self):
        self.material_subtype = self.json.get("material_subtype")

    def set_amount(self):
        self.amount = self.json.get("amount")

    def set_unity(self):
        self.unity = self.json.get("unity")

    def set_type(self):
        self.type = self.json.get("type")

    def set_coordinates(self):
        self.coordinates = tuple(self.json.get("coordinates"))

    def set_lat(self):
        self.lat = self.coordinates[0]

    def set_lon(self):
        self.lon = self.coordinates[1]

    def set_alt(self):
        self.alt = self.coordinates[2]

    def set_user_attending(self):
        self.user_attending = self.json.get("user_attending")

    def set_weight(self):
        # define
        pass

    def set_available_days(self):
        self.available_days = self.json.get("days_of_the_week")

    def get_available_days(self):
        return self.available_days

    def get_id(self):
        return self.id

    def get_user_id(self):
        return self.user_id

    def get_material_type(self):
        return self.material_type

    def get_material_subtype(self):
        return self.material_subtype

    def get_amount(self):
        return self.amount

    def get_unity(self):
        return self.unity

    def get_type(self):
        return self.type

    def get_coordinates(self):
        return self.coordinates

    def get_lat(self):
        return self.lat

    def get_lon(self):
        return self.lon

    def get_alt(self):
        return self.alt

    def get_user_attending(self):
        return self.user_attending

    def main(self):
        self.set_coordinates()
        self.set_lat()
        self.set_lon()
        self.set_alt()
        self.set_id()
        self.set_type()
        self.set_user_attending()
        self.set_user_id()
        self.set_amount()
        self.set_material_type()
        self.set_material_subtype()
        self.set_unity()
        self.set_available_days()


if __name__ == '__main__':
    id_ads = "0001"
    file = "Ads" + id_ads
    file_ads = JsonDB.JsonDB(file)
    json_ads = file_ads.get_file_content()
    anuncio = Ads(json_ads)
    print("Test with ads:", anuncio.get_lon())
