import discord
import os
import json
from discord.ext import commands


class MaidChan(commands.Bot):
    __TOKEN = ""
    __PREFIX = ""
    __instance = None

    @staticmethod
    def instance():
        if MaidChan.__instance is not MaidChan:
            print("Maid Chan instance is None, creating instance")
            MaidChan()
        return MaidChan.__instance

    def __init__(self):
        if MaidChan.__instance is MaidChan:
            raise Exception("MaidChan is a singleton!")
        else:
            MaidChan.__instance = MaidChan()
            try:
                with open('config.json') as f:
                    config_dict = json.load(f)
                self.TOKEN = config_dict['TOKEN']
                self.PREFIX = config_dict['PREFIX']
            except FileNotFoundError:
                print(f"MAID ERROR: \'config.json\' NOT FOUND UNDER CURRENT DIRECTORY: {os.getcwd()}")
            # Create the bot
            super().__init__(command_prefix=commands.when_mentioned_or(self.PREFIX), intents=discord.Intents.all());
            super().load_extension('extensions.debugging')
            #self.load_extensions()
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
