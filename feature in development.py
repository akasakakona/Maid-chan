import discord
from discord.ext import commands
import random
import youtube_dl
import os
import asyncio
import shutil
import pixivpy3
import time
from pixivpy3 import *
import subprocess

TOKEN = ""
maid = commands.Bot(command_prefix = commands.when_mentioned_or("!",".","?","MC ","mc ","Mc ","maid chan ","Maid chan ",'妹抖酱', "！"))
ENGuilds = []
CNGuilds = []
random.seed(time.time())
PID = ""
PPASS = ""

@maid.event
async def on_ready():
    await maid.change_presence(status=discord.Status.idle, activity = discord.Game(" with いーちゃん"))
    print(f"Logged in as {maid.user.name}")

XD = False
really = False
prevMessage = ""
messageRepeat = 0
@maid.event###Reserved for personal use! (Mostly to spam Reaily XD)
async def on_message(message):
    global XD
    global really
    channel = message.channel
    originalMessage = message.content
    lowerMessage = originalMessage.lower()
    reallyIndex = lowerMessage.find('really')
    shotIndex = lowerMessage.find('shot')
    if(shotIndex >= 0 and message.author.id != 645438533397512201):
        await channel.send("Did someone say SHOT?!\n https://cdn.discordapp.com/attachments/177595404324438016/505788828167176195/1540657957240.png")
        await maid.process_commands(message)
    if(message.author.id == 378085550499954699 and message.author.guild.id == 352312296309260289 and XD == True):
        await channel.send('XD')
        await maid.process_commands(message)
    elif(reallyIndex >= 0 and message.author.id != 555273228440829954 and message.author.guild.id == 352312296309260289 and really == True):
        await channel.send(f'Hey! {message.author.mention}! I think you meant <@378085550499954699> instead of "{originalMessage[reallyIndex : reallyIndex + 6]}"! <:thonk:615740280913657866>')
        await maid.process_commands(message)
    else:
        await maid.process_commands(message)

