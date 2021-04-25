import json
import matplotlib.pyplot as plt
import numpy as np
import Graphs


def plot_pdf_speed_BH():

    files_result = [
        '../data/results/m43.96267779776494_m19.944747838679202_m43.929659815391865_m19.905049264605925_0_weight_pdf_speeds_True',
        '../data/results/m43.96267779776494_m19.944747838679202_m43.929659815391865_m19.905049264605925_0_impedance_pdf_speeds_True',
        '../data/results/m43.96267779776494_m19.944747838679202_m43.929659815391865_m19.905049264605925_0_distance_pdf_speeds_True',
        '../data/results/m43.96267779776494_m19.944747838679202_m43.929659815391865_m19.905049264605925_0_weight_pdf_speeds_False',
        '../data/results/m43.96267779776494_m19.944747838679202_m43.929659815391865_m19.905049264605925_0_impedance_pdf_speeds_False',
        '../data/results/m43.96267779776494_m19.944747838679202_m43.929659815391865_m19.905049264605925_0_distance_pdf_speeds_False'

    ]
    #'../data/results/m43.96267779776494_m19.944747838679202_m43.929659815391865_m19.905049264605925_weight_pdf_speeds_False'

    dados = dict(Graphs.open_file(files_result[0]))
    x1 = np.array(list(map(int, dados.keys())))
    y1 = np.array(list(dados.values()))

    dados = dict(Graphs.open_file(files_result[1]))
    x2 = np.array(list(map(int, dados.keys())))
    y2 = np.array(list(dados.values()))

    dados = dict(Graphs.open_file(files_result[2]))
    x3 = np.array(list(map(int, dados.keys())))
    y3 = np.array(list(dados.values()))

    dados = dict(Graphs.open_file(files_result[3]))
    x4 = np.array(list(map(int, dados.keys())))
    y4 = np.array(list(dados.values()))

    dados = dict(Graphs.open_file(files_result[4]))
    x5 = np.array(list(map(int, dados.keys())))
    y5 = np.array(list(dados.values()))

    dados = dict(Graphs.open_file(files_result[5]))
    x6 = np.array(list(map(int, dados.keys())))
    y6 = np.array(list(dados.values()))

    # fig = plt.figure(figsize=(15, 5))

    lim_x_inf = 10
    lim_x_sup = 85

    lim_y_inf = min(min(y1), min(y2), min(y3))
    lim_y_sup = max(max(y1), max(y2), max(y3))

    plt.xlim(lim_x_inf-3.5, lim_x_sup+1)
    plt.ylim(lim_y_inf, lim_y_sup+10)

    space = 1
    new = [i for i in range(lim_x_inf, lim_x_sup, 10)]
    print(new)

    plt.bar(x1[new] - 0.8 * space, y1[new], label='PMT', color='tab:blue', width=0.8)
    #plt.bar(x2[new] + 0.0 * space, y2[new], label='PMI', color='tab:red', width=0.8)
    #plt.bar(x3[new] + 0.8 * space, y3[new], label='PMD', color='tab:green', width=0.8)
    plt.bar(x4[new] + 0.8 * space, y4[new], label='PMT 2', color='tab:pink', width=0.4)
    #plt.bar(x5[new] + 0.12 * space, y5[new], label='PMI 2', color='tab:purple', width=0.4)
    #plt.bar(x6[new] + 0.16 * space, y6[new], label='PMD 2', color='tab:orange', width=0.4)

    #plt.ylabel('Empirical Probability Density Function (%)', fontweight="bold")
    plt.ylabel('Função Densidade de Probabilidade (%)', fontweight="bold")
    plt.xlabel('Velocidade máxima da via', fontweight="bold")

    plt.xticks(new)
    plt.legend(numpoints=1, loc="upper right", ncol=3)  # ,bbox_to_anchor=(-0.02, 1.15)
    plt.grid(True, which="both", ls="-", linewidth=0.1, color='0.10', zorder=0)
    plt.show()
    plt.close()


def plot_pdf():

    files_result = [
        '../data/results/oficial/m43.96267779776494_m19.944747838679202_m43.929659815391865_m19.905049264605925_weight_pdf',
        '../data/results/oficial/m43.96267779776494_m19.944747838679202_m43.929659815391865_m19.905049264605925_impedance_pdf',
        '../data/results/oficial/m43.96267779776494_m19.944747838679202_m43.929659815391865_m19.905049264605925_length_pdf',
    ]

    dados = dict(Graphs.open_file(files_result[0]))
    x1 = np.array(list(map(int, dados.keys())))
    y1 = np.array(list(dados.values()))

    dados = dict(Graphs.open_file(files_result[1]))
    x2 = np.array(list(map(int, dados.keys())))
    y2 = np.array(list(dados.values()))

    dados = dict(Graphs.open_file(files_result[2]))
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


if __name__ == '__main__':
    plot_pdf_speed_BH()
    # plot_pdf()