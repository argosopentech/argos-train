import codecs
import itertools
import json
import os
import random
import uuid
import zipfile
from collections import deque
from multiprocessing import Pool
from pathlib import Path
from random import random, randrange
from urllib import parse, request
from urllib.parse import urlparse

import argostrain.networking
from argostrain import settings, utils
from argostrain.utils import error, info, warning


class IDataset:
    def data(self, length=None):
        """Returns a tuple of source and target data.

        Args:
            length (int): Trim to length if not None

        Source and target data is collections.deque
        """
        raise NotImplementedError()

    def datapath(self):
        """Returns a tuple of (source_dataset_path, target_dataset_path)
        If a local file doesn't exist create it
        """
        raise NotImplementedError()

    def __str__(self):
        return "Dataset"

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
        source = deque(itertools.islice(source, 0, length))
        target = deque(itertools.islice(target, 0, length))
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
        self.datapath = None
        self.guid = None

    def data(self, length=None):
        return trim_to_length_random(self.source, self.target, length)

    def datapath(self):
        if self.datapath is not None:
            return self.datapath
        self.guid = uuid.uuid4()
        source_datapath = settings.CACHE_PATH / f"{str(self.guid)}_source.txt"
        target_datapath = settings.CACHE_PATH / f"{str(self.guid)}_target.txt"
        with open(source_datapath, "w") as source_file:
            source_file.writelines(self.source)
        with open(target_datapath, "w") as target_file:
            target_file.writelines(self.target)
        self.datapath = (source_datapath, target_datapath)
        return self.datapath

    def __len__(self):
        return len(self.source)

def append_datapaths(dataset1, dataset2, output_datapath_):
    """Appends the datapaths of two datasets and returns the new datapaths.

    Use shell commands for efficiency.

    Args:
        dataset1 (IDataset): The first dataset
        dataset2 (IDataset): The second dataset
        output_datapath (pathlib.Path): The output datapath

    Returns:
        pathlib.Path: The output datapath
    """
    source1_path, target1_path = dataset1.datapath()
    source2_path, target2_path = dataset2.datapath()
    output_source_path = output_datapath / "source"
    output_target_path = output_datapath / "target"
    os.system(f"cat {source1_path} {source2_path} > {output_source_path}")
    os.system(f"cat {target1_path} {target2_path} > {output_target_path}")
    return (output_source_path, output_target_path)

class CachedDataset(IDataset):
    def __init__(self, source_datapath, target_datapath):
        """Creates a CachedDataset.

        Args:
            source_datapath (pathlib.Path): The path to the source data file
            target_datapath (pathlib.Path): The path to the target data file
        """
        self.source_datapath = source_datapath
        self.target_datapath = target_datapath
        self.source = None
        self.target = None

    def data(self, length=None):
        if self.source == None and self.target == None:
            with open(self.source_datapath) as source_file:
                self.source = source_file.readlines()
            with open(self.target_datapath) as target_file:
                self.target = target_file.readlines()
        return trim_to_length_random(self.source, self.target, length)

    def __len__(self):
        source, target = self.data()
        return len(source)

    def datapath(self):
        return (self.source_datapath, self.target_datapath)


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
        sum_of_weights = sum(
            [dataset_and_weight[1] for dataset_and_weight in self.datasets]
        )
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

    def datapath(self):
        source_datapath = settings.CACHE_PATH / f"composite_{str(uuid.uuid4())}_source.txt"
        target_datapath = settings.CACHE_PATH / f"composite_{str(uuid.uuid4())}_target.txt"
        for dataset, weight in self.datasets:
            dataset_source_datapath, dataset_target_datapath = dataset.datapath()
            for i in range(weight):
                os.system(f"cat {dataset_source_datapath} >> {source_datapath}")
                os.system(f"cat {dataset_target_datapath} >> {target_datapath}")
        return (source_datapath, target_datapath)


    def __len__(self):
        return sum([len(dataset) for dataset in self.datasets])


class LocalDataset(IDataset):
    def __init__(self, filepath):
        """Creates a LocalDataset.

        Args:
            filepath (pathlib.Path): A path to an argos data package with a .argosdata extension.
        """
        self.unzip_dir = settings.CACHE_PATH / f"{str(uuid.uuid4())}"
        if not self.unzip_dir.exists():
            with zipfile.ZipFile(filepath, "r") as zip_cache:
                zip_cache.extractall(self.unzip_dir)
        with open(self.unzip_dir / "metadata.json") as metadata_file:
            metadata = json.load(metadata_file)
            self.load_metadata_from_json(metadata)
        self.source = None
        self.target = None

    def __str__(self):
        return (
            str(self.name).lower() + "-" + str(self.from_code) + "_" + str(self.to_code)
        )

    def load_metadata_from_json(self, metadata):
        """Loads package metadata from a JSON object.

        Args:
            metadata: A json object from json.load
        """
        self.name = metadata.get("name")
        self.type = metadata.get("type")
        self.from_code = metadata.get("from_code")
        self.to_code = metadata.get("to_code")
        self.size = metadata.get("size")
        self.links = metadata.get("links")

    def data(self, length=None):
        if self.source == None and self.target == None:
            self.source = deque()
            self.target = deque()
            with open(self.unzip_dir / "source", "r", encoding="utf8") as source_file:
                for line in source_file:
                    self.source.append(line)
            with open(self.unzip_dir / "target", "r", encoding="utf8") as target_file:
                for line in target_file:
                    self.target.append(line)

        return trim_to_length_random(self.source, self.target, length)

    def datapath(self):
        return (self.unzip_dir / "source", self.unzip_dir / "target")

    def __len__(self):
        return len(self.source)


