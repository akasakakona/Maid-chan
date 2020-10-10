import discord
from discord.ext import commands
import json
import lavalink

class Music(commands.Cog):
    def __init__(self, maid):
        self.maid = maid

    @commands.command()
    async def play(self, url:str):
        print('fixme!')
        """
        Refer to https://github.com/Devoxin/Lavalink.py/blob/master/lavalink/models.py
        Search for async def play
        There will be a list of actions that can be performed to the lavalink player!!!
        """
def setup(maid):
    maid.add_cog(Music(maid))