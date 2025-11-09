import argparse
import os
import random
import sys
from functools import partial

import argostrain
from argostrain.dataset import *


def prepare_data(source_data_path, target_data_path):
    VALID_SIZE = 2000
    os.makedirs("run/split_data", exist_ok=True)

    # Split source file
    os.system(f"head -n {VALID_SIZE} {source_data_path} > run/split_data/src-val.txt")
    os.system(f"tail -n +{VALID_SIZE + 1} {source_data_path} > run/split_data/src-train.txt")

    # Split target file
    os.system(f"head -n {VALID_SIZE} {target_data_path} > run/split_data/tgt-val.txt")
    os.system(f"tail -n +{VALID_SIZE + 1} {target_data_path} > run/split_data/tgt-train.txt")

    print("Done splitting data")

