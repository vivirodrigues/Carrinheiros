import json


class JsonDB:
    def __init__(self, file_name, path):
        self.file_name = file_name
        self.path = path

    def get_file_content(self):
        f = open(self.path + self.file_name + '.json', "r")
        if f.mode == 'r':
            contents = f.read()
            contents = json.loads(contents)
            return contents
