import json


def load_file(file_path):
    with open(file_path, "r") as file:
        return file.read()


def read_json(path):
    with open(str(path)) as file:
        content = json.load(file)
    return content


def write_json(path, data):
    with open(str(path), "w") as file:
        json.dump(data, file, indent=4)
