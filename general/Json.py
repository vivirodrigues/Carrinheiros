import json


def json_content(directory, file_name):
    """
    This function gets the content of a json file and
    returns as dictionary.

    :param directory:    String
                         The folder where the json file is located

    :param file_name:    String
                         The name of the json file

    :return:             dict
                         The content of the json file as python
                         dictionary
    """
    f = open(directory + file_name + '.json', "r")
    if f.mode == 'r':
        contents = f.read()
        contents = json.loads(contents)
        return contents


