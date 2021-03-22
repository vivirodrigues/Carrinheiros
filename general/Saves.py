import os
from geography import Coordinates


def files_directory(file_name, extension):

    directory = file_name.split(sep='/')
    directory = directory[:-1]
    directory = '/'.join(directory)
    caminhos = [os.path.join(directory, nome) for nome in os.listdir(directory)]
    arquivos = [arq for arq in caminhos if os.path.isfile(arq)]
    specific_type = [file.split(sep='/')[-1:] for file in arquivos if file.lower().endswith("." + extension)]

    # [min_lon, min_lat, max_lon, max_lat]
    files_directory = []
    for i in specific_type:
        coords = i[0].split(sep='_')
        last = coords[-1].split(sep='.')[:-1]
        extension = coords[-1].split(sep='.')[-1]
        last = '.'.join(last)
        coords.pop(-1)
        coords.append(last)
        coords.append(extension)
        if len(coords) > 3:
            files_directory.append(coords)
    return files_directory


def coord_value(value):
    if value[0] == 'm':
        return -float(value[1:])
    else:
        return float(value)


def verify_file_exists(coordinates_list, file_name):

    # it gets all names of osm files inside the same directory of 'file_name'
    extension = file_name.split(sep='.')[-1]
    files_dir = files_directory(file_name, extension)

    if len(files_dir) > 0:
        # it verifies if the current coordinate is inside any coordinate already downloaded
        for i in files_dir:
            if coordinates_list[0] >= coord_value(i[0]) and \
                    coordinates_list[1] >= coord_value(i[1]) and \
                    coordinates_list[2] <= coord_value(i[2]) and \
                    coordinates_list[3] <= coord_value(i[3]) and \
                    extension == i[4]:
                return list_to_file_name(i)
    return False


def list_to_file_name(file_list):
    """
    This function transforms the list that verify_file_exists function returns
    in a file name.

    :param file_list:       list

    :return:                String
    """

    name = file_list[0]
    for i in range(1, len(file_list)-1):
        name += '_' + file_list[i]
    name += '.' + file_list[-1]
    return name


def def_file_name(directory, coordinates_points, extension):
    coordinates_list = Coordinates.coordinates_list_bbox(coordinates_points)
    file_name = directory + Coordinates.def_file_name(coordinates_list) + extension

    return file_name