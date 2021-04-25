from __future__ import division

import os
import sys
import subprocess
import random
import socket
import threading
import time
from route import Scenario
import json
from decimal import Decimal, ROUND_HALF_UP
from Constants import *
from geography import GeoTiff, OpenSteetMap, Coordinates, Map
from general import Saves
from route import Graph_Collect
from simulation import Map_Simulation
import Carrinheiro
import osmnx as ox
from scipy import constants
from route import Graph


if 'SUMO_HOME' in os.environ:
    tools = os.path.join(os.environ['SUMO_HOME'], 'tools')
    sys.path.append(tools)
else:
    sys.exit("Environment variable SUMO_HOME not defined")

sys.path.append(os.path.join('/home/-/sumo-1.8.0/tools'))

import traci


class UnusedPortLock:
    lock = threading.Lock()

    def __init__(self):
        self.acquired = False

    def __enter__(self):
        self.acquire()

    def __exit__(self):
        self.release()

    def acquire(self):
        if not self.acquired:
            UnusedPortLock.lock.acquire()
            self.acquired = True

    def release(self):
        if self.acquired:
            UnusedPortLock.lock.release()
            self.acquired = False


def find_unused_port():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0)
    sock.bind(('127.0.0.1', 0))
    sock.listen(socket.SOMAXCONN)
    ipaddr, port = sock.getsockname()
    sock.close()
    return port


def terminate_sumo(sumo):
    if sumo.returncode is not None:
        os.system("taskkill.exe /F /im sumo.exe")
        time.sleep(1)


def calculate_power(G, dict_edges_net, id_edge, vehicle_mass, speed):

    nodes = Map_Simulation.edges_to_nodes(id_edge, dict_edges_net)
    data_edge = G.get_edge_data(nodes[0], nodes[1])

    slope = data_edge.get(0).get('grade')
    surface_floor = data_edge.get(0).get('surface')

    current_force = Graph.force(vehicle_mass, surface_floor, slope)
    power = current_force * speed # * math.cos(slope)

    return power


def calculate_energy(vehicle_mass, speed, z):
    Em = ((vehicle_mass * (speed ** 2)) / 2) + vehicle_mass * constants.g * z
    return Em


def time_streets(G, dict_edges_net, id_edge):
    nodes = Map_Simulation.edges_to_nodes(id_edge, dict_edges_net)
    data_edge = G.get_edge_data(nodes[0], nodes[1])

    max_speed = data_edge.get(0).get('maxspeed')

    return float(max_speed)


def calculate_force(G, dict_edges_net, id_edge, vehicle_mass, speed):
    nodes = Map_Simulation.edges_to_nodes(id_edge, dict_edges_net)
    data_edge = G.get_edge_data(nodes[0], nodes[1])

    slope = data_edge.get(0).get('grade')
    surface_floor = data_edge.get(0).get('surface')

    current_force = Graph.force(vehicle_mass, surface_floor, slope, speed)
    return current_force


def calculate_length(G, dict_edges_net, id_edge):
    nodes = Map_Simulation.edges_to_nodes(id_edge, dict_edges_net)
    data_edge = G.get_edge_data(nodes[0], nodes[1])

    return data_edge.get(0).get('length')


