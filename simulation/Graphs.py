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

    files_result = [
        '../data/results/m43.96267779776494_m19.944747838679202_m43.929659815391865_m19.905049264605925_coords_weight',
        '../data/results/m43.96267779776494_m19.944747838679202_m43.929659815391865_m19.905049264605925_coords_impedance',
        '../data/results/m43.96267779776494_m19.944747838679202_m43.929659815391865_m19.905049264605925_coords_length',
    ]

    for i in range(len(files_result)):
        dados = dict(open_file(files_result[i]))
        paths = dados.get('path')

        fig, ax = ox.plot_graph_routes(G, paths, route_linewidth=7, node_size=0, bgcolor='w',
                                       bbox=(-19.910, -19.940, -43.932, -43.958), figsize=(7.7, 10))

        #ax.legend(loc='lower center', bbox_to_anchor=(0.5, 1),
        #              ncol=4, fancybox=True, shadow=True)


def plot_Belem():

    files_map = '../data/maps/m48.488877797764935_m1.484547838679201_m48.45585981539186_m1.4448492646059234.graphml'
    G = ox.load_graphml(files_map)

    files_result = [
        '../data/results/m48.488877797764935_m1.484547838679201_m48.45585981539186_m1.4448492646059234_coords_weight',
        '../data/results/m48.488877797764935_m1.484547838679201_m48.45585981539186_m1.4448492646059234_coords_impedance',
        '../data/results/m48.488877797764935_m1.484547838679201_m48.45585981539186_m1.4448492646059234_coords_length'
    ]

    for i in range(len(files_result)):
        dados = dict(open_file(files_result[i]))
        paths = dados.get('path')

        fig, ax = ox.plot_graph_routes(G, paths, route_linewidth=7, node_size=0, bgcolor='w', figsize=(7.7, 10), bbox=(-1.449, -1.479, -48.462, -48.488))


def plot_BH_2():

    files_map = '../data/maps/m43.96267779776494_m19.944747838679202_m43.929659815391865_m19.905049264605925.graphml'
    G = ox.load_graphml(files_map)

    files_result = [
        '../data/results/m43.96267779776494_m19.944747838679202_m43.929659815391865_m19.905049264605925_coords_weight',
        '../data/results/m43.96267779776494_m19.944747838679202_m43.929659815391865_m19.905049264605925_coords_impedance',
        '../data/results/m43.96267779776494_m19.944747838679202_m43.929659815391865_m19.905049264605925_coords_length',
    ]

    rotas = []
    for i in range(len(files_result)):
        paths = []
        dados = dict(open_file(files_result[i]))
        lista = dados.get('path')
        [paths.extend(i[:-1]) for i in lista]
        rotas.append(paths)

    fig, ax = ox.plot_graph_routes(G, rotas, ['r', 'b', 'g'], route_linewidth=7, node_size=0, bgcolor='w',
                                   bbox=(-19.910, -19.940, -43.932, -43.958), figsize=(7.7, 10))


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
    norm = plt.Normalize(vmin=min(list(nx.get_node_attributes(G, 'elevation').values())),
                         vmax=max(list(nx.get_node_attributes(G, 'elevation').values())))
    sm = mpl.cm.ScalarMappable(norm=norm, cmap=cmap)
    sm.set_array([])

    fig, ax = ox.plot_graph(G, node_color=nc, node_size=45, edge_linewidth=0.7, bgcolor='w', show=False)
    # pad: position of colorbar, shrink=.92: colorbar size
    cb = fig.colorbar(cm.ScalarMappable(norm=norm, cmap=cmap), ax=ax, orientation='vertical', shrink=.94, fraction=0.15,
                      pad=-0.0001)
    cb.ax.tick_params(labelsize=25)
    cb.set_label('Altitude (m)', fontsize=25, labelpad=23, fontweight='bold')
    plt.show()


