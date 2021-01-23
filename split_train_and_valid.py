#!/usr/bin/env python3

import sys

from_file_name = sys.argv[1]
src_or_tgt = sys.argv[2]

with open(from_file_name, 'r', encoding='utf-8') as source:
    line_count = 0
    valid_lines = 0
    valid_file = open('split_data/' + src_or_tgt + '-val.txt', 'w', encoding='utf-8')
    train_file = open('split_data/' + src_or_tgt + '-train.txt', 'w', encoding='utf-8')
    for line in source:
        if valid_lines < 2000:
            valid_file.write(line)
            valid_lines = valid_lines + 1
        else:
            train_file.write(line)
        line_count += 1

