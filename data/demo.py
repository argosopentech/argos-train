#!/usr/bin/env python3

from argostrain.dataset import *
from argostrain.sbd import *

# Load data
input_dataset = FileDataset(open('testdata_source'), open('testdata_target'))

# Generate SBD data
sbd_dataset = generate_sbd_data(input_dataset)
# At most use 0.1 as much sbd data as input data
trimmed_sbd_data = sbd_dataset.data(int(len(input_dataset) * 0.1))
sbd_dataset = Dataset(trimmed_sbd_data[0], trimmed_sbd_data[1])

# Combine datasets
dataset = CompositeDataset(input_dataset) + CompositeDataset(sbd_dataset)


print(dataset)
