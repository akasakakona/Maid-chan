import json
import os
from ..core import Util


class SimpleConfig:
    path = None
    config = None

    def __init__(self, path):
        self.path = path
        try:
            with open(path) as file:
                self.config = json.load(file)
            Util.log(f"Loaded SimpleConfig \'{path}\'")
        except FileNotFoundError:
            Util.log(f"MAID ERROR: \'{path}\' NOT FOUND UNDER \'{os.getcwd()}\'")
        pass

    def get_path(self):
        return self.path

    def get_config(self):
        return self.config

    def get(self, key):
        return self.config[key]

    def set(self, key, value):
        self.config[key] = value

    def save(self):
        with open(self.path, "w") as file:
            json.dump(self.config, file, indent=4)

    # try to use set() and save() instead of this
    def dump(self, data):
        with open(self.path) as file:
            json.dump(data, file, indent=4)
