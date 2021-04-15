from config.SimpleConfig import SimpleConfig


class ConfigManager:

    __instance = None

    @staticmethod
    def instance():
        if ConfigManager.__instance is None:
            print("ConfigManager instance is None, creating instance")
            ConfigManager()
        return ConfigManager.__instance

    __global_config = None
    __server_configs = dict()

    def __init__(self):
        if ConfigManager.__instance is not None:
            raise Exception("ConfigManager is a singleton!")
        else:
            ConfigManager.__instance = self
            __global_config = SimpleConfig("config.json")
        pass

    def get_global_config(self):
        return self.__global_config

    def get_server_config(self, server_id):
        return self.__server_configs[server_id]