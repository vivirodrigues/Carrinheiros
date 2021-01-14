from models.adServer import User, Path, JsonDB, DateTime
from models.mapsServer import ScenarioOSM, ScenarioGeo


class Scenario:
    def __init__(self, id_user, date):
        self.id_user = id_user
        self.collection_day = date
        self.carrinheiro = User.get_user(id_user, self.directory_json)
        self.path = Path.Path(self.carrinheiro, date, self.directory_json)
        self.directory_json = '../models/DB/'
        self.directory_maps = '../models/maps/'

    def main(self):
        # get user stop points
        stop_points = self.path.get_stop_points()
        # download the osm file (scenario)
        osm_scenario = ScenarioOSM.ScenarioOsm(self.directory_maps, stop_points)
        # download the GeoTiff file (scenario)
        geo_scenario = ScenarioGeo.ScenarioGeo(self.directory_maps, stop_points)


if __name__ == '__main__':
    id_user1 = "000"
    date = "25 01 2021"
    scenario = Scenario(id_user1, date)
    scenario.main()


