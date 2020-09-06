import discord
from discord.ext import commands

class Debugging(commands.Cog):
    def __init__(self, maid):
        self.maid = maid
    
    @commands.Cog.listener()
    async def on_ready(self):
        await self.maid.change_presence(status=discord.Status.idle, activity = discord.Game(" with catgirls"))
        print(f"Logged in as {self.maid.user.name}")

    @commands.command()
    async def ping(self, ctx):
        await ctx.send(f'The ping is {round(self.maid.latency * 1000)}ms')


def setup(maid):
    maid.add_cog(Debugging(maid))