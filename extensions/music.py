import discord
from discord.ext import commands
import json

class Music(commands.Cog):
    def __init__(self, maid):
        self.maid = maid

def setup(maid):
    maid.add_cog(Music(maid))