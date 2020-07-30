import json
import csv


def load_json_file(path):
    with open(path) as file:
        data = json.load(file)
    return data


def load_csv_to_dict(path):
    return csv.DictReader(open(path))