def plot_work():

    files_result = [
        '../data/results/m43.96267779776494_m19.944747838679202_m43.929659815391865_m19.905049264605925_coords_weight',
        '../data/results/m43.96267779776494_m19.944747838679202_m43.929659815391865_m19.905049264605925_coords_impedance',
        '../data/results/m43.96267779776494_m19.944747838679202_m43.929659815391865_m19.905049264605925_coords_length',
    ]
    values = []
    for i in range(len(files_result)):
        dados = dict(open_file(files_result[i]))
        values.append(float(dados.get('work_total')) / 1000)

    fig, ax = plt.subplots()

    space = [1 * 0.2, 2 * 0.2, 3 * 0.2, 4 * 0.2]
    labels = ['Mean Speed', 'Total Fuel', 'Time']
    xticklabels = ['Minimiza trabalho', 'Minimiza aclives', 'Minimiza distância']

    color = "red"
    hatch = '|'

    color = ['#1d3557', '#457b9d', '#a8dadc']
    hatch = ["/", ".", "o"]

    ax.bar([0.4],
           [values[0],
            ],
           label=labels[0],
           width=0.2,
           alpha=0.9,
           edgecolor='black',
           # hatch='.',
           color='#1d3557',
           capsize=2)

    ax.bar([1.4],
           [values[1],
            ],
           label=labels[1],
           width=0.2,
           alpha=0.9,
           edgecolor='black',
           # hatch='/',
           color='#457b9d',
           capsize=2)

    ax.bar([2.4],
           [values[2],
            ],
           label=labels[2],
           width=0.2,
           alpha=0.9,
           edgecolor='black',
           # hatch='..',
           color='#a8dadc',
           capsize=2)

    ax.set_ylabel('Trabalho Total (kJ)', fontweight='bold')
    ax.set_xlabel('Estratégia', fontweight='bold')
    ax.set_xticks(np.arange(len(xticklabels)) + 0.4)
    ax.set_xticklabels(xticklabels)
    # ax.legend(loc='lower center', bbox_to_anchor=(0.5, 1),
    #               ncol=4, fancybox=True, shadow=True)

    ax.grid(linestyle='--', axis='y', alpha=0.4, color='black')
    plt.show()


def plot_work_belem():

    files_result = [
        '../data/results/m48.488877797764935_m1.484547838679201_m48.45585981539186_m1.4448492646059234_coords_weight_speed_True',
        '../data/results/m48.488877797764935_m1.484547838679201_m48.45585981539186_m1.4448492646059234_coords_impedance_speed_True',
        '../data/results/m48.488877797764935_m1.484547838679201_m48.45585981539186_m1.4448492646059234_coords_length_speed_True'
    ]
    values = []
    for i in range(len(files_result)):
        dados = dict(open_file(files_result[i]))
        values.append(float(dados.get('work_total')) / 1000)

    fig, ax = plt.subplots()

    space = [1 * 0.2, 2 * 0.2, 3 * 0.2, 4 * 0.2]
    labels = ['Mean Speed', 'Total Fuel', 'Time']
    xticklabels = ['Minimiza trabalho', 'Minimiza aclives', 'Minimiza distância']

    color = "red"
    hatch = '|'

    color = ['#1d3557', '#457b9d', '#a8dadc']
    hatch = ["/", ".", "o"]

    ax.bar([0.4],
           [values[0],
            ],
           label=labels[0],
           width=0.2,
           alpha=0.9,
           edgecolor='black',
           # hatch='.',
           color='#1d3557',
           capsize=2)

    ax.bar([1.4],
           [values[1],
            ],
           label=labels[1],
           width=0.2,
           alpha=0.9,
           edgecolor='black',
           # hatch='/',
           color='#457b9d',
           capsize=2)

    ax.bar([2.4],
           [values[2],
            ],
           label=labels[2],
           width=0.2,
           alpha=0.9,
           edgecolor='black',
           # hatch='..',
           color='#a8dadc',
           capsize=2)

    ax.set_ylabel('Trabalho Total (kJ)', fontweight='bold')
    ax.set_xlabel('Estratégia', fontweight='bold')
    ax.set_xticks(np.arange(len(xticklabels)) + 0.4)
    ax.set_xticklabels(xticklabels)
    # ax.legend(loc='lower center', bbox_to_anchor=(0.5, 1),
    #               ncol=4, fancybox=True, shadow=True)

    ax.grid(linestyle='--', axis='y', alpha=0.4, color='black')
    plt.show()


