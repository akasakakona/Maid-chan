import nextcord
from nextcord.ext import commands
from ..core.MaidChan import MaidChan
from ..config.ConfigManager import ConfigManager


class Debugging(commands.Cog):
    def __init__(self):
        self.maid = MaidChan.instance()
        config_dict = ConfigManager.instance().get_global_config()
        self.ADMIN = config_dict.get("ADMIN")

    @commands.Cog.listener()
    async def on_ready(self):
        await self.maid.change_presence(status=nextcord.Status.online, activity=nextcord.Game(" with catgirls"))
        print(f"Logged in as {self.maid.user.name}")

    @commands.command()
    async def ping(self, ctx):
        await ctx.send(f'The ping is {round(self.maid.latency * 1000)}ms')

    @commands.command(aliases=['off'])
    async def shutdown(self, ctx):
        if ctx.author.id != self.ADMIN:
            return await ctx.send("MAID ERROR: ACCESS DENIED! YOU ARE NOT AKASAKAKONA-SAMA! GO AWAY!! ‎(︶ ︿ ︶)")
        await ctx.send('Settings Saved! AkasakaKona-Sama! See you later~  (> ^ <)')

        await self.maid.close()


def setup(maid):
    maid.add_cog(Debugging())
