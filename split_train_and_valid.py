#!/usr/bin/env python3

import sys
import os
import argparse
import random
import emoji

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
print("Read data from file")

# Check that source and target data are the same length
if len(source_data) != len(target_data):
    raise Exception(
            f'Source and target data not the same size ' \
            '{len(source_data)} vs {len(target_data)}')

# Filter out bad data
html_entities = ['&apos;', '&nbsp;', '&lt;', '&gt;', '&quot;']
html_tags = ['<a>', '<p>', '<h1>', '<i>']
naughty_strings = html_entities + html_tags + list(emoji.UNICODE_EMOJI_ENGLISH.keys())
filtered_source_data = []
filtered_target_data = []
for i in range(len(source_data)):
    should_filter = False
    for naughty_string in naughty_strings:
        if naughty_string in source_data[i] or naughty_string in target_data[i]:
            should_filter = True
            break
    if should_filter:
        print(f'Filtering {source_data[i]} - {target_data[i]}')
    else:
        filtered_source_data.append(source_data[i])
        filtered_target_data.append(target_data[i])
print(f'After filtering {len(filtered_source_data)} lines remaining')
source_data = filtered_source_data
target_data = filtered_target_data

# Split and write data
os.mkdir('split_data')
source_valid_file = open('split_data/src-val.txt', 'w')
source_train_file = open('split_data/src-train.txt', 'w')
target_valid_file = open('split_data/tgt-val.txt', 'w')
target_train_file = open('split_data/tgt-train.txt', 'w')

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

