import csv
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import numpy as np
import pandas as pd
import json

def open_file(nameFile):
    try:
        f = open(nameFile + ".json", "r")
        dados = json.loads(f.read())
        f.close()
    except:
        dados = 0
        pass

    return dados

x = []
y = []

x1 = []
y1 = []

x2 = []
y2 = []

x3 = []
y3 = []

a1 = 'weight'
a2 = 'impedance'
a3 = 'length'

file = '../data/results/m43.96267779776494_m19.944747838679202_m43.929659815391865_m19.905049264605925_length_pdf'

arquivo = 'Empirical_Probability_Density'

dados = dict(open_file(file))

for i in list(dados.keys()):
    x.append(int(i))
    y.append(float(dados.get(str(i))))

x = np.array(x)
y = np.array(y)

"""
with open(a2 + '.csv', newline='') as csvfile:
    spamreader = csv.reader(csvfile, delimiter=':', quotechar='|')
    for row1 in spamreader:
        x1.append(int(row1[0]))
        y1.append(float(row1[1]))

x1 = np.array(x1)
y1 = np.array(y1)

with open(a3 + '.csv', newline='') as csvfile:
    spamreader2 = csv.reader(csvfile, delimiter=':', quotechar='|')
    for row2 in spamreader2:
        x2.append(int(row2[0]))
        y2.append(float(row2[1]))

x2 = np.array(x2)
y2 = np.array(y2)

with open(a4 + '.csv', newline='') as csvfile:
    spamreader3 = csv.reader(csvfile, delimiter=':', quotechar='|')
    for row3 in spamreader3:
        x3.append(int(row3[0]))
        y3.append(float(row3[1]))

x3 = np.array(x3)
y3 = np.array(y3)

"""

def plottt(x, x1, x2, x3, y, y1, y2, y3):
    limInf = 85
    limSup = 109
    space = 0.6

    new = []
    for i in range(len(x)):
        if i >= limInf and i <= limSup:
            new.append(int(x[i]))

    fig = plt.figure(figsize=(15, 5))
    plt.ylim(0, max(y1) + 5)
    plt.xlim(limInf, limSup)

    plt.bar(x - 0.43 * space, y2, label='Neural Network', color='tab:blue', width=0.2)
    plt.bar(x - 0.1 * space, y, label='Fuzzy1', color='tab:orange', width=0.2)
    plt.bar(x + 0.2 * space, y1, label='Fuzzy2', color='tab:green', width=0.2)
    plt.bar(x + 0.5 * space, y3, label='SUMO', color='tab:red', width=0.2)
    plt.ylabel('Empirical Probability Density Function (%)', fontweight="bold")
    plt.xlabel('Speed (km/h)', fontweight="bold")

    plt.xticks(new)
    plt.legend(numpoints=1, loc="upper left", ncol=2)  # ,bbox_to_anchor=(-0.02, 1.15)
    plt.grid(True, which="both", ls="-", linewidth=0.1, color='0.10', zorder=0)
    name = arquivo
    fig.savefig(name + '.png', bbox_inches='tight')
    plt.close(fig)


def plott(x, y):
    limInf = -1
    limSup = 80

    new = []
    for i in range(len(x)):
        if i >= limInf and i <= limSup:
            new.append(int(x[i]))

    fig = plt.figure(figsize=(15, 5))
    plt.ylim(0, max(y) + 5)
    plt.xlim(limInf, limSup)

    plt.bar(x, y, label='Length', color='tab:blue')
    plt.ylabel('Empirical Probability Density Function (%)', fontweight="bold")
    plt.xlabel('Power', fontweight="bold")

    plt.xticks(new)
    plt.legend(numpoints=1, loc="upper left", ncol=2)  # ,bbox_to_anchor=(-0.02, 1.15)
    plt.grid(True, which="both", ls="-", linewidth=0.1, color='0.10', zorder=0)
    name = arquivo
    fig.savefig(name + '.png', bbox_inches='tight')
    plt.show()
    plt.close(fig)


def plot_means():
    fig, ax = plt.subplots()

    space = [1 * 0.2, 2 * 0.2, 3 * 0.2, 4 * 0.2]
    labels = ['Mean Speed', 'Total Fuel', 'Time']
    xticklabels = ['Work', 'Impedance', 'Length']

    color = "red"
    hatch = '|'

    color = ['#1d3557', '#457b9d', '#a8dadc']
    hatch = ["/", ".", "o"]


    ax.bar([0.4],
           [237797,
            ],
           label=labels[0],
           width=0.2,
           alpha=0.9,
           edgecolor='black',
           hatch='.',
           color='#1d3557',
           capsize=2)

    ax.bar([1.4],
           [290621,
            ],
           label=labels[1],
           width=0.2,
           alpha=0.9,
           edgecolor='black',
           hatch='/',
           color='#457b9d',
           capsize=2)

    ax.bar([2.4],
           [991319,
            ],
           label=labels[2],
           width=0.2,
           alpha=0.9,
           edgecolor='black',
           hatch='..',
           color='#a8dadc',
           capsize=2)

    ax.set_ylabel('Sum of Power (W)', fontweight='bold')
    ax.set_xlabel('Strategies', fontweight='bold')
    ax.set_xticks(np.arange(len(xticklabels)) + 0.4)
    ax.set_xticklabels(xticklabels)
    # ax.legend(loc='lower center', bbox_to_anchor=(0.5, 1),
    #               ncol=4, fancybox=True, shadow=True)

    ax.grid(linestyle='--', axis='y', alpha=0.4, color='black')
    plt.show()

plot_means()
#plott(x, y)