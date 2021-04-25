MAPS_DIRECTORY = 'data/maps/'
RESULTS_DIRECTORY = 'data/results/'
FILE_NAME_OSM = 'map.osm'
VEHICLE = 'pedestrian'
VEHICLE_MASS = 110
AIR_DENSITY = 1.2  # km / m³
AERODYNAMIC_COEFFICIENT = 1  # flat surface
FRONTAL_VEHICLE_AREA = 1  # m²
SPEED = 0.83  # m/s = 3 km/h
COVERAGE_AREA = 5000  # meters
BIDIRECTIONAL = True
TWO_WAY = ['living_street', 'secondary_link', 'tertiary', 'residential', 'unclassified', 'tertiary_link', 'service', 'pedestrian', 'track', 'sidewalk', 'footway', 'crossing', 'cycleway']
GRADE_FACTOR = False
SPEED_FACTOR = False
STREET_COLLECT = True

# Genetic Algorithms
AMOUNT_INDIVIDUALS = 10
MUTATION_PERCENTAGE = 10
CROSSOVER_PERCENTAGE = 80 # must be an even number
LIMIT_ITERATION = 10

# Simulation
NET = 'simulation/map.net.xml'
SUMO_CONFIG = 'simulation/map.sumocfg'