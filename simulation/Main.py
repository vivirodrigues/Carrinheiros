from __future__ import division

import math
import os
import sys
import subprocess
import random
import socket
import threading
import time
import itertools
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


def run(route, G, dict_edges_net, file_name_json):

    power = []
    energy = []
    force = []

    dicionario_power = {}
    dicionario_e = {}
    dicionario_force = {}

    incline = {}
    inclination = []
    total = 0

    total_length = 0
    before_edge_id = 0

    step = 1
    consumption = 0
    totalConsumption = 0

    dados = []

    # adition = Simulation.Vehicles.add1(traci)
    traci.route.add("path", route)
    traci.vehicle.add("carrinheiro", "path", departLane="best")
    # traci.vehicle.setParameter("carrinheiro", "carFollowModel", "KraussPS")
    traci.vehicle.setVehicleClass("carrinheiro", "pedestrian")
    traci.vehicle.setShapeClass("carrinheiro", "pedestrian")
    traci.vehicle.setMaxSpeed("carrinheiro", 1)  # aprox 8 km/h
    # traci.vehicle.setLateralAlignment("carrinheiro", "right")  # or "nice"

    while step == 1 or traci.simulation.getMinExpectedNumber() > 0:

        speed = traci.vehicle.getSpeed("carrinheiro")

        if speed < 0:
            speed = float(0)

        # speed = speedI #* 3.6  # m/s para km/h

        num = Decimal(float(speed)).quantize(0, ROUND_HALF_UP)

        # pdfSpeed[int(num)] += 1

        # speedList.append(speed)

        # traci.vehicle.setSpeed("caminhao",speed)
        slope = traci.vehicle.getSlope("carrinheiro")
        acceleration = traci.vehicle.getAcceleration("carrinheiro")

        # consumption = calculate_real_fuel2(speedI, acceleration, slope)

        if consumption < 0:
            consumption = float(0)
        num = Decimal(float(consumption)).quantize(0, ROUND_HALF_UP)

        # pdfFuel[int(num)] += 1
        total += 1

        # fuelList.append(consumption)

        totalConsumption += consumption

        x, y, z = traci.vehicle.getPosition3D("carrinheiro")
        dados.append({"x": x, "y": y, "z": z, "slope": slope})

        edge_id = traci.vehicle.getRoadID("carrinheiro")
        if len(edge_id) > 0:
            if step > 1 and edge_id[0] != ":":
                inclination.append(z)
                power.append(calculate_power(G, dict_edges_net, edge_id, 110, speed))
                force.append(calculate_force(G, dict_edges_net, edge_id, 110, speed))
                energy.append(calculate_energy(110, speed, float(z)))

                if edge_id != before_edge_id:
                    total_length += calculate_length(G, dict_edges_net, edge_id)
                    before_edge_id = edge_id

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
    """
    for i in range(len(pdfSpeed)):
        pdfSpeed[i] = (pdfSpeed[i] / total) * 100
        sett = {i: pdfSpeed[i]}
        dicionarioSpeed.update(sett)
    """

    print("Total length", total_length, "steps", step)
    traci.close()
    sys.stdout.flush()
    write_json(dicionario_force, file_name_json + '_' + IMPEDANCE + '_f')
    write_json(dicionario_power, file_name_json + '_' + IMPEDANCE)
    write_json(dicionario_e, file_name_json + '_' + IMPEDANCE + '_e')
    write_json(incline, file_name_json + '_' + IMPEDANCE + '_i')

    return totalConsumption


def start_simulation(sumo, scenario, output, route, G, dict_edges_net, file_name_json):
    unused_port_lock = UnusedPortLock()
    unused_port_lock.__enter__()
    remote_port = find_unused_port()

    sumo = subprocess.Popen(
        [sumo, "-c", scenario, "--tripinfo-output", output, "--device.emissions.probability", "1.0", "--remote-port",
         str(remote_port), "--duration-log.statistics", "--log", "logfile.txt"], stdout=sys.stdout, stderr=sys.stderr)
    unused_port_lock.release()

    try:
        traci.init(remote_port)
        consumption = run(route, G, dict_edges_net, file_name_json)
    except Exception as e:
        print(e)
        raise
    finally:
        terminate_sumo(sumo)
        unused_port_lock.__exit__()

    return consumption


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
        weight_total += data_edge.get(0).get('weight')
    print("TOTAL", weight_total)


def create_route(stop_points, material_weights, json_files):

    name_file_net = 'map.net.xml'
    sumo_config = "map.sumocfg"
    geotiff_name_out = MAPS_DIRECTORY + 'out.tif'

    # download the osm file (scenario)
    osm_file_name = OpenSteetMap.file_osm(MAPS_DIRECTORY, stop_points)

    if BIDIRECTIONAL is True:
        Map_Simulation.edit_map(osm_file_name)

    # download the GeoTiff file (scenario)
    geotiff_name = GeoTiff.geotiff(MAPS_DIRECTORY, stop_points)

    geotiff_name = MAPS_DIRECTORY + geotiff_name + '.tif'

    geotiff_transformation(geotiff_name, geotiff_name_out)

    max_lat, min_lat, max_lon, min_lon = Coordinates.create_osmnx(stop_points)

    coordinates_list = Coordinates.coordinates_list_bbox(stop_points)
    G_file_name = Saves.def_file_name(MAPS_DIRECTORY, stop_points, '.graphml')
    file_name_json = Saves.def_file_name('../data/results/', stop_points, '')
    json_files.append(file_name_json)
    write_json(dict(stop_points), file_name_json + '_coords' + '_' + IMPEDANCE)

    # Scenario graph (paths are edges and junctions are nodes)
    G = ox.graph_from_bbox(max_lat, min_lat, max_lon, min_lon, network_type='all')

    #if Saves.verify_file_exists(coordinates_list, G_file_name) is False:

    #else:
    #    print("Entrou aqui")
    #    G = nx.read_graphml(G_file_name, node_type=<type 'str'>)

    print("Stop points", stop_points)

    G, nodes_coordinates, nodes_mass_increment = Graph.configure_graph_simulation(G, geotiff_name, stop_points,
                                                                                        material_weights, osm_file_name)
    index_source = list(nodes_coordinates.values()).index(stop_points[0])
    node_source = list(nodes_coordinates.keys())[index_source]
    print("node source", node_source)

    index_target = list(nodes_coordinates.values()).index(stop_points[-1])
    node_target = list(nodes_coordinates.keys())[index_target]
    print("target", node_target)

    H = Graph_Collect.create_graph_route(nodes_coordinates, nodes_mass_increment)

    Graph.save_graph_file(G, G_file_name)

    dict_edges_net = Map_Simulation.edges_net(name_file_net)

    cost_total, paths = Carrinheiro.closest_insertion_path(G, H, node_source, node_target)

    print("cost total", cost_total)

    print(paths)

    list1 = []
    for i in paths:
        list1 += i[1:]
    print(list1)
    get_work(G, list1)

    sumo_route = []
    for i in paths:
        sumo_route.extend(Map_Simulation.nodes_to_edges(i, dict_edges_net))

    print(sumo_route)
    start_simulation('sumo', sumo_config, 'out.xml', sumo_route, G, dict_edges_net, file_name_json)

    fig, ax = ox.plot_graph_route(G, list1, route_linewidth=6, node_size=0, bgcolor='w')

    return paths, json_files


def get_seed(seed_id):
    seeds = [960703545, 2009044369, 934100682, 1972392646, 1936856304,
             186872697, 1859168769, 1598189534, 1822174485,
             1871883252, 605846893, 222735214, 694388766,
             188312339, 2101442385, 2125204119, 2041095833,
             1895218768, 1384311643, 1334983095, 773370613, 1000004583,
             144443207, 720236707, 762772169, 437720306,
             939612284, 425414105, 1998078925, 981631283,
             1024155645, 822780843, 701857417,
             89865291, 898723423, 1859531344, 764283187,
             1349341884, 678622600, 778794064, 1319566104, 1277478588,
             538474442, 683102175, 999157082, 985046914,
             722594620, 1695858027, 1700738670, 1995749838,
             1147024708, 346983590, 565528207, 513791680,
             1072664641, 558746720, 1644999263, 358485174,
             1996632795, 2081634991, 1769370802, 349544396,
             1996610406, 1973272912]
    return seeds[seed_id]


def main():

    material_weights = [(0, 'Kg'), (52, 'Kg'), (10, 'Kg'), (34, 'Kg'), (7, 'Kg'), (99, 'Kg'), (15, 'Kg'), (6, 'Kg'), (9, 'Kg'), (0, 'Kg')]

    n_points = 10
    sigma = 0.005  # standard deviation

    # scenarios: Campinas, Belém, BH
    mean_lon = [-43.9438]
    mean_lat = [-19.9202]
    # lon: -47.068523   -48.47000   -43.9438
    # lat: -22.804202   -1.46000    -19.9202

    n_seeds = 1
    json_files = []

    for a in range(0, n_seeds):

        random.seed(get_seed(a))
        longitudes = [random.gauss(mean_lon[0], sigma) for i in range(n_points)]
        latitudes = [random.gauss(mean_lat[0], sigma) for i in range(n_points)]
        stop_points = [(latitudes[i], longitudes[i]) for i in range(len(latitudes))]
        stop_points.append((latitudes[0], longitudes[0]))  # mesmo ponto inicial e final
        paths, json_files = create_route(stop_points, material_weights, json_files)

    print(json_files)


if __name__ == "__main__":
    main()
