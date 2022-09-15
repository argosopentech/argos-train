#!/bin/env python

import random
from pathlib import Path

import argostrain
from argostrain.dataset import *

MAX_DATASET_SIZE = 5 * (10 ** 5)

source_file_path = Path("run/source")
target_file_path = Path("run/target")

assert not source_file_path.exists()
assert not target_file_path.exists()

available_datasets = get_available_datasets()

datasets = [
    TrimmedDataset(available_dataset, MAX_DATASET_SIZE)
    for available_dataset in available_datasets
]

for dataset in datasets:
    generated_source = list()
    generated_target = list()
    source_data, target_data = dataset.data()
    for i in range(0, len(source_data) - 1):
        first_sentence = source_data[i]
        second_sentence = source_data[i + 1]

        # Randomly split second sentence
        second_sentence = second_sentence[0 : random.randint(0, len(second_sentence))]

        # Space pad end of first sentence
        if first_sentence[-1] != " ":
            first_sentence = first_sentence + " "

        generated_source.append(first_sentence + second_sentence)
        generated_target.append(first_sentence)

        # Write generated data to file
        with open(source_file_path, "a") as source_file:
            source_file.writelines(generated_source)
        with open(target_file_path, "a") as target_file:
            target_file.writelines(generated_target)
