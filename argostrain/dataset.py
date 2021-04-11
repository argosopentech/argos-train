from argostrain.utils import *

from pathlib import Path
from collections import deque
from random import randrange, random
import json
import random
import zipfile
import codecs

import requests

class IDataset:
    def data(self, length=None):
        """Returns a tuple of source and target data.

        Args:
            length: Trim to length if not None

        Source and target data is collections.deque
        """
        raise NotImplementedError()

    def __str__(self):
        source, target = self.data()
        to_return = ''
        for i in range(len(source)):
            to_return += source[i]
            to_return += target[i]
            to_return += '\n'
        return to_return

class Dataset:
    def __init__(self, source, target):
        """Creates a Dataset.

        Args:
            source (collections.deque): Source data
            target (collections.deque): Target data
        """
        self.source = source
        self.target = target

    def data(self, length=None):
        return (self.source, self.target)

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

    def add_dataset(self, child_dataset, weight=1):
        self.datasets.append((child_dataset, weight))

    def __add__(self, other):
        """Adds two CompositeDataset's

        Args:
            other (CompositeDataset): The CompositeDataset to add with
        """
        to_return = CompositeDataset(self)
        to_return.add_dataset(other)
        return to_return

    def __mul__(self, weight):
        """Multiply a CompositeDataset by a weight

        Args:
            weight (int): The weight to multiply with
        """
        return CompositeDataset(self, weight)

    def data(self, length=None):
        source = []
        target = []
        sum_of_weights = sum([dataset_and_weight[1]
                for dataset_and_weight in self.datasets])
        for dataset, weight in self.datasets:
            data = dataset.data(length)
            if length == None:
                for i in range(weight):
                    source += data[0]
                    target += data[1]
            else:
            # Randomly select data to take if over limit
                limit = (weight / sum_of_weights) * length
                if limit < len(data):
                    random.shuffle(data)
                source += data[0][:limit]
                target += data[1][:limit]
        return (source, target)

class NetworkDataset(IDataset):
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

class FileDataset(IDataset):
    def __init__(self, source_file, target_file):
        """Creates a FileDataset

        Args:
            source_file (file): The file-like object containing source data
            target_file (file): The file-like object containing target data
        """
        self.source_file = source_file
        self.target_file = target_file
        self.source = None
        self.target = None

    def data(self, length=None):
        if self.source == None and self.target == None:
            self.source = self.source_file.readlines()
            self.target = self.target_file.readlines()
        return (self.source, self.target)
