import discord
import discord.utils
from discord.ext import commands
from ..core.MaidChan import MaidChan
from ..config.ConfigManager import ConfigManager


class Moderation(commands.Cog):
    def __init__(self):
        self.maid = MaidChan.instance()

    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        ConfigManager.instance().add_new_server(guild.id)

    @commands.Cog.listener()
    async def on_member_join(self, member):
        s_config = ConfigManager.instance().get_server_config(member.guild.id).get_main()
        if member.guild.id == 352312296309260289:
            role = discord.utils.get(member.guild.roles, name="Notification")
            await member.add_roles(role)
        channel = member.guild.get_channel(s_config.get("greetChannel"))
        if channel is not None:
            greetPhrase = s_config.get("greetPhrase")
            if greetPhrase != "":
                await channel.send(greetPhrase.format(memberID=member.id))

    # Reserved for personal use
    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        messageID = payload.message_id
        if messageID == 654642859156307980:
            guildID = payload.guild_id
            guild = self.maid.get_guild(guildID)
            if payload.emoji.name == 'derp':
                role = discord.utils.get(guild.roles, name="Notification")
            if role is not None:
                member = guild.get_member(payload.user_id)
                if member is not None:
                    if role not in member.roles:
                        await member.add_roles(role)
                        print(f'The member {member} from server {guild} has joined the role')
                    else:
                        await member.remove_roles(role)
                        print(f'The member {member} from {guild} has left the role.')
                else:
                    print('Member not found!')
            else:
                print('Role not found!')

    # Reserved for personal use
    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, payload):
        global role
        messageID = payload.message_id
        if messageID == 654642859156307980:
            guildID = payload.guild_id
            guild = self.maid.get_guild(guildID)
            if payload.emoji.name == 'derp':
                role = discord.utils.get(guild.roles, name="Notification")
            if role is not None:
                member = guild.get_member(payload.user_id)
                if member is not None:
                    if role in member.roles:
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
    async def setLang(self, ctx, lang: str):
        s_config = ConfigManager.instance().get_server_config(ctx.author.guild.id).get_main()
        if not is_mod(ctx):
            await ctx.send('MAID ERROR: PERMISSION DENIED! YOU MUST BE AN ADMIN OR A SERVER MOD!')
            return
        if (lang == "cn" or lang == "en"):
            s_config.get("lang")
            s_config.save()
            await ctx.send(f"Successfully set the server language to {lang}!")
            return
        await ctx.send(
            "MAID ERROR: IMPROPER USAGE, PLEASE REFER TO THE DOCUMENTATION!\nhttps://github.com/akasakakona/Maid-chan")

    @commands.command()
    async def setGreet(self, ctx):
        s_config = ConfigManager.instance().get_server_config(ctx.author.guild.id).get_main()
        if not is_mod(ctx):
            await ctx.send('MAID ERROR: PERMISSION DENIED! YOU MUST BE AN ADMIN OR A SERVER MOD!')
            return
        greetPhrase = ctx.content[9:]
        if (greetPhrase != ""):
            s_config.set("greetPhrase", greetPhrase)
            await ctx.send(f'Successfully set the server\'s greeting phrase to \"{greetPhrase}\"!')
            s_config.save()
            return
        await ctx.send(
            "MAID ERROR: IMPROPER USAGE, PLEASE REFER TO THE DOCUMENTATION!\nhttps://github.com/akasakakona/Maid-chan")

    @commands.command()
    async def setGreetCh(self, ctx):
        s_config = ConfigManager.instance().get_server_config(ctx.author.guild.id).get_main()
        if not is_mod(ctx):
            await ctx.send('MAID ERROR: PERMISSION DENIED! YOU MUST BE AN ADMIN OR A SERVER MOD!')
            return
        s_config.set("greetChannel", ctx.channel.id)
        await ctx.send(f'Successfully set the server\'s greeting channel!')
        s_config.save()
        return

    @commands.command()
    async def serverInfo(self, ctx):
        """FIXME: send an embed about this server's info"""

    @commands.command()
    async def setMod(self, ctx):
        s_config = ConfigManager.instance().get_server_config(ctx.author.guild.id).get_main()
        if not is_mod(ctx):
            await ctx.send('MAID ERROR: PERMISSION DENIED! YOU MUST BE AN ADMIN OR A SERVER MOD!')
            return
        for modID in ctx.message.raw_mentions:
            s_config.get("modList").append(modID)
        await ctx.send("Successfully set as mod!")
        s_config.save()
        return


def is_mod(ctx):
    g_config = ConfigManager.instance().get_global_config()
    s_config = ConfigManager.instance().get_server_config(ctx.author.guild.id).get_main()
    return ctx.author.id == g_config.get("ADMIN") or ctx.author.id in s_config.get("modList")


def setup(maid):
    maid.add_cog(Moderation())
