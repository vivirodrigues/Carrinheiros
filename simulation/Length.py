import matplotlib.pyplot as plt
import numpy as np
from xml.dom import minidom
import Graphs

TRABALHO = 'Trabalho'
IMPEDANCIA = "Impedância"
DISTANCIA = "Distância"

PENALIDADE = 'Caminhos mais seguros'
SEM_PENALIDADE = 'Caminhos menos seguros'


def plot_all_length_BH():

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
        duration = [float(node.attributes['routeLength'].value) for node in tag]
        print(i, duration)
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
           [times[0]/1000,
            ],
           label=labels[0],
           width=0.15,
           alpha=0.9,
           edgecolor='black',
           #hatch='.',
           color='#a8dadc',
           capsize=2)

    ax.bar([0.475],
           [times[3] / 1000,
            ],
           label=labels[1],
           width=0.15,
           alpha=0.9,
           edgecolor='black',
           #hatch='.',
           color='#1d3557',
           capsize=2)

    ax.bar([1.325],
           [times[1]/1000,
            ],
           #label=labels[1],
           width=0.15,
           alpha=0.9,
           edgecolor='black',
           #hatch='/',
           color='#a8dadc',
           capsize=2)

    ax.bar([1.475],
           [times[4] / 1000,
            ],
           #label=labels[1],
           width=0.15,
           alpha=0.9,
           edgecolor='black',
           #hatch='/',
           color='#1d3557',
           capsize=2)

    ax.bar([2.325],
           [times[2]/1000,
            ],
           #label=labels[2],
           width=0.15,
           alpha=0.9,
           edgecolor='black',
           #hatch='..',
           color='#a8dadc',
           capsize=2)

    ax.bar([2.475],
           [times[5] / 1000,
            ],
           #label=labels[2],
           width=0.15,
           alpha=0.9,
           edgecolor='black',
           #hatch='..',
           color='#1d3557',
           capsize=2)

    ax.set_ylabel('Distância percorrida (km)', fontweight='bold')
    ax.set_xlabel('Estratégia', fontweight='bold')
    ax.set_xticks(np.arange(len(xticklabels)) + 0.4)
    ax.set_xticklabels(xticklabels)
    ax.legend(loc='lower center', bbox_to_anchor=(0.5, 1),
                   ncol=2, fancybox=True, shadow=True)

    ax.grid(linestyle='--', axis='y', alpha=0.4, color='black')
    plt.show()


def plot_all_length_BH_2():

    files_result = [
        '../data/results/m43.96267779776494_m19.944747838679202_m43.929659815391865_m19.905049264605925_coords_weight_speed_True',
        '../data/results/m43.96267779776494_m19.944747838679202_m43.929659815391865_m19.905049264605925_coords_impedance_speed_True',
        '../data/results/m43.96267779776494_m19.944747838679202_m43.929659815391865_m19.905049264605925_coords_distance_speed_True',
        '../data/results/m43.96267779776494_m19.944747838679202_m43.929659815391865_m19.905049264605925_coords_weight_speed_False',
        '../data/results/m43.96267779776494_m19.944747838679202_m43.929659815391865_m19.905049264605925_coords_impedance_speed_False',
        '../data/results/m43.96267779776494_m19.944747838679202_m43.929659815391865_m19.905049264605925_coords_distance_speed_False'
    ]

    values = []
    for i in range(len(files_result)):
        dados = dict(Graphs.open_file(files_result[i]))
        print(i, float(dados.get('total_length')))
        values.append(float(dados.get('total_length')) / 1000)

    fig, ax = plt.subplots()

    # space = [1 * 0.2, 2 * 0.2, 3 * 0.2, 4 * 0.2]
    labels = [PENALIDADE, SEM_PENALIDADE]
    xticklabels = [TRABALHO, IMPEDANCIA, DISTANCIA]

    # color = "red"
    # hatch = '|'

    # color = ['#1d3557', '#457b9d', '#a8dadc']
    hatch = ["/", ".", "o"]

    ax.bar([0.325],
           [values[0]/1000,
            ],
           label=labels[0],
           width=0.15,
           alpha=0.9,
           edgecolor='black',
           #hatch='.',
           color='#a8dadc',
           capsize=2)

    ax.bar([0.475],
           [values[3] / 1000,
            ],
           label=labels[1],
           width=0.15,
           alpha=0.9,
           edgecolor='black',
           #hatch='.',
           color='#1d3557',
           capsize=2)

    ax.bar([1.325],
           [values[1]/1000,
            ],
           #label=labels[1],
           width=0.15,
           alpha=0.9,
           edgecolor='black',
           #hatch='/',
           color='#a8dadc',
           capsize=2)

    ax.bar([1.475],
           [values[4] / 1000,
            ],
           #label=labels[1],
           width=0.15,
           alpha=0.9,
           edgecolor='black',
           #hatch='/',
           color='#1d3557',
           capsize=2)

    ax.bar([2.325],
           [values[2]/1000,
            ],
           #label=labels[2],
           width=0.15,
           alpha=0.9,
           edgecolor='black',
           #hatch='..',
           color='#a8dadc',
           capsize=2)

    ax.bar([2.475],
           [values[5] / 1000,
            ],
           #label=labels[2],
           width=0.15,
           alpha=0.9,
           edgecolor='black',
           #hatch='..',
           color='#1d3557',
           capsize=2)

    ax.set_ylabel('Distância percorrida (km)', fontweight='bold')
    ax.set_xlabel('Estratégia', fontweight='bold')
    ax.set_xticks(np.arange(len(xticklabels)) + 0.4)
    ax.set_xticklabels(xticklabels)
    ax.legend(loc='lower center', bbox_to_anchor=(0.5, 1),
                   ncol=2, fancybox=True, shadow=True)

    ax.grid(linestyle='--', axis='y', alpha=0.4, color='black')
    plt.show()


if __name__ == '__main__':
    plot_all_length_BH_2()