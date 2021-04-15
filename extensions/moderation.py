import json

import discord
import discord.utils
from discord.ext import commands
import MaidChan


class Server:
    def __init__(self, guildID):
        self.id = guildID
        self.modList = []
        self.lang = "en"
        self.greetChannel = 0
        self.greetPhrase = ""


class Moderation(commands.Cog):
    def __init__(self, maid):
        self.maid = MaidChan.instance()

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
        if(member.guild.id == 352312296309260289):
            role = discord.utils.get(member.guild.roles, name = "Notification")
            await member.add_roles(role)
        channel = member.guild.get_channel(config_dict['ServerList'][str(member.guild.id)]['greetChannel'])
        if(channel is not None):
            greetPhrase = config_dict['ServerList'][str(member.guild.id)]['greetPhrase']
            if(greetPhrase != ""):
                await channel.send(greetPhrase.format(memberID =  member.id))

    #Reserved for personal use
    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        messageID = payload.message_id
        if (messageID == 654642859156307980):
            guildID = payload.guild_id
            guild = self.maid.get_guild(guildID)
            if(payload.emoji.name == 'derp'):
                role = discord.utils.get(guild.roles, name = "Notification")
            if(role is not None):
                member = guild.get_member(payload.user_id)
                if(member is not None):
                    if(role not in member.roles):
                        await member.add_roles(role)
                        print(f'The member {member} from server {guild} has joined the role')
                    else:
                        await member.remove_roles(role)
                        print(f'The member {member} from {guild} has left the role.')
                else:
                    print('Member not found!')
            else:
                print('Role not found!')

    #Reserved for personal use
    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, payload):
        messageID = payload.message_id
        if (messageID == 654642859156307980):
            guildID = payload.guild_id
            guild = self.maid.get_guild(guildID)
            if(payload.emoji.name == 'derp'):
                role = discord.utils.get(guild.roles, name = "Notification")
            if(role is not None):
                member = guild.get_member(payload.user_id)
                if(member is not None):
                    if(role in member.roles):
                        await member.remove_roles(role)
                        print(f'The member {member} from {guild} has left the role.')
                    else:
                        await member.add_roles(role)
                        print(f'The member {member} from server {guild} has joined the role')
                else:
                    print('Member not found!')
            else:
                print('Role not found!')

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
            self.modSet(config_dict)
            return
        await ctx.send("MAID ERROR: IMPROPER USAGE, PLEASE REFER TO THE DOCUMENTATION!\nhttps://github.com/akasakakona/Maid-chan")
    
    @commands.command()
    async def setGreetCh(self, ctx):
        with open('config.json') as f:
            config_dict = json.load(f)
            f.close()
        if(ctx.author.id != config_dict["ADMIN"] and ctx.author.id not in config_dict['ServerList'][str(ctx.author.guild.id)]['modList']):
            await ctx.send('MAID ERROR: PERMISSION DENIED! YOU MUST BE AN ADMIN OR A SERVER MOD!')
            return
        config_dict['ServerList'][str(ctx.author.guild.id)]['greetChannel'] = ctx.channel.id
        await ctx.send(f'Successfully set the server\'s greeting channel!')
        self.modSet(config_dict)
        return
    
    @commands.command()
    async def serverInfo(self, ctx):
        """FIXME: send an embed about this server's info"""

    @commands.command()
    async def setMod(self, ctx):
        with open('config.json') as f:
            config_dict = json.load(f)
            f.close()
        if(ctx.author.id != config_dict["ADMIN"] and ctx.author.id not in config_dict['ServerList'][str(ctx.author.guild.id)]['modList']):
            await ctx.send('MAID ERROR: PERMISSION DENIED! YOU MUST BE AN ADMIN OR A SERVER MOD!')
            return
        for modID in ctx.raw_mentions:
            config_dict['ServerList'][str(ctx.author.guild.id)]['modList'].append(modID)
        await ctx.send("Successfully set as mod!")
        self.modSet(config_dict)
        return

    def modSet(self, data):
        with open('config.json', 'w') as json_file:
            json.dump (data, json_file, indent=4)
            json_file.close()



def setup(maid):
    maid.add_cog(Moderation(maid))