def plot_all_work_2():

    files_result = [
        '../data/results/m43.96267779776494_m19.944747838679202_m43.929659815391865_m19.905049264605925_coords_weight_speed_True',
        '../data/results/m43.96267779776494_m19.944747838679202_m43.929659815391865_m19.905049264605925_coords_impedance_speed_True',
        '../data/results/m43.96267779776494_m19.944747838679202_m43.929659815391865_m19.905049264605925_coords_length',
        '../data/results/m43.96267779776494_m19.944747838679202_m43.929659815391865_m19.905049264605925_coords_weight_speed_False',
        '../data/results/m43.96267779776494_m19.944747838679202_m43.929659815391865_m19.905049264605925_coords_impedance_speed_False',
    ]
    values = []
    for i in range(len(files_result)):
        dados = dict(open_file(files_result[i]))
        values.append(float(dados.get('work_total')) / 1000)

    fig, ax = plt.subplots()

    space = [1 * 0.2, 2 * 0.2, 3 * 0.2, 4 * 0.2]
    labels = ['Com fator velocidade', 'Sem fator velocidade']
    xticklabels = ['Minimiza trabalho', 'Minimiza aclives', 'Minimiza distância']

    color = "red"
    hatch = '|'

    color = ['#1d3557', '#457b9d', '#a8dadc']
    hatch = ["/", ".", "o"]

    ax.bar([0.4],
           [values[0],
            ],
           label=labels[0],
           width=0.1,
           alpha=0.9,
           edgecolor='black',
           #hatch='.',
           color='#457b9d',
           capsize=2)

    ax.bar([0.5],
           [values[3],
            ],
           label=labels[1],
           width=0.1,
           alpha=0.9,
           edgecolor='black',
           #hatch='/',
           color='#a8dadc',
           capsize=2)

    ax.bar([1.4],
           [values[1],
            ],
           #label=labels[0],
           width=0.1,
           alpha=0.9,
           edgecolor='black',
           #hatch='.',
           color='#457b9d',
           capsize=2)

    ax.bar([1.5],
           [values[4],
            ],
           #label=labels[1],
           width=0.1,
           alpha=0.9,
           edgecolor='black',
           #hatch='/',
           color='#a8dadc',
           capsize=2)

    ax.bar([2.4],
           [values[2],
            ],
           #label=labels[0],
           width=0.1,
           alpha=0.9,
           edgecolor='black',
           #hatch='.',
           color='#457b9d',
           capsize=2)

    ax.bar([2.5],
           [values[2],
            ],
           #label=labels[1],
           width=0.1,
           alpha=0.9,
           edgecolor='black',
           #hatch='/',
           color='#a8dadc',
           capsize=2)

    ax.set_ylabel('Trabalho Total (kJ)', fontweight='bold')
    ax.set_xlabel('Estratégia', fontweight='bold')
    ax.set_xticks(np.arange(len(xticklabels)) + 0.4)
    ax.set_xticklabels(xticklabels)
    ax.legend(loc='lower center', bbox_to_anchor=(0.5, 1),
                   ncol=2, fancybox=True, shadow=True)

    ax.grid(linestyle='--', axis='y', alpha=0.4, color='black')
    plt.show()


