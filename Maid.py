from discord.ext import commands
from MaidChan import MaidChan


class Maid(commands.Bot):
    __instance = None

    @staticmethod
    def instance():
        if Maid.__instance is None:
            Maid.__instance = MaidChan()
        return Maid.__instance
