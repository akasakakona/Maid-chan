import discord
from discord.ext import commands
import os
import json

# @maid.command(brief = '***FEATURE DEVELOPMEN*** DO NOT USE!!!')#FIXME: A config file is needed to limit  this  to certain roles
# async def assign(ctx):#Command should be "!assign @name role"
#     guildID = ctx.message.guild.id#Get which server this message is from
#     guild = discord.utils.find(lambda g : g.id == guildID, maid.guilds)#from all of the guilds maid-chan had joined, find this guild by guild_id
#     content = ctx.message.content#get content of the message
#     word_list = content.split()#split the words into a list
#     role = discord.utils.get(guild.roles, name = word_list[-1])#find the role in the guild by reading the first item from the left of the list
#     mentions = ctx.message.raw_mentions#get a list of user id of those mentioned in the message
#     if(role is not None):
#         member = discord.utils.find(lambda m : m.id == mentions[0], guild.members)#find who those members in a list of members from the guild specified earlier
#         if(member is not None):#if found member
#             await member.add_roles(role)#add the role to the member
#             print(f'The member {member} from server {guild} has joined the role {role}.')#print in console
#             if(guildID in CNGuilds):
#                 ctx.send(f"欢迎{member}的加入！现在开始你也是\"{role}\"的一员了！")
#             if(guildID in ENGuilds):
#                 ctx.send(f"Welcome {member}! A new member of\"{role}\"! ")
#         else:
#             print('MAID ERROR: Member not found!')
#             if(guildID in CNGuilds):
#                 ctx.send("MAID ERROR: 没有找到该成员！")
#             if(guildID in ENGuilds):
#                 ctx.send("MAID ERROR: Member not found!")
#     else:
#         print('MAID ERROR: Role not found!')
#         if(guildID in CNGuilds):
#             ctx.send("MAID ERROR: 没有找到该角色！")
#         if(guildID in ENGuilds):
#             ctx.send("MAID ERROR: Role not found!")

# @maid.command(brief = '***FEATURE IN DEVELOPMENT*** DO NOT USE!!!')#FIXME: A config file is needed to limit  this  to certain roles
# async def remove(ctx):
#     guildID = ctx.message.guild.id
#     guild = discord.utils.find(lambda g : g.id == guildID, maid.guilds)
#     content = ctx.message.content
#     word_list = content.split()
#     role = discord.utils.get(guild.roles, name = word_list[-1])
#     mentions = ctx.message.raw_mentions
#     if(role is not None):
#         member = discord.utils.find(lambda m : m.id == mentions[0], guild.members)
#         if(member is not None):
#             await member.remove_roles(role)
#             print(f'The member {member} from server {guild} has left the role {role}.')
#         else:
#             print('Member not found!')
#     else:
#         print('Role not found!')

