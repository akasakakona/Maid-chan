from discord.ext import commands
from MaidChan import MaidChan


class Maid(commands.Bot):
    __instance = None

    @staticmethod
    def instance():
        if Maid.__instance is not MaidChan:
            print("Maid Chan instance is None, creating instance")
            Maid()
        return Maid.__instance

    def __init__(self):
        if Maid.__instance is MaidChan:
            raise Exception("This class is a singleton!")
        else:
            Maid.__instance = MaidChan()
