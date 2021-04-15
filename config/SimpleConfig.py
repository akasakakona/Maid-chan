import json
import MaidChan


class SimpleConfig:

    file = None
    config = None

    def __init__(self, path):
        try:
            self.file = open(path)
            self.config = json.load(self.file)
            MaidChan.log("Loaded SimpleConfig \'{path}\'")
        except FileNotFoundError:
            MaidChan.log(f"MAID ERROR: path \'{path}\' NOT FOUND")
        pass

    def get(self, key):
        return self.config[key]
