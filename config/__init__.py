import json
from pathlib import Path

import config.config as __config
from config.config import *

# Get the config for a key
# @arg k: str - key
# @arg d - default, if there is no config option `key`
def get(k: str, d=None):
    return getattr(__config, k, d)

# Setup the dynamic configuration helper

class DynamicConfig:
    def __init__(self):
        self.filename = 'config/dynamic_config.json'

        self.data = {}
        if Path(self.filename).is_file():
            with open(self.filename, 'r') as f:
                try:
                    self.data = json.load(f)
                except json.JSONDecodeError:
                    self.data = {}

    # Get the value of a key 
    def get(self, key, default=None):
        return self.data.get(key, default)

    # Set the value of a key
    def set(self, key, value):
        self.data[key] = value
        with open('config/dynamic_config.json', 'w') as f:
            json.dump(self.data, f)

dynamic = DynamicConfig()