def plot_all_work():

    files_result = [
        '../data/results/m43.96267779776494_m19.944747838679202_m43.929659815391865_m19.905049264605925_coords_weight_speed_True',
        '../data/results/m43.96267779776494_m19.944747838679202_m43.929659815391865_m19.905049264605925_coords_impedance_speed_True',
        '../data/results/m43.96267779776494_m19.944747838679202_m43.929659815391865_m19.905049264605925_coords_length',
        '../data/results/m48.488877797764935_m1.484547838679201_m48.45585981539186_m1.4448492646059234_coords_weight_speed_True',
        '../data/results/m48.488877797764935_m1.484547838679201_m48.45585981539186_m1.4448492646059234_coords_impedance_speed_True',
        '../data/results/m48.488877797764935_m1.484547838679201_m48.45585981539186_m1.4448492646059234_coords_length'
    ]
    values = []
    for i in range(len(files_result)):
        dados = dict(open_file(files_result[i]))
        values.append(float(dados.get('work_total')) / 1000)

    fig, ax = plt.subplots()

    space = [1 * 0.2, 2 * 0.2, 3 * 0.2, 4 * 0.2]
    labels = ['Mean Speed', 'Total Fuel', 'Time']
    xticklabels = ['Minimiza trabalho', 'Minimiza aclives', 'Minimiza distância']

    color = "red"
    hatch = '|'

    color = ['#1d3557', '#457b9d', '#a8dadc']
    hatch = ["/", ".", "o"]

    ax.bar([0.4],
           [values[0],
            ],
           label=labels[0],
           width=0.1,
           alpha=0.9,
           edgecolor='black',
           # hatch='.',
           color='#1d3557',
           capsize=2)

    ax.bar([0.5],
           [values[3],
            ],
           label=labels[0],
           width=0.1,
           alpha=0.9,
           edgecolor='black',
           # hatch='.',
           color='#1d3557',
           capsize=2)

    ax.bar([1.4],
           [values[1],
            ],
           label=labels[1],
           width=0.1,
           alpha=0.9,
           edgecolor='black',
           # hatch='/',
           color='#457b9d',
           capsize=2)

    ax.bar([1.5],
           [values[4],
            ],
           label=labels[1],
           width=0.1,
           alpha=0.9,
           edgecolor='black',
           # hatch='/',
           color='#457b9d',
           capsize=2)

    ax.bar([2.4],
           [values[2],
            ],
           label=labels[2],
           width=0.1,
           alpha=0.9,
           edgecolor='black',
           # hatch='..',
           color='#a8dadc',
           capsize=2)

    ax.bar([2.5],
           [values[5],
            ],
           label=labels[2],
           width=0.1,
           alpha=0.9,
           edgecolor='black',
           # hatch='..',
           color='#a8dadc',
           capsize=2)

    ax.set_ylabel('Trabalho Total (kJ)', fontweight='bold')
    ax.set_xlabel('Estratégia', fontweight='bold')
    ax.set_xticks(np.arange(len(xticklabels)) + 0.4)
    ax.set_xticklabels(xticklabels)
    # ax.legend(loc='lower center', bbox_to_anchor=(0.5, 1),
    #               ncol=4, fancybox=True, shadow=True)

    ax.grid(linestyle='--', axis='y', alpha=0.4, color='black')
    plt.show()


def plot_time():

    files_result = [
        '../data/results/m43.96267779776494_m19.944747838679202_m43.929659815391865_m19.905049264605925_weight.xml',
        '../data/results/m43.96267779776494_m19.944747838679202_m43.929659815391865_m19.905049264605925_impedance.xml',
        '../data/results/m43.96267779776494_m19.944747838679202_m43.929659815391865_m19.905049264605925_length.xml',
    ]

    times = []
    for i in range(len(files_result)):
        file = minidom.parse(files_result[i])
        tag = file.getElementsByTagName('tripinfo')
        duration = [float(node.attributes['duration'].value) for node in tag]
        times.append(duration[0])

    fig, ax = plt.subplots()

    # space = [1 * 0.2, 2 * 0.2, 3 * 0.2, 4 * 0.2]
    labels = ['Mean Speed', 'Total Fuel', 'Time']
    xticklabels = ['Minimiza trabalho', 'Minimiza aclives', 'Minimiza distância']

    # color = "red"
    # hatch = '|'

    # color = ['#1d3557', '#457b9d', '#a8dadc']
    hatch = ["/", ".", "o"]

    ax.bar([0.4],
           [times[0]/3600,
            ],
           label=labels[0],
           width=0.2,
           alpha=0.9,
           edgecolor='black',
           # hatch='.',
           color='#1d3557',
           capsize=2)

    ax.bar([1.4],
           [times[1]/3600,
            ],
           label=labels[1],
           width=0.2,
           alpha=0.9,
           edgecolor='black',
           # hatch='/',
           color='#457b9d',
           capsize=2)

    ax.bar([2.4],
           [times[2]/3600,
            ],
           label=labels[2],
           width=0.2,
           alpha=0.9,
           edgecolor='black',
           # hatch='..',
           color='#a8dadc',
           capsize=2)

    ax.set_ylabel('Tempo (h)', fontweight='bold')
    ax.set_xlabel('Estratégia', fontweight='bold')
    ax.set_xticks(np.arange(len(xticklabels)) + 0.4)
    ax.set_xticklabels(xticklabels)
    #ax.legend(loc='lower center', bbox_to_anchor=(0.5, 1),
    #               ncol=4, fancybox=True, shadow=True)

    ax.grid(linestyle='--', axis='y', alpha=0.4, color='black')
    plt.show()


