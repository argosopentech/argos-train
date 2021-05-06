from argostrain.utils import *

from pathlib import Path
from collections import deque
from random import randrange, random
import json
import random
import zipfile
import codecs
from multiprocessing import Pool

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
        source = source[:length]
        target = target[:length]
        return (source, target)

class Dataset(IDataset):
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

class LocalDataset(IDataset):
    def __init__(self, filepath):
        """Creates a LocalDataset.

        Args:
            filepath (pathlib.Path): A path to an argos data package with a .argosdata extension.
        """
        source = None
        target = None
        with zipfile.ZipFile(filepath, 'r') as zip_cache:
            dir_names = [info.filename for info in zip_cache.infolist() if info.is_dir()]
            assert(len(dir_names) > 0)
            dir_name = dir_names[0]
            with zip_cache.open(dir_name + 'metadata.json') as metadata_file:
                metadata = json.load(metadata_file)
                self.load_metadata_from_json(metadata)
            with zip_cache.open(dir_name + 'source', 'r') as source_file:
                source = deque()
                for line in codecs.iterdecode(source_file, 'utf8'):
                    source.append(line)
            with zip_cache.open(dir_name + 'target', 'r') as target_file:
                target = deque()
                for line in codecs.iterdecode(target_file, 'utf8'):
                    target.append(line)
        assert(source != None)
        assert(target != None)
        assert(len(source) == len(target))
        self.source = source
        self.target = target
        filepath = Path(filepath)

    def __str__(self):
        return str(self.name).lower() + '-' + \
                str(self.from_code) + '_' + \
                str(self.to_code)

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

    def data(self, length=None):
        return trim_to_length_random(self.source, self.target, length)

    def __len__(self):
        return len(self.source)

class NetworkDataset(IDataset):
    # Only runs in project root
    CACHE_PATH = Path('data') / Path('cache')

    def __init__(self, metadata):
        """Creates a NetworkDataset.

        Args:
            metadata: A json object from json.load  
        """
        self.load_metadata_from_json(metadata)
        self.local_dataset = None

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
        return str(self) + '.argosdata'

    def filepath(self):
        return Path(NetworkDataset.CACHE_PATH) / self.filename()

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
        if not Path(filepath).exists():
            self.download()
        assert(zipfile.is_zipfile(filepath))
        if self.local_dataset == None:
            self.local_dataset = LocalDataset(filepath)
        return self.local_dataset.data(length)

    def __len__(self):
        return len(self.data()[0])

def get_available_datasets():
    """Returns a list of available NetworkDatasets

    Returns:
        [NetworkDataset]: The available datasets.
    """
    # Needs to be run from project root
    DATA_INDEX = Path('data') / Path('index.json')
    available_datasets = []
    with open(DATA_INDEX) as data_index:
        index = json.load(data_index)
        for metadata in index:
            dataset = NetworkDataset(metadata)
            available_datasets.append(dataset)
    return available_datasets

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
    """A dataset with a max length"""
    def __init__(self, dataset, length=None):
        """Creates a TrimmedDataset.

        Args:
            dataset (IDataset): The dataset to be trimmed.
            length (int): The length to trim to.
        """
        self.dataset = dataset
        self.length = length

    def data(self, length=None):
        source, target = self.dataset.data(self.length)
        return trim_to_length_random(source, target, length)

    def __len__(self):
        if self.length == None:
            return len(self.dataset)
        return min(len(self.dataset), self.length)

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

class TransformedDatasetNew(IDataset):
    """A dataset with a tranformation applied to it."""
    def __init__(self, dataset, transform):
        """Creates a TransformedDataset.

        Args:
            dataset (IDataset): The dataset to be transformed.
            transform ((str, str) -> (str, str)): A lambda transformation to apply to data.
        """
        self.dataset = dataset
        self.transform = transform

    def data(self, length=None):
        source, target = self.dataset.data(length)
        data = list(zip(source, target))

        try:
            # Split over multiple processes
            transformed_data = None
            with Pool() as procs_pool:
                transformed_data = procs_pool.map(self.transform, data)

                source = [source_line for source_line, target_line in transformed_data]
                target = [target_line for source_line, target_line in transformed_data]
                return trim_to_length_random(source, target, length)
        except Exception as e:
            warning(f'Failed to transform data with exception {str(e)}')
            return (deque(), deque())

    def __len__(self):
        return len(self.dataset)

class InvertedDataset(IDataset):
    """A Dataset with source and target flipped"""
    def __init__(self, dataset):
        self.non_inverted_dataset = dataset
        self.inverted_source = None
        self.inverted_target = None

    def data(self, length=None):
        if self.inverted_source == None:
            source, target = self.non_inverted_dataset.data(length)
            self.inverted_source = target
            self.inverted_target = source
        return (self.inverted_source, self.inverted_target)

    def __len__(self):
        return len(self.non_inverted_dataset)

class ShuffledDataset(IDataset):
    """A dataset with elements in a randomized order."""
    def __init__(self, dataset):
        self.dataset = dataset
        self.shuffled_dataset = None

    def data(self, length=None):
        if self.shuffled_dataset == None:
            source, target = self.dataset.data()
            zipped_data = list(zip(source, target))
            random.shuffle(zipped_data)
            shuffled_source = [x[0] for x in zipped_data]
            shuffled_target = [x[1] for x in zipped_data]
            self.shuffled_dataset = Dataset(shuffled_source, shuffled_target)
        return self.shuffled_dataset.data()

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

def export_dataset(dataset):
    source_filepath = Path('source_export')
    target_filepath = Path('target_export')
    assert(not source_filepath.exists())
    assert(not target_filepath.exists())
    source, target = dataset.data()
    with open(source_filepath, 'w') as f:
        f.writelines(source)
    with open(target_filepath, 'w') as f:
        f.writelines(target)
    
