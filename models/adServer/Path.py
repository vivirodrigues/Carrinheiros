from models.adServer import Ads, User
import DateTime
import JsonDB


class Path:

    def __init__(self, id_user):
        self.id_user = id_user  # user id carrinheiro
        self.day_collection = '25 01 2021'  # collection day
        self.stop_points = []
        self.n_stop_points = 0
        self.start_point = ()
        self.end_point = ()
        self.weights = []
        self.materials = []
        self.available_ads = []
        self.main()

    def set_carrinheiro(self):
        file_name = get_file_user(self.id_user)
        file_user = JsonDB.JsonDB(file_name)
        json_user = file_user.get_file_content()
        self.carrinheiro = User.User(json_user)

    def set_start_point(self):
        x = self.carrinheiro.get_lat()
        y = self.carrinheiro.get_lon()
        z = self.carrinheiro.get_alt()
        self.start_point = (x, y, z)

    def get_start_point(self):
        return self.start_point

    def set_end_point(self):
        x = self.carrinheiro.get_lat_depot()
        y = self.carrinheiro.get_lon_depot()
        z = self.carrinheiro.get_alt_depot()
        self.end_point = (x, y, z)

    def get_end_point(self):
        return self.end_point

    def set_available_ads(self):
        weekday_collection = DateTime.DateTime(self.day_collection).get_weekday_pt()
        orders = self.carrinheiro.get_orders()
        available_ads = []
        for i in orders:
            ads = self.get_ads(i)
            days_collection = ads.get_available_days()
            if weekday_collection in days_collection:
                available_ads.append(i)
        self.available_ads = available_ads

    def get_available_ads(self):
        return self.available_ads

    def set_coordinates_path(self):
        coordinates_ads = []
        for i in self.available_ads:
            ads = self.get_ads(i)
            lat = ads.get_lat()
            lon = ads.get_lon()
            alt = ads.get_alt()
            coordinates = (lat, lon, alt)
            coordinates_ads.append(coordinates)
        coordinates_ads.insert(0, self.start_point)
        coordinates_ads.insert(-1, self.end_point)
        self.stop_points = coordinates_ads
        self.n_stop_points = len(self.stop_points)

    def get_coordinates_path(self):
        return self.stop_points

    @staticmethod
    def get_ads(id_ads):
        file_name = get_file_ads(id_ads)
        file_ads = JsonDB.JsonDB(file_name)
        json_ads = file_ads.get_file_content()
        ads = Ads.Ads(json_ads)
        return ads

    def main(self):
        self.set_carrinheiro()
        print(self.carrinheiro.get_name())
        self.set_start_point()
        self.set_end_point()
        self.set_available_ads()
        self.set_coordinates_path()


def get_file_user(id_user):
    file_user = "User" + str(id_user)
    return file_user


def get_file_ads(id_ads):
    file_ads = "Ads" + str(id_ads)
    return file_ads


if __name__ == "__main__":
    path = Path("000")
    print(path.get_coordinates_path())
