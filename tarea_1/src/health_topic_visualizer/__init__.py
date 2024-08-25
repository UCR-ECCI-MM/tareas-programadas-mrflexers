import json

dummy_data_file_path = './data/dummy_data.json'

with open(dummy_data_file_path) as dummy_data_file:
    dummy_data = json.load(dummy_data_file)