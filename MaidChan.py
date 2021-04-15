import discord
import os
import json
from discord.ext import commands


class MaidChan(commands.Bot):
    __instance = None
    __TOKEN = ""
    __PREFIX = ""

    def __init__(self):
        try:
            with open('config.json') as f:
                config_dict = json.load(f)
            self.TOKEN = config_dict['TOKEN']
            self.PREFIX = config_dict['PREFIX']
        except FileNotFoundError:
            print(f"MAID ERROR: \'config.json\' NOT FOUND UNDER CURRENT DIRECTORY: {os.getcwd()}")
        # Create the bot
        super().__init__(command_prefix=commands.when_mentioned_or(self.PREFIX), intents=discord.Intents.all());
        #self.load_extensions()
        self.run()
        pass

    def load_extensions(self):
        for extension in os.listdir('./extensions'):  # load extensions
            if extension.endswith('.py') and extension != "music.py":
                self.load_extension(f'extensions.{extension[:-3]}')
        pass

    @staticmethod
    def instance():
        if MaidChan.__instance is None:
            MaidChan()
        return MaidChan.__instance

    @staticmethod
    def run():
        MaidChan.instance()
        pass

    @staticmethod
    def get_token():
        return MaidChan.__TOKEN

    @staticmethod
    def get_prefix():
        return MaidChan.__PREFIX