MUSIC_VOLUME = 0.0
LOOP_SINGLE = False
LOOP_ALL = False
musicList = []
currIndex = 0
@maid.command()
async def play(ctx,url: str):
    global voice
    global musicList
    global currIndex
    if(ctx.message.author.voice != None):#if the author of the message is in voice channel
        channel = ctx.message.author.voice.channel#get what channel he is in
        voice = ctx.guild.voice_client#from a list of voice connections, find the connection  for this server. Replacement for get(maid.voice_clients, guild = ctx.guild)
        if(ctx.guild.id in ENGuilds):
            await ctx.send(f"Play request received! Processing Master {ctx.message.author.name}\'s play request!")
        elif(ctx.guild.id in CNGuilds):
            await ctx.send(f"收到点歌请求！正在处理{ctx.message.author.name}様的点歌请求！")
        musicList.append(url)
        if(voice is not None):
            return
    else:
        if(ctx.guild.id in ENGuilds):
            await ctx.send("Nobody is in the voice channel... I\'m lonely...")
        elif(ctx.guild.id in CNGuilds):
            await ctx.send("没人在语音频道里欸...好寂寞...")
        return

    while(len(musicList) != 0):
        try:
            os.system(f"youtube-dl -f bestaudio -o \"%(title)s.%(ext)s\" {musicList[currIndex]}")
            name = subprocess.check_output(f"youtube-dl --get-title {musicList[currIndex]}", shell = True).decode().rstrip()
            duration = subprocess.check_output(f"youtube-dl --get-duration {musicList[currIndex]}", shell = True).decode()
            thumbnail = subprocess.check_output(f"youtube-dl --get-thumbnail {musicList[currIndex]}", shell = True).decode()
            description = subprocess.check_output(f"youtube-dl --get-description {musicList[currIndex]}", shell = True).decode()
        except:
            await ctx.send(f"MAID ERROR: VIDEO EXTRACTION FAILED FOR URL: {musicList[currIndex]} ! PLEASE TRY AGAIN!")
            musicList.remove(musicList[currIndex])
            continue

        await asyncio.sleep(3) #need to wait for youtube-dl to merge fragment files before preceeding
        for file in os.listdir("./"):
            if(file.startswith(name)):
                tempArr = file.split('.')
                fileformat = tempArr[len(tempArr) - 1]
                break
        
        filename = f"{name}.{fileformat}"
        audioSouce = discord.FFmpegPCMAudio(filename)

        if(voice and voice.is_connected()):#if there is a connection AND maid-chan is connected
            await voice.move_to(channel)#move to the channel where the author is
        else:
            voice = await channel.connect()#or else, connect to the channel directly

        voice.play(audioSouce)#will leave the channel AFTER a song finished playing. This evokes def leave(error) above
        voice.source = discord.PCMVolumeTransformer(voice.source)#sets volume of the song playing
        voice.source.volume = MUSIC_VOLUME#0.7 is 70%, might make a function that make volume adjustable later

        embed = discord.Embed(title = name, description = f"{description}\n```Duration: {duration}```", colour = discord.Color.magenta(), url = url)
        embed.set_footer(text = ctx.message.author.name, icon_url=ctx.message.author.avatar_url)
        embed.set_thumbnail(url = thumbnail)
        if(ctx.message.guild.id in ENGuilds):
            await ctx.send(content = f"Playing \"{name}\" for you right now! Master {ctx.message.author.name}!", embed = embed)
        elif(ctx.message.guild.id in CNGuilds):
            await ctx.send(content = f"正在播放{ctx.message.author.name}様点播的《{name}》！", embed = embed)#notify user the song started playing
        while(voice.is_playing() or voice.is_paused()):
            await asyncio.sleep(1)
        if(len(musicList) == 1 and not LOOP_ALL and not LOOP_SINGLE):
            musicList.pop(0)
            os.remove(filename)
            await voice.disconnect()
        elif(currIndex == len(musicList) - 1 and LOOP_ALL):
            currIndex = 0
            os.remove(filename)
        elif(len(musicList) > 1 and not LOOP_ALL and not LOOP_SINGLE):
            if(currIndex == 0):
                musicList.pop(0)
            else:
                for i in range(0, currIndex + 1):
                    musicList.pop(i)
            os.remove(filename)
            currIndex = 0
        elif(len(musicList) > 1 and LOOP_ALL and not LOOP_SINGLE):
            currIndex += 1
            os.remove(filename)
        elif(len(musicList) > 1 and not LOOP_ALL and LOOP_SINGLE):
            pass
    
@maid.command()
async def loop(ctx, state: str):
    global LOOP_ALL
    global LOOP_SINGLE
    state = state.lower()
    if(state == "all"):
        if(LOOP_SINGLE):
            LOOP_SINGLE = False
        LOOP_ALL = True
        if(ctx.guild.id in ENGuilds):
            await ctx.send("Loop all is on!")
        else:
            await ctx.send("开启全曲洗脑循环！")
    elif(state == "single"):
        if(LOOP_ALL):
            LOOP_ALL = False
        LOOP_SINGLE = True
        if(ctx.guild.id in ENGuilds):
            await ctx.send("Loop single is on!")
        else:
            await ctx.send("开启单曲洗脑循环！")
    elif(state == "off"):
        LOOP_SINGLE = False
        LOOP_ALL = False
        if(ctx.guild.id in ENGuilds):
            await ctx.send("Loop is off!")
        else:
            await ctx.send("洗脑循环关闭！")

