from .SimpleConfig import SimpleConfig
from .ConfigManager import ConfigManager
import os


class ServerConfig:

    __CONFIG_MAIN = "config"

    def __init__(self, server_id):
        folder = ConfigManager.SERVERS_PATH+server_id+"/"
        self.configs = dict()
        # Main config
        self.configs[self.__CONFIG_MAIN] = SimpleConfig(folder+"config.json")

    def get(self, key):
        return self.configs[key]
