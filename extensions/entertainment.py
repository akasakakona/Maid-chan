import discord
from discord.ext import commands
import random
import json
from gtts import gTTS
import os
import pixivpy3
from pixivpy3 import AppPixivAPI

class Entertainment(commands.Cog):
    def __init__(self, maid):
        self.maid = maid
        self.bullets = [0, 0, 0, 0, 0, 0]
        self.shotCounter = 0
        self.ENGuilds = []
        self.CNGuilds = []
        self.VOLUME = 0.0
        self.PID = ""
        self.PPASS = ""
        try:
            with open('config.json') as f:
                config_dict = json.load(f)
                for gid in config_dict['ENGuilds']:
                    self.ENGuilds.append(gid)
                for gid in config_dict['CNGuilds']:
                    self.CNGuilds.append(gid)
                self.VOLUME = config_dict['volume']
                self.PID = config_dict['PID']
                self.PPASS = config_dict['PPASS']
        except FileNotFoundError:
            print("File not found!")

    
    @commands.command(brief = "Play Russian Roulette with your friends!")
    async def RR(self, ctx):
        if(self.shotCounter == 0):
            self.bullets.insert(random.randint(0, 6), 1)

        if(self.bullets[0] == 1):
            self.shotCounter += 1
            if(ctx.message.guild.id in self.ENGuilds):
                await ctx.send(f"OOF, {ctx.author.name} is dead! The chance of this happening is {round((self.shotCounter / 7.0)*100)}%!")
            elif(ctx.message.guild.id in self.CNGuilds):
                await ctx.send(f"啊，{ctx.author.name}挂了！概率是{round((self.shotCounter / 7.0)*100)}%！")
            self.shotCounter = 0
            self.bullets = [0, 0, 0, 0, 0, 0]
        else:
            self.shotCounter += 1
            self.bullets.pop(0)
            if(ctx.message.guild.id in self.ENGuilds):
                await ctx.send(f"Congrats! {ctx.author.name} is still alive!")
            elif(ctx.message.guild.id in self.CNGuilds):
                await ctx.send(f"恭喜! {ctx.author.name}还活着!")
    
    @commands.command()
    async def say(self, ctx, language:str):
        if(ctx.message.author.voice is not None):#if the author of the message is in voice channel
            channel = ctx.message.author.voice.channel#get what channel he is in
            voice = ctx.guild.voice_client#from a list of voice connections, find the connection  for this server. Replacement for get(maid.voice_clients, guild = ctx.guild)
            if(voice and voice.is_connected()):#if there is a connection AND maid-chan is connected
                await voice.move_to(channel)#move to the channel where the author is
            else:
                voice = await channel.connect()#or else, connect to the channel directly
        else:
            if(ctx.message.guild.id in self.ENGuilds):
                await ctx.send(f"{ctx.author.mention} is not in the voice channel... I\'m lonely...")
            elif(ctx.message.guild.id in self.CNGuilds):
                await ctx.send(f"{ctx.author.mention}不在语音频道里欸...好寂寞...")
            return
        if(language == 'cn'):
            language = 'zh-cn'
        elif(language == 'jp'):
            language = 'ja'
        elif(language == 'dc' or language == 'fuckoff'):
            await voice.disconnect()
            return
        txt = ctx.message.content[8:]
        voiceObj = gTTS(text = txt, lang = language, slow = False)
        voiceObj.save("tts.mp3")
        voice.play(discord.FFmpegPCMAudio("tts.mp3"))
        voice.source = discord.PCMVolumeTransformer(voice.source)
        voice.source.volume = self.VOLUME
    
    @commands.command()
    async def picSearch(self, ctx, title:str):
        pixivAPI = AppPixivAPI()
        pixivAPI.login(self.PID, self.PPASS)
        result = pixivAPI.search_illust(title)
        if(len(result.illusts) != 0):
            illust = result.illusts[random.randint(0, len(result.illusts) - 1)]
            imagePresent = os.path.isfile(f'illust.jpg')
            if(imagePresent):
                os.remove(f'illust.jpg')
            pixivAPI.download(illust.image_urls.large, fname=f'illust.jpg')
            await ctx.send(content = f"Title: {illust.title}", file=discord.File(f'illust.jpg'))
        else:
            await ctx.send("Image can\'t be found! 无法找到图片！")
    

def setup(maid):
    maid.add_cog(Entertainment(maid))

