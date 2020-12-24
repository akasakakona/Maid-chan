import discord
from discord.ext import commands
import json
import os

class Debugging(commands.Cog):
    def __init__(self, maid):
        self.maid = maid
        with open('config.json') as f:
            config_dict = json.load(f)
            self.ADMIN = config_dict['ADMIN']
            f.close()
    
    @commands.Cog.listener()
    async def on_ready(self):
        await self.maid.change_presence(status=discord.Status.online, activity = discord.Game(" with catgirls"))
        self.maid.load_extension(f'extensions.music')
        print(f"Logged in as {self.maid.user.name}")

    @commands.command()
    async def ping(self, ctx):
        await ctx.send(f'The ping is {round(self.maid.latency * 1000)}ms')

    @commands.command(aliases=['off'])
    async def shutdown(self, ctx):
        if(ctx.author.id != self.ADMIN):
            return await ctx.send("MAID ERROR: ACCESS DENIED! YOU ARE NOT AKASAKAKONA-SAMA! GO AWAY!! ‎(︶ ︿ ︶)")
        await ctx.send('Settings Saved! AkasakaKona-Sama! See you later~  (> ^ <)')

        await self.maid.close()

def setup(maid):
    maid.add_cog(Debugging(maid))