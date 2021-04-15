

class ConfigManager:

    __instance = None

    @staticmethod
    def instance():
        if ConfigManager.__instance is None:
            print("ConfigManager instance is None, creating instance")
            ConfigManager()
        return ConfigManager.__instance

    __global_file = None
    __global_config = None
    __server_configs = dict()

    def __init__(self):
        if ConfigManager.__instance is not None:
            raise Exception("ConfigManager is a singleton!")
        else:
            ConfigManager.__instance = self
            try:
                __global_file = open('config.json')
                with open('config.json') as f:
                    __global_config = json.load(f)
            except FileNotFoundError:
                print(f"MAID ERROR: \'config.json\' NOT FOUND UNDER CURRENT DIRECTORY: {os.getcwd()}")
        pass