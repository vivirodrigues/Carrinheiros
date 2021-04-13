import matplotlib.pyplot as plt
import numpy as np
from xml.dom import minidom
import Graphs


TRABALHO = 'Trabalho'
IMPEDANCIA = "Impedância"
DISTANCIA = "Distância"

PENALIDADE = 'Caminhos por vias de menor velocidade máxima'
SEM_PENALIDADE = 'Caminho '


def plot_work():
    files_result = [
        '../data/results/m43.96267779776494_m19.944747838679202_m43.929659815391865_m19.905049264605925_coords_weight',
        '../data/results/m43.96267779776494_m19.944747838679202_m43.929659815391865_m19.905049264605925_coords_impedance',
        '../data/results/m43.96267779776494_m19.944747838679202_m43.929659815391865_m19.905049264605925_coords_length',
    ]
    values = []
    for i in range(len(files_result)):
        dados = dict(Graphs.open_file(files_result[i]))
        values.append(float(dados.get('work_total')) / 1000)

    fig, ax = plt.subplots()

    space = [1 * 0.2, 2 * 0.2, 3 * 0.2, 4 * 0.2]
    labels = [PENALIDADE, SEM_PENALIDADE]
    xticklabels = [TRABALHO, IMPEDANCIA, DISTANCIA]

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
        dados = dict(Graphs.open_file(files_result[i]))
        values.append(float(dados.get('work_total')) / 1000)

    fig, ax = plt.subplots()

    space = [1 * 0.2, 2 * 0.2, 3 * 0.2, 4 * 0.2]
    labels = [PENALIDADE, SEM_PENALIDADE]
    xticklabels = [TRABALHO, IMPEDANCIA, DISTANCIA]

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
        '../data/results/m43.96267779776494_m19.944747838679202_m43.929659815391865_m19.905049264605925_coords_distance_speed_True',
        '../data/results/m43.96267779776494_m19.944747838679202_m43.929659815391865_m19.905049264605925_coords_weight_speed_False',
        '../data/results/m43.96267779776494_m19.944747838679202_m43.929659815391865_m19.905049264605925_coords_impedance_speed_False',
        '../data/results/m43.96267779776494_m19.944747838679202_m43.929659815391865_m19.905049264605925_coords_distance_speed_False'
    ]

    values = []
    for i in range(len(files_result)):
        dados = dict(Graphs.open_file(files_result[i]))
        print(i, float(dados.get('work_total')))
        values.append(float(dados.get('work_total')) / 1000)

    fig, ax = plt.subplots()

    space = [1 * 0.2, 2 * 0.2, 3 * 0.2, 4 * 0.2]
    labels = [PENALIDADE, SEM_PENALIDADE]
    xticklabels = [TRABALHO, IMPEDANCIA, DISTANCIA]

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
           color='#457b9d',
           capsize=2)

    ax.bar([0.5],
           [values[3],
            ],
           label=labels[1],
           width=0.1,
           alpha=0.9,
           edgecolor='black',
           # hatch='/',
           color='#a8dadc',
           capsize=2)

    ax.bar([1.4],
           [values[1],
            ],
           # label=labels[0],
           width=0.1,
           alpha=0.9,
           edgecolor='black',
           # hatch='.',
           color='#457b9d',
           capsize=2)

    ax.bar([1.5],
           [values[4],
            ],
           # label=labels[1],
           width=0.1,
           alpha=0.9,
           edgecolor='black',
           # hatch='/',
           color='#a8dadc',
           capsize=2)

    ax.bar([2.4],
           [values[2],
            ],
           # label=labels[0],
           width=0.1,
           alpha=0.9,
           edgecolor='black',
           # hatch='.',
           color='#457b9d',
           capsize=2)

    ax.bar([2.5],
           [values[5],
            ],
           # label=labels[1],
           width=0.1,
           alpha=0.9,
           edgecolor='black',
           # hatch='/',
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
        dados = dict(Graphs.open_file(files_result[i]))
        values.append(float(dados.get('work_total')) / 1000)

    fig, ax = plt.subplots()

    space = [1 * 0.2, 2 * 0.2, 3 * 0.2, 4 * 0.2]
    labels = [PENALIDADE, SEM_PENALIDADE]
    xticklabels = [TRABALHO, IMPEDANCIA, DISTANCIA]

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


if __name__ == '__main__':
    plot_all_work_2()
    #plot_work_belem()
    #plot_work()
    #plot_all_work()