# MUSIC_VOLUME = 0.0
# LOOP_SINGLE = False
# LOOP_ALL = False
# musicList = []
# currIndex = 0
# @maid.command(brief = '***FEATURE IN BETA*** Play music. Usage: !play [YouTube url]')
# async def play(ctx,url: str):
#     global voice
#     global musicList
#     global currIndex
#     if(ctx.message.author.voice is not None):#if the author of the message is in voice channel
#         channel = ctx.message.author.voice.channel#get what channel he is in
#         voice = ctx.guild.voice_client#from a list of voice connections, find the connection  for this server. Replacement for get(maid.voice_clients, guild = ctx.guild)
#         youtube = build("youtube", "v3", developerKey=DEV_KEY)
#         if(url.find("playlist?list=") >= 0):
#             request = youtube.playlistItems().list(part="contentDetails", maxResults=50, playlistId=url[url.find("playlist?list=")+14 : len(url)])
#             result = request.execute()
#             for item in result["items"]:
#                 tempUrl = "https://www.youtube.com/watch?v=" + item["contentDetails"]["videoId"]
#                 request1 = youtube.videos().list(part = "snippet,contentDetails", id = tempUrl)
#                 result1 = request1.execute()
#                 musicList.append(Video(result1["items"][0]["snippet"]["title"], result1["items"][0]["snippet"]["thumbnails"]["maxres"]["url"], result1["items"][0]["contentDetails"]["duration"], tempUrl, ctx.message.author))
#         else:
#             request = youtube.videos().list(part = "snippet,contentDetails", id = url[-11:])
#             result = request.execute()
#             musicList.append(Video(result["items"][0]["snippet"]["title"], result["items"][0]["snippet"]["thumbnails"]["maxres"]["url"], result["items"][0]["contentDetails"]["duration"], url[-11:], ctx.message.author))
#             if(ctx.guild.id in ENGuilds):
#                 await ctx.send(f"Play request received! Processing Master {ctx.message.author.name}\'s play request!")
#             elif(ctx.guild.id in CNGuilds):
#                 await ctx.send(f"收到点歌请求！正在处理{ctx.message.author.name}様的点歌请求！")
#         if(voice is not None):
#             return
#     else:
#         if(ctx.message.guild.id in ENGuilds):
#             await ctx.send("Nobody is in the voice channel... I\'m lonely...")
#         elif(ctx.message.guild.id in CNGuilds):
#             await ctx.send("没人在语音频道里欸...好寂寞...")
#             return
    
#     while(len(musicList) != 0):
#         try:
#             os.system(f"youtube-dl -f bestaudio -o \"%(title)s.%(ext)s\" {musicList[currIndex].url}")
#         except:
#             await ctx.send(f"MAID ERROR: VIDEO EXTRACTION FAILED FOR URL: {musicList[currIndex].url} ! PLEASE TRY AGAIN!")
#             musicList.remove(musicList[currIndex])
#             if(len(musicList) == 0):
#                 break
#             continue

#         await asyncio.sleep(3) #need to wait for youtube-dl to merge fragment files before preceeding
#         filename = difflib.get_close_matches(musicList[currIndex].title, os.listdir("./"), n=1)[0]
        
#         audioSouce = discord.FFmpegPCMAudio(filename)

#         if(voice and voice.is_connected()):#if there is a connection AND maid-chan is connected
#             await voice.move_to(channel)#move to the channel where the author is
#         else:
#             voice = await channel.connect()#or else, connect to the channel directly

#         voice.play(audioSouce)#will leave the channel AFTER a song finished playing. This evokes def leave(error) above
#         voice.source = discord.PCMVolumeTransformer(voice.source)#sets volume of the song playing
#         voice.source.volume = MUSIC_VOLUME#0.7 is 70%, might make a function that make volume adjustable later

#         embed = discord.Embed(title = musicList[currIndex].title, description = f"```Duration: {musicList[currIndex].duration}```", colour = discord.Color.magenta(), url = url)
#         embed.set_footer(text = musicList[currIndex].name, icon_url=musicList[currIndex].author.avatar_url)
#         embed.set_thumbnail(url = musicList[currIndex].thumbnail)
#         if(ctx.message.guild.id in ENGuilds):
#             await ctx.send(content = f"Playing \"{musicList[currIndex].title}\" for you right now! Master {musicList[currIndex].name}!", embed = embed)
#         elif(ctx.message.guild.id in CNGuilds):
#             await ctx.send(content = f"正在播放{musicList[currIndex].name}様点播的《{musicList[currIndex].title}》！", embed = embed)#notify user the song started playing
#         while(voice.is_playing() or voice.is_paused()):
#             await asyncio.sleep(1)
#         if(len(musicList) == 1 and not LOOP_ALL and not LOOP_SINGLE):
#             musicList.pop(0)
#             os.remove(filename)
#             await voice.disconnect()
#         elif(currIndex == len(musicList) - 1 and LOOP_ALL):
#             currIndex = 0
#             os.remove(filename)
#         elif(len(musicList) > 1 and not LOOP_ALL and not LOOP_SINGLE):
#             if(currIndex == 0):
#                 musicList.pop(0)
#             else:
#                 for i in range(0, currIndex + 1):
#                     musicList.pop(i)
#             os.remove(filename)
#             currIndex = 0
#         elif(len(musicList) > 1 and LOOP_ALL and not LOOP_SINGLE):
#             currIndex += 1
#             os.remove(filename)
#         elif(len(musicList) > 1 and not LOOP_ALL and LOOP_SINGLE):
#             pass

