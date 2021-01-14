from models.adServer import User, Path, JsonDB, DateTime


class Scenario:
    def __init__(self, id_user, date):
        self.id_user = id_user
        self.collection_day = date
        self.directory_json = '../models/DB/'
        self.carrinheiro = User.get_user(id_user, self.directory_json)
        self.path = Path.Path(self.carrinheiro, date, self.directory_json)

    def main(self):
        print(self.path.get_stop_points())


if __name__ == '__main__':
    id_user1 = "000"
    date = "25 01 2021"
    scenario = Scenario(id_user1, date)
    scenario.main()


