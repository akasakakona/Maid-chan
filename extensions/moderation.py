import json
import discord
from discord.ext import commands
import discord.utils

class Server:
    def __init__(self, guildID):
        self.id = guildID
        self.modList = []
        self.greetChannel = 0
        self.greetPhrase = ""
        self.musicQueue = []

class Moderation(commands.Cog):
    def __init__(self, maid):
        self.maid = maid

    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        newServer = Server(guild.id)
        newServer.modList.append(guild.owner_id)


    @commands.Cog.listener()
    async def on_member_join(self, member):
        if(member.guild.id == 352312296309260289):
            channel = member.guild.get_channel(352314900359413761)
            await channel.send(f'Welcome to the Passerines! <@{member.id}>!')
        elif(member.guild.id == 358473448076607499):
            channel = member.guild.get_channel(358473448076607500)
            await channel.send(f'欢迎<@{member.id}>様！いらっしゃいませ！')
        elif(member.guild.id == 431610460307980302):
            channel = member.guild.get_channel(431610460307980306)
            await channel.send(f'欢迎<@{member.id}>様！いらっしゃいませ！')
        elif(member.guild.id == 392194794018963456):
            channel = member.guild.get_channel(392194794018963459)
            await channel.send(f'欢迎<@{member.id}>様！いらっしゃいませ！欢迎来到DOLLARS的时差党！')

def modSet(modType, modData, modAction = None):
    with open('config.json') as f:
        config_dict = json.load(f)
    f.close()
    if(modAction is not None):
        if(modAction == "del"):
            config_dict[modType].pop(config_dict[modType].index(modData))
        else:
            config_dict[modType].append(modData)
    else:
        config_dict[modType] = modData
    with open('config.json', 'w') as json_file:
        json.dump(config_dict, json_file, indent = 1)
    json_file.close()

def setup(maid):
    maid.add_cog(Moderation(maid))