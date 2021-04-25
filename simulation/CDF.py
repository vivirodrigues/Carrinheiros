import matplotlib.pyplot as plt
import networkx as nx
from route import Graph
import numpy as np
import Graphs


def plot_cdf_BH():

    print("BH")
    files_result = [
        '../data/results/m43.96267779776494_m19.944747838679202_m43.929659815391865_m19.905049264605925_0_weight_pdf_speed_False',
        '../data/results/m43.96267779776494_m19.944747838679202_m43.929659815391865_m19.905049264605925_0_impedance_pdf_speed_False',
        '../data/results/m43.96267779776494_m19.944747838679202_m43.929659815391865_m19.905049264605925_0_distance_pdf_speed_False'
    ]

    dados = dict(Graphs.open_file(files_result[0]))
    x1 = np.array(list(map(int, dados.keys())))
    cdf1 = list(dados.values())
    cumulative = 0
    for i in range(len(cdf1)):
        print(i, "peso", cumulative)
        cumulative += cdf1[i]
        cdf1[i] = cumulative

    dados = dict(Graphs.open_file(files_result[1]))
    x2 = np.array(list(map(int, dados.keys())))
    cdf2 = list(dados.values())
    cumulative = 0
    for i in range(len(cdf2)):
        print(i, "impe", cumulative)
        cumulative += cdf2[i]
        cdf2[i] = cumulative

    dados = dict(Graphs.open_file(files_result[2]))
    x3 = np.array(list(map(int, dados.keys())))
    cdf3 = list(dados.values())
    cumulative = 0
    for i in range(len(cdf3)):
        print(i, "dist", cumulative)
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

    plt.errorbar(x1, cdf1, ls='-', label='PMT', color='tab:orange', zorder=3)
    plt.errorbar(x2, cdf2, ls='-', label='PMI', color='tab:blue', zorder=3)
    plt.errorbar(x3, cdf3, ls='-', label='PMD', color='tab:pink', zorder=3)

    ylabel = 'Função de Distribuição Acumulada Empírica (%)'
    xlabel = 'Potência instantânea (W)'

    plt.ylabel(ylabel, fontweight="bold")
    plt.xlabel(xlabel, fontweight="bold")

    plt.legend(numpoints=1, loc="lower right", ncol=1)  # ,bbox_to_anchor=(-0.02, 1.15)
    plt.show()
    plt.close(fig)


def plot_cdf_belem():
    print("Belem")

    files_result = [
        '../data/results/m48.488877797764935_m1.484547838679201_m48.45585981539186_m1.4448492646059234_0_weight_pdf_speed_False',
        '../data/results/m48.488877797764935_m1.484547838679201_m48.45585981539186_m1.4448492646059234_0_impedance_pdf_speed_False',
        '../data/results/m48.488877797764935_m1.484547838679201_m48.45585981539186_m1.4448492646059234_0_distance_pdf_speed_False'
    ]

    dados = dict(Graphs.open_file(files_result[0]))
    x1 = np.array(list(map(int, dados.keys())))
    cdf1 = list(dados.values())
    cumulative = 0
    for i in range(len(cdf1)):
        cumulative += cdf1[i]
        print("trab", i, cumulative)
        cdf1[i] = cumulative

    dados = dict(Graphs.open_file(files_result[1]))
    x2 = np.array(list(map(int, dados.keys())))
    cdf2 = list(dados.values())
    cumulative = 0
    for i in range(len(cdf2)):
        cumulative += cdf2[i]
        print("imp", i, cumulative)
        cdf2[i] = cumulative

    dados = dict(Graphs.open_file(files_result[2]))
    x3 = np.array(list(map(int, dados.keys())))
    cdf3 = list(dados.values())
    cumulative = 0
    for i in range(len(cdf3)):
        cumulative += cdf3[i]
        print("dist", i, cumulative)
        cdf3[i] = cumulative

    fig = plt.figure(1)

    yMax = max(cdf1) or max(cdf2)
    yMim = min(cdf1) and min(cdf2)

    xMax = 150
    xMim = min(x1) - 5

    plt.xlim(xMim, xMax)

    plt.xticks(rotation="horizontal")

    plt.grid(True, which="both", ls="-", linewidth=0.1, color='0.10', zorder=0)

    plt.errorbar(x1, cdf1, ls='-', label='PMT', color='tab:orange', zorder=3)
    plt.errorbar(x2, cdf2, ls='-', label='PMI', color='tab:blue', zorder=3)
    plt.errorbar(x3, cdf3, ls='-', label='PMD', color='tab:pink', zorder=3)

    ylabel = 'Função de Distribuição Acumulada Empírica (%)'
    xlabel = 'Potência instantânea (W)'

    plt.ylabel(ylabel, fontweight="bold")
    plt.xlabel(xlabel, fontweight="bold")

    plt.legend(numpoints=1, loc="lower right", ncol=1)  # ,bbox_to_anchor=(-0.02, 1.15)
    plt.show()
    plt.close(fig)


