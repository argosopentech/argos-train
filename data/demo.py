from argostrain.dataset import *
from argostrain.sbd import *

input_dataset = FileDataset(open('testdata_source'), open('testdata_target'))
sbd_dataset = generate_sbd_data(input_dataset)

dataset = CompositeDataset(input_dataset) + CompositeDataset(sbd_dataset)


print(dataset)
