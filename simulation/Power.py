import Graphs


def force():
    files_result = [
            '../data/results/m43.96267779776494_m19.944747838679202_m43.929659815391865_m19.905049264605925_weight_f_speed_True',
            '../data/results/m43.96267779776494_m19.944747838679202_m43.929659815391865_m19.905049264605925_impedance_f_speed_True',
            '../data/results/m43.96267779776494_m19.944747838679202_m43.929659815391865_m19.905049264605925_distance_f_speed_True',
            '../data/results/m43.96267779776494_m19.944747838679202_m43.929659815391865_m19.905049264605925_weight_f_speed_False',
            '../data/results/m43.96267779776494_m19.944747838679202_m43.929659815391865_m19.905049264605925_impedance_f_speed_False',
            '../data/results/m43.96267779776494_m19.944747838679202_m43.929659815391865_m19.905049264605925_distance_f_speed_False'
        ]


    todas_medias = []

    for a in range(len(files_result)):
        tempo = 0
        eixo_x = []
        eixo_y = []
        y_y_std = []
        media_power = 0
        dados = dict(Graphs.open_file(files_result[a]))

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
        print("force", a, media_power)
        todas_medias.append(media_power)


def power_BH():
    files_result = [
        '../data/results/m43.96267779776494_m19.944747838679202_m43.929659815391865_m19.905049264605925_weight_speed_True',
        '../data/results/m43.96267779776494_m19.944747838679202_m43.929659815391865_m19.905049264605925_impedance_speed_True',
        '../data/results/m43.96267779776494_m19.944747838679202_m43.929659815391865_m19.905049264605925_distance_speed_True',
        '../data/results/m43.96267779776494_m19.944747838679202_m43.929659815391865_m19.905049264605925_weight_speed_False',
        '../data/results/m43.96267779776494_m19.944747838679202_m43.929659815391865_m19.905049264605925_impedance_speed_False',
        '../data/results/m43.96267779776494_m19.944747838679202_m43.929659815391865_m19.905049264605925_distance_speed_False'
    ]

    todas_medias = []

    for a in range(len(files_result)):
        tempo = 0
        eixo_x = []
        eixo_y = []
        y_y_std = []
        media_power = 0
        dados = dict(Graphs.open_file(files_result[a]))

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
        print("power", a, media_power)
        todas_medias.append(media_power)


def power_Belem():
    files_result = [
        '../data/results/m43.96267779776494_m19.944747838679202_m43.929659815391865_m19.905049264605925_0_weight_speed_False',
        '../data/results/m43.96267779776494_m19.944747838679202_m43.929659815391865_m19.905049264605925_0_impedance_speed_False',
        '../data/results/m43.96267779776494_m19.944747838679202_m43.929659815391865_m19.905049264605925_0_distance_speed_False',
        '../data/results/m48.488877797764935_m1.484547838679201_m48.45585981539186_m1.4448492646059234_0_weight_speed_False',
        '../data/results/m48.488877797764935_m1.484547838679201_m48.45585981539186_m1.4448492646059234_0_impedance_speed_False',
        '../data/results/m48.488877797764935_m1.484547838679201_m48.45585981539186_m1.4448492646059234_0_distance_speed_False'
    ]

    todas_medias = []

    for a in range(len(files_result)):
        tempo = 0
        eixo_x = []
        eixo_y = []
        y_y_std = []
        media_power = 0
        dados = dict(Graphs.open_file(files_result[a]))

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
        print("power", a, media_power)
        todas_medias.append(media_power)


if __name__ == '__main__':
    power_Belem()
    #power_BH()
    #force()