def run(route, G, dict_edges_net, file_name_json, edges_weight, impedance):

    power = []
    energy = []
    force = []

    dicionario_power = {}
    dicionario_e = {}
    dicionario_force = {}
    pdf_power_dict = {}
    pdf_max_speed_dict = {}

    incline = {}
    inclination = []
    total = 0

    total_length = 0
    before_edge_id = 0

    step = 1
    max_speeds = []

    dados = []

    vehicle_weight = VEHICLE_MASS
    path_traveled = []

    vehicle_id = "carrinheiro"

    # adition = Simulation.Vehicles.add1(traci)
    traci.route.add("path", route)
    traci.vehicle.add(vehicle_id, "path")# , departLane="best")
    traci.vehicle.setParameter("carrinheiro", "carFollowModel", "KraussPS")
    traci.vehicle.setVehicleClass(vehicle_id, "ignoring")
    traci.vehicle.setShapeClass(vehicle_id, VEHICLE)
    traci.vehicle.setEmissionClass(vehicle_id, "Zero")
    traci.vehicle.setMaxSpeed(vehicle_id, 1)  # aprox 8 km/h

    # traci.vehicle.setLateralAlignment("carrinheiro", "right")  # or "nice"

    while step == 1 or traci.simulation.getMinExpectedNumber() > 0:

        #traci.vehicle.setSpeed("carrinheiro", 0.83)
        speed = traci.vehicle.getSpeed("carrinheiro")

        if speed < 0:
            speed = float(0)

        # speed = speedI #* 3.6  # m/s para km/h

        # speedList.append(speed)

        slope = traci.vehicle.getSlope(vehicle_id)
        acceleration = traci.vehicle.getAcceleration(vehicle_id)

        total += 1

        x, y, z = traci.vehicle.getPosition3D(vehicle_id)
        dados.append({"x": x, "y": y, "z": z, "slope": slope})

        edge_id = traci.vehicle.getRoadID(vehicle_id)
        if len(edge_id) > 0:

            if step > 1 and edge_id[0] != ":":

                inclination.append(z)
                power.append(calculate_power(G, dict_edges_net, edge_id, vehicle_weight, speed))
                force.append(calculate_force(G, dict_edges_net, edge_id, vehicle_weight, speed))
                energy.append(calculate_energy(vehicle_weight, speed, float(z)))

                max_speeds.append(time_streets(G, dict_edges_net, edge_id))

                if edge_id != before_edge_id:
                    total_length += calculate_length(G, dict_edges_net, edge_id)

                    # if the edge is a stop point and the edge has not yet been traveled
                    if edge_id in list(edges_weight.keys()) and edge_id not in path_traveled:

                        # the vehicle needs to stop to pick up the material
                        traci.vehicle.slowDown(vehicle_id, 0, 5)

                        # weight is added to the vehicle
                        vehicle_weight += edges_weight.get(edge_id)

                    before_edge_id = edge_id
                    path_traveled.append(edge_id)

        traci.simulationStep()
        vehicles = traci.simulation.getEndingTeleportIDList()

        for vehicle in vehicles:
            traci.vehicle.remove(vehicle, reason=4)

        step += 1

    for i in range(len(power)):
        sett = {i: power[i]}
        dicionario_power.update(sett)

    for i in range(len(force)):
        sett = {i: force[i]}
        dicionario_force.update(sett)

    for i in range(len(energy)):
        sett = {i: energy[i]}
        dicionario_e.update(sett)

    for i in range(len(inclination)):
        set2 = {i: inclination[i]}
        incline.update(set2)

    # PDF
    max_power = max(power)
    pdf_power = [0] * (int(max_power) + 10)

    max_speed = max(max_speeds)
    pdf_max_speeds = [0] * (int(max_speed) + 10)

    for i in power:
        num = Decimal(float(i)).quantize(0, ROUND_HALF_UP)
        pdf_power[int(num)] += 1

    for i in range(len(pdf_power)):
        pdf_power[i] = (pdf_power[i] / len(power)) * 100
        sett = {i: pdf_power[i]}
        pdf_power_dict.update(sett)

    for i in max_speeds:
        # num = Decimal(float(i)).quantize(0, ROUND_HALF_UP)
        #pdf_max_speeds[int(num)] += 1
        pdf_max_speeds[int(i)] += 1

    for i in range(len(pdf_max_speeds)):
        pdf_max_speeds[i] = (pdf_max_speeds[i] / len(max_speeds)) * 100
        sett = {i: pdf_max_speeds[i]}
        pdf_max_speed_dict.update(sett)

    traci.close()
    sys.stdout.flush()
    write_json(pdf_power_dict, file_name_json + '_' + impedance + '_pdf' + '_speed_' + str(SPEED_FACTOR))
    write_json(pdf_max_speed_dict, file_name_json + '_' + impedance + '_pdf_speeds_' + str(SPEED_FACTOR))
    write_json(dicionario_force, file_name_json + '_' + impedance + '_f' + '_speed_' + str(SPEED_FACTOR))
    write_json(dicionario_power, file_name_json + '_' + impedance + '_speed_' + str(SPEED_FACTOR))
    write_json(dicionario_e, file_name_json + '_' + impedance + '_e' + '_speed_' + str(SPEED_FACTOR))
    write_json(incline, file_name_json + '_' + impedance + '_i' + '_speed_' + str(SPEED_FACTOR))

    return total_length


