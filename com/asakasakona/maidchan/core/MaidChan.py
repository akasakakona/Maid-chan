import discord
import os
from discord.ext import commands
from ..config.ConfigManager import ConfigManager
from . import Util


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

    def __init__(self):
        if MaidChan.__instance is not None:
            raise Exception("MaidChan is a singleton!")
        else:
            MaidChan.__instance = self
            ConfigManager.instance()
            self.TOKEN = ConfigManager.get_global_config().get("TOKEN")
            self.PREFIX = ConfigManager.get_global_config().get("PREFIX")
            Util.log(self.TOKEN + " " + self.PREFIX)
            # Create the bot
            super().__init__(command_prefix=commands.when_mentioned_or(self.PREFIX), intents=discord.Intents.all());
            self.load_extensions()
            Util.log("Maid-Chan Created")
            pass

    def load_extensions(self):
        for extension in os.listdir('./extensions'):  # load extensions
            if extension.endswith('.py'):
                try:
                    super().load_extension(f'extensions.{extension[:-3]}')
                except Exception as e:
                    Util.log(f"{extension} Could not be loaded!")
                    Util.log()
                else:
                    Util.log("{} has been loaded".format(extension))
        pass

    @staticmethod
    def run():
        Util.log("Starting Maid Chan")
        super(MaidChan.instance()).run(MaidChan.__TOKEN)
        pass