@maid.command(aliases = ['list', 'ls'])
async def playlist(ctx):
    playlist = ""
    i = 1
    for url in musicList:
        name = subprocess.check_output(f"youtube-dl --get-title {url}", shell = True).decode()
        playlist += f"{i}. {name}\n"
        i += 1
    if(LOOP_ALL):
        playlist += "```LOOP_ALL: ON\n"
    else:
        playlist += "```LOOP_ALL: OFF\n"
    if(LOOP_SINGLE):
        playlist += "LOOP_SINGLE: ON```"
    else:
        playlist += "LOOP_SINGLE: OFF```"
    embed = discord.Embed(title = f"{ctx.guild.name}\'s Playlist", description = playlist, colour = discord.Color.blue())
    embed.set_footer(text = ctx.guild.name, icon_url=ctx.guild.icon_url)
    await ctx.send(embed = embed)

@maid.command(aliases = ['del', 'd', 'remove'])
async def delete(ctx, num: int):
    global musicList
    name = subprocess.check_output(f"youtube-dl --get-title {musicList[num - 1]}", shell = True).decode()
    musicList.pop(num - 1)
    if(ctx.guild.id in ENGuilds):
        await ctx.send(f"\"{name}\" has been deleted for Master {ctx.author.name}!")
    else:
        await ctx.send(f"已经为{ctx.author.name}删除了《{name}》!")

@maid.command()
async def pause(ctx):
    voice = ctx.guild.voice_client
    if(voice and voice.is_playing()):
        voice.pause()
        if(ctx.message.guild.id in ENGuilds):
            await ctx.send(f"I have paused the music for you, Master {ctx.message.author.name}!THE WORLD!!Time, STOP!!!")
        elif(ctx.message.guild.id in CNGuilds):
            await ctx.send(f"已经为{ctx.message.author.name}様暂停了音乐！！THE WORLD！！時よ止まれ！！")
    else:
        if(ctx.message.guild.id in ENGuilds):
            await ctx.send("MAID ERROR: MUSIC IS NOT PLAYING!")
        elif(ctx.message.guild.id in CNGuilds):
            await ctx.send("MAID ERROR: 暂无音乐播放中！")

@maid.command()
async def resume(ctx):
    voice = ctx.guild.voice_client
    if(voice and voice.is_paused()):
        voice.resume()
        if(ctx.message.guild.id in ENGuilds):
            await ctx.send(f"I have resumed the music for you, Master {ctx.message.author.name}!...And so, time flows again.")
        elif(ctx.message.guild.id in CNGuilds):
            await ctx.send(f"已经为{ctx.message.author.name}様重启了音乐。然后，时间开始流动。")
    else:
        print("MAID ERROR: MUSIC IS NOT PLAYING")
        if(ctx.message.guild.id in ENGuilds):
            await ctx.send("MAID ERROR: MUSIC IS NOT PAUSED!")
        elif(ctx.message.guild.id in CNGuilds):
            await ctx.send("MAID ERROR: 音乐未被暂停！")

@maid.command()
async def stop(ctx):#PLANNING TO REPLACE STOP W/ SKIP. THAT WAY I CAN USE KING CRIMSON REFERENCE
    global musicList
    global currIndex
    global LOOP_SINGLE
    global LOOP_ALL
    LOOP_ALL = False
    LOOP_SINGLE = False
    voice = ctx.guild.voice_client
    if(voice and voice.is_playing()):
        voice.stop()
        for i in range(0, len(musicList)):
            musicList.pop(0)
        currIndex = 0
        if(ctx.message.guild.id in ENGuilds):
            await ctx.send(f"I have stopped the music for you, Master {ctx.message.author.name}!THE WORLD!!Time, STOP!!!")
        elif(ctx.message.guild.id in CNGuilds):
            await ctx.send(f"已经为{ctx.message.author.name}様停止了音乐。THE WORLD！！時よ止まれ！！")
        await voice.disconnect()
    else:
        print("MAID ERROR: MUSIC IS NOT PLAYING")
        if(ctx.message.guild.id in ENGuilds):
            await ctx.send("MAID ERROR: MUSIC IS NOT PLAYING!")
        elif(ctx.message.guild.id in CNGuilds):
            await ctx.send("MAID ERROR: 暂无音乐播放中！")

def saveSet():
    try:
        fout = open("config1.txt", 'w')
        fout.write(f'token: {TOKEN}\n')
        fout.write("ENGuilds: ")
        for gid in ENGuilds:
          fout.write(f'{gid} ')
        fout.write('\n')
        fout.write("CNGuilds: ")
        for gid in CNGuilds:
          fout.write(f'{gid} ')
        fout.write('\n')
        if(XD):
            fout.write("XD: True\n")
        else:
            fout.write("XD: False\n")
        if(really):
            fout.write("really: True\n")
        else:
            fout.write("really: False\n")
        fout.write(f'volume: {MUSIC_VOLUME}\n')
        fout.write(f'PID: {PID}\n')
        fout.write(f'PPASS: {PPASS}')
        fout.close()
        return True
    except FileNotFoundError:
        return False

@maid.command(brief = "***Private Feature***")
async def setGuild(ctx, gtype:str):
    if(ctx.guild.id in CNGuilds or ctx.guild.id in ENGuilds):
        if(gtype.lower() == "cn" and ctx.guild.id in ENGuilds):
            ENGuilds.pop(ENGuilds.index(ctx.guild.id))
            CNGuilds.append(ctx.guild.id)
            await ctx.send(f'{ctx.guild.name}\'s language has been set to Chinese!')
            return
        elif(gtype.lower() == "en" and ctx.guild.id in CNGuilds):
            CNGuilds.pop(CNGuilds.index(ctx.guild.id))
            ENGuilds.append(ctx.guild.id)
            await ctx.send(f'{ctx.guild.name}\'s language has been set to English!')
            return
        else:
            await ctx.send("MAID ERROR: GUILD ALREADY EXISTS")
            return

    if(gtype.lower() == "cn"):
        CNGuilds.append(ctx.guild.id)
        await ctx.send(f'{ctx.guild.name}\'s language has been set to Chinese!')
    elif(gtype.lower() == "en"):
        ENGuilds.append(ctx.guild.id)
        await ctx.send(f'{ctx.guild.name}\'s language has been set to English!')
    else:
        await ctx.send("MAID ERROR: IMPROPER USAGE")

@maid.command()#For debugging purposes
async def ping(ctx):
    await ctx.send(f'The ping is {round(maid.latency * 1000)}ms')

@maid.command()
async def shutdown(ctx):
    if(ctx.author.id != 358838608779673600):
        await ctx.send("MAID ERROR: ACCESS DENIED! YOU ARE NOT AKASAKAKONA-SAMA! GO AWAY!! ‎(︶ ︿ ︶)")
        return
    if(saveSet()):
        await ctx.send('Settings Saved! AkasakaKona-Sama! See you later~  (> ^ <)')
    else:
        await ctx.send('MAID ERROR: SAVE SETTINGS ERROR... I\'m sorry AkasakaKona-Sama... (Q A Q)')
    await maid.close()

def loadSet():
    global ENGuilds
    global CNGuilds
    global TOKEN
    global really
    global XD
    global PID
    global PPASS
    global MUSIC_VOLUME
    try:
        fin = open("config1.txt", 'r')
        TOKEN = ((fin.readline()).split())[1]
        for gid in ((fin.readline()).split())[1:]:
          ENGuilds.append(int(gid))
        for gid in ((fin.readline()).split())[1:]:
          CNGuilds.append(int(gid))
        if(((fin.readline()).split())[1] == "True"):
          XD = True
        else:
          XD = False
        if(((fin.readline()).split())[1] == "True"):
          really = True
        else:
          really = False
        MUSIC_VOLUME= float(((fin.readline()).split())[1])
        PID = ((fin.readline()).split())[1]
        PPASS = ((fin.readline()).split())[1]
        fin.close()
    except FileNotFoundError:
        print("File not found!")

loadSet()
maid.run(TOKEN)