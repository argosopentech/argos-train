#!/usr/bin/env python3

import json

with open('data-index.json') as index_file:
    index = json.load(index_file)
    index.sort(key=lambda x: x['from_code'] + x['to_code'])
    print(json.dumps(index, indent=4))
