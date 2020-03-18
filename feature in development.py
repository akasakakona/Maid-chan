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

TOKEN = ""
maid = commands.Bot(command_prefix = commands.when_mentioned_or("!",".","?","MC ","mc ","Mc ","maid chan ","Maid chan ",'妹抖酱', "！"))
ENGuilds = []
CNGuilds = []
random.seed(time.time())
PID = ""
PPASS = ""

@maid.event
async def on_ready():
    await maid.change_presence(status=discord.Status.idle, activity = discord.Game(" with Araragi"))
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
@maid.command()
async def play(ctx,url: str):
    def check_queue():
        queue_infile = os.path.isdir("./Queue")
        if(queue_infile):
            DIR = os.path.abspath(os.path.realpath("Queue"))
            length = len(os.listdir(DIR))
            queueLeft = length - 1
            try:
                first_file = os.listdir(DIR)[0]
            except:
                print("No more queued song(s)\n")
                queues.clear()
                return
            main_location = os.path.dirname(os.path.realpath(__file__))
            song_path = os.path.abspath(os.path.realpath("Queue") + "\\" + first_file)
            if(length != 0):
                print("Song done, playing next queued\n")
                print(f"Songs still in queue: {queueLeft}")
                song_there = os.path.isfile("song.mp3")
                if(song_there):
                    os.remove("song.mp3")
                shutil.move(song_path, main_location)
                for file in os.listdir("./") :
                    if(file.endswith(".mp3")):
                        os.rename(file, "song.mp3")

                voice.play(discord.FFmpegPCMAudio("song.mp3"), after=lambda e: check_queue())#will leave the channel AFTER a song finished playing. This evokes def leave(error) above
                voice.source = discord.PCMVolumeTransformer(voice.source)#sets volume of the song playing
                voice.source.volume = 0.7#0.7 is 70%, might make a function that make volume adjustable later

            else:
                queue.clear()
                return
        else:
            queue.clear()
            print("The queue is empty.")
            voice.disconnect()


    global voice
    if(url.find("youtu.be/") != -1):
        url.replace("youtu.be/", "www.youtube.com/watch?v=")
    if(ctx.message.author.voice != None):#if the author of the message is in voice channel
        channel = ctx.message.author.voice.channel#get what channel he is in
        voice = ctx.guild.voice_client#from a list of voice connections, find the connection  for this server. Replacement for get(maid.voice_clients, guild = ctx.guild)
        if(voice and voice.is_connected()):#if there is a connection AND maid-chan is connected
            await voice.move_to(channel)#move to the channel where the author is
        else:
            voice = await channel.connect()#or else, connect to the channel directly
    else:
        if(ctx.guild.id in ENGuilds):
            await ctx.send("Nobody is in the voice channel... I\'m lonely...")
        elif(ctx.guild.id in CNGuilds):
            await ctx.send("没人在语音频道里欸...好寂寞...")
        return

    songPresent = os.path.isfile("song.mp3")#if a file called "song.mp3" presents, it will be true
    try:
        if(songPresent):#if the file is there
            os.remove("song.mp3")#try to delete it
            queue.clear()
            print("Old song file removed")
    except:
        print("File removal failed. Access denied because it is still playing")#if can't remove because it is playing, output this
        if(ctx.message.guild.id in ENGuilds):
            await ctx.send("ERROR: MUSIC IS PLAYING")
            return


    queue_infile = os.path.isdir("./Queue")
    try:
        Queue_folder = "./Queue"
        if(queue_infile is True):
            print("Removed old Queue Folder")
            shutil.rmtree(Queue_folder)
    except:
        print("No old queue folder")

    youtube_dlConfig = {#Configuring youtube_dl
        'format': 'bestaudio/best',
        'quiet': True,
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }

    with youtube_dl.YoutubeDL(youtube_dlConfig) as ydl:#shortening youtube_dl.YoutubeDL(youtube_dlConfig) into ydl
        print("Downloading audio now.\n")
        ydl.download([url])#start downloading the song
    for file in os.listdir("./"): #change name of the file to "song.mp3" so it can be found and deleted later
        if(file.endswith(".mp3")):
            name = file
            os.rename(file, "song.mp3")
            print("Renaming the file...\n")

    voice.play(discord.FFmpegPCMAudio("song.mp3"), after=lambda e: check_queue())#will leave the channel AFTER a song finished playing. This evokes def leave(error) above
    voice.source = discord.PCMVolumeTransformer(voice.source)#sets volume of the song playing
    voice.source.volume = MUSIC_VOLUME#0.7 is 70%, might make a function that make volume adjustable later

    if(ctx.message.guild.id in ENGuilds):
        await ctx.send(f"Playing \"{name[:-16]}\" for you right now! Master {ctx.message.author.name}!")
    elif(ctx.message.guild.id in CNGuilds):
        await ctx.send(f"正在播放{ctx.message.author.name}様点播的《{name[:-16]}》！")#notify user the song started playing

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
        voice.pause()
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
    voice = ctx.guild.voice_client
    queues.clear()
    if(voice and voice.is_playing()):
        voice.stop()
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

queues = {}

@maid.command()
async def queue(ctx, url: str):
    queue_infile = os.path.isdir("./Queue")#check if there is a folder called Queue under the working directory
    if(queue_infile is False):#if not
        os.mkdir("Queue")#make a queue folder
    DIR = os.path.abspath(os.path.realpath("Queue"))#Get absolute path of the file Queue
    q_num = len(os.listdir(DIR))#count how many files(songs) are under  this directory
    q_num += 1
    add_queue = True
    while(add_queue):
        if(q_num in queues):#Count how many songs are present in queue
            q_num += 1
        else:
            add_queue = False
            queues[q_num] = q_num

    queue_path = os.path.abspath(os.path.realpath("Queue") + f"\song{q_num}.%(ext)s")

    youtube_dlConfig = {#Configuring youtube_dl
        'format': 'bestaudio/best',
        'quiet': True,
        'outtmpl': queue_path,
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }

    with youtube_dl.YoutubeDL(youtube_dlConfig) as ydl:#shortening youtube_dl.YoutubeDL(youtube_dlConfig) into ydl
        print("Downloading audio now.\n")
        ydl.download([url])#start downloading the song

    if(ctx.guild.id in ENGuilds):
        await ctx.send(f"I have added the song \"{str(q_num)}\" to the queue for you, Master {ctx.message.author.name}!")
    elif(ctx.guild.id in CNGuilds):
        await ctx.send(f"已经为{ctx.message.author.name}様将《{str(q_num)}》加入了歌单中!")

@maid.command()#For debugging purposes
async def ping(ctx):
    await ctx.send(f'The ping is {round(maid.latency * 1000)}ms')

@maid.command(brief = "***Private Feature***")
async def saveSet(ctx):
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
        await ctx.send("File Saved!")
    except FileNotFoundError:
        await ctx.send("MAID ERROR: CONFIG FILE SAVE ERROR")

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