# @maid.command()
# async def skip(ctx):
#     voice = ctx.guild.voice_client
#     if(voice and voice.is_playing):
#         voice.stop()
#         if(ctx.guild.id in ENGuilds):
#             await ctx.send("Current Song Skipped!")
#         else:
#             await ctx.send("已跳过当前歌曲！")
#     else:
#         if(ctx.message.guild.id in ENGuilds):
#             await ctx.send("MAID ERROR: MUSIC IS NOT PLAYING!")
#         elif(ctx.message.guild.id in CNGuilds):
#             await ctx.send("MAID ERROR: 暂无音乐播放中！")

# @maid.command()
# async def loop(ctx, state: str):
#     global LOOP_ALL
#     global LOOP_SINGLE
#     state = state.lower()
#     if(state == "all"):
#         if(LOOP_SINGLE):
#             LOOP_SINGLE = False
#         LOOP_ALL = True
#         if(ctx.guild.id in ENGuilds):
#             await ctx.send("Loop all is on!")
#         else:
#             await ctx.send("开启全曲洗脑循环！")
#     elif(state == "single"):
#         if(LOOP_ALL):
#             LOOP_ALL = False
#         LOOP_SINGLE = True
#         if(ctx.guild.id in ENGuilds):
#             await ctx.send("Loop single is on!")
#         else:
#             await ctx.send("开启单曲洗脑循环！")
#     elif(state == "off"):
#         LOOP_SINGLE = False
#         LOOP_ALL = False
#         if(ctx.guild.id in ENGuilds):
#             await ctx.send("Loop is off!")
#         else:
#             await ctx.send("洗脑循环关闭！")

# @maid.command(aliases = ['list', 'ls'])
# async def playlist(ctx):
#     playlist = ""
#     i = 1
#     for url in musicList:
#         name = url.title
#         playlist += f"{i}. {name}\n"
#         i += 1
#     if(LOOP_ALL):
#         playlist += "```LOOP_ALL: ON\n"
#     else:
#         playlist += "```LOOP_ALL: OFF\n"
#     if(LOOP_SINGLE):
#         playlist += "LOOP_SINGLE: ON```"
#     else:
#         playlist += "LOOP_SINGLE: OFF```"
#     embed = discord.Embed(title = f"{ctx.guild.name}\'s Playlist", description = playlist, colour = discord.Color.blue())
#     embed.set_footer(text = ctx.guild.name, icon_url=ctx.guild.icon_url)
#     await ctx.send(embed = embed)

# @maid.command(aliases = ['rm'])
# async def remove(ctx, num: int):
#     global musicList
#     name = musicList[num - 1].title
#     musicList.pop(num - 1)
#     if(ctx.guild.id in ENGuilds):
#         await ctx.send(f"\"{name}\" has been deleted for Master {ctx.author.name}!")
#     else:
#         await ctx.send(f"已经为{ctx.author.name}删除了《{name}》!")

