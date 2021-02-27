from general import Json


class Advertisement:
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
        self.main()

    def set_id(self):
        # ad id
        self.id = self.json.get("id")

    def set_user_id(self):
        # id of the user who made the ad
        self.user_id = self.json.get("user_id")

    def set_type(self):
        # the ad can be a material offer or request
        self.type = self.json.get("type")

    def set_material_type(self):
        # String("paper", "metal", "glass", "plastic", etc)
        self.material_type = self.json.get("material_type")

    def set_material_subtype(self):
        ###
        # based on the type of material, there are different subtypes
        # example: material_type : paper
        # material_subtype : String("magazines", "books", "cardboard", "journal", etc)
        ###
        self.material_subtype = self.json.get("material_subtype")

    def set_amount(self):
        # the amount of materials
        self.amount = self.json.get("amount")

    def set_measure_unit(self):
        ###
        # the unit of measure can be a unit of mass, volume, etc.
        # String: L = "liters", ml = "milliliters", Kg = "kilograms", g ="grams", u = "units", etc)
        ###
        self.measure_unit = self.json.get("measure_unit")

    def set_available_days(self):
        ###
        # days of the week that the user is available to materials deliver/collect
        # example: String("Seg", "Ter", "Qua", "Qui", "Sex", "Sab", "Dom") in portuguese
        ###
        self.available_days = self.json.get("days_of_the_week")

    def set_user_attending(self):
        # id of the user who expressed interest in the ad
        self.user_attending = self.json.get("user_attending")

    def set_status(self):
        ###
        # advertisement status
        # String("done", "in progress", "available")
        ###
        self.status = self.json.get("status")

    def set_coordinates(self):
        ###
        # a list with user instant geographic coordinates
        # list -> tuple (latitude, longitude)
        ###
        self.coordinates = tuple(self.json.get("coordinates"))

    def set_lat(self):
        self.lat = self.coordinates[0]

    def set_lon(self):
        self.lon = self.coordinates[1]

    def set_weight(self):
        # define
        pass

    def get_id(self):
        return self.id

    def get_user_id(self):
        return self.user_id

    def get_type(self):
        return self.type

    def get_material_type(self):
        return self.material_type

    def get_material_subtype(self):
        return self.material_subtype

    def get_amount(self):
        return self.amount

    def get_measure_unit(self):
        return self.measure_unit

    def get_available_days(self):
        return self.available_days

    def get_user_attending(self):
        return self.user_attending

    def get_status(self):
        return self.status

    def get_coordinates(self):
        return self.coordinates

    def get_lat(self):
        return self.lat

    def get_lon(self):
        return self.lon

    def main(self):
        self.set_id()
        self.set_type()
        self.set_user_id()
        self.set_material_type()
        self.set_material_subtype()
        self.set_amount()
        self.set_measure_unit()
        self.set_available_days()
        self.set_user_attending()
        self.set_status()
        self.set_coordinates()
        self.set_lat()
        self.set_lon()


def get_ads(id_ad, directory_json):
    file_name = get_file_ads(id_ad)
    json_ad = Json.json_content(directory_json, file_name)
    ad = Advertisement(json_ad)
    return ad


def get_file_ads(id_ad):
    file_name = "Ads" + str(id_ad)
    return file_name


if __name__ == '__main__':
    id_ads = "0001"
    directory_file_json = "../data/DB/"
    file = get_file_ads(id_ads)
    json_ads = Json.json_content(directory_file_json, file)
    anuncio = Advertisement(json_ads)
    print("Test with ads:", anuncio.get_lon())
    ###########################################
    ads = get_ads(id_ads, directory_file_json)
    print("Test 2 with ads:", ads.get_lon())
