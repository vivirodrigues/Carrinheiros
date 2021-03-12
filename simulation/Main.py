from __future__ import division
import os
import sys
import subprocess
import random
import socket
import threading
import time
from route import Graph
import json
from decimal import Decimal, ROUND_HALF_UP
import Constants
from route import Scenario
from geography import GeoTiff, OpenSteetMap, Coordinates
from route import Graph_Collect
from simulation import Map_osm
import Carrinheiro
import osmnx as ox


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
    if sumo.returncode != None:
        os.system("taskkill.exe /F /im sumo.exe")
        time.sleep(1)
    """
    if sumo.returncode == None:
        os.kill(sumo.pid, signal.SIGILL)
        # time.sleep(0.5)
        if sumo.returncode == None:
            os.kill(sumo.pid, signal.SIGKILL)
            # time.sleep(1)
            if sumo.returncode == None:
                time.sleep(0.5)
    """


def calculate_work(speed, accel, slope):
    pass


def run(route):
    # speedList = []
    # fuelList = []
    # pdfSpeed = [0] * 110
    # pdfFuel = [0] * 30

    total = 0

    step = 1
    consumption = 0
    totalConsumption = 0

    dados = []

    # adition = Simulation.Vehicles.add1(traci)
    traci.route.add("path", route)
    traci.vehicle.add("carrinheiro", "path")
    traci.vehicle.setParameter("carrinheiro", "carFollowModel", "KraussPS")
    traci.vehicle.setVehicleClass("carrinheiro", "pedestrian")
    traci.vehicle.setShapeClass("carrinheiro", "pedestrian")
    traci.vehicle.setMaxSpeed("carrinheiro", 1)  # aprox 8 km/h
    traci.vehicle.setLateralAlignment("carrinheiro", "right") # or "nice"

    while step == 1 or traci.simulation.getMinExpectedNumber() > 0:

        speedI = traci.vehicle.getSpeed("carrinheiro")

        if speedI < -100:
            speedI = float(0)

        speed = speedI * 3.6  # m/s para km/h

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

        traci.simulationStep()
        vehicles = traci.simulation.getEndingTeleportIDList()

        for vehicle in vehicles:
            traci.vehicle.remove(vehicle, reason=4)

        step += 1

    """
    for i in range(len(pdfSpeed)):
        pdfSpeed[i] = (pdfSpeed[i] / total) * 100
        sett = {i: pdfSpeed[i]}
        dicionarioSpeed.update(sett)
    """
    traci.close()
    sys.stdout.flush()
    # writeJson1(dicionarioMap, 'map' + file)
    return totalConsumption


def start_simulation(sumo, scenario, output, route):
    unused_port_lock = UnusedPortLock()
    unused_port_lock.__enter__()
    remote_port = find_unused_port()

    sumo = subprocess.Popen(
        [sumo, "-c", scenario, "--tripinfo-output", output, "--device.emissions.probability", "1.0", "--remote-port",
         str(remote_port), "--duration-log.statistics", "--log", "logfile.txt"], stdout=sys.stdout, stderr=sys.stderr)
    unused_port_lock.release()

    try:
        traci.init(remote_port)
        consumption = run(route)
    except Exception as e:
        print(e)
        raise
    finally:
        # print("Terminating SUMO")
        terminate_sumo(sumo)
        unused_port_lock.__exit__()

    return consumption


def writeJson(content, fileName):
    with open('results/rotas5/' + fileName + '.json', 'w') as json_file:
        json.dump(content, json_file, separators=(',', ':'), ensure_ascii=False, sort_keys=True, indent=4)


def writeJson1(content, fileName):
    with open('results/PDF/' + fileName + '.json', 'w') as json_file:
        json.dump(content, json_file, separators=(',', ':'), ensure_ascii=False, sort_keys=True, indent=4)


def geotiff_transformation(name_file_in, name_file_out):
    gdal_command = "gdal_translate -of GTiff -ot Int16 -co TFW=YES " + name_file_in + " " + name_file_out
    process_gdal = subprocess.Popen(gdal_command.split(), stdout=subprocess.PIPE)
    output, error = process_gdal.communicate()


def netconvert_geotiff(name_file_osm, name_file_geotiff, name_file_output):
    netconvert_command = "netconvert --osm-files " + name_file_osm + " --heightmap.geotiff " + name_file_geotiff + " -o "+ name_file_output
    process_netconvert = subprocess.Popen(netconvert_command.split(), stdout=subprocess.PIPE)
    output, error = process_netconvert.communicate()


def create_route(stop_points, material_weights):

    name_file_net = 'map.net.xml'
    sumo_config = "map.sumocfg"
    geotiff_name_out = Constants.MAPS_DIRECTORY + 'out.tif'

    # download the osm file (scenario)
    osm_file_name = OpenSteetMap.file_osm(Constants.MAPS_DIRECTORY, stop_points)

    # download the GeoTiff file (scenario)
    geotiff_name = GeoTiff.geotiff(Constants.MAPS_DIRECTORY, stop_points)

    geotiff_name = Constants.MAPS_DIRECTORY + geotiff_name + '.tif'

    geotiff_transformation(geotiff_name, geotiff_name_out)

    dict_edges_net = Map_osm.edges_net(name_file_net)

    max_lat, min_lat, max_lon, min_lon = Coordinates.create_osmnx(stop_points)

    # Scenario graph (paths are edges and junctions are nodes)
    G = ox.graph_from_bbox(max_lat, min_lat, max_lon, min_lon, network_type='all')

    G, nodes_coordinates, nodes_mass_increment = Graph.configure_graph_simulation(G, geotiff_name, stop_points, material_weights, osm_file_name)

    H = Graph_Collect.create_graph_route(nodes_coordinates, nodes_mass_increment)

    node_source = list(nodes_coordinates.keys())[0]
    node_target = list(nodes_coordinates.keys())[-1]

    cost_total, paths = Carrinheiro.closest_insertion_path(G, H, node_source, node_target)

    sumo_route = []
    for i in paths:
        sumo_route.extend(Map_osm.nodes_to_edges(i, dict_edges_net))

    print(sumo_route)

    start_simulation('sumo', sumo_config, 'out.xml', sumo_route)

    for i in paths:
        fig, ax = ox.plot_graph_route(G, i, route_linewidth=6, node_size=0, bgcolor='w')


    return paths


def main():

    stop_points = [(-1.4690963838114115, -48.47907737431437), (-1.4669727715675633, -48.47476438242888),
                   (-1.4617914926718831, -48.48735602308006), (-1.4552257213149151, -48.476854602085865),
                   (-1.4570295065392669, -48.46451272534284), (-1.473840715457675, -48.4597131060169)]

    material_weights = [(15, 'Kg'), (52, 'Kg'), (10, 'Kg'), (34, 'Kg'), (17, 'Kg'), (99, 'Kg')]

    a = random.seed(1973272912)
    mu = -48.4790
    sigma = 0.001 # standard deviation
    print(random.gauss(mu, sigma))

    # paths = create_route(stop_points, material_weights)

    # consumption = start_simulation("sumo", sumo_config, "output.xml", sumo_route)


if __name__ == "__main__":
    main()
