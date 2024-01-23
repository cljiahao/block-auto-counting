import json


def read_settings():
    """Get settings data that does not need to be written back \n
    by reading json file consisting basic setting information"""
    settings = read_json("json/settings.json")
    def_code = read_json("json/staticnames.json")
    color = read_json("json/colors.json")
    settings.update(def_code)
    settings.update(color)

    return settings


def read_json(file_path):
    with open(file_path, "r") as f:
        data = json.load(f)

    return data


def write_json(file_path, data):
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
