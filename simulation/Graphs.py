import json
import osmnx as ox
import matplotlib.cm as cm
import matplotlib as mpl
import matplotlib.pyplot as plt
import networkx as nx
from route import Graph
import numpy as np
from xml.dom import minidom


def open_file(name_file):
    try:
        f = open(name_file + ".json", "r")
        dados = json.loads(f.read())
        f.close()
    except:
        dados = 0
        pass

    return dados


def plot_BH():

    files_map = '../data/maps/m43.96267779776494_m19.944747838679202_m43.929659815391865_m19.905049264605925.graphml'
    G = ox.load_graphml(files_map)
    #Graph.plot_graph(G)

    files_result = [
        #'../data/results/m43.96267779776494_m19.944747838679202_m43.929659815391865_m19.905049264605925_coords_weight_speed_True',
        '../data/results/m43.96267779776494_m19.944747838679202_m43.929659815391865_m19.905049264605925_0_coords_weight_speed_False',
        #'../data/results/m43.96267779776494_m19.944747838679202_m43.929659815391865_m19.905049264605925_coords_impedance_speed_True',
        '../data/results/m43.96267779776494_m19.944747838679202_m43.929659815391865_m19.905049264605925_0_coords_impedance_speed_False',
        #'../data/results/m43.96267779776494_m19.944747838679202_m43.929659815391865_m19.905049264605925_coords_length_speed_True',
        '../data/results/m43.96267779776494_m19.944747838679202_m43.929659815391865_m19.905049264605925_0_coords_distance_speed_False'
    ]

    for i in range(len(files_result)):
        dados = dict(open_file(files_result[i]))
        paths = dados.get('path')
        print(paths)

        fig, ax = ox.plot_graph_routes(G, paths, route_linewidth=7, node_size=0, bgcolor='w',# node_color='#A0CBE2',
                                       bbox=(-19.910, -19.940, -43.932, -43.958), figsize=(7.7, 10))

        #ax.legend(loc='lower center', bbox_to_anchor=(0.5, 1),
        #              ncol=4, fancybox=True, shadow=True)


def plot_Belem():

    files_map = '../data/maps/m48.488877797764935_m1.484547838679201_m48.45585981539186_m1.4448492646059234.graphml'
    G = ox.load_graphml(files_map)

    files_result = [
        '../data/results/m48.488877797764935_m1.484547838679201_m48.45585981539186_m1.4448492646059234_0_coords_weight_speed_False',
        '../data/results/m48.488877797764935_m1.484547838679201_m48.45585981539186_m1.4448492646059234_0_coords_impedance_speed_False',
        '../data/results/m48.488877797764935_m1.484547838679201_m48.45585981539186_m1.4448492646059234_0_coords_distance_speed_False'
        #'../data/results/m48.488877797764935_m1.484547838679201_m48.45585981539186_m1.4448492646059234_coords_impedance_speed_True',
        #'../data/results/m48.488877797764935_m1.484547838679201_m48.45585981539186_m1.4448492646059234_coords_length_speed_True'
    ]

    for i in range(len(files_result)):
        dados = dict(open_file(files_result[i]))
        paths = dados.get('path')

        fig, ax = ox.plot_graph_routes(G, paths, route_linewidth=7, node_size=0, bgcolor='w', figsize=(7.7, 10), bbox=(-1.449, -1.479, -48.462, -48.488))


def plot_BH_2():

    files_map = '../data/maps/m43.96267779776494_m19.944747838679202_m43.929659815391865_m19.905049264605925.graphml'
    G = ox.load_graphml(files_map)

    files_result = [
        '../data/results/m43.96267779776494_m19.944747838679202_m43.929659815391865_m19.905049264605925_coords_weight_speed_False',
        '../data/results/m43.96267779776494_m19.944747838679202_m43.929659815391865_m19.905049264605925_coords_weight_speed_True'
    ]

    rotas = []
    for i in range(len(files_result)):
        paths = []
        dados = dict(open_file(files_result[i]))
        lista = dados.get('path')
        [paths.append(i[:-1]) for i in lista] #extend
        rotas.extend(paths)

    #
    fig, ax = ox.plot_graph_routes(G, rotas, ['g','g','g','g','g','g','g','g','g', 'r','r','r','r','r','r','r','r', 'r'], route_linewidth=7, node_size=0, bgcolor='w',
                                   bbox=(-19.910, -19.940, -43.932, -43.958), figsize=(7.7, 10), route_alpha=.5, orig_dest_size=200)


