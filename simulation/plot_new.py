import json
import matplotlib.pyplot as plt
import matplotlib.markers as plm
import itertools
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


files2 = ['../data/maps/m47.090945764173824_m22.826546972177805_m47.04400930219237_m22.782058485564765_f',
         '../data/maps/m47.092787342530336_m22.826778581450746_m47.044892385394256_m22.781960971130726_f',
         '../data/maps/m47.089863735145656_m22.82660570694287_m47.04495808611153_m22.783195765772078_f',
         '../data/maps/m47.092517678301064_m22.827088220317794_m47.04523090429913_m22.78103114308082_f',
         '../data/maps/m47.09149721669476_m22.828629085340964_m47.04694245353613_m22.77962787237699_f',
         '../data/maps/m47.09048825204406_m22.825368741113234_m47.04514528080126_m22.78082969717853_f',
         '../data/maps/m47.09142061198647_m22.826152455343_m47.044630370791225_m22.78073178356891_f',
         '../data/maps/m47.09217884572687_m22.825252699619366_m47.04714584275249_m22.782268335151034_f',
         '../data/maps/m47.091139047595114_m22.826097574050436_m47.04565231845635_m22.781571931006177_f',
         '../data/maps/m47.08909726909863_m22.827062449216513_m47.04727691142185_m22.780893482571315_f',
         '../data/maps/m47.09200629935452_m22.828010552381063_m47.04648463205214_m22.782888306201855_f',
         '../data/maps/m47.091475826869704_m22.82697162874025_m47.04618252889077_m22.7826641980065_f',
         '../data/maps/m47.09269703583942_m22.82553767901721_m47.04618385870027_m22.78063045937135_f',
         '../data/maps/m47.090967267705096_m22.82816360548482_m47.04554383596302_m22.78212304274011_f',
         '../data/maps/m47.0903675118926_m22.8279731065199_m47.04625004357257_m22.77941931020167_f']

files = ['../data/results/m47.090945764173824_m22.826546972177805_m47.04400930219237_m22.782058485564765',
         '../data/results/m47.090536763743934_m22.828175436423383_m47.04651875914464_m22.78312645467597',
         '../data/results/m47.090372855471934_m22.826113342524344_m47.04352105005745_m22.78149400478119',
         '../data/results/m47.09110062288439_m22.82733615687412_m47.04618602563977_m22.780896841563113',
         '../data/results/m47.089358787894966_m22.826081657605354_m47.04526622999367_m22.78127206014417',
         '../data/results/m47.08979445023549_m22.824958307360387_m47.0466027477289_m22.78199773807116',
         '../data/results/m47.09019900406304_m22.82685981691653_m47.04599778856166_m22.782242884455037',
         '../data/results/m47.09027510823729_m22.827563812913837_m47.046697252779246_m22.782547048660557',
         '../data/results/m47.09026530272549_m22.825037719983204_m47.045197375024465_m22.781737144631354',
         '../data/results/m47.09141508860358_m22.827558826222177_m47.04588780688781_m22.779057314249847',
         '../data/results/m47.09306352155317_m22.825709088411497_m47.04492429008716_m22.78091931733442',
         '../data/results/m47.0904437286875_m22.82731554993794_m47.044872619028126_m22.782067671866823',
         '../data/results/m47.09068611611949_m22.827626794836473_m47.04577130346136_m22.780390428492353',
         '../data/results/m47.0898929671025_m22.828257227489562_m47.045474482445044_m22.783337719353195',
         '../data/results/m47.093157129712964_m22.827476062177798_m47.04508745303291_m22.779889875909333',
         '../data/results/m47.090967267705096_m22.82816360548482_m47.04554383596302_m22.78212304274011',
         '../data/results/m47.0903675118926_m22.8279731065199_m47.04625004357257_m22.77941931020167',
         '../data/results/m47.091475826869704_m22.82697162874025_m47.04618252889077_m22.7826641980065',
         '../data/results/m47.09269703583942_m22.82553767901721_m47.04618385870027_m22.78063045937135',
         '../data/results/m47.08909726909863_m22.827062449216513_m47.04727691142185_m22.780893482571315',
         '../data/results/m47.09200629935452_m22.828010552381063_m47.04648463205214_m22.782888306201855',
         '../data/results/m47.09217884572687_m22.825252699619366_m47.04714584275249_m22.782268335151034',
         '../data/results/m47.091139047595114_m22.826097574050436_m47.04565231845635_m22.781571931006177',
         '../data/results/m47.09048825204406_m22.825368741113234_m47.04514528080126_m22.78082969717853',
         '../data/results/m47.09142061198647_m22.826152455343_m47.044630370791225_m22.78073178356891',
         '../data/results/m47.09075495706285_m22.824700073604347_m47.04788293090288_m22.78232265870227',
         '../data/results/m47.092517678301064_m22.827088220317794_m47.04523090429913_m22.78103114308082',
         '../data/results/m47.09149721669476_m22.828629085340964_m47.04694245353613_m22.77962787237699',
         '../data/results/m47.092787342530336_m22.826778581450746_m47.044892385394256_m22.781960971130726',
         '../data/results/m47.089863735145656_m22.82660570694287_m47.04495808611153_m22.783195765772078'
         ]


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
    todas_medias.append(media_power)
    print("tempo", tempo)
    """
    eixo_x_2 = []
    eixo_y_2 = []
    y_y_std = []

    dados = dict(openFile(files_i[a]))

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
