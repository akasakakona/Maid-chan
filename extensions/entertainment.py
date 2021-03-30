import discord
from discord.ext import commands
import random
import json
from gtts import gTTS
import os
import pixivpy3
from pixivpy3 import AppPixivAPI
import time

random.seed(time.time())

class Entertainment(commands.Cog):
    def __init__(self, maid):
        self.maid = maid
        self.bullets = [0, 0, 0, 0, 0, 0]
        self.shotCounter = 0

    
    @commands.command(brief = "Play Russian Roulette with your friends!")
    async def RR(self, ctx):
        with open('config.json') as f:
            config_dict = json.load(f)
            f.close()
        if(self.shotCounter == 0):
            self.bullets.insert(random.randint(0, 6), 1)

        if(self.bullets[0] == 1):
            self.shotCounter += 1
            if(config_dict['ServerList'][str(ctx.message.guild.id)]['lang'] == "en"):
                await ctx.send(f"OOF, {ctx.author.name} is dead! The chance of this happening is {round((self.shotCounter / 7.0)*100)}%!")
            elif(config_dict['ServerList'][str(ctx.message.guild.id)]['lang'] == "cn"):
                await ctx.send(f"啊，{ctx.author.name}挂了！概率是{round((self.shotCounter / 7.0)*100)}%！")
            self.shotCounter = 0
            self.bullets = [0, 0, 0, 0, 0, 0]
        else:
            self.shotCounter += 1
            self.bullets.pop(0)
            if(config_dict['ServerList'][str(ctx.message.guild.id)]['lang'] == "en"):
                await ctx.send(f"Congrats! {ctx.author.name} is still alive!")
            elif(config_dict['ServerList'][str(ctx.message.guild.id)]['lang'] == "cn"):
                await ctx.send(f"恭喜! {ctx.author.name}还活着!")
    
    @commands.command()
    async def say(self, ctx, language:str):
        with open('config.json') as f:
            config_dict = json.load(f)
            f.close()
        if(ctx.message.author.voice is not None):#if the author of the message is in voice channel
            channel = ctx.message.author.voice.channel#get what channel he is in
            voice = ctx.guild.voice_client#from a list of voice connections, find the connection  for this server. Replacement for get(maid.voice_clients, guild = ctx.guild)
            if(voice and voice.is_connected()):#if there is a connection AND maid-chan is connected
                await voice.move_to(channel)#move to the channel where the author is
            else:
                voice = await channel.connect()#or else, connect to the channel directly
        else:
            if(config_dict['ServerList'][str(ctx.message.guild.id)]['lang'] == "en"):
                await ctx.send(f"{ctx.author.mention} is not in the voice channel... I\'m lonely...")
            elif(config_dict['ServerList'][str(ctx.message.guild.id)]['lang'] == "cn"):
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
        voice.source.volume = config_dict['volume']
    
    @commands.command(aliases=['色图'])
    async def picSearch(self, ctx, title:str=""):
        with open('config.json') as f:
            config_dict = json.load(f)
            f.close()
        pixivAPI = AppPixivAPI()
        # pixivAPI.login(config_dict['Pixiv']['ID'], config_dict['Pixiv']['Pass'])
        pixivAPI.auth(refresh_token=config_dict['Pixiv']['TOKEN'])
        if(title == ""):
            result = pixivAPI.illust_ranking('day_male')
        elif(title == "r18"):
            result = pixivAPI.illust_ranking('day_male_r18')
        else:
            result = pixivAPI.search_illust(title, sort="popular_desc",search_target='title_and_caption')
        embed = discord.Embed(color=discord.Color.dark_red())
        if(len(result.illusts) != 0):
            illust = result.illusts[random.randint(0, len(result.illusts) - 1)]
            imagePresent = os.path.isfile(f'illust.jpg')
            if(imagePresent):
                os.remove(f'illust.jpg')
            pixivAPI.download(illust.image_urls.large, fname=f'illust.jpg')
            embed.title = illust.title
            embed.url = f"https://www.pixiv.net/artworks/{illust.id}"
            embed.set_image(url="attachment://illust.jpg")
            embed.set_author(name=illust.user.name, url=f"https://www.pixiv.net/users/{illust.user.id}")
            await ctx.send(embed=embed, file=discord.File(f'illust.jpg'))
        else:
            embed.title = "Image can\'t be found! 无法找到图片！"
            await ctx.send(embed=embed)
    

def setup(maid):
    maid.add_cog(Entertainment(maid))

