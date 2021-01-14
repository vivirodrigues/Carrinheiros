from models.adServer import Advertisement, User, DateTime, JsonDB


class Path:

    def __init__(self, user, day_collection, dir_json):
        self.carrinheiro = user
        self.day_collection = day_collection  # collection day
        self.available_ads = []
        self.stop_points = []
        self.start_point = ()
        self.end_point = ()
        self.weights = []
        self.directory_file_json = dir_json # '../DB/'
        self.main()

    def set_start_point(self):
        # geographical coordinates of the place of departure (beginning of the route)
        self.start_point = self.carrinheiro.get_coordinates()

    def set_end_point(self):
        # geographical coordinates of the place of arrival (usually deposit, end of the route)
        self.end_point = self.carrinheiro.get_coordinates_depot()

    def set_available_ads(self):
        # announcements available for collection day
        weekday_collection = DateTime.DateTime(self.day_collection).get_weekday_pt()
        orders = self.carrinheiro.get_attended_ads()
        available_ads = []
        for i in orders:
            ads = Advertisement.get_ads(i, self.directory_file_json)
            days_collection = ads.get_available_days()
            if weekday_collection in days_collection:
                available_ads.append(i)
        self.available_ads = available_ads

    def set_stop_points(self):
        ###
        # configures the route in a list
        # each item in the list contains a tuple with the coordinates of the stop point
        # example: [(x1,y1,z1),...,(x,y,z)]
        # where x: latitude, y: longitude, z: altitude
        ###
        coordinates_ads = []
        for i in self.available_ads:
            ads = Advertisement.get_ads(i, self.directory_file_json)
            coordinates = ads.get_coordinates()
            coordinates_ads.append(coordinates)
        coordinates_ads.insert(0, self.start_point)
        coordinates_ads.insert(len(coordinates_ads), self.end_point)
        self.stop_points = coordinates_ads

    def get_start_point(self):
        return self.start_point

    def get_end_point(self):
        return self.end_point

    def get_available_ads(self):
        return self.available_ads

    def get_stop_points(self):
        return self.stop_points

    def main(self):
        self.set_start_point()
        self.set_end_point()
        self.set_available_ads()
        self.set_stop_points()


if __name__ == "__main__":
    collection_day = '25 01 2021'
    dir_DB = '../DB/'
    file_user = JsonDB.JsonDB('User000', dir_DB)
    json_user = file_user.get_file_content()
    carrinheiro = User.User(json_user)
    path = Path(carrinheiro, collection_day, dir_DB)
    print("Test", path.get_stop_points())