def start_simulation(sumo, scenario, output, route, G, dict_edges_net, file_name_json, edges_weight, impedance):
    unused_port_lock = UnusedPortLock()
    unused_port_lock.__enter__()
    remote_port = find_unused_port()

    sumo = subprocess.Popen(
        [sumo, "-c", scenario, "--tripinfo-output", output, "--device.emissions.probability", "1.0", "--remote-port",
         str(remote_port), "--duration-log.statistics", "--log", "logfile.txt"], stdout=sys.stdout, stderr=sys.stderr)
    unused_port_lock.release()

    length_total = 0

    try:
        traci.init(remote_port)
        length_total = run(route, G, dict_edges_net, file_name_json, edges_weight, impedance)
    except Exception as e:
        print(e)
        #pass
        raise
    finally:
        terminate_sumo(sumo)
        unused_port_lock.__exit__()

    return length_total


def write_json(content, fileName):
    with open(fileName + '.json', 'w') as json_file:
        json.dump(content, json_file, separators=(',', ':'), ensure_ascii=False, sort_keys=True, indent=4)


def geotiff_transformation(name_file_in, name_file_out):

    gdal_command = "gdal_translate -of GTiff -ot Int16 -co TFW=YES " + name_file_in + " " + name_file_out
    process_gdal = subprocess.Popen(gdal_command.split(), stdout=subprocess.PIPE)
    output, error = process_gdal.communicate()


def netconvert_geotiff(name_file_osm, name_file_geotiff, name_file_output):

    netconvert_command = "netconvert --osm-files " + name_file_osm + " --heightmap.geotiff " + name_file_geotiff + " -o " + name_file_output # + " -t " + " map.typ.xml "
    process_netconvert = subprocess.Popen(netconvert_command.split(), stdout=subprocess.PIPE)
    output, error = process_netconvert.communicate()


def get_work(G, nodes):
    weight_total = 0
    for i in range(len(nodes)-1):
        data_edge = G.get_edge_data(nodes[i], nodes[i+1])
        weight_total += data_edge.get(0).get('length')
    print("TOTAL", weight_total)


def calculate_work_total(G, paths, nodes_mass_increment):

    sum_path_costs = 0
    vehicle_mass = VEHICLE_MASS

    for i in paths:

        # updates the weight of all edges of the scenario according
        # to the current weight of the vehicle
        G = Graph.update_weight(G, vehicle_mass, speed_factor=False)

        sum_path_costs += Graph_Collect.sum_costs(G, i, 'weight')
        vehicle_mass += nodes_mass_increment.get(i[-1])

        G = Graph.update_weight(G, VEHICLE_MASS, speed_factor=False)

    return sum_path_costs


def verify_graph_exists(file_name, stop_points, coordinates_list):

    try:
        G = ox.load_graphml(file_name)
        lats = [a_tuple[0] for a_tuple in stop_points]
        lons = [a_tuple[1] for a_tuple in stop_points]
        nodes = [(n, d) for n, d in G.nodes(data=True) if d['y'] in lats and d['x'] in lons]
        if len(nodes) == len(stop_points):
            return True
    except:
        pass
    return False


