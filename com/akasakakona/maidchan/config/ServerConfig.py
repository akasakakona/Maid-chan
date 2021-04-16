from .SimpleConfig import SimpleConfig
import os
import json
from ..core import Util


class ServerConfig:

    # KEEP IDENTICAL TO ConfigManager __SERVER_PATH
    __SERVERS_PATH = "./servers/"

    __CONFIG_MAIN = "config"
    __CONFIG_MAIN_FILE = "config.json"

    def __init__(self, server_id):
        self.server_id = server_id
        folder = self.__SERVERS_PATH+server_id+"/"
        self.configs = dict()
        # Main config
        folder = self.__SERVERS_PATH + self.server_id + "/"
        if not os.path.isfile(folder + self.__CONFIG_MAIN_FILE):
            Util.log(self.server_id + " does not have a config.json, generating one for them.")
            with open(folder + self.__CONFIG_MAIN_FILE, "x") as file:
                json.dump(self.get_config_main_default(), file, indent=4)
        self.configs[self.__CONFIG_MAIN] = SimpleConfig(folder+self.__CONFIG_MAIN_FILE)

    def get_config_main_default(self):
        data = {
            "id": self.server_id,
            "modList": [],
            "lang": "en",
            "greetChannel": 0,
            "greetPhase": ""
        }
        return data

    def get(self, key):
        return self.configs[key]
