class Route:
    def __init__(self, mass_vehicle, nodes):
        self.vehicle_mass = mass_vehicle
        self.visited_nodes = []
        self.not_visited_nodes = nodes

    def set_vehicle_mass(self, increment_mass):
        self.vehicle_mass += increment_mass

    def get_vehicle_mass(self):
        return self.vehicle_mass

    def set_visited_nodes(self, node):
        self.visited_nodes.append(node)
        self.not_visited_nodes.remove(node)

    def get_visited_nodes(self):
        return self.visited_nodes
