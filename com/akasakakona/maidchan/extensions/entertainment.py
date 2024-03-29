import nextcord
from nextcord.ext import commands
import random
from gtts import gTTS
import os
from pixivpy3 import AppPixivAPI
import time
import ctypes
from ctypes import util
from ..core.MaidChan import MaidChan
from ..config.ConfigManager import ConfigManager
from ..config.ServerConfig import ServerConfig

random.seed(time.time())


class Entertainment(commands.Cog):
    def __init__(self):
        self.maid = MaidChan.instance()
        self.bullets = [0, 0, 0, 0, 0, 0]
        self.shotCounter = 0

    @commands.command(brief="Play Russian Roulette with your friends!")
    async def RR(self, ctx):
        if self.shotCounter == 0:
            self.bullets.insert(random.randint(0, 6), 1)

        if self.bullets[0] == 1:
            self.shotCounter += 1
            if lang(ctx) == "en":
                await ctx.send(
                    f"OOF, {ctx.author.name} is dead! The chance of this happening is {round((self.shotCounter / 7.0) * 100)}%!")
            elif lang(ctx) == "cn":
                await ctx.send(f"啊，{ctx.author.name}挂了！概率是{round((self.shotCounter / 7.0) * 100)}%！")
            self.shotCounter = 0
            self.bullets = [0, 0, 0, 0, 0, 0]
        else:
            self.shotCounter += 1
            self.bullets.pop(0)
            if lang(ctx) == "en":
                await ctx.send(f"Congrats! {ctx.author.name} is still alive!")
            elif lang(ctx) == "cn":
                await ctx.send(f"恭喜! {ctx.author.name}还活着!")

    @commands.command()
    async def say(self, ctx, language: str):
        s_config = ConfigManager.instance().get_server_config(ctx.author.guild.id).get(ServerConfig.CONFIG_MAIN)
        if ctx.message.author.voice is not None:  # if the author of the message is in voice channel
            channel = ctx.message.author.voice.channel  # get what channel he is in
            voice = ctx.guild.voice_client  # from a list of voice connections, find the connection  for this server. Replacement for get(maid.voice_clients, guild = ctx.guild)
            if voice and voice.is_connected():  # if there is a connection AND maid-chan is connected
                await voice.move_to(channel)  # move to the channel where the author is
            else:
                voice = await channel.connect()  # or else, connect to the channel directly
        else:
            if lang(ctx) == "en":
                await ctx.send(f"{ctx.author.mention} is not in the voice channel... I\'m lonely...")
            elif lang(ctx) == "cn":
                await ctx.send(f"{ctx.author.mention}不在语音频道里欸...好寂寞...")
            return
        if language == 'cn':
            language = 'zh-cn'
        elif language == 'jp':
            language = 'ja'
        elif language == 'dc' or language == 'fuckoff':
            await voice.disconnect()
            return
        txt = ctx.message.content[8:]
        nextcord.opus.load_opus(ctypes.util.find_library('opus'))
        voiceObj = gTTS(text=txt, lang=language, slow=False)
        voiceObj.save("tts.mp3")
        voice.play(nextcord.FFmpegOpusAudio("tts.mp3"))
        # voice.source = nextcord.PCMVolumeTransformer(voice.source)
        # voice.source.volume = s_config.get("volume")

    @commands.command(aliases=['色图'])
    async def picSearch(self, ctx, title: str = ""):
        g_config = ConfigManager.instance().get_global_config()
        pixivAPI = AppPixivAPI()
        # pixivAPI.login(config_dict.get("Pixiv")['ID'], config_dict.get("Pixiv")['Pass'])
        try:
            pixivAPI.auth(refresh_token=g_config.get("Pixiv")["TOKEN"])
        except:
            return await ctx.send("MAID ERROR: FUCK PIXIV! REQUEST FAILED, PLEASE TRY AGAIN!")
        if title == "":
            try:
                result = pixivAPI.illust_ranking('day_male')
            except:
                return await ctx.send("MAID ERROR: FUCK PIXIV! REQUEST FAILED, PLEASE TRY AGAIN!")
        elif title == "r18":
            try:
                result = pixivAPI.illust_ranking('day_male_r18')
            except:
                return await ctx.send("MAID ERROR: FUCK PIXIV! REQUEST FAILED, PLEASE TRY AGAIN!")
        else:
            try:
                result = pixivAPI.search_illust(title, sort="popular_desc", search_target='title_and_caption')
            except:
                return await ctx.send("MAID ERROR: FUCK PIXIV! REQUEST FAILED, PLEASE TRY AGAIN!")
        embed = nextcord.Embed(color=nextcord.Color.dark_red())
        if len(result.illusts) != 0:
            illust = result.illusts[random.randint(0, len(result.illusts) - 1)]
            imagePresent = os.path.isfile(f'illust.jpg')
            if (imagePresent):
                os.remove(f'illust.jpg')
            pixivAPI.download(illust.image_urls.large, fname=f'illust.jpg')
            embed.title = illust.title
            embed.url = f"https://www.pixiv.net/artworks/{illust.id}"
            embed.set_image(url="attachment://illust.jpg")
            embed.set_author(name=illust.user.name, url=f"https://www.pixiv.net/users/{illust.user.id}")
            await ctx.send(embed=embed, file=nextcord.File(f'illust.jpg'))
        else:
            embed.title = "Image can\'t be found! 无法找到图片！"
            await ctx.send(embed=embed)


def lang(ctx):
    return ConfigManager.instance().get_server_config(ctx.guild.id).get_main().get("lang")


def setup(maid):
    maid.add_cog(Entertainment())
