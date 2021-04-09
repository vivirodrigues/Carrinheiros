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


def plot_all_work():

    files_result = [
        '../data/results/m43.96267779776494_m19.944747838679202_m43.929659815391865_m19.905049264605925_coords_weight',
        '../data/results/m43.96267779776494_m19.944747838679202_m43.929659815391865_m19.905049264605925_coords_impedance',
        '../data/results/m43.96267779776494_m19.944747838679202_m43.929659815391865_m19.905049264605925_coords_length',
        '../data/results/m48.488877797764935_m1.484547838679201_m48.45585981539186_m1.4448492646059234_coords_weight',
        '../data/results/m48.488877797764935_m1.484547838679201_m48.45585981539186_m1.4448492646059234_coords_impedance',
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
        '../data/results/m43.96267779776494_m19.944747838679202_m43.929659815391865_m19.905049264605925_weight.xml',
        '../data/results/m43.96267779776494_m19.944747838679202_m43.929659815391865_m19.905049264605925_impedance.xml',
        '../data/results/m43.96267779776494_m19.944747838679202_m43.929659815391865_m19.905049264605925_length.xml',
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


def plot_pdf():

    files_result = [
        '../data/results/m43.96267779776494_m19.944747838679202_m43.929659815391865_m19.905049264605925_weight_pdf',
        '../data/results/m43.96267779776494_m19.944747838679202_m43.929659815391865_m19.905049264605925_impedance_pdf',
        '../data/results/m43.96267779776494_m19.944747838679202_m43.929659815391865_m19.905049264605925_length_pdf',
    ]

    dados = dict(open_file(files_result[0]))
    x1 = np.array(list(map(int, dados.keys())))
    y1 = np.array(list(dados.values()))

    dados = dict(open_file(files_result[1]))
    x2 = np.array(list(map(int, dados.keys())))
    y2 = np.array(list(dados.values()))

    dados = dict(open_file(files_result[2]))
    x3 = np.array(list(map(int, dados.keys())))
    y3 = np.array(list(dados.values()))

    fig = plt.figure(figsize=(15, 5))

    lim_x_inf = min(min(x1), min(x2), min(x3))
    lim_x_sup = max(max(x1), max(x2), max(x3))

    lim_y_inf = min(min(y1), min(y2), min(y3))
    lim_y_sup = max(max(y1), max(y2), max(y3))

    plt.xlim(lim_x_inf-1, 40)
    plt.ylim(lim_y_inf, lim_y_sup+0.5)

    space = 0.5
    new = [i for i in range(0,40)]

    plt.bar(x1[:40] + 0.5 * space, y1[:40], label='Minimiza trabalho', color='tab:blue', width=0.3)
    plt.bar(x2[:40] - 0.5*space, y2[:40], label='Minimiza aclives', color='tab:pink', width=0.3)
    plt.bar(x3[:40] + 0.0*space, y3[:40], label='Minimiza distância', color='tab:red', width=0.3)

    #plt.ylabel('Empirical Probability Density Function (%)', fontweight="bold")
    plt.ylabel('Função Densidade de Probabilidade (%)', fontweight="bold")
    plt.xlabel('Potência instantânea', fontweight="bold")

    plt.xticks(new)
    plt.legend(numpoints=1, loc="upper right", ncol=3)  # ,bbox_to_anchor=(-0.02, 1.15)
    plt.grid(True, which="both", ls="-", linewidth=0.1, color='0.10', zorder=0)
    plt.show()
    plt.close()


def plot_all_cdf():

    files_result = [
        '../data/results/m43.96267779776494_m19.944747838679202_m43.929659815391865_m19.905049264605925_weight_pdf',
        '../data/results/m43.96267779776494_m19.944747838679202_m43.929659815391865_m19.905049264605925_impedance_pdf',
        '../data/results/m43.96267779776494_m19.944747838679202_m43.929659815391865_m19.905049264605925_length_pdf',
        '../data/results/m48.488877797764935_m1.484547838679201_m48.45585981539186_m1.4448492646059234_weight_pdf',
        '../data/results/m48.488877797764935_m1.484547838679201_m48.45585981539186_m1.4448492646059234_impedance_pdf',
        '../data/results/m48.488877797764935_m1.484547838679201_m48.45585981539186_m1.4448492646059234_length_pdf'
    ]

    dados = dict(open_file(files_result[0]))
    x1 = np.array(list(map(int, dados.keys())))
    cdf1 = list(dados.values())
    cumulative = 0
    for i in range(len(cdf1)):
        cumulative += cdf1[i]
        cdf1[i] = cumulative

    dados = dict(open_file(files_result[1]))
    x2 = np.array(list(map(int, dados.keys())))
    cdf2 = list(dados.values())
    cumulative = 0
    for i in range(len(cdf2)):
        cumulative += cdf2[i]
        cdf2[i] = cumulative

    dados = dict(open_file(files_result[2]))
    x3 = np.array(list(map(int, dados.keys())))
    cdf3 = list(dados.values())
    cumulative = 0
    for i in range(len(cdf3)):
        cumulative += cdf3[i]
        cdf3[i] = cumulative

    dados = dict(open_file(files_result[3]))
    x4 = np.array(list(map(int, dados.keys())))
    cdf4 = list(dados.values())
    cumulative = 0
    for i in range(len(cdf4)):
        cumulative += cdf4[i]
        cdf4[i] = cumulative

    dados = dict(open_file(files_result[4]))
    x5 = np.array(list(map(int, dados.keys())))
    cdf5 = list(dados.values())
    cumulative = 0
    for i in range(len(cdf5)):
        cumulative += cdf5[i]
        cdf5[i] = cumulative

    dados = dict(open_file(files_result[5]))
    x6 = np.array(list(map(int, dados.keys())))
    cdf6 = list(dados.values())
    cumulative = 0
    for i in range(len(cdf6)):
        cumulative += cdf6[i]
        cdf6[i] = cumulative

    fig = plt.figure(1)

    yMax = max(cdf1) or max(cdf2)
    yMim = min(cdf1) and min(cdf2)

    xMax = 400
    xMim = min(x1) - 5

    plt.xlim(xMim, xMax)

    plt.xticks(rotation="horizontal")

    plt.grid(True, which="both", ls="-", linewidth=0.1, color='0.10', zorder=0)

    plt.errorbar(x1, cdf1, ls='-', label='Minimiza trabalho 1', color='tab:orange', zorder=3)
    plt.errorbar(x2, cdf2, ls='-', label='Minimiza aclives 1', color='tab:blue', zorder=3)
    plt.errorbar(x3, cdf3, ls='-', label='Minimiza distância 1', color='tab:pink', zorder=3)
    plt.errorbar(x4, cdf4, ls='-', label='Minimiza trabalho 2', color='tab:green', zorder=3)
    plt.errorbar(x5, cdf5, ls='-', label='Minimiza aclives 2', color='tab:red', zorder=3)
    plt.errorbar(x6, cdf6, ls='-', label='Minimiza distância 2', color='tab:purple', zorder=3)

    ylabel = 'Função de Distribuição Acumulada Empírica (%)'
    xlabel = 'Potência instantânea (W)'

    plt.ylabel(ylabel, fontweight="bold")
    plt.xlabel(xlabel, fontweight="bold")

    plt.legend(numpoints=1, loc="lower right", ncol=1)  # ,bbox_to_anchor=(-0.02, 1.15)
    plt.show()
    plt.close(fig)


def plot_cdf_BH():

    files_result = [
        '../data/results/m43.96267779776494_m19.944747838679202_m43.929659815391865_m19.905049264605925_weight_pdf',
        '../data/results/m43.96267779776494_m19.944747838679202_m43.929659815391865_m19.905049264605925_impedance_pdf',
        '../data/results/m43.96267779776494_m19.944747838679202_m43.929659815391865_m19.905049264605925_length_pdf'
    ]

    dados = dict(open_file(files_result[0]))
    x1 = np.array(list(map(int, dados.keys())))
    cdf1 = list(dados.values())
    cumulative = 0
    for i in range(len(cdf1)):
        cumulative += cdf1[i]
        cdf1[i] = cumulative

    dados = dict(open_file(files_result[1]))
    x2 = np.array(list(map(int, dados.keys())))
    cdf2 = list(dados.values())
    cumulative = 0
    for i in range(len(cdf2)):
        cumulative += cdf2[i]
        cdf2[i] = cumulative

    dados = dict(open_file(files_result[2]))
    x3 = np.array(list(map(int, dados.keys())))
    cdf3 = list(dados.values())
    cumulative = 0
    for i in range(len(cdf3)):
        cumulative += cdf3[i]
        cdf3[i] = cumulative

    fig = plt.figure(1)

    yMax = max(cdf1) or max(cdf2)
    yMim = min(cdf1) and min(cdf2)

    xMax = 400
    xMim = min(x1) - 5

    plt.xlim(xMim, xMax)

    plt.xticks(rotation="horizontal")

    plt.grid(True, which="both", ls="-", linewidth=0.1, color='0.10', zorder=0)

    plt.errorbar(x1, cdf1, ls='-', label='Minimiza trabalho', color='tab:orange', zorder=3)
    plt.errorbar(x2, cdf2, ls='-', label='Minimiza aclives', color='tab:blue', zorder=3)
    plt.errorbar(x3, cdf3, ls='-', label='Minimiza distância', color='tab:pink', zorder=3)

    ylabel = 'Função de Distribuição Acumulada Empírica (%)'
    xlabel = 'Potência instantânea (W)'

    plt.ylabel(ylabel, fontweight="bold")
    plt.xlabel(xlabel, fontweight="bold")

    plt.legend(numpoints=1, loc="lower right", ncol=1)  # ,bbox_to_anchor=(-0.02, 1.15)
    plt.show()
    plt.close(fig)


def plot_cdf_belem():

    files_result = [
        '../data/results/m48.488877797764935_m1.484547838679201_m48.45585981539186_m1.4448492646059234_weight_pdf',
        '../data/results/m48.488877797764935_m1.484547838679201_m48.45585981539186_m1.4448492646059234_impedance_pdf',
        '../data/results/m48.488877797764935_m1.484547838679201_m48.45585981539186_m1.4448492646059234_length_pdf'
    ]

    dados = dict(open_file(files_result[0]))
    x1 = np.array(list(map(int, dados.keys())))
    cdf1 = list(dados.values())
    cumulative = 0
    for i in range(len(cdf1)):
        cumulative += cdf1[i]
        cdf1[i] = cumulative

    dados = dict(open_file(files_result[1]))
    x2 = np.array(list(map(int, dados.keys())))
    cdf2 = list(dados.values())
    cumulative = 0
    for i in range(len(cdf2)):
        cumulative += cdf2[i]
        cdf2[i] = cumulative

    dados = dict(open_file(files_result[2]))
    x3 = np.array(list(map(int, dados.keys())))
    cdf3 = list(dados.values())
    cumulative = 0
    for i in range(len(cdf3)):
        cumulative += cdf3[i]
        cdf3[i] = cumulative

    fig = plt.figure(1)

    yMax = max(cdf1) or max(cdf2)
    yMim = min(cdf1) and min(cdf2)

    xMax = 140
    xMim = min(x1) - 5

    plt.xlim(xMim, xMax)

    plt.xticks(rotation="horizontal")

    plt.grid(True, which="both", ls="-", linewidth=0.1, color='0.10', zorder=0)

    plt.errorbar(x1, cdf1, ls='-', label='Minimiza trabalho', color='tab:orange', zorder=3)
    plt.errorbar(x2, cdf2, ls='-', label='Minimiza aclives', color='tab:blue', zorder=3)
    plt.errorbar(x3, cdf3, ls='-', label='Minimiza distância', color='tab:pink', zorder=3)

    ylabel = 'Função de Distribuição Acumulada Empírica (%)'
    xlabel = 'Potência instantânea (W)'

    plt.ylabel(ylabel, fontweight="bold")
    plt.xlabel(xlabel, fontweight="bold")

    plt.legend(numpoints=1, loc="lower right", ncol=1)  # ,bbox_to_anchor=(-0.02, 1.15)
    plt.show()
    plt.close(fig)


def plot_pdf_speed_BH():

    files_result = [
        #'../data/results/m43.96267779776494_m19.944747838679202_m43.929659815391865_m19.905049264605925_weight_pdf_speeds_True',
        #'../data/results/m43.96267779776494_m19.944747838679202_m43.929659815391865_m19.905049264605925_weight_pdf_speeds_False',
        #'../data/results/m43.96267779776494_m19.944747838679202_m43.929659815391865_m19.905049264605925_impedance_pdf_speeds_True',
        #'../data/results/m43.96267779776494_m19.944747838679202_m43.929659815391865_m19.905049264605925_impedance_pdf_speeds_False',
        #'../data/results/m43.96267779776494_m19.944747838679202_m43.929659815391865_m19.905049264605925_length_pdf_speeds_True',
        '../data/results/m48.488877797764935_m1.484547838679201_m48.45585981539186_m1.4448492646059234_weight_pdf_speeds_True',
        '../data/results/m48.488877797764935_m1.484547838679201_m48.45585981539186_m1.4448492646059234_weight_pdf_speeds_False',
        '../data/results/m48.488877797764935_m1.484547838679201_m48.45585981539186_m1.4448492646059234_impedance_pdf_speeds_True',
        '../data/results/m48.488877797764935_m1.484547838679201_m48.45585981539186_m1.4448492646059234_impedance_pdf_speeds_False',
        '../data/results/m48.488877797764935_m1.484547838679201_m48.45585981539186_m1.4448492646059234_length_pdf_speeds_True',

    ]
    #'../data/results/m43.96267779776494_m19.944747838679202_m43.929659815391865_m19.905049264605925_weight_pdf_speeds_False'

    dados = dict(open_file(files_result[0]))
    x1 = np.array(list(map(int, dados.keys())))
    y1 = np.array(list(dados.values()))

    dados = dict(open_file(files_result[1]))
    x2 = np.array(list(map(int, dados.keys())))
    y2 = np.array(list(dados.values()))

    dados = dict(open_file(files_result[2]))
    x3 = np.array(list(map(int, dados.keys())))
    y3 = np.array(list(dados.values()))

    dados = dict(open_file(files_result[3]))
    x4 = np.array(list(map(int, dados.keys())))
    y4 = np.array(list(dados.values()))

    dados = dict(open_file(files_result[4]))
    x5 = np.array(list(map(int, dados.keys())))
    y5 = np.array(list(dados.values()))

    fig = plt.figure(figsize=(15, 5))

    lim_x_inf = min(min(x1), min(x2), min(x3))
    lim_x_sup = max(max(x1), max(x2), max(x3))

    lim_y_inf = min(min(y1), min(y2), min(y3))
    lim_y_sup = max(max(y1), max(y2), max(y3))

    plt.xlim(lim_x_inf-1, lim_x_sup)
    plt.ylim(lim_y_inf, lim_y_sup+0.5)

    space = 0.5
    new = [i for i in range(0, lim_x_sup)]

    #plt.bar(x1[:lim_x_sup] + 0.5 * space, y1[:lim_x_sup], label='Minimiza trabalho com puni', color='tab:blue', width=0.3)
    #plt.bar(x2[:lim_x_sup] - 0.5 * space, y2[:lim_x_sup], label='Minimiza trabalho sem puni', color='tab:pink', width=0.3)
    plt.bar(x3[:lim_x_sup] + 0.0 * space, y3[:lim_x_sup], label='Minimiza aclives com', color='tab:red', width=0.3)
    plt.bar(x4[:lim_x_sup] + 0.5 * space, y4[:lim_x_sup], label='Minimiza aclives sem', color='tab:purple', width=0.3)
    #plt.bar(x5[:lim_x_sup] - 0.5 * space, y5[:lim_x_sup], label='Minimiza distancia com', color='tab:green', width=0.3)

    #plt.ylabel('Empirical Probability Density Function (%)', fontweight="bold")
    plt.ylabel('Função Densidade de Probabilidade (%)', fontweight="bold")
    plt.xlabel('Potência instantânea', fontweight="bold")

    plt.xticks(new)
    plt.legend(numpoints=1, loc="upper right", ncol=3)  # ,bbox_to_anchor=(-0.02, 1.15)
    plt.grid(True, which="both", ls="-", linewidth=0.1, color='0.10', zorder=0)
    plt.show()
    plt.close()
    

def plot_cdf_speed_belem():

    files_result = [
        '../data/results/m48.488877797764935_m1.484547838679201_m48.45585981539186_m1.4448492646059234_weight_pdf',
        '../data/results/m48.488877797764935_m1.484547838679201_m48.45585981539186_m1.4448492646059234_impedance_pdf',
        '../data/results/m48.488877797764935_m1.484547838679201_m48.45585981539186_m1.4448492646059234_length_pdf'
    ]

    dados = dict(open_file(files_result[0]))
    x1 = np.array(list(map(int, dados.keys())))
    cdf1 = list(dados.values())
    cumulative = 0
    for i in range(len(cdf1)):
        cumulative += cdf1[i]
        cdf1[i] = cumulative

    dados = dict(open_file(files_result[1]))
    x2 = np.array(list(map(int, dados.keys())))
    cdf2 = list(dados.values())
    cumulative = 0
    for i in range(len(cdf2)):
        cumulative += cdf2[i]
        cdf2[i] = cumulative

    dados = dict(open_file(files_result[2]))
    x3 = np.array(list(map(int, dados.keys())))
    cdf3 = list(dados.values())
    cumulative = 0
    for i in range(len(cdf3)):
        cumulative += cdf3[i]
        cdf3[i] = cumulative

    fig = plt.figure(1)

    yMax = max(cdf1) or max(cdf2)
    yMim = min(cdf1) and min(cdf2)

    xMax = 140
    xMim = min(x1) - 5

    plt.xlim(xMim, xMax)

    plt.xticks(rotation="horizontal")

    plt.grid(True, which="both", ls="-", linewidth=0.1, color='0.10', zorder=0)

    plt.errorbar(x1, cdf1, ls='-', label='Minimiza trabalho', color='tab:orange', zorder=3)
    plt.errorbar(x2, cdf2, ls='-', label='Minimiza aclives', color='tab:blue', zorder=3)
    plt.errorbar(x3, cdf3, ls='-', label='Minimiza distância', color='tab:pink', zorder=3)

    ylabel = 'Função de Distribuição Acumulada Empírica (%)'
    xlabel = 'Potência instantânea (W)'

    plt.ylabel(ylabel, fontweight="bold")
    plt.xlabel(xlabel, fontweight="bold")

    plt.legend(numpoints=1, loc="lower right", ncol=1)  # ,bbox_to_anchor=(-0.02, 1.15)
    plt.show()
    plt.close(fig)


if __name__ == '__main__':
    #plot_elevation()
    #plot_elevation_belem()
    #plot_work()
    #plot_all_work()
    #plot_BH()
    #plot_BH_2()
    #plot_cdf_BH()
    #plot_cdf_belem()
    #plot_all_cdf()
    #plot_pdf()
    plot_pdf_speed_BH()
    #plot_time()
    #plot_all_time()
    # plot_Belem()