# @maid.command(brief = 'Pause the music.')
# async def pause(ctx):
#     voice = ctx.guild.voice_client
#     if(voice and voice.is_playing()):
#         voice.pause()
#         if(ctx.message.guild.id in ENGuilds):
#             await ctx.send(f"I have paused the music for you, Master {ctx.message.author.name}!THE WORLD!!Time, STOP!!!")
#         elif(ctx.message.guild.id in CNGuilds):
#             await ctx.send(f"已经为{ctx.message.author.name}様暂停了音乐！！THE WORLD！！時よ止まれ！！")
#     else:
#         if(ctx.message.guild.id in ENGuilds):
#             await ctx.send("MAID ERROR: MUSIC IS NOT PLAYING!")
#         elif(ctx.message.guild.id in CNGuilds):
#             await ctx.send("MAID ERROR: 暂无音乐播放中！")

# @maid.command(brief = "Resume the music.")
# async def resume(ctx):
#     voice = ctx.guild.voice_client
#     if(voice and voice.is_paused()):
#         voice.resume()
#         if(ctx.message.guild.id in ENGuilds):
#             await ctx.send(f"I have resumed the music for you, Master {ctx.message.author.name}!...And so, time flows again.")
#         elif(ctx.message.guild.id in CNGuilds):
#             await ctx.send(f"已经为{ctx.message.author.name}様重启了音乐。然后，时间开始流动。")
#     else:
#         if(ctx.message.guild.id in ENGuilds):
#             await ctx.send("MAID ERROR: MUSIC IS NOT PAUSED!")
#         elif(ctx.message.guild.id in CNGuilds):
#             await ctx.send("MAID ERROR: 音乐未被暂停！")

# @maid.command(brief = "Stop the music. (Cannot be resumed)")
# async def stop(ctx):#PLANNING TO REPLACE STOP W/ SKIP. THAT WAY I CAN USE KING CRIMSON REFERENCE
#     global musicList
#     global currIndex
#     global LOOP_SINGLE
#     global LOOP_ALL
#     LOOP_ALL = False
#     LOOP_SINGLE = False
#     voice = ctx.guild.voice_client
#     if(voice and voice.is_playing()):
#         voice.stop()
#         for i in range(0, len(musicList)):
#             musicList.pop(0)
#         currIndex = 0
#         if(ctx.message.guild.id in ENGuilds):
#             await ctx.send(f"I have stopped the music for you, Master {ctx.message.author.name}!THE WORLD!!Time, STOP!!!")
#         elif(ctx.message.guild.id in CNGuilds):
#             await ctx.send(f"已经为{ctx.message.author.name}様停止了音乐。THE WORLD！！時よ止まれ！！")
#         await voice.disconnect()
#     else:
#         print("MAID ERROR: MUSIC IS NOT PLAYING")
#         if(ctx.message.guild.id in ENGuilds):
#             await ctx.send("MAID ERROR: MUSIC IS NOT PLAYING!")
#         elif(ctx.message.guild.id in CNGuilds):
#             await ctx.send("MAID ERROR: 暂无音乐播放中！")

# @maid.command(brief = 'Set the volume. Usage: !volume [A decimal number between 0 to 1]')
# async def setVol(ctx, vol:float):
#     global MUSIC_VOLUME
#     MUSIC_VOLUME = vol
#     modSet(modType="volume", modData=vol)
#     if(ctx.message.guild.id in CNGuilds):
#         await ctx.send(f"已经为{ctx.message.author.name}様将音量设为了{vol * 100}%!将在下一首歌生效!")
#     else:
#         await ctx.send(f"I have changed the volume to {vol * 100}%, Master {ctx.message.author.name}!It will take effect when the next song starts!")
    

# @maid.command(brief = "***PRIVATE FEATURE***", aliases = ['你真可爱，嫁给我好吗♡', '婚礼定在6月28号可以吗？'])
# async def love(ctx):
#     if(ctx.message.author.id == 570112738681028608):
#         await ctx.send(f'```言いたいことがあるんだよ!\nやっばり{ctx.message.author.name}はかわいいよ!\nすきすき大好き!やっば好き!\nやっと見つけたお姫様!\nボクが生まれてきた理由\nそれは{ctx.message.author.name}に出会うため!\nボクと一緒に人生歩もう!\n世界で一番愛してる!\nア·イ·シ·テ·ル! !```')    
#     else:
#         return

