#!/usr/bin/env python3

from argostrain.dataset import *
from argostrain.sbd import *

import random

# Load data
input_dataset = FileDataset(open('testdata_source'), open('testdata_target'))
input_data_length = len(input_dataset)

# Generate SBD data
sbd_dataset = generate_sbd_data(input_dataset)
# At most use 0.1 as much sbd data as input data
trimmed_sbd_data = sbd_dataset.data(int(input_data_length * 0.1))
sbd_dataset = Dataset(trimmed_sbd_data[0], trimmed_sbd_data[1])

# Combine datasets
dataset = CompositeDataset(input_dataset) + CompositeDataset(sbd_dataset)

# Generate capitalization data
CAPITAL_RATIO = 0.01
capital_length = int(CAPITAL_RATIO * input_data_length)
input_copy = copy_dataset(input_dataset)
all_upper_dataset = TrimmedDataset(input_copy, capital_length)
all_upper_dataset = TransformedDataset(all_upper_dataset, str.upper)
all_lower_dataset = TrimmedDataset(input_copy, capital_length)
all_lower_dataset = TransformedDataset(all_lower_dataset, str.lower)
def random_caps(s):
    to_return = ''
    for c in s:
        caps = random.choice(range(3))
        if caps == 0:
            to_return += c.lower()
        elif caps == 1:
            to_return += c
        else:
            to_return += c.upper()
    return to_return
random_caps_dataset = TrimmedDataset(input_copy, capital_length)
random_caps_dataset = TransformedDataset(random_caps_dataset, random_caps)
all_caps_dataset = CompositeDataset(all_upper_dataset) + CompositeDataset(all_lower_dataset) + \
        CompositeDataset(random_caps_dataset)
dataset += all_caps_dataset

print(dataset)
