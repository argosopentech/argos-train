#!/usr/bin/env python3

import sys
import os
import argparse
import random
from functools import partial

import argostrain
from argostrain.dataset import *

# Read args
parser = argparse.ArgumentParser()
parser.add_argument('source_data')
parser.add_argument('target_data')
args = parser.parse_args()

# Build dataset
dataset = FileDataset(open(args.source_data), open(args.target_data))
print("Read data from file")

# Check source and target same length
assert_eql_src_tgt_len(dataset)

# Filter out bad data
html_entities = ['&apos;', '&nbsp;', '&lt;', '&gt;', '&quot;']
html_tags = ['<a>', '<p>', '<h1>', '<i>']
naughty_strings = html_entities + html_tags
unfiltered_source, unfiltered_target = dataset.data()
source = deque()
target = deque()
for i in range(len(unfiltered_source)):
    source_line = unfiltered_source[i]
    target_line = unfiltered_target[i]
    for n in naughty_strings:
        if n in source_line or n in target_line:
            continue
        source.append(source_line)
        target.append(target_line)
dataset = Dataset(source, target)

print("Done filtering data")

# Split and write data
source_data, target_data = dataset.data()
source_data = list(source_data)
target_data = list(target_data)

os.mkdir('run/split_data')
source_valid_file = open('run/split_data/src-val.txt', 'w')
source_train_file = open('run/split_data/src-train.txt', 'w')
target_valid_file = open('run/split_data/tgt-val.txt', 'w')
target_train_file = open('run/split_data/tgt-train.txt', 'w')

VALID_SIZE = 2000
assert(len(source_data) > VALID_SIZE)
source_valid_file.writelines(source_data[0:VALID_SIZE])
source_train_file.writelines(source_data[VALID_SIZE:])
target_valid_file.writelines(target_data[0:VALID_SIZE])
target_train_file.writelines(target_data[VALID_SIZE:])

source_valid_file.close()
source_train_file.close()
target_valid_file.close()
target_train_file.close()
print('Done splitting data')