# @maid.command(brief = "***Private Feature***")
# async def setGuild(ctx, gtype:str):
#     if(ctx.guild.id in CNGuilds or ctx.guild.id in ENGuilds):
#         if(gtype.lower() == "cn" and ctx.guild.id in ENGuilds):
#             ENGuilds.pop(ENGuilds.index(ctx.guild.id))
#             modSet(modType="ENGuilds", modAction="del", modData=ctx.guild.id)
#             CNGuilds.append(ctx.guild.id)
#             modSet(modType="CNGuilds", modAction="add", modData=ctx.guild.id)
#             await ctx.send(f'{ctx.guild.name}的语言已被设为中文！')
#             return
#         elif(gtype.lower() == "en" and ctx.guild.id in CNGuilds):
#             CNGuilds.pop(CNGuilds.index(ctx.guild.id))
#             modSet(modType="CNGuilds", modAction="del", modData=ctx.guild.id)
#             ENGuilds.append(ctx.guild.id)
#             modSet(modType="ENGuilds", modAction="add", modData=ctx.guild.id)
#             await ctx.send(f'{ctx.guild.name}\'s language has been set to English!')
#             return
#         else:
#             await ctx.send("MAID ERROR: GUILD ALREADY EXISTS")
#             return
#     else:
#         await ctx.send("MAID ERROR: GUILD DOES NOT EXIST")
#         return

#     if(gtype.lower() == "cn"):
#         modSet(modType="CNGuilds", modAction="add", modData=ctx.guild.id)
#         await ctx.send(f'{ctx.guild.name}的语言已被设为中文！')
#     elif(gtype.lower() == "en"):
#         modSet(modType="ENGuilds", modAction="add", modData=ctx.guild.id)
#         await ctx.send(f'{ctx.guild.name}\'s language has been set to English!')
#     else:
#         await ctx.send("MAID ERROR: IMPROPER USAGE `!setGuild [en/cn]`")

# @maid.command(brief = "***Private Feature***")
# async def delGuild(ctx):
#     if(ctx.guild.id in CNGuilds):
#         CNGuilds.pop(CNGuilds.index(ctx.guild.id))
#         modSet(modType="CNGuilds", modAction="del", modData=ctx.guild.id)
#         await ctx.send(f'{ctx.guild.name} has been deleted!')
#     elif(ctx.guild.id in ENGuilds):
#         ENGuilds.pop(ENGuilds.index(ctx.guild.id))
#         modSet(modType="ENGuilds", modAction="del", modData=ctx.guild.id)
#         await ctx.send(f'{ctx.guild.name} has been deleted!')
#     else:
#         await ctx.send(f'MAID ERROR: GUILD IS NOT ON RECORD')

# @maid.command(brief = "***Private Feature***")
# async def delete(ctx, messageID: int):
#     message = await ctx.channel.fetch_message(messageID)
#     await message.delete()
#     await ctx.send("Message deleted!")




maid = commands.Bot(command_prefix = commands.when_mentioned_or("!",".","?","MC ","mc ","Mc ","maid chan ","Maid chan ",'妹抖酱',"老婆","媳妇","小可爱","小宝贝", '！'), intents = discord.Intents.all())


TOKEN = ""
try:
    with open('config.json') as f:
        config_dict = json.load(f)
    TOKEN = config_dict['TOKEN']
except FileNotFoundError:
    print(f"MAID ERROR: \'config.json\' NOT FOUND UNDER CURRENT DIRECTORY!\nCURRENT DIRECTORTY: {os.getcwd()}")


for extension in os.listdir('./extensions'): #load extensions
        if extension.endswith('.py'):
            maid.load_extension(f'extensions.{extension[:-3]}')

maid.run(TOKEN)
