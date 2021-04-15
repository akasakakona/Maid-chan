import discord
from discord.ext import commands
import os
import json

TOKEN = ""
PREFIX = ""
try:
    with open('config.json') as f:
        config_dict = json.load(f)
    TOKEN = config_dict['TOKEN']
    PREFIX = config_dict['PREFIX']
except FileNotFoundError:
    print(f"MAID ERROR: \'config.json\' NOT FOUND UNDER CURRENT DIRECTORY: {os.getcwd()}")

maid = commands.Bot(command_prefix=commands.when_mentioned_or(PREFIX), intents=discord.Intents.all())

for extension in os.listdir('./extensions'):  # load extensions
    if extension.endswith('.py') and extension != "music.py":
        maid.load_extension(f'extensions.{extension[:-3]}')

maid.run(TOKEN)
