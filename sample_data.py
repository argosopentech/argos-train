#!/usr/bin/env python3

import random
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('source')
parser.add_argument('target')
args = parser.parse_args()

source = [line for line in open(args.source)]
target = [line for line in open(args.target)]

source_len = len(source)
target_len = len(target)
print(f'Source length: {source_len}')
print(f'Target length: {target_len}')
assert(source_len == target_len)

for i in range(10):
    sample = random.randrange(0, source_len)
    print(source[sample])
    print(target[sample])
    print()