class NetworkDataset(IDataset):
    def __init__(self, metadata):
        """Creates a NetworkDataset.

        Args:
            metadata: A json object from json.load
        """
        self.load_metadata_from_json(metadata)
        self.filepath = None
        self.local_dataset = None

    def load_metadata_from_json(self, metadata):
        """Loads package metadata from a JSON object.

        Args:
            metadata: A json object from json.load
        """
        self.name = metadata.get("name")
        self.type = metadata.get("type")
        self.from_code = metadata.get("from_code")
        self.to_code = metadata.get("to_code")
        self.size = metadata.get("size")
        self.links = metadata.get("links")
        self.reference = metadata.get("reference")

    def __str__(self):
        return (
            str(self.name).lower() + "-" + str(self.from_code) + "_" + str(self.to_code)
        )

    def filename(self):
        return str(self) + ".argosdata"

    def download(self):
        """Downloads the package and returns its path"""
        url = self.links[0]
        parsed_url = urlparse(url)
        self.filepath = None
        if parsed_url.scheme == "file":
            self.filepath = Path(parsed_url.path)
        elif parsed_url.scheme == "http" or parsed_url.scheme == "https":
            settings.CACHE_PATH.mkdir(parents=True, exist_ok=True)
            self.filepath = settings.CACHE_PATH / self.filename()
            if not self.filepath.exists():
                data = argostrain.networking.get(url)
                if data is None:
                    error(f"Could not download {url}")
                with open(self.filepath, "wb") as f:
                    f.write(data)
        else:
            raise Exception("Unknown scheme " + url)
        assert zipfile.is_zipfile(self.filepath)
        if self.local_dataset == None:
            self.local_dataset = LocalDataset(self.filepath)
        return self.filepath

    def data(self, length=None):
        if self.local_dataset is None:
            self.download()
        return self.local_dataset.data(length)

    def datapath(self):
        if self.local_dataset is None:
            self.download()
        return self.local_dataset.datapath()


    def __len__(self):
        return len(self.data()[0])


def get_available_datasets():
    """Returns a list of available NetworkDatasets

    Returns:
        [IDataset]: The available datasets.
    """
    # Needs to be run from project root
    DATA_INDEX = Path("data-index.json")
    available_datasets = []
    with open(DATA_INDEX) as data_index:
        index = json.load(data_index)
        for metadata in index:
            dataset = NetworkDataset(metadata)
            available_datasets.append(dataset)
    return available_datasets



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
        self.target_transform = (
            transform if target_transform == None else target_transform
        )

    def data(self, length=None):
        source, target = self.dataset.data(length)
        source = [self.transform(x) for x in source]
        target = [self.target_transform(x) for x in target]
        return trim_to_length_random(source, target, length)

    def __len__(self):
        return len(self.dataset)


class TransformedDatasetNew(IDataset):
    """A dataset with a tranformation applied to it."""

    """Lambdas must be defined at top level of file: https://stackoverflow.com/questions/8804830/python-multiprocessing-picklingerror-cant-pickle-type-function"""

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
                print(self.transform, type(data))
                transformed_data = procs_pool.map(self.transform, data)

                source = [source_line for source_line, target_line in transformed_data]
                target = [target_line for source_line, target_line in transformed_data]
                return trim_to_length_random(source, target, length)
        except Exception as e:
            warning(f"Failed to transform data with exception {str(e)}")
            return None

    def __len__(self):
        return len(self.dataset)


# Does not work
class FilteredDataset(IDataset):
    """A dataset with a filter lambda applied to it"""

    def __init__(self, dataset, filter_lambda):
        """Creates a FilteredDataset.

        Args:
            dataset (IDataset): The dataset to be transformed.
            filter_lambda ((str, str) -> bool): A lambda filter to apply to data.
        """
        self.dataset = dataset
        self.filter_lambda = filter_lambda
        self.filtered = None

    def data(self, length=None):
        if self.filtered is not None:
            return self.filtered
        transform_lambda = lambda x: x if self.filter_lambda(x) else (None, None)
        transformed_dataset = TransformedDatasetNew(self.dataset, transform_lambda)
        transformed_data = transformed_dataset.data()
        source = deque()
        target = deque()
        for source_line, target_line in transformed_data:
            if source_line is not None and target_line is not None:
                source.append(source_line)
                target.append(target_line)
        self.filtered = trim_to_length_random(source, target, length)
        return self.filtered

    def __len__(self):
        if self.filtered is None:
            self.data()
        return len(self.filtered[0])


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
    source_filepath = Path("source_export")
    target_filepath = Path("target_export")
    assert not source_filepath.exists()
    assert not target_filepath.exists()
    source, target = dataset.data()
    with open(source_filepath, "w") as f:
        f.writelines(source)
    with open(target_filepath, "w") as f:
        f.writelines(target)


def assert_eql_src_tgt_len(dataset):
    data = dataset.data()
    assert len(data[0]) == len(data[1])
