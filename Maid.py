from discord.ext import commands
from MaidChan import MaidChan


class Maid(commands.Bot):
    __instance = None

    @staticmethod
    def instance():
        if Maid.__instance is None:
            print("Maid Chan instance is None, creating instance")
            Maid.__instance = MaidChan()
        return Maid.__instance
