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
            length (int): Trim to length if not None

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

    def __len__(self):
        raise NotImplementedError()

def trim_to_length_random(source, target, length):
    """Trim data to a max of length.

    Data is shuffled in place if over limit.

    Args:
        source (collections.deque): Source data
        target (collections.deque): Target data
        length (int): Trim to length

    Returns:
        (collections.deque, collections.deque): Trimmed data
    """
    if length == None:
        return (source, target)
    else:
        # Randomly select data to use if over length
        if length < len(source):
            zipped_data = list(zip(source, target))
            random.shuffle(zipped_data)
            source = [x[0] for x in zipped_data]
            target = [x[1] for x in zipped_data]
        source += source[:length]
        target += target[:length]
        return (source, target)

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
        return trim_to_length_random(self.source, self.target, length)

    def __len__(self):
        return len(self.source)

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
        """Adds two CompositeDatasets

        Args:
            other (IDataset): The IDataset to add with
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

    def __len__(self):
        return sum([len(dataset) for dataset in self.datasets])

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

    def data(self, length=None):
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
        return trim_to_length_random(source, target, length)

    def __len__(self):
        return len(self.data()[0])

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
        return trim_to_length_random(self.source, self.target, length)

    def __len__(self):
        return len(self.data()[0])

class TrimmedDataset(IDataset):
    """A dataset with max length"""
    def __init__(self, dataset, length=None):
        """Creates a TrimmedDataset.

        Args:
            dataset (IDataset): The dataset to be trimmed.
            length (int): The length to trim to.
        """
        self.dataset = dataset
        self.length = length

    def data(self, length=None):
        source, target = self.dataset.data(length)
        return (source, target)

    def __len__(self):
        if length == None:
            return len(self.dataset)
        return min(len(self.dataset), length)

class TransformedDataset(IDataset):
    """A dataset with a tranformation applied to it."""
    def __init__(self, dataset, transform, target_transform=None):
        """Creates a TransformedDataset.

        Args:
            dataset (IDataset): The dataset to be transformed.
            transform (str -> str): A lambda transformation to apply to data.
            target_transform (str -> str): A transformation to apply to target data.
                    transform is used if target_transform=None.
        """
        self.dataset = dataset
        self.transform = transform
        self.target_transform = transform if target_transform == None else target_transform

    def data(self, length=None):
        source, target = self.dataset.data(length)
        source = [self.transform(x) for x in source]
        target = [self.target_transform(x) for x in target]
        return trim_to_length_random(source, target, length)

    def __len__(self):
        return len(self.dataset)

def copy_dataset(dataset):
    """Copies a dataset and returns the copy.

    Args:
        dataset (IDataset): The dataset to copy

    Returns:
        IDataset: A copy of the dataset
    """
    source, target = dataset.data()
    return Dataset(source.copy(), target.copy())
