MAPS_DIRECTORY = '../data/maps/'
DATABASE_DIRECTORY = 'data/DB/'
FILE_NAME_OSM = 'map.osm'
GRAPH_NAME = '../data/maps/'
VEHICLE = 'pedestrian'
VEHICLE_MASS = 110
AIR_DENSITY = 1.2  # km / m³
AERODYNAMIC_COEFFICIENT = 1  # flat surface
FRONTAL_VEHICLE_AREA = 1  # m²
SPEED = 0.83  # m/s = 3 km/h
COVERAGE_AREA = 5000  # meters
BIDIRECTIONAL = True
TWO_WAY = ['living_street', 'secondary_link', 'tertiary', 'residential', 'unclassified', 'tertiary_link', 'service', 'pedestrian', 'track', 'sidewalk', 'footway', 'crossing', 'cycleway']
IMPEDANCE = 'weight'  # 'impedance' #'weight' # 'length' # 'travel_time' # 'distance'
GRADE_FACTOR = False
SPEED_FACTOR = False
STREET_COLLECT = True

########## Genetic Algorithms
AMOUNT_INDIVIDUALS = 10
MUTATION_PERCENTAGE = 10
CROSSOVER_PERCENTAGE = 80 # must be an even number
LIMIT_ITERATION = 10

######## Simulation
SIMULATION = True
NET = 'map.net.xml'


# --remove-edges.by-vclass rail_slow,rail_fast,bicycle,pedestrian