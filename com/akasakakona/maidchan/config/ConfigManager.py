from .SimpleConfig import SimpleConfig
from .ServerConfig import ServerConfig
from ..core import Util
import os


# Singleton ConfigManager class!
# To access configs, use
# from ConfigManager import ConfigManager
# and
# ConfigManager.instance().get_global_config()
# or
# ConfigManager.instance().get_server_config(server_id)
class ConfigManager:
    __instance = None

    # DO NOT TOUCH THIS WHILE RUNNING
    SERVERS_PATH = "./servers/"

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
        self.load_servers()

    def load_global(self):
        self.__global_config = SimpleConfig("config.json")
        Util.log("Loaded " + self.__global_config.path)

    def load_servers(self):
        if not os.path.isdir(self.SERVERS_PATH):
            os.mkdir(self.SERVERS_PATH)
        Util.log(os.listdir(self.SERVERS_PATH))
        for file in os.listdir(self.SERVERS_PATH):
            if os.path.isdir(file):
                self.__server_configs[file] = ServerConfig(file)

    def get_global_config(self):
        return self.__global_config

    def get_server_config(self, server_id):
        return self.__server_configs[server_id]
