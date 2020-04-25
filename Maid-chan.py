import discord
from discord.ext import commands
from discord.utils import get
import random
import youtube_dl
import os
import asyncio
import pixivpy3
from pixivpy3 import *
import time

random.seed(time.time())

TOKEN = ""
maid = commands.Bot(command_prefix = commands.when_mentioned_or("!",".","?","MC ","mc ","Mc ","maid chan ","Maid chan ",'妹抖酱',"老婆","媳妇","小可爱","小宝贝", '！'))
ENGuilds = []
CNGuilds = []

queque = {}
players = {}
XD = False
really = False
prevMessage = ""
messageRepeat = 0

@maid.event
async def on_ready():
    await maid.change_presence(status=discord.Status.idle, activity = discord.Game(" with catgirls"))
    print(f"Logged in as {maid.user.name}")

@maid.event
async def on_member_join(member):
    guild = member.guild.name
    print(f'{member} has joined {guild}.')
    if(member.guild.id == 352312296309260289):
        channel = member.guild.get_channel(352314900359413761)
        await channel.send(f'Welcome to the Passerines! <@{member.id}>!')
    elif(member.guild.id == 358473448076607499):
        channel = member.guild.get_channel(358473448076607500)
        await channel.send(f'欢迎<@{member.id}>様！いらっしゃいませ！')
    elif(member.guild.id == 431610460307980302):
        channel = member.guild.get_channel(431610460307980306)
        await channel.send(f'欢迎<@{member.id}>様！いらっしゃいませ！')
    elif(member.guild.id == 392194794018963456):
        channel = member.guild.get_channel(392194794018963459)
        await channel.send(f'欢迎<@{member.id}>様！いらっしゃいませ！欢迎来到DOLLARS的时差党！')

@maid.event
async def on_member_remove(member):
    guild = member.guild.name
    print(f'{member} has left {guild}.')

@maid.event
async def on_raw_reaction_add(payload):
    messageID = payload.message_id
    if (messageID == 654642859156307980):
        guildID = payload.guild_id
        guild = maid.get_guild(guildID)
        if(payload.emoji.name == 'derp'):
            role = guild.get_role(402649667843915776)
        else:
            role = discord.utils.get(guild.roles, name = payload.emoji.name)

        if(role is not None):
            member = discord.utils.find(lambda m : m.id == payload.user_id, guild.members)
            if(member is not None):
                await member.add_roles(role)
                print(f'The member {member} from server {guild} has joined the role')
            else:
                print('Member not found!')
        else:
            print('Role not found!')

@maid.event
async def on_raw_reaction_remove(payload):
    messageID = payload.message_id
    if (messageID == 654642859156307980):
        guildID = payload.guild_id
        guild = maid.get_guild(guildID)
        if(payload.emoji.name == 'derp'):
            role = guild.get_role(402649667843915776)
        else:
            role = discord.utils.get(guild.roles, name = payload.emoji.name)

        if(role is not None):
            member = discord.utils.find(lambda m : m.id == payload.user_id, guild.members)
            if(member is not None):
                await member.remove_roles(role)
                print(f'The member {member} from {guild} has left the role.')
            else:
                print('Member not found!')
        else:
            print('Role not found!')

@maid.event###Reserved for personal use! (Mostly to spam Reaily XD)
async def on_message(message):
    global XD
    global really
    global prevMessage
    global messageRepeat
    channel = message.channel
    originalMessage = message.content
    if(originalMessage == prevMessage):
        messageRepeat += 1
    if(messageRepeat > 1):
        messageRepeat = 0
        await channel.send(originalMessage)
        await maid.process_commands(message)
    prevMessage = originalMessage
    lowerMessage = originalMessage.lower()
    reallyIndex = lowerMessage.find('really')
    shotIndex = lowerMessage.find('shot')
    if(shotIndex >= 0 and message.author.id != 555273228440829954):
        await channel.send("Did somebody say SHOT?!\n https://cdn.discordapp.com/attachments/177595404324438016/505788828167176195/1540657957240.png")
        await maid.process_commands(message)
    if(message.author.id == 378085550499954699 and message.author.guild.id == 352312296309260289 and XD == True):
        await channel.send('XD')
        await maid.process_commands(message)
    elif(reallyIndex >= 0 and message.author.id != 555273228440829954 and message.author.guild.id == 352312296309260289 and really == True):
        await channel.send(f'Hey! {message.author.mention}! I think you meant <@378085550499954699> instead of "{originalMessage[reallyIndex : reallyIndex + 6]}"! <:thonk:615740280913657866>')
        await maid.process_commands(message)
    else:
        await maid.process_commands(message)

