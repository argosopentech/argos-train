#!/usr/bin/env python3

import sys
import os
import argparse
import random

# Read args
parser = argparse.ArgumentParser()
parser.add_argument('source_data')
parser.add_argument('target_data')
args = parser.parse_args()

# Read data from file
source_data_file = open(args.source_data, 'r')
target_data_file = open(args.target_data, 'r')
source_data = source_data_file.readlines()
source_data_file.close()
target_data = target_data_file.readlines()
target_data_file.close()

# Check that source and target data are the same length
if len(source_data) != len(target_data):
    raise Exception(
            f'Source and target data not the same size ' \
            '{len(source_data)} vs {len(target_data)}')

# Filter out bad data
html_entities = ['&apos;', '&nbsp;', '&lt;', '&gt;', '&quot;']
html_tags = ['<a>', '<p>', '<h1>', '<i>']
naughty_strings = html_entities + html_tags
indices_to_remove = []
for i in range(len(source_data)):
    for naughty_string in naughty_strings:
        if naughty_string in source_data[i] or naughty_string in target_data[i]:
            print('Removing line: ' + source_data[i] + ' ' + target_data[i])
            indices_to_remove.append(i)
source_data = [v for i, v in enumerate(source_data) if i not in indices_to_remove]
target_data = [v for i, v in enumerate(target_data) if i not in indices_to_remove]

# Split and write data
VALID_RATIO = 0.3

os.mkdir('split_data')
source_valid_file = open('split_data/src-val.txt', 'w')
source_train_file = open('split_data/src-train.txt', 'w')
target_valid_file = open('split_data/tgt-val.txt', 'w')
target_train_file = open('split_data/tgt-train.txt', 'w')

valid_index = int(VALID_RATIO * len(source_data))
source_valid_file.writelines(source_data[0:valid_index])
source_train_file.writelines(source_data[valid_index:])
target_valid_file.writelines(target_data[0:valid_index])
target_train_file.writelines(target_data[valid_index:])

source_valid_file.close()
source_train_file.close()
target_valid_file.close()
target_train_file.close()

