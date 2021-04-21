from argostrain.dataset import *
from argostrain.utils import *

from collections import deque
import random

OPEN_TAG = '<x>'
CLOSE_TAG = '</x>'

# Returns the index after end of tag if start of open tag
# -1 otherwise
def is_start_of_open_tag(index, line):
    # First character is a '<'
    if line[index] != '<':
        return -1

    # Second isn't /
    if len(line) >= 2 and line[index + 1] == '/':
        return -1

    # Look for '>'
    i = index + 1
    while i < len(line):
        if line[i] == '<':
            return -1
        if line[i] == '>':
            return i + 1
        i += 1
    return -1

# Returns the index after end of tag if start of close tag
# -1 otherwise
def is_start_of_close_tag(index, line):
    if len(line) < 2:
        return -1

    # First two characters are '</'
    if line[index:index + 2] != '</':
        return -1

    # Look for '>'
    i = index + 2
    while i < len(line):
        if line[i] == '<':
            return -1
        if line[i] == '>':
            return i + 1
        i += 1
    return -1

# Returns tuple of source and target line normalized if possible
# None otherwise
def normalize_tags(source_line, target_line):
    tag_count_of_source = -1
    candidate_line_of_source = None
    for source_or_target_index, line in enumerate([source_line, target_line]):
        candidate_line = ''
        tag_depth = 0
        tag_count = 0
        i = 0
        while i < len(line):
            is_open = is_start_of_open_tag(i, line)
            is_close = is_start_of_close_tag(i, line)
            if is_open != -1:
                tag_depth += 1
                tag_count += 1
                candidate_line += OPEN_TAG
                i = is_open - 1
            elif is_close != -1:
                tag_depth -= 1
                tag_count += 1
                candidate_line += CLOSE_TAG
                i = is_close - 1
            else:
                candidate_line += line[i]

            if tag_depth < 0:
                break

            i += 1
        if tag_depth != 0:
            # Invalid tags
            return None

        if source_or_target_index == 0:
            tag_count_of_source = tag_count
            candidate_line_of_source = candidate_line
        elif source_or_target_index == 1:
            if tag_count_of_source == tag_count and tag_count > 0:
                return (candidate_line_of_source, candidate_line)
            else:
                return None


        

    