def plot_cdf_speed_belem():

    files_result = [
        '../data/results/m48.488877797764935_m1.484547838679201_m48.45585981539186_m1.4448492646059234_weight_pdf_speeds_True',
        #'../data/results/m48.488877797764935_m1.484547838679201_m48.45585981539186_m1.4448492646059234_weight_pdf_speeds_False',
        '../data/results/m48.488877797764935_m1.484547838679201_m48.45585981539186_m1.4448492646059234_impedance_pdf_speeds_True',
        #'../data/results/m48.488877797764935_m1.484547838679201_m48.45585981539186_m1.4448492646059234_impedance_pdf_speeds_False',
        '../data/results/m48.488877797764935_m1.484547838679201_m48.45585981539186_m1.4448492646059234_distance_pdf_speeds_True'
    ]

    dados = dict(Graphs.open_file(files_result[0]))
    x1 = np.array(list(map(int, dados.keys())))
    cdf1 = list(dados.values())
    cumulative = 0
    for i in range(len(cdf1)):
        cumulative += cdf1[i]
        cdf1[i] = cumulative

    dados = dict(Graphs.open_file(files_result[1]))
    x2 = np.array(list(map(int, dados.keys())))
    cdf2 = list(dados.values())
    cumulative = 0
    for i in range(len(cdf2)):
        cumulative += cdf2[i]
        cdf2[i] = cumulative

    dados = dict(Graphs.open_file(files_result[2]))
    x3 = np.array(list(map(int, dados.keys())))
    cdf3 = list(dados.values())
    cumulative = 0
    for i in range(len(cdf3)):
        cumulative += cdf3[i]
        cdf3[i] = cumulative

    fig = plt.figure(1)

    yMax = max(cdf1) or max(cdf2)
    yMim = min(cdf1) and min(cdf2)

    xMax = 70
    xMim = min(x1) - 5

    plt.xlim(xMim, xMax)

    plt.xticks(rotation="horizontal")

    plt.grid(True, which="both", ls="-", linewidth=0.1, color='0.10', zorder=0)

    plt.errorbar(x1, cdf1, ls='-', label='PMT', color='tab:red', zorder=3)
    # plt.errorbar(x2, cdf2, ls='-', label='Minimiza trabalho 2', color='tab:blue', zorder=3)
    plt.errorbar(x2, cdf2, ls='-', label='PMI', color='tab:pink', zorder=3)
    # plt.errorbar(x4, cdf4, ls='-', label='Minimiza aclives 2', color='tab:green', zorder=3)
    plt.errorbar(x3, cdf3, ls='-', label='PMD', color='tab:orange', zorder=3)

    ylabel = 'Função de Distribuição Acumulada Empírica (%)'
    xlabel = 'Velocidade máxima da via (km/h)'

    plt.ylabel(ylabel, fontweight="bold")
    plt.xlabel(xlabel, fontweight="bold")

    plt.legend(numpoints=1, loc="lower right", ncol=1)  # ,bbox_to_anchor=(-0.02, 1.15)
    plt.show()
    plt.close(fig)


def plot_all_cdf():

    files_result = [
        '../data/results/m43.96267779776494_m19.944747838679202_m43.929659815391865_m19.905049264605925_weight_pdf',
        '../data/results/m43.96267779776494_m19.944747838679202_m43.929659815391865_m19.905049264605925_impedance_pdf',
        '../data/results/m43.96267779776494_m19.944747838679202_m43.929659815391865_m19.905049264605925_length_pdf',
        '../data/results/m48.488877797764935_m1.484547838679201_m48.45585981539186_m1.4448492646059234_weight_pdf',
        '../data/results/m48.488877797764935_m1.484547838679201_m48.45585981539186_m1.4448492646059234_impedance_pdf',
        '../data/results/m48.488877797764935_m1.484547838679201_m48.45585981539186_m1.4448492646059234_length_pdf'
    ]

    dados = dict(Graphs.open_file(files_result[0]))
    x1 = np.array(list(map(int, dados.keys())))
    cdf1 = list(dados.values())
    cumulative = 0
    for i in range(len(cdf1)):
        cumulative += cdf1[i]
        cdf1[i] = cumulative

    dados = dict(Graphs.open_file(files_result[1]))
    x2 = np.array(list(map(int, dados.keys())))
    cdf2 = list(dados.values())
    cumulative = 0
    for i in range(len(cdf2)):
        cumulative += cdf2[i]
        cdf2[i] = cumulative

    dados = dict(Graphs.open_file(files_result[2]))
    x3 = np.array(list(map(int, dados.keys())))
    cdf3 = list(dados.values())
    cumulative = 0
    for i in range(len(cdf3)):
        cumulative += cdf3[i]
        cdf3[i] = cumulative

    dados = dict(Graphs.open_file(files_result[3]))
    x4 = np.array(list(map(int, dados.keys())))
    cdf4 = list(dados.values())
    cumulative = 0
    for i in range(len(cdf4)):
        cumulative += cdf4[i]
        cdf4[i] = cumulative

    dados = dict(Graphs.open_file(files_result[4]))
    x5 = np.array(list(map(int, dados.keys())))
    cdf5 = list(dados.values())
    cumulative = 0
    for i in range(len(cdf5)):
        cumulative += cdf5[i]
        cdf5[i] = cumulative

    dados = dict(Graphs.open_file(files_result[5]))
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


if __name__ == '__main__':
    # plot_all_cdf()
    #plot_cdf_BH()
    plot_cdf_belem()
    #plot_cdf_speed_belem()