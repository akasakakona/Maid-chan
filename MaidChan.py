import discord
import os
import json
from discord.ext import commands
import traceback


class MaidChan(commands.Bot):
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
        self.load_extensions()
        print("Maid-Chan Created")
        pass

    def load_extensions(self):
        for extension in os.listdir('./extensions'):  # load extensions
            if extension.endswith('.py'):
                try:
                    extension = f"{extension.replace('.py', '')}"
                    super().load_extension(f'extensions.{extension[:-3]}')
                except Exception as e:
                    print(f"{extension} Could not be loaded!")
                    traceback.print_exc()
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
