import config.config as __config
from config.config import *

# Get the config for a key
# @arg k: str - key
# @arg d - default, if there is no config option `key`
def get(k: str, d=None):
    return getattr(__config, k, d)
