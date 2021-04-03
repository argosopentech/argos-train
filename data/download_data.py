#!/usr/bin/env python3

from pathlib import Path
import json

import requests

class Dataset:
    CACHE_PATH = Path('cache')

    def load_metadata_from_json(self, metadata):
        """Loads package metadata from a JSON object.
        Args:
            metadata: A json object from json.load
        """
        self.name = metadata.get('name')
        self.type = metadata.get('type')
        self.from_code = metadata.get('from_code')
        self.to_code = metadata.get('to_code')
        self.size = metadata.get('size')
        self.links = metadata.get('links')

    def __str__(self):
        return '-'.join([
                str(self.name),
                str(self.type),
                str(self.from_code),
                str(self.to_code),
                str(self.name)])

    def download(self):
        """Downloads the package and returns its path"""
        url = self.links[0]
        filename = str(self) + '.argosdata'
        filepath = CACHE_PATH / filename
        if not filepath.exists():
            r = requests.get(url, allow_redirects=True)
            open(filepath, 'wb').write(r.content)
        return filepath


DATA_INDEX = Path('index.json')
with open(DATA_INDEX) as data_index:
    index = json.load(data_index)
    print(index)
