import discord
import os
from discord.ext import commands
from ..config.ConfigManager import ConfigManager
from . import Util


class MaidChan(commands.Bot):
    __instance = None

    @staticmethod
    def instance():
        if MaidChan.__instance is None:
            print("MaidChan instance is None, creating instance")
            MaidChan()
        return MaidChan.__instance

    def __init__(self):
        __PREFIX = ""
        __TOKEN = ""
        if MaidChan.__instance is not None:
            raise Exception("MaidChan is a singleton!")
        else:
            MaidChan.__instance = self
            ConfigManager.instance()
            self.TOKEN = ConfigManager.instance().get_global_config().get("TOKEN")
            self.PREFIX = ConfigManager.instance().get_global_config().get("PREFIX")
            # Create the bot
            super().__init__(command_prefix=commands.when_mentioned_or(self.PREFIX), intents=discord.Intents.all())
            self.load_all_extensions()
            Util.log("Maid-Chan Created")
            pass

    def load_all_extensions(self):
        extensions = ["debugging", "entertainment", "moderation"]
        for extension in extensions:
            self.load_one_extension(extension)
        pass

    def load_one_extension(self, name):
        base_path = "com.akasakakona.maidchan.extensions."
        try:
            super().load_extension(base_path+name)
        except Exception as e:
            Util.log(f"{name} Could not be loaded!")
            raise e
        else:
            Util.log("{} has been loaded".format(name))

    def run(self):
        Util.log("Starting Maid Chan")
        super().run(MaidChan.instance().TOKEN)
        pass
