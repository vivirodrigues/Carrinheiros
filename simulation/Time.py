import matplotlib.pyplot as plt
import numpy as np
from xml.dom import minidom
import Graphs

TRABALHO = 'Trabalho'
IMPEDANCIA = "Impedância"
DISTANCIA = "Distância"

PENALIDADE = 'Caminhos por vias de menor velocidade máxima'
SEM_PENALIDADE = 'Caminho '


def plot_all_time_belem():
    files_result = [
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
    labels = [PENALIDADE, SEM_PENALIDADE]
    xticklabels = [TRABALHO, IMPEDANCIA, DISTANCIA]

    # color = "red"
    # hatch = '|'

    # color = ['#1d3557', '#457b9d', '#a8dadc']
    hatch = ["/", ".", "o"]

    ax.bar([0.325],
           [times[0] / 3600,
            ],
           label=labels[0],
           width=0.15,
           alpha=0.9,
           edgecolor='black',
           # hatch='.',
           color='#a8dadc',
           capsize=2)

    ax.bar([0.475],
           [times[3] / 3600,
            ],
           label=labels[1],
           width=0.15,
           alpha=0.9,
           edgecolor='black',
           # hatch='.',
           color='#1d3557',
           capsize=2)

    ax.bar([1.325],
           [times[1] / 3600,
            ],
           # label=labels[1],
           width=0.15,
           alpha=0.9,
           edgecolor='black',
           # hatch='/',
           color='#a8dadc',
           capsize=2)

    ax.bar([1.475],
           [times[4] / 3600,
            ],
           # label=labels[1],
           width=0.15,
           alpha=0.9,
           edgecolor='black',
           # hatch='/',
           color='#1d3557',
           capsize=2)

    ax.bar([2.325],
           [times[2] / 3600,
            ],
           # label=labels[2],
           width=0.15,
           alpha=0.9,
           edgecolor='black',
           # hatch='..',
           color='#a8dadc',
           capsize=2)

    ax.bar([2.475],
           [times[5] / 3600,
            ],
           # label=labels[2],
           width=0.15,
           alpha=0.9,
           edgecolor='black',
           # hatch='..',
           color='#1d3557',
           capsize=2)

    ax.set_ylabel('Tempo (h)', fontweight='bold')
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


def plot_all_time_BH():

    files_result = [
        '../data/results/m43.96267779776494_m19.944747838679202_m43.929659815391865_m19.905049264605925_weight_speed_True.xml',
        '../data/results/m43.96267779776494_m19.944747838679202_m43.929659815391865_m19.905049264605925_impedance_speed_True.xml',
        '../data/results/m43.96267779776494_m19.944747838679202_m43.929659815391865_m19.905049264605925_distance_speed_True.xml',
        '../data/results/m43.96267779776494_m19.944747838679202_m43.929659815391865_m19.905049264605925_weight_speed_False.xml',
        '../data/results/m43.96267779776494_m19.944747838679202_m43.929659815391865_m19.905049264605925_impedance_speed_False.xml',
        '../data/results/m43.96267779776494_m19.944747838679202_m43.929659815391865_m19.905049264605925_distance_speed_False.xml'
    ]

    times = []
    for i in range(len(files_result)):
        file = minidom.parse(files_result[i])
        tag = file.getElementsByTagName('tripinfo')
        duration = [float(node.attributes['duration'].value) for node in tag]
        print(i, duration[0]/3600)
        times.append(duration[0])

    fig, ax = plt.subplots()

    # space = [1 * 0.2, 2 * 0.2, 3 * 0.2, 4 * 0.2]
    labels = [PENALIDADE, SEM_PENALIDADE]
    xticklabels = [TRABALHO, IMPEDANCIA, DISTANCIA]

    # color = "red"
    # hatch = '|'

    # color = ['#1d3557', '#457b9d', '#a8dadc']
    hatch = ["/", ".", "o"]

    ax.bar([0.325],
           [times[0]/3600,
            ],
           label=labels[0],
           width=0.15,
           alpha=0.9,
           edgecolor='black',
           #hatch='.',
           color='#a8dadc',
           capsize=2)

    ax.bar([0.475],
           [times[3] / 3600,
            ],
           label=labels[1],
           width=0.15,
           alpha=0.9,
           edgecolor='black',
           #hatch='.',
           color='#1d3557',
           capsize=2)

    ax.bar([1.325],
           [times[1]/3600,
            ],
           #label=labels[1],
           width=0.15,
           alpha=0.9,
           edgecolor='black',
           #hatch='/',
           color='#a8dadc',
           capsize=2)

    ax.bar([1.475],
           [times[4] / 3600,
            ],
           #label=labels[1],
           width=0.15,
           alpha=0.9,
           edgecolor='black',
           #hatch='/',
           color='#1d3557',
           capsize=2)

    ax.bar([2.325],
           [times[2]/3600,
            ],
           #label=labels[2],
           width=0.15,
           alpha=0.9,
           edgecolor='black',
           #hatch='..',
           color='#a8dadc',
           capsize=2)

    ax.bar([2.475],
           [times[5] / 3600,
            ],
           #label=labels[2],
           width=0.15,
           alpha=0.9,
           edgecolor='black',
           #hatch='..',
           color='#1d3557',
           capsize=2)

    ax.set_ylabel('Tempo (h)', fontweight='bold')
    ax.set_xlabel('Estratégia', fontweight='bold')
    ax.set_xticks(np.arange(len(xticklabels)) + 0.4)
    ax.set_xticklabels(xticklabels)
    ax.legend(loc='lower center', bbox_to_anchor=(0.5, 1),
                   ncol=2, fancybox=True, shadow=True)

    ax.grid(linestyle='--', axis='y', alpha=0.4, color='black')
    plt.show()


if __name__ == '__main__':
    #plot_time()
    # plot_all_time_2()
    plot_all_time_BH()