import discord
from discord.ext import commands
import random
import json

class Entertainment(commands.Cog):
    def __init__(self, maid):
        self.maid = maid
        self.bullets = [0, 0, 0, 0, 0, 0]
        self.shotCounter = 0
        self.ENGuilds = []
        self.CNGuilds = []
        try:
            with open('config.json') as f:
                config_dict = json.load(f)
                for gid in config_dict['ENGuilds']:
                    self.ENGuilds.append(gid)
                for gid in config_dict['CNGuilds']:
                    self.CNGuilds.append(gid)
        except FileNotFoundError:
            print("File not found!")

    
    @commands.command(brief = "Play Russian Roulette with your friends!")
    async def RR(self, ctx):
        if(self.shotCounter == 0):
            self.bullets.insert(random.randint(0, 6), 1)

        if(self.bullets[0] == 1):
            self.shotCounter += 1
            if(ctx.message.guild.id in self.ENGuilds):
                await ctx.send(f"OOF, {ctx.author.name} is dead! The chance of this happening is {round((self.shotCounter / 7.0)*100)}%!")
            elif(ctx.message.guild.id in self.CNGuilds):
                await ctx.send(f"啊，{ctx.author.name}挂了！概率是{round((self.shotCounter / 7.0)*100)}%！")
            self.shotCounter = 0
            self.bullets = [0, 0, 0, 0, 0, 0]
        else:
            self.shotCounter += 1
            self.bullets.pop(0)
            if(ctx.message.guild.id in self.ENGuilds):
                await ctx.send(f"Congrats! {ctx.author.name} is still alive!")
            elif(ctx.message.guild.id in self.CNGuilds):
                await ctx.send(f"恭喜! {ctx.author.name}还活着!")
    

def setup(maid):
    maid.add_cog(Entertainment(maid))