def nodes_data(file_name, stop_points, material_weights, file_osm):

    G = ox.load_graphml(file_name)
    lats = [a_tuple[0] for a_tuple in stop_points]
    lons = [a_tuple[1] for a_tuple in stop_points]

    nodes_coordinates = {}
    nodes_mass_increment = {}

    [nodes_coordinates.update([(list(G.neighbors(n))[0], (d['y'], d['x']))]) \
     for n, d in G.nodes(data=True) if d['y'] in lats and d['x'] in lons and len(list(G.neighbors(n))) == 1]

    [nodes_mass_increment.update([(list(G.neighbors(n))[0], material_weights.get((d['y'], d['x']))[0])]) \
     for n, d in G.nodes(data=True) if d['y'] in lats and d['x'] in lons and len(list(G.neighbors(n))) == 1]

    if len(list(nodes_coordinates.keys())) != len(stop_points):

        [nodes_coordinates.update([(n, (d['y'], d['x']))]) for n, d in G.nodes(data=True) if
         d['y'] in lats and d['x'] in lons]

        [nodes_mass_increment.update([(n, material_weights.get((d['y'], d['x']))[0])]) \
         for n, d in G.nodes(data=True) if d['y'] in lats and d['x'] in lons]

    Scenario.simulation_edit_graph(G, file_osm)
    #G = Graph.set_node_elevation_simulation(G, 'map.net.xml')
    G = Graph.set_node_elevation(G, '../data/maps/19S45_ZN')
    G = Graph.edge_grades(G)
    G = Graph.hypotenuse(G)
    G = Graph.surface(G, file_osm)
    G = Graph.maxspeed(G)
    G = Graph.update_weight(G, VEHICLE_MASS)
    Graph.save_graph_file(G, file_name)

    return G, nodes_coordinates, nodes_mass_increment


def create_route(stop_points, material_weights, json_files, n = None):

    name_file_net = 'map.net.xml'
    sumo_config = "map.sumocfg"
    geotiff_name_out = MAPS_DIRECTORY + 'out.tif'

    # download the osm file (scenario)
    osm_file = OpenSteetMap.file_osm(MAPS_DIRECTORY, stop_points)

    # download the GeoTiff file (scenario)
    geotiff_name = GeoTiff.geotiff(MAPS_DIRECTORY, stop_points)
    print("geotiff", geotiff_name)

    geotiff_name = MAPS_DIRECTORY + geotiff_name + '.tif'

    geotiff_transformation(geotiff_name, geotiff_name_out)

    max_lat, min_lat, max_lon, min_lon = Coordinates.create_osmnx(stop_points)

    coordinates_list = Coordinates.coordinates_list_bbox(stop_points)
    G_file = Saves.def_file_name(MAPS_DIRECTORY, stop_points, '.graphml')
    file_name_json = Saves.def_file_name('../data/results/', stop_points, '') + '_' + str(n)
    json_files.append(file_name_json)

    #if verify_graph_exists(G_file, stop_points, coordinates_list) is True:

        #netconvert_geotiff(osm_file, MAPS_DIRECTORY + 'out.tif', NET)

        #G, nodes_coordinates, nodes_mass_increment = nodes_data(G_file, stop_points, material_weights, osm_file)

    #else:

    Map_Simulation.delete_osm_items(osm_file)

    if BIDIRECTIONAL is True:
        Map_Simulation.edit_map(osm_file)

    # Scenario graph (paths are edges and junctions are nodes)
    G = ox.graph_from_bbox(max_lat, min_lat, max_lon, min_lon, network_type='all')

    G, nodes_coordinates, nodes_mass_increment = Graph.configure_graph_simulation(G, geotiff_name, stop_points, material_weights, osm_file, G_file)

    ####################

    index_source = list(nodes_coordinates.values()).index(stop_points[0])
    node_source = list(nodes_coordinates.keys())[index_source]
    print("node source", node_source)

    index_target = list(nodes_coordinates.values()).index(stop_points[-1])
    node_target = list(nodes_coordinates.keys())[index_target]
    print("target", node_target)

    H = Graph_Collect.create_graph_route(nodes_coordinates, nodes_mass_increment)

    dict_edges_net = Map_Simulation.edges_net(name_file_net)

    Map_Simulation.allow_vehicle(name_file_net)

    impedances = ['weight', 'impedance', 'distance']

    for j in impedances:

        cost_total, paths = Carrinheiro.nearest_neighbor_path(G, H, node_source, node_target, j)
        #cost_total_2, paths = Carrinheiro.closest_insertion_path(G, H, node_source, node_target, j)
        #cost_total_3, paths = Carrinheiro.further_insertion_path(G, H, node_source, node_target, j)

        # cost_total, paths = Carrinheiro.genetic_algorithm(G, H, node_source, node_target, nodes_coordinates)

        if j != 'weight':
            cost_total = calculate_work_total(G, paths, nodes_mass_increment)

        result_work = {}
        [result_work.update([(str(i), [stop_points[i]])]) for i in range(len(stop_points))]
        result_work.update([('work_total', float(cost_total))])
        #result_work.update([('path', paths)])
        print(paths)
        #write_json(result_work, file_name_json + '_coords' + '_' + IMPEDANCE + '_speed_' + str(SPEED_FACTOR))
        print("cost total", cost_total)

        # print(paths)

        list1 = []
        for i in paths:
            list1 += i[1:]
        # print(list1)

        sumo_route = []
        edges_stop = []
        edges_weight = {}
        for i in paths:
            route_edges = Map_Simulation.nodes_to_edges(i, dict_edges_net)
            edges_stop.append(route_edges[0])
            sumo_route.extend(route_edges)
        #print("sumo", sumo_route)

        [edges_weight.update([(edges_stop[i], nodes_mass_increment.get(paths[i][0]))]) for i in range(len(edges_stop))]

        out = file_name_json + '_' + j + '_speed_'+ str(SPEED_FACTOR) + '.xml'

        total_length = start_simulation('sumo', sumo_config, out, sumo_route, G, dict_edges_net, file_name_json, edges_weight, j)

        result_work.update([('total_length', float(total_length))])
        write_json(result_work, file_name_json + '_coords_' + j + '_speed_' + str(SPEED_FACTOR))

        #fig, ax = ox.plot_graph_route(G, paths[7], route_linewidth=6, node_size=0, bgcolor='w')
        ## fig, ax = ox.plot_graph_routes(G, paths, route_linewidth=6, node_size=0, bgcolor='w')

    return json_files


def get_seed(seed_id):
    seeds = [960703545, 1277478588, 1936856304,
             186872697, 1859168769, 1598189534,
             1822174485, 1871883252, 694388766,
             188312339, 773370613, 2125204119,
             2041095833, 1384311643, 1000004583,
             358485174, 1695858027,
             762772169, 437720306, 939612284,
             425414105, 1998078925, 981631283, #1024155645
             1024155645, 558746720,
             1349341884, 678622600, 1319566104,
             538474442, 722594620,
             1700738670, 1995749838, 1147024708,
             346983590, 565528207, 513791680,
             1996632795, 2081634991, 1769370802, 349544396,
             1996610406, 1973272912, 1972392646, 605846893,
             934100682, 222735214, 2101442385, 2009044369,
             1895218768, 701857417, 89865291, 144443207,
             720236707, 822780843, 898723423,
             1644999263, 985046914, 1859531344,
             764283187, 778794064, 683102175, 1334983095, 1072664641, 999157082]
    return seeds[seed_id]


def main():

    n_points = 10
    max_mass_material = 50

    random.seed(get_seed(0))
    mass_increments = [random.randint(0, max_mass_material) for i in range(n_points-2)]
    material_weights = [(mass_increments[i], 'Kg') for i in range(n_points-2)]
    material_weights.append((0, 'Kg'))
    material_weights.insert(0, (0, 'Kg'))

    sigma = 0.005  # standard deviation

    # scenarios: Campinas, Belém, BH
    mean_lon = [-43.9438]
    mean_lat = [-19.9202]
    # lon: -47.068523   -48.47000   -43.9438
    # lat: -22.804202   -1.46000    -19.9202

    n_seeds = 11
    json_files = []
    materials = {}

    for a in range(1, n_seeds):

        random.seed(get_seed(a))
        print(get_seed(a))
        longitudes = [random.gauss(mean_lon[0], sigma) for i in range(n_points)]
        latitudes = [random.gauss(mean_lat[0], sigma) for i in range(n_points)]
        stop_points = [(float(latitudes[i]), float(longitudes[i])) for i in range(len(latitudes))]
        [materials.update([((latitudes[i], longitudes[i]), material_weights[i])]) for i in range(len(latitudes))]
        json_files = create_route(stop_points, materials, json_files, a)

    print(json_files)


if __name__ == "__main__":
    main()
