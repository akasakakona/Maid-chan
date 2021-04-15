from .SimpleConfig import SimpleConfig
from .. core import Util


class ConfigManager:

    __instance = None

    @staticmethod
    def instance():
        if ConfigManager.__instance is None:
            Util.log("ConfigManager instance is None, creating instance")
            ConfigManager()
        return ConfigManager.__instance

    def __init__(self):
        if ConfigManager.__instance is not None:
            raise Exception("ConfigManager is a singleton!")
        else:
            ConfigManager.__instance = self
            self.load()
        pass

    __global_config = None
    __server_configs = dict()

    def load(self):
        self.load_global()

    def load_global(self):
        self.__global_config = SimpleConfig("config.json")
        Util.log("Loaded " + self.__global_config.file.name)

    @staticmethod
    def get_global_config():
        return ConfigManager.__global_config

    @staticmethod
    def get_server_config(server_id):
        return ConfigManager.__server_configs[server_id]