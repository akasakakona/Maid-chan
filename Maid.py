import discord
import os
import json
from discord.ext import commands
from MaidChan import MaidChan


class Maid(commands.Bot):
    __instance = None

    @staticmethod
    def instance():
        if Maid.__instance is None:
            Maid.__instance = MaidChan()
        return Maid.__instance

    @staticmethod
    def run():
        if Maid.instance().is_closed():
            Maid.instance().run()
        pass

    @staticmethod
    def get_token():
        return Maid.instance().TOKEN

    @staticmethod
    def get_prefix():
        return Maid.instance().PREFIX
