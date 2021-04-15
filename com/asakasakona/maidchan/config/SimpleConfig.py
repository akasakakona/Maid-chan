import json
import os
from ..core import Util


class SimpleConfig:
    file = None
    config = None

    def __init__(self, path):
        try:
            self.file = open(path)
            self.config = json.load(self.file)
            Util.log("Loaded SimpleConfig \'{path}\'")
        except FileNotFoundError:
            Util.log(f"MAID ERROR: \'{path}\' NOT FOUND UNDER \'{os.getcwd()}\'")
        pass

    def get(self, key):
        return self.config[key]