@maid.command(brief = 'Get the ping of maid-chan.')
async def ping(ctx):
    await ctx.send(f'The ping is {round(maid.latency * 1000)}ms')

@maid.command(brief = 'Get a random and cute response from maid-chan.')
async def hi(ctx):
    guild = ctx.message.guild.id
    member = ctx.message.author.name
    if(guild in CNGuilds):
        possible_responses = [
        '哟，今天的风儿好喧嚣啊',
        '哟！不得了了，隔壁超市薯片半价了！！',
        'こんにちは！',
        '你好啊！',
        f'欢迎回来！{member}様!お帰りなさい！'
         ]
        await ctx.send(random.choice(possible_responses) + ctx.message.author.mention)
    elif(guild in ENGuilds):
        possible_responses = [
        'Hey!',
        'Hi!',
        'Whassup!'
         ]
        await ctx.send(random.choice(possible_responses) + ctx.message.author.mention)
    else:
        await ctx.send("Please contact admin to set your language preference!\n请联系管理员设定你的语言！" + ctx.message.author.mention)

@maid.command(brief = '***FEATURE DEVELOPMEN*** DO NOT USE!!!')#FIXME: A config file is needed to limit  this  to certain roles
async def assign(ctx):#Command should be "!assign @name role"
    guildID = ctx.message.guild.id#Get which server this message is from
    guild = discord.utils.find(lambda g : g.id == guildID, maid.guilds)#from all of the guilds maid-chan had joined, find this guild by guild_id
    content = ctx.message.content#get content of the message
    word_list = content.split()#split the words into a list
    role = discord.utils.get(guild.roles, name = word_list[-1])#find the role in the guild by reading the first item from the left of the list
    mentions = ctx.message.raw_mentions#get a list of user id of those mentioned in the message
    if(role is not None):
        member = discord.utils.find(lambda m : m.id == mentions[0], guild.members)#find who those members in a list of members from the guild specified earlier
        if(member is not None):#if found member
            await member.add_roles(role)#add the role to the member
            print(f'The member {member} from server {guild} has joined the role {role}.')#print in console
            if(guildID in CNGuilds):
                ctx.send(f"欢迎{member}的加入！现在开始你也是\"{role}\"的一员了！")
            if(guildID in ENGuilds):
                ctx.send(f"Welcome {member}! A new member of\"{role}\"! ")
        else:
            print('MAID ERROR: Member not found!')
            if(guildID in CNGuilds):
                ctx.send("MAID ERROR: 没有找到该成员！")
            if(guildID in ENGuilds):
                ctx.send("MAID ERROR: Member not found!")
    else:
        print('MAID ERROR: Role not found!')
        if(guildID in CNGuilds):
            ctx.send("MAID ERROR: 没有找到该角色！")
        if(guildID in ENGuilds):
            ctx.send("MAID ERROR: Role not found!")

@maid.command(brief = '***FEATURE IN DEVELOPMENT*** DO NOT USE!!!')#FIXME: A config file is needed to limit  this  to certain roles
async def remove(ctx):
    guildID = ctx.message.guild.id
    guild = discord.utils.find(lambda g : g.id == guildID, maid.guilds)
    content = ctx.message.content
    word_list = content.split()
    role = discord.utils.get(guild.roles, name = word_list[-1])
    mentions = ctx.message.raw_mentions
    if(role is not None):
        member = discord.utils.find(lambda m : m.id == mentions[0], guild.members)
        if(member is not None):
            await member.remove_roles(role)
            print(f'The member {member} from server {guild} has left the role {role}.')
        else:
            print('Member not found!')
    else:
        print('Role not found!')

def leave(error):#Inserts coroutine into an async function, for play()
    global voice
    coro = voice.disconnect()
    fut = asyncio.run_coroutine_threadsafe(coro, maid.loop)
    try:
        fut.result()
    except:
        pass

