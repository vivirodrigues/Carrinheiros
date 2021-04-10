import json
import matplotlib.pyplot as plt
import matplotlib.markers as plm
import osmnx as ox
import scipy.stats
import numpy as np
import scipy.stats as st


def openFile(nameFile):
    try:
        f = open(nameFile + ".json", "r")
        dados = json.loads(f.read())
        f.close()
    except:
        dados = 0
        pass

    return dados


def mean_confidence_interval(data, confidence=0.90):
    a = 1.0 * np.array(data)
    n = len(a)
    m, se = np.mean(a), scipy.stats.sem(a)
    h = se * scipy.stats.t.ppf((1 + confidence) / 2., n - 1)
    print(m, h)
    return m, m - h, m + h


files = ['../data/results/m43.96267779776494_m19.944747838679202_m43.929659815391865_m19.905049264605925_impedance',
         '../data/results/m43.96267779776494_m19.944747838679202_m43.929659815391865_m19.905049264605925_weight',
         '../data/results/m43.96267779776494_m19.944747838679202_m43.929659815391865_m19.905049264605925_length']


# 12
# files_i = ['../data/maps/m48.509235074196255_m1.4943061226299288_m48.441691211800055_m1.4384730034943134_i']
todas_medias = []

for a in range(len(files)):
    tempo = 0
    eixo_x = []
    eixo_y = []
    y_y_std = []
    media_power = 0
    dados = dict(openFile(files[a]))

    if dados != 0:
        # print("File: ", files[a])
        for i in list(dados.keys()):
            eixo_x.append(int(i))
            eixo_y.append(float(dados.get(str(i))))
            # print("inst", int(i), float(dados.get(str(i))))
            media_power += int(dados.get(str(i)))
            tempo += 1
            y_y_std.append(0)

    media_power = media_power / len(list(dados.keys()))
    print("power", media_power)
    todas_medias.append(media_power)
    # print("tempo", tempo)

    """
    eixo_x_2 = []
    eixo_y_2 = []
    y_y_std = []

    dados = dict(openFile(files[a] + '_i'))

    if dados != 0:
        # print("File: ", files_i[a])
        for i in list(dados.keys()):
            eixo_x_2.append(int(i))
            eixo_y_2.append(float(dados.get(str(i))))
            y_y_std.append(0)
    

    print(media_power)
    fig, axs = plt.subplots(2)
    fig.suptitle('Potência vs Altitude')
    # print(eixo_y)
    axs[0].plot(eixo_x_2, eixo_y, '-')
    plt.ylabel("potência")
    axs[1].plot(eixo_x_2, eixo_y_2)
    plt.ylabel("Altitude")

    plt.show()
    """


print(todas_medias)
mean_confidence_interval(todas_medias)
# define sample data
data = todas_medias  # [12, 12, 13, 13, 15, 16, 17, 22, 23, 25, 26, 27, 28, 28, 29]

# create 95% confidence interval for population mean weight
print(st.t.interval(alpha=0.95, df=len(data) - 1, loc=np.mean(data), scale=st.sem(data)))

