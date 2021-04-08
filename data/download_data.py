#!/usr/bin/env python3

from dataset import *

DATA_INDEX = Path('index.json')
available_datasets = []
with open(DATA_INDEX) as data_index:
    index = json.load(data_index)
    for data_metadata in index:
        dataset = NetworkDataset()
        dataset.load_metadata_from_json(data_metadata)
        available_datasets.append(dataset)

# Get Spanish data
es_data = list(filter(
        lambda x: x.to_code == 'es',
        available_datasets))
dataset = es_data[0]
dataset.download()
data = dataset.data()

