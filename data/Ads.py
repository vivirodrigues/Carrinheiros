try:
    from Scenario import JsonFile
except:
    pass


class Ads:
    def __init__(self, json):
        self.json = json
        self.id = ''
        self.user_id = ''
        self.material_type = ''
        self.amount = ''
        self.description = ''
        self.material_subtype = ''
        self.unity = ''
        self.type = ''
        self.lat = ''
        self.lon = ''
        self.alt = ''
        self.user_attending = ''
        self.avaiable_days = ''
        self.main()

    def set_id(self):
        self.id = self.json.get("id")

    def set_user_id(self):
        self.user_id = self.json.get("user_id")

    def set_material_type(self):
        self.material_type = self.json.get("material_type")

    def set_material_subtype(self):
        self.material_subtype = self.json.get("material_subtype")

    def set_amount(self):
        self.amount = self.json.get("amount")

    def set_unity(self):
        self.unity = self.json.get("unity")

    def set_type(self):
        self.type = self.json.get("type")

    def set_lat(self):
        self.lat = self.json.get("latitude")

    def set_lon(self):
        self.lon = self.json.get("longitude")

    def set_alt(self):
        self.alt = self.json.get("altitude")

    def set_user_attending(self):
        self.user_attending = self.json.get("user_attending")

    def set_weight(self):
        # define
        pass

    def set_avaiable_days(self):
        self.avaiable_days = self.json.get("days_of_the_week")

    def get_avaiable_days(self):
        return self.avaiable_days

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

    def get_lat(self):
        return self.lat

    def get_lon(self):
        return self.lon

    def get_alt(self):
        return self.alt

    def get_user_attending(self):
        return self.user_attending

    def main(self):
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
        self.set_avaiable_days()


if __name__ == '__main__':
    id_ads = "0001"
    file = "Ads" + id_ads
    file_ads = JsonFile.JsonFile(file)
    json_ads = file_ads.get_file_content()
    anuncio = Ads(json_ads)
    print("Test with ads:", anuncio.get_material_subtype())
