class Node:
    def __init__(self, id_node):
        self.id = id_node
        self.adjacent_nodes = {}

    def set_adjacent_nodes(self, target, cost, vehicle_mass):
        self.adjacent_nodes.update([(target, cost)])