def plot_all_time():

    files_result = [
        #'../data/results/m43.96267779776494_m19.944747838679202_m43.929659815391865_m19.905049264605925_weight.xml',
        #'../data/results/m43.96267779776494_m19.944747838679202_m43.929659815391865_m19.905049264605925_impedance.xml',
        #'../data/results/m43.96267779776494_m19.944747838679202_m43.929659815391865_m19.905049264605925_length.xml',
        '../data/results/m48.488877797764935_m1.484547838679201_m48.45585981539186_m1.4448492646059234_weight.xml',
        '../data/results/m48.488877797764935_m1.484547838679201_m48.45585981539186_m1.4448492646059234_impedance.xml',
        '../data/results/m48.488877797764935_m1.484547838679201_m48.45585981539186_m1.4448492646059234_length.xml'
    ]

    times = []
    for i in range(len(files_result)):
        file = minidom.parse(files_result[i])
        tag = file.getElementsByTagName('tripinfo')
        duration = [float(node.attributes['duration'].value) for node in tag]
        times.append(duration[0])

    fig, ax = plt.subplots()

    # space = [1 * 0.2, 2 * 0.2, 3 * 0.2, 4 * 0.2]
    labels = ['Mean Speed', 'Total Fuel', 'Time']
    xticklabels = ['Minimiza trabalho', 'Minimiza aclives', 'Minimiza distância']

    # color = "red"
    # hatch = '|'

    # color = ['#1d3557', '#457b9d', '#a8dadc']
    hatch = ["/", ".", "o"]

    ax.bar([0.4],
           [times[0]/3600,
            ],
           label=labels[0],
           width=0.1,
           alpha=0.9,
           edgecolor='black',
           # hatch='.',
           color='#1d3557',
           capsize=2)

    ax.bar([0.5],
           [times[3] / 3600,
            ],
           label=labels[0],
           width=0.1,
           alpha=0.9,
           edgecolor='black',
           # hatch='.',
           color='#1d3557',
           capsize=2)

    ax.bar([1.4],
           [times[1]/3600,
            ],
           label=labels[1],
           width=0.1,
           alpha=0.9,
           edgecolor='black',
           # hatch='/',
           color='#457b9d',
           capsize=2)

    ax.bar([1.5],
           [times[4] / 3600,
            ],
           label=labels[1],
           width=0.1,
           alpha=0.9,
           edgecolor='black',
           # hatch='/',
           color='#457b9d',
           capsize=2)

    ax.bar([2.4],
           [times[2]/3600,
            ],
           label=labels[2],
           width=0.1,
           alpha=0.9,
           edgecolor='black',
           # hatch='..',
           color='#a8dadc',
           capsize=2)

    ax.bar([2.5],
           [times[5] / 3600,
            ],
           label=labels[2],
           width=0.1,
           alpha=0.9,
           edgecolor='black',
           # hatch='..',
           color='#a8dadc',
           capsize=2)

    ax.set_ylabel('Tempo (h)', fontweight='bold')
    ax.set_xlabel('Estratégia', fontweight='bold')
    ax.set_xticks(np.arange(len(xticklabels)) + 0.4)
    ax.set_xticklabels(xticklabels)
    #ax.legend(loc='lower center', bbox_to_anchor=(0.5, 1),
    #               ncol=4, fancybox=True, shadow=True)

    ax.grid(linestyle='--', axis='y', alpha=0.4, color='black')
    plt.show()


if __name__ == '__main__':
    #plot_elevation()
    #plot_elevation_belem()
    #plot_work()
    #plot_work_belem()
    plot_all_work_2()
    #plot_BH()
    #plot_BH_2()
    #plot_time()
    #plot_all_time()
    # plot_Belem()

