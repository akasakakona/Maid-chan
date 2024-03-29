import os
import json
from ..core import Util
from ..config.SimpleConfig import SimpleConfig


class ServerConfig:
    # KEEP IDENTICAL TO ConfigManager SERVER_PATH
    SERVERS_PATH = "./servers/"

    __CONFIG_MAIN = "config"

    def __init__(self, server_id):
        self.server_id = server_id
        self.configs = dict()
        # Add configs
        folder = self.SERVERS_PATH + str(self.server_id) + "/"
        if not os.path.isdir(folder):
            os.mkdir(path=folder)
        self.__add_config(self.__CONFIG_MAIN, {
            "id": self.server_id,
            "modList": [],
            "lang": "en",
            "greetChannel": 0,
            "greetPhase": "",
            "volume": 0.5
        })

    def __add_config(self, name, default):
        folder = self.SERVERS_PATH + str(self.server_id) + "/"
        if not os.path.isfile(folder + name + ".json"):
            Util.log(str(self.server_id) + f" does not have a {name}.json, generating one for them.")
            with open(folder + name + ".json", "x") as file:
                json.dump(default, file, indent=4)
        self.configs[self.__CONFIG_MAIN] = SimpleConfig(folder + name + ".json")

    def get_main(self):
        return self.configs[self.__CONFIG_MAIN]
