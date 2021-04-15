import discord
import os
from discord.ext import commands
from config.ConfigManager import ConfigManager


class MaidChan(commands.Bot):
    __TOKEN = ""
    __PREFIX = ""
    __instance = None

    @staticmethod
    def instance():
        if MaidChan.__instance is None:
            print("MaidChan instance is None, creating instance")
            MaidChan()
        return MaidChan.__instance

    @staticmethod
    def log(message):
        print("[Maid-Chan] " + message)

    def __init__(self):
        if MaidChan.__instance is not None:
            raise Exception("MaidChan is a singleton!")
        else:
            MaidChan.__instance = self
            self.TOKEN = ConfigManager.get_global_config().get("TOKEN")
            self.PREFIX = ConfigManager.get_global_config().get("PREFIX")
            # Create the bot
            super().__init__(command_prefix=commands.when_mentioned_or(self.PREFIX), intents=discord.Intents.all());
            self.load_extensions()
            print("Maid-Chan Created")
            pass

    def load_extensions(self):
        for extension in os.listdir('./extensions'):  # load extensions
            if extension.endswith('.py'):
                try:
                    super().load_extension(f'extensions.{extension[:-3]}')
                except Exception as e:
                    print(f"{extension} Could not be loaded!")
                    print()
                else:
                    print("{} has been loaded".format(extension))
        pass

    def run(self):
        print("Starting Maid Chan")
        super().run(self.TOKEN)
        pass

    def get_token(self):
        return self.TOKEN

    def get_prefix(self):
        return self.TOKEN