MUSIC_VOLUME = 0.0
@maid.command(brief = '***FEATURE IN BETA*** Play music. Usage: !play [YouTube url]')
async def play(ctx,url: str):
    global voice
    global MUSIC_VOLUME
    if(url.find("youtu.be/") != -1):
        url.replace("youtu.be/", "www.youtube.com/watch?v=")
    if(ctx.message.author.voice is not None):#if the author of the message is in voice channel
        channel = ctx.message.author.voice.channel#get what channel he is in
        voice = ctx.guild.voice_client#from a list of voice connections, find the connection  for this server. Replacement for get(maid.voice_clients, guild = ctx.guild)
        if(voice and voice.is_connected()):#if there is a connection AND maid-chan is connected
            await voice.move_to(channel)#move to the channel where the author is
        else:
            voice = await channel.connect()#or else, connect to the channel directly
    else:
        if(ctx.message.guild.id in ENGuilds):
            await ctx.send("Nobody is in the voice channel... I\'m lonely...")
        elif(ctx.message.guild.id in CNGuilds):
            await ctx.send("没人在语音频道里欸...好寂寞...")
            return

    songPresent = os.path.isfile("song.mp3")#if a file called "song.mp3" presents, it will be true
    try:
        if(songPresent):#if the file is there
            os.remove("song.mp3")#try to delete it
            print("Old song file removed")
    except:
        print("File removal failed. Access denied because it is still playing")#if can't remove because it is playing, output this
        if(ctx.message.guild.id in ENGuilds):
            await ctx.send("ERROR: MUSIC IS PLAYING")
            return

    youtube_dlConfig = {#Configuring youtube_dl
        'format': 'bestaudio/best',
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

    voice.play(discord.FFmpegPCMAudio("song.mp3"), after=leave)#will leave the channel AFTER a song finished playing. This evokes def leave(error) above
    voice.source = discord.PCMVolumeTransformer(voice.source)#sets volume of the song playing
    voice.source.volume = MUSIC_VOLUME

    if(ctx.message.guild.id in ENGuilds):
        await ctx.send(f"Playing \"{name[:-16]}\" for you right now! Master {ctx.message.author.name}!")
    elif(ctx.message.guild.id in CNGuilds):
        await ctx.send(f"正在播放{ctx.message.author.name}様点播的《{name[:-16]}》！")#notify user the song started playing

@maid.command(brief = 'Pause the music.')
async def pause(ctx):
    voice = ctx.guild.voice_client
    if(voice and voice.is_playing()):
        voice.pause()
        if(ctx.message.guild.id in ENGuilds):
            await ctx.send(f"I have paused the music for you, Master {ctx.message.author.name}!THE WORLD!!Time, STOP!!!")
        elif(ctx.message.guild.id in CNGuilds):
            await ctx.send(f"已经为{ctx.message.author.name}様暂停了音乐！！THE WORLD！！時よ止まれ！！")
        await voice.disconnect()
    else:
        if(ctx.message.guild.id in ENGuilds):
            await ctx.send("MAID ERROR: MUSIC IS NOT PLAYING!")
        elif(ctx.message.guild.id in CNGuilds):
            await ctx.send("MAID ERROR: 暂无音乐播放中！")

@maid.command(brief = "Resume the music.")
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

@maid.command(brief = "Stop the music. (Cannot be resumed)")
async def stop(ctx):#PLANNING TO REPLACE STOP W/ SKIP. THAT WAY I CAN USE KING CRIMSON REFERENCE
    voice = ctx.guild.voice_client
    if(voice and voice.is_playing()):
        voice.stop()
        if(ctx.message.guild.id in ENGuilds):
            await ctx.send(f"I have stopped the music for you, Master {ctx.message.author.name}!THE WORLD!!Time, STOP!!!")
        elif(ctx.message.guild.id in CNGuilds):
            await ctx.send(f"已经为{ctx.message.author.name}様停止了音乐。THE WORLD！！時よ止まれ！！")
    else:
        print("MAID ERROR: MUSIC IS NOT PLAYING")
        if(ctx.message.guild.id in ENGuilds):
            await ctx.send("MAID ERROR: MUSIC IS NOT PLAYING!")
        elif(ctx.message.guild.id in CNGuilds):
            await ctx.send("MAID ERROR: 暂无音乐播放中！")

@maid.command(brief = 'Set the volume. Usage: !volume [A decimal number between 0 to 1]')
async def setVol(ctx, vol:float):
    global MUSIC_VOLUME
    MUSIC_VOLUME = vol
    if(ctx.message.guild.id in CNGuilds):
        await ctx.send(f"已经为{ctx.message.author.name}様将音量设为了{vol * 100}%!将在下一首歌生效!")
    else:
        await ctx.send(f"I have changed the volume to {vol * 100}%, Master {ctx.message.author.name}!It will take effect when the next song starts!")

@maid.command(brief = "***PRIVATE FEATURE***")
async def noXD(ctx):
    global XD
    XD = False
    await ctx.send('Okay... Guess I\'m just an annoying bot that no one likes... QAQ')

@maid.command(brief = "***PRIVATE FEATURE***")
async def yesXD(ctx):
    global XD
    XD = True
    await ctx.send('Yay! Guess you still like me after all! XD')

@maid.command(brief = "***PRIVATE FEATURE***")
async def noReally(ctx):
    global really
    really = False
    await ctx.send('Okay... I\'m a dumb bot...>A<')

@maid.command(brief = "***PRIVATE FEATURE***")
async def yesReally(ctx):
    global really
    really = True
    await ctx.send('Yay! Guess I\'m smart after all! Smarter than you dumb humans! ^V^')

@maid.command(brief = "***PRIVATE FEATURE***", aliases = ['你真可爱，嫁给我好吗♡', '婚礼定在6月28号可以吗？'])
async def love(ctx):
    if(ctx.message.author.id == 570112738681028608):
        await ctx.send(f'```言いたいことがあるんだよ!\nやっばり{ctx.message.author.name}はかわいいよ!\nすきすき大好き!やっば好き!\nやっと見つけたお姫様!\nボクが生まれてきた理由\nそれは{ctx.message.author.name}に出会うため!\nボクと一緒に人生歩もう!\n世界で一番愛してる!\nア·イ·シ·テ·ル! !```')    
    else:
        return

PID = ""
PPASS = ""
@maid.command(brief = "Search for pics on Pixiv! Usage: !picSearch [keyword] or !色图 [keyword]", aliases = ['色图'],)
async def picSearch(ctx, title: str):
    global PID
    global PPASS
    pixivAPI = AppPixivAPI()
    pixivAPI.login(PID, PPASS)
    result = pixivAPI.search_illust(title)
    if(len(result.illusts) != 0):
        illust = result.illusts[random.randint(0, len(result.illusts) - 1)]
        imagePresent = os.path.isfile(f'illust.jpg')
        if(imagePresent):
            os.remove(f'illust.jpg')
        pixivAPI.download(illust.image_urls.large, fname=f'illust.jpg')
        await ctx.send(f"Title: {illust.title}")
        await ctx.send(file=discord.File(f'illust.jpg'))
    else:
        await ctx.send("Image can\'t be found! 无法找到图片！")

bullets = [0, 0, 0, 0, 0, 0]
shotCounter = 0
@maid.command(brief = "Play Russian Roulette with your friends!")
async def RR(ctx):
    global shotCounter
    global bullets
    if(shotCounter == 0):
        bullets.insert(random.randint(0, 6), 1)

    if(bullets[0] == 1):
        shotCounter += 1
        if(ctx.message.guild.id in ENGuilds):
            await ctx.send(f"OOF, {ctx.author.name} is dead! The chance of this happening is {round((shotCounter / 7.0)*100)}%!")
        elif(ctx.message.guild.id in CNGuilds):
            await ctx.send(f"啊，{ctx.author.name}挂了！概率是{round((shotCounter / 7.0)*100)}%！")
        shotCounter = 0
        bullets = [0, 0, 0, 0, 0, 0]
    else:
        shotCounter += 1
        bullets.pop(0)
        if(ctx.message.guild.id in ENGuilds):
            await ctx.send(f"Congrats! {ctx.author.name} is still alive!")
        elif(ctx.message.guild.id in CNGuilds):
            await ctx.send(f"恭喜! {ctx.author.name}还活着!")

@maid.command(brief = "***Private Feature***")
async def saveSet(ctx):
    try:
        fout = open("config.txt", 'w')
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
        await ctx.send("Config File Saved!")
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

@maid.command(brief = "***Private Feature***")
async def delGuild(ctx):
    if(ctx.guild.id in CNGuilds):
        CNGuilds.pop(CNGuilds.index(ctx.guild.id))
        await ctx.send(f'{ctx.guild.name} has been deleted!')
    elif(ctx.guild.id in ENGuilds):
        ENGuilds.pop(ENGuilds.index(ctx.guild.id))
        await ctx.send(f'{ctx.guild.name} has been deleted!')
    else:
        await ctx.send(f'MAID ERROR: GUILD IS NOT ON RECORD')

@maid.command(brief = "***Private Feature***")
async def delete(ctx, messageID: int):
    message = await ctx.channel.fetch_message(messageID)
    await message.delete()
    await ctx.send("Message deleted!")

maid.command()
async def say(ctx, language:str):
    if(ctx.message.author.voice is not None):#if the author of the message is in voice channel
        channel = ctx.message.author.voice.channel#get what channel he is in
        voice = ctx.guild.voice_client#from a list of voice connections, find the connection  for this server. Replacement for get(maid.voice_clients, guild = ctx.guild)
        if(voice and voice.is_connected()):#if there is a connection AND maid-chan is connected
            await voice.move_to(channel)#move to the channel where the author is
        else:
            voice = await channel.connect()#or else, connect to the channel directly
    else:
        if(ctx.message.guild.id in ENGuilds):
            await ctx.send(f"{ctx.author.mention} is in the voice channel... I\'m lonely...")
        elif(ctx.message.guild.id in CNGuilds):
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
    voice.source.volume = MUSIC_VOLUME

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
        fin = open("config.txt", 'r')
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
