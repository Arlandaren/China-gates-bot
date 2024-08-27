import json

import os

directory_path = 'data/'

files = [f for f in os.listdir(directory_path) if os.path.isfile(os.path.join(directory_path, f))]


for file_name in files:

    with open(directory_path+file_name, "r", encoding="utf-8") as file:
        data = json.load(file)

    counts = []
    counts_list = []

    for item in data:
        for inner_item in item['data']:
            count_value = inner_item['count']
            bph_value = inner_item['bph']

            if count_value != 0:
                counts.append(count_value)
                counts_list.append(file_name)
    print(counts_list)

