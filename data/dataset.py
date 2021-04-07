from pathlib import Path
from collections import deque
from random import randrange, random
import json
import zipfile
import codecs

import requests

class IDataset:
    def data(self):
        """Returns a tuple of source and target data.

        Source and target data is collections.deque
        """
        raise NotImplementedError()

class CompositeDataset(IDataset):
    def __init__(self, child_dataset=None, weight=1):
        """Creates a new CompositeDataset

        Args:
            child_dataset (IDataset): A child IDataset
            weight (int): The weight for the child_dataset
        """
        # [(<IDataset>, int), (<IDataset>, int)]
        # A list of tuples representing the child datasets and their weights
        self.datasets = list()
        if child_dataset != None:
            self.add_dataset(child_dataset, weight)

    def add_dataset(self, child_dataset, weight):
        self.datasets.append((child_dataset, weight))

    def __add__(self, other):
        """Adds two CompositeDataset's

        Args:
            other (CompositeDataset): The CompositeDataset to add with
        """
        to_return = CompositeDataset(self)
        to_return.add_dataset(other)

    def __mul__(self, weight):
        """Multiply a CompositeDataset by a weight

        Args:
            weight (int): The weight to multiply with
        """
        return CompositeDataset(self, weight)

class Dataset(IDataset):
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
        filepath = self.filepath()
        assert(Path(filepath).exists())
        assert(zipfile.is_zipfile(filepath))
        source = None
        target = None
        with zipfile.ZipFile(filepath, 'r') as zip_cache:
            with zip_cache.open(str(self) + '/source', 'r') as source_file:
                source = deque()
                for line in codecs.iterdecode(source_file, 'utf8'):
                    source.append(line)
            with zip_cache.open(str(self) + '/target', 'r') as target_file:
                target = deque()
                for line in codecs.iterdecode(target_file, 'utf8'):
                    target.append(line)
        assert(source != None)
        assert(target != None)
        assert(len(source) == len(target))
        return (source, target)
