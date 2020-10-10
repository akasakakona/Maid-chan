import json
import discord
from discord.ext import commands
import discord.utils
import os

class Server:
    def __init__(self, guildID):
        self.id = guildID
        self.modList = []
        self.lang = "en"
        self.greetChannel = 0
        self.greetPhrase = ""


class Moderation(commands.Cog):
    def __init__(self, maid):
        self.maid = maid

    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        with open('config.json') as f:
            config_dict = json.load(f)
            f.close()
        newServer = Server(guild.id)
        newServer.modList.append(guild.owner_id)
        #FIXME: maybe prompt the owner to set up the bot
        config_dict['ServerList'][guild.id] = newServer.__dict__
        self.modSet(config_dict)
        


    @commands.Cog.listener()
    async def on_member_join(self, member):
        with open('config.json') as f:
            config_dict = json.load(f)
            f.close()
        channel = member.guild.get_channel(config_dict['ServerList'][str(member.guild.id)]['greetChannel'])
        if(channel is not None):
            greetPhrase = config_dict['ServerList'][str(member.guild.id)]['greetPhrase']
            if(greetPhrase != ""):
                await channel.send(greetPhrase)

    @commands.command()
    async def setLang(self, ctx, lang:str):
        with open('config.json') as f:
            config_dict = json.load(f)
            f.close()
        if(ctx.author.id != config_dict["ADMIN"] and ctx.author.id not in config_dict['ServerList'][str(ctx.author.guild.id)]['modList']):
            await ctx.send('MAID ERROR: PERMISSION DENIED! YOU MUST BE AN ADMIN OR A SERVER MOD!')
            return
        if(lang == "cn" or lang == "en"):
            config_dict['ServerList'][str(ctx.guild.id)]['lang'] = lang
            self.modSet(config_dict)
            await ctx.send(f"Successfully set the server language to {lang}!")
            return
        await ctx.send("MAID ERROR: IMPROPER USAGE, PLEASE REFER TO THE DOCUMENTATION!\nhttps://github.com/akasakakona/Maid-chan")
    
    @commands.command()
    async def setGreet(self, ctx):
        with open('config.json') as f:
            config_dict = json.load(f)
            f.close()
        if(ctx.author.id != config_dict["ADMIN"] and ctx.author.id not in config_dict['ServerList'][str(ctx.author.guild.id)]['modList']):
            await ctx.send('MAID ERROR: PERMISSION DENIED! YOU MUST BE AN ADMIN OR A SERVER MOD!')
            return
        greetPhrase = ctx.content[9:]
        if(greetPhrase != ""):
            config_dict['ServerList'][str(ctx.author.guild.id)]['greetPhrase'] = greetPhrase
            await ctx.send(f'Successfully set the server\'s greeting phrase to \"{greetPhrase}\"!')
            return
        await ctx.send("MAID ERROR: IMPROPER USAGE, PLEASE REFER TO THE DOCUMENTATION!\nhttps://github.com/akasakakona/Maid-chan")

        

    def modSet(self, data):
        with open('config.json', 'w') as json_file:
            json.dump (data, json_file, indent=4)
            json_file.close()



def setup(maid):
    maid.add_cog(Moderation(maid))