def plot_edge_grades():
    files_map = '../data/maps/m43.96267779776494_m19.944747838679202_m43.929659815391865_m19.905049264605925.graphml'
    G = ox.load_graphml(files_map)

    max_lat = -19.910
    min_lat = -19.940
    max_lon = -43.958
    min_lon = -43.932

    name_geotiff = '../data/maps/19S45_ZN.tif'
    G = ox.graph_from_bbox(max_lat, min_lat, max_lon, min_lon, network_type='all')
    G = Graph.set_node_elevation(G, name_geotiff)
    deadends = [(u, v) for u, v, k, data in G.edges(keys=True, data=True) if data['highway'] == '']
    # print(deadends)
    # G2.remove_nodes_from(deadends)
    G = Graph.edge_grades(G)
    G_proj = ox.project_graph(G)
    ec = ox.plot.get_edge_colors_by_attr(G_proj, "grade", cmap="plasma", num_bins=5, equal_size=True)
    fig, ax = ox.plot_graph(G_proj, edge_color=ec, edge_linewidth=0.5, node_size=0, bgcolor="w")


def plot_elevation():

    files_map = '../data/maps/m43.96267779776494_m19.944747838679202_m43.929659815391865_m19.905049264605925.graphml'
    G = ox.load_graphml(files_map)

    max_lat = -19.910
    min_lat = -19.940
    max_lon = -43.958
    min_lon = -43.932

    name_geotiff = '../data/maps/19S45_ZN.tif'
    G = ox.graph_from_bbox(max_lat, min_lat, max_lon, min_lon, network_type='all')
    G = Graph.set_node_elevation(G, name_geotiff)
    G = Graph.edge_grades(G)
    # G_proj = ox.project_graph(G)
    nc = ox.plot.get_node_colors_by_attr(G, 'elevation', cmap='plasma', num_bins=10)  # , start=0, stop=1
    cmap = plt.cm.get_cmap('plasma')
    #norm = plt.Normalize(vmin= 0, vmax=max(list(nx.get_node_attributes(G, 'elevation').values())) - min(list(nx.get_node_attributes(G, 'elevation').values())))
    print("BH", max(list(nx.get_node_attributes(G, 'elevation').values()))-
          min(list(nx.get_node_attributes(G, 'elevation').values())))
    norm = plt.Normalize(vmin=min(list(nx.get_node_attributes(G, 'elevation').values())),
                         vmax=max(list(nx.get_node_attributes(G, 'elevation').values())))
    sm = mpl.cm.ScalarMappable(norm=norm, cmap=cmap)
    sm.set_array([])

    fig, ax = ox.plot_graph(G, node_color=nc, node_size=35, edge_linewidth=0.7, bgcolor='w', show=False)
    # pad: position of colorbar, shrink=.92: colorbar size
    cb = fig.colorbar(cm.ScalarMappable(norm=norm, cmap=cmap), ax=ax, orientation='vertical', shrink=.94, fraction=0.15,
                      pad=-0.0001)
    cb.ax.tick_params(labelsize=25)
    cb.set_label('Altitude (m)', fontsize=25, labelpad=23, fontweight='bold')
    plt.show()


def plot_elevation_belem():

    files_map = '../data/maps/m48.488877797764935_m1.484547838679201_m48.45585981539186_m1.4448492646059234.graphml'
    G = ox.load_graphml(files_map)

    max_lat = -1.449
    min_lat = -1.479
    max_lon = -48.462
    min_lon = -48.488

    name_geotiff = '../data/maps/01S495ZN.tif'
    G = ox.graph_from_bbox(max_lat, min_lat, max_lon, min_lon, network_type='all')
    G = Graph.set_node_elevation(G, name_geotiff)
    G = Graph.edge_grades(G)
    # G_proj = ox.project_graph(G)
    nc = ox.plot.get_node_colors_by_attr(G, 'elevation', cmap='plasma', num_bins=10)  # , start=0, stop=1
    cmap = plt.cm.get_cmap('plasma')
    print("belem", max(list(nx.get_node_attributes(G, 'elevation').values()))-
          min(list(nx.get_node_attributes(G, 'elevation').values())))
    norm = plt.Normalize(vmin=min(list(nx.get_node_attributes(G, 'elevation').values())), vmax=max(list(nx.get_node_attributes(G, 'elevation').values())))
    sm = mpl.cm.ScalarMappable(norm=norm, cmap=cmap)
    sm.set_array([])

    fig, ax = ox.plot_graph(G, node_color=nc, node_size=45, edge_linewidth=0.7, bgcolor='w', show=False)
    # pad: position of colorbar, shrink=.92: colorbar size
    cb = fig.colorbar(cm.ScalarMappable(norm=norm, cmap=cmap), ax=ax, orientation='vertical', shrink=.94, fraction=0.15,
                      pad=-0.0001)
    cb.ax.tick_params(labelsize=25)
    cb.set_label('Elevação (m)', fontsize=25, labelpad=23, fontweight='bold')
    plt.show()




if __name__ == '__main__':
    #plot_elevation()
    #plot_elevation_belem()
    #plot_all_work_2()
    plot_BH()
    #plot_edge_grades()
    #plot_Belem()
    #plot_BH_2()

