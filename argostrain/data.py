import sys
import os
import argparse
import random
from functools import partial

import argostrain
from argostrain.dataset import *


def prepare_data(source_data, target_data):

    # Build dataset
    dataset = FileDataset(open(source_data), open(target_data))
    print("Read data from file")

    # Split and write data
    source_data, target_data = dataset.data()
    source_data = list(source_data)
    target_data = list(target_data)

    VALID_SIZE = 2000
    assert(len(source_data) > VALID_SIZE)

    os.mkdir('run/split_data')

    source_valid_file = open('run/split_data/src-val.txt', 'w')
    source_valid_file.writelines(source_data[0:VALID_SIZE])
    source_valid_file.close()

    source_train_file = open('run/split_data/src-train.txt', 'w')
    source_train_file.writelines(source_data[VALID_SIZE:])
    source_train_file.close()

    target_valid_file = open('run/split_data/tgt-val.txt', 'w')
    target_valid_file.writelines(target_data[0:VALID_SIZE])
    target_valid_file.close()

    target_train_file = open('run/split_data/tgt-train.txt', 'w')
    target_train_file.writelines(target_data[VALID_SIZE:])
    target_train_file.close()

    print('Done splitting data')
