#!/usr/bin/env python3

from pathlib import Path
from collections import deque
import json
import zipfile


import requests

class Dataset:
    CACHE_PATH = Path('cache')

    def load_metadata_from_json(self, metadata):
        """Loads package metadata from a JSON object.
        Args:
            metadata: A json object from json.load
        """
        self.name = metadata.get('name')
        self.type = metadata.get('type')
        self.from_code = metadata.get('from_code')
        self.to_code = metadata.get('to_code')
        self.size = metadata.get('size')
        self.links = metadata.get('links')

    def __str__(self):
        return str(self.name).lower() + '-' + \
                str(self.from_code) + '_' + \
                str(self.to_code)

    def filename(self):
        return str(self) + '.argosmodel'

    def filepath(self):
        return Path(Dataset.CACHE_PATH) / self.filename()

    def download(self):
        """Downloads the package and returns its path"""
        url = self.links[0]
        filepath = self.filepath()
        if not filepath.exists():
            print(f'Downloading {filepath}')
            r = requests.get(url, allow_redirects=True)
            open(filepath, 'wb').write(r.content)
        return filepath

    def data(self):
        """Returns a tuple of source and target data.

        Source and target data is collections.deque
        """
        filepath = self.filepath()
        assert(Path(filepath).exists())
        assert(zipfile.is_zipfile(filepath))
        source = None
        target = None
        with zipfile.ZipFile(filepath, 'r') as zip_cache:
            with zip_cache.open(str(self) + '/source', 'r') as source_file:
                source = deque(source_file.readlines())
            with zip_cache.open(str(self) + '/target', 'r') as target_file:
                target = deque(target_file.readlines())
        assert(source != None)
        assert(target != None)
        assert(len(source) == len(target))
        return (source, target)

DATA_INDEX = Path('index.json')
available_datasets = []
with open(DATA_INDEX) as data_index:
    index = json.load(data_index)
    for data_metadata in index:
        dataset = Dataset()
        dataset.load_metadata_from_json(data_metadata)
        available_datasets.append(dataset)

# Get Spanish data
es_data = list(filter(
        lambda x: x.to_code == 'es',
        available_datasets))
for dataset in es_data:
    dataset.download()
    data = dataset.data()
    print(data)

