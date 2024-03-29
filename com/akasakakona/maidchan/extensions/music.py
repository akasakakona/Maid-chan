"""
Class Definition for Lavalink.py can be found here:
https://github.com/Devoxin/Lavalink.py/blob/master/lavalink/models.py
Documentation for Lavalink.py:
https://lavalink.readthedocs.io/en/latest/lavalink.html
Implementation information for Lavalink can be found here:
https://github.com/Frederikam/Lavalink/blob/master/IMPLEMENTATION.md                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 
"""
import re
import secrets
import nextcord
import lavalink
from nextcord.ext import commands
from ..core.MaidChan import MaidChan
from ..config.ConfigManager import ConfigManager

url_rx = re.compile(r'https?://(?:www\.)?.+')


class Music(commands.Cog):
    def __init__(self):
        self.maid = MaidChan.instance()
        self.g_config = ConfigManager.instance().get_global_config()
        self.config = self.g_config.get("Lavalink")
        if not hasattr(self.maid, "lavalink"):  # This ensures the client isn't overwritten during cog reloads.
            self.maid.lavalink = lavalink.Client(int.from_bytes(secrets.token_bytes(4), "big"))
            self.maid.lavalink.add_node(self.config['Host'], self.config['Port'], self.config['Pass'], self.config['Region'], self.config['Node'])  # Host, Port, Password, Region, Name
            self.maid.add_listener(self.maid.lavalink.voice_update_handler, 'on_socket_response')

        lavalink.add_event_hook(self.track_hook)

    def cog_unload(self):
        """ Cog unload handler. This removes any event hooks that were registered. """
        self.maid.lavalink._event_hooks.clear()

    async def cog_before_invoke(self, ctx):
        """ Command before-invoke handler. """
        guild_check = ctx.guild is not None


        if guild_check:
            await self.ensure_voice(ctx)

        return guild_check

    async def cog_command_error(self, ctx, error):
        if isinstance(error, commands.CommandInvokeError):
            await ctx.send(f"MAID ERROR:{error.original}")

    async def ensure_voice(self, ctx):
        """ This check ensures that the maid and command author are in the same voicechannel. """
        player = self.maid.lavalink.player_manager.create(ctx.guild.id, endpoint=str(ctx.guild.region))
        should_connect = ctx.command.name in ('play',)

        if not ctx.author.voice or not ctx.author.voice.channel:
            raise commands.CommandInvokeError('Join a voicechannel first.')

        if not player.is_connected:
            if not should_connect:
                raise commands.CommandInvokeError('Not connected.')

            permissions = ctx.author.voice.channel.permissions_for(ctx.me)

            if not permissions.connect or not permissions.speak:  # Check user limit too?
                raise commands.CommandInvokeError('I need the `CONNECT` and `SPEAK` permissions.')

            player.store('channel', ctx.channel.id)
            await self.connect_to(ctx.guild.id, str(ctx.author.voice.channel.id))
        else:
            if int(player.channel_id) != ctx.author.voice.channel.id:
                raise commands.CommandInvokeError('You need to be in my voicechannel.')

    async def track_hook(self, event):
        if isinstance(event, lavalink.events.QueueEndEvent):
            guild_id = int(event.player.guild_id)
            await self.connect_to(guild_id, None)

    async def connect_to(self, guild_id: int, channel_id: str):
        """ Connects to the given voicechannel ID. A channel_id of `None` means disconnect. """
        ws = self.maid._connection._get_websocket(guild_id)
        await ws.voice_state(str(guild_id), channel_id)
        # The above looks dirty, we could alternatively use `maid.shards[shard_id].ws` but that assumes
        # the maid instance is an AutoShardedBot.

    def msToHrMinSec(self, ms):
        sec = (ms//1000)%60
        minute = (ms//(1000*60))%60
        hr = (ms//(1000*60*60))%24
        return (hr, minute, sec)

    @commands.command(aliases=['p'])
    async def play(self, ctx, *, query: str = ""):
        """ Searches and plays a song from a given query. """
        # Get the player for this guild from cache.
        player = self.maid.lavalink.player_manager.get(ctx.guild.id)
        # Remove leading and trailing <>. <> may be used to suppress embedding links in Discord.

        if player.paused:
            return await player.set_pause(False)
        elif not player.paused and query == "":
            return await ctx.send(" MAID ERROR: Correct Usage: !play [query/url]")

        query = query.strip('<>')

        # Check if the user input might be a URL. If it isn't, we can Lavalink do a YouTube search for it instead.
        # SoundCloud searching is possible by prefixing "scsearch:" instead.
        if not url_rx.match(query):
            query = f'ytsearch:{query}'

        # Get the results for the query from Lavalink.
        results = await player.node.get_tracks(query)

        # Results could be None if Lavalink returns an invalid response (non-JSON/non-200 (OK)).
        # ALternatively, resullts['tracks'] could be an empty array if the query yielded no tracks.
        if not results or not results['tracks']:
            return await ctx.send('Nothing found!')

        embed = nextcord.Embed(color=nextcord.Color.dark_red())

        # Valid loadTypes are:
        #   TRACK_LOADED    - single video/direct URL)
        #   PLAYLIST_LOADED - direct URL to playlist)
        #   SEARCH_RESULT   - query prefixed with either ytsearch: or scsearch:.
        #   NO_MATCHES      - query yielded no results
        #   LOAD_FAILED     - most likely, the video encountered an exception during loading.
        if results['loadType'] == 'PLAYLIST_LOADED':
            tracks = results['tracks']

            for track in tracks:
                # Add all of the tracks from the playlist to the queue.
                player.add(requester=ctx.author.id, track=track)
            embed.title = results["playlistInfo"]["name"]
            if lang(ctx) == "en":
                embed.description = f'Successfully added playlist \"{results["playlistInfo"]["name"]}\" into the playlist! {ctx.author.name}-sama!\n***This playlist will contain {len(tracks)} songs!***'
            elif lang(ctx) == "cn":
                embed.description = f'成功为{ctx.author.name}様将您点播的歌单《{results["playlistInfo"]["name"]}》加入歌单！\n***这个歌单中包含了：{len(tracks)}首歌！***'
        else:
            track = results['tracks'][0]
            embed.title = track["info"]["title"]
            embed.url = track["info"]["uri"]
            embed.set_author(name=track["info"]["author"])
            if lang(ctx) == "en":
                embed.description = f'Playing \"{track["info"]["title"]}\" for you right now! {ctx.author.name}-sama!\n'
            elif lang(ctx) == "cn":
                embed.description = f'成功为{ctx.author.name}様播放《{track["info"]["title"]}》！\n'

            if track["info"]["isStream"] and lang(ctx) == "cn":
                embed.description += f"***啊啊啊！！{ctx.author.name}様又在DD！ぷんぷん！！女仆酱我要吃醋了哦！***"
            elif not track["info"]["isStream"]:
                length = track["info"]["length"]
                duration = self.msToHrMinSec(ms=length)
                embed.description += f"***Duration: {duration[0]}:{duration[1]}:{duration[2]}***"
            # You can attach additional information to audiotracks through kwargs, however this involves
            # constructing the AudioTrack class yourself.
            track = lavalink.models.AudioTrack(track, ctx.author.id, recommended=True)
            player.add(requester=ctx.author.id, track=track)

        await ctx.send(embed=embed)

        # We don't want to call .play() if the player is playing as that will effectively skip
        # the current track.
        if not player.is_playing:
            await player.play()

    @commands.command(aliases=['dc'])
    async def disconnect(self, ctx):
        """ Disconnects the player from the voice channel and clears its queue. """
        player = self.maid.lavalink.player_manager.get(ctx.guild.id)

        if not player.is_connected:
            # We can't disconnect, if we're not connected.
            return await ctx.send('Not connected.')

        if not ctx.author.voice or (player.is_connected and ctx.author.voice.channel.id != int(player.channel_id)):
            # Abuse prevention. Users not in voice channels, or not in the same voice channel as the maid
            # may not disconnect the maid.
            return await ctx.send('You\'re not in my voicechannel!')

        # Clear the queue to ensure old tracks don't start playing
        # when someone else queues something.
        player.queue.clear()
        # Stop the current track so Lavalink consumes less resources.
        await player.stop()
        # Disconnect from the voice channel.
        await self.connect_to(ctx.guild.id, None)
        if lang(ctx) == "en":
            await ctx.send(f"Successfully disconnected for you! {ctx.author.name}-sama!")
        elif lang(ctx) == "cn":
            await ctx.send(f"成功为您断开连接！{ctx.author.name}様！")

    @commands.command()
    async def pause(self, ctx):
        player = self.maid.lavalink.player_manager.get(ctx.guild.id)
        if not player.is_connected:
            # We can't disconnect, if we're not connected.
            return await ctx.send('MAID ERROR: Not connected.')

        if not ctx.author.voice or (player.is_connected and ctx.author.voice.channel.id != int(player.channel_id)):
            # Abuse prevention. Users not in voice channels, or not in the same voice channel as the maid
            # may not disconnect the maid.
            return await ctx.send('MAID ERROR: Not in my voicechannel!')

        if player.paused:
            #check if the player has been paused already
            return await ctx.send('MAID ERROR: Player already paused!')
        else:
            await player.set_pause(True)
            embed = nextcord.Embed(color=nextcord.Color.dark_red())
            embed.title = player.current.title
            embed.url = player.current.uri
            if lang(ctx) == "en":
                embed.description = f"Successfully paused\"{player.current.title}\" for you! {ctx.author.name}-sama!"
            elif lang(ctx) == "cn":
                embed.description = f"成功为您暂停了《{player.current.title}》！{ctx.author.name}様！"
            await ctx.send(embed)

    @commands.command()
    async def skip(self, ctx):
        player = self.maid.lavalink.player_manager.get(ctx.guild.id)
        if not player.is_connected:
            return await ctx.send('MAID ERROR: Not connected!')

        if not ctx.author.voice or (player.is_connected and ctx.author.voice.channel.id != int(player.channel_id)):
            return await ctx.send('MAID ERROR: Not in my voicechannel!')
        try:
            embed = nextcord.Embed(color=nextcord.Color.dark_red())
            embed.title = player.current.title
            embed.url = player.current.uri
            embed.set_author(name=player.current.author)
            await player.skip()
            if lang(ctx) == "en":
                embed.description = f"Successfully skipped\"{player.current.title}\" for you! {ctx.author.name}-sama!"
            elif lang(ctx) == "cn":
                embed.description = f"成功为您跳过了《{player.current.title}》！{ctx.author.name}様！"
            return await ctx.send(embed=embed)
        except:
            return await ctx.send("MAID ERROR: Failed to skip!")

    @commands.command()
    async def shuffle(self, ctx):
        player = self.maid.lavalink.player_manager.get(ctx.guild.id)
        if not player.is_connected:
            # We can't disconnect, if we're not connected.
            return await ctx.send('MAID ERROR: Not connected!')

        if not ctx.author.voice or (player.is_connected and ctx.author.voice.channel.id != int(player.channel_id)):
            return await ctx.send('MAID ERROR: Not in my voicechannel!')
        if player.shuffle:
            player.set_shuffle(False)
            if lang(ctx) == "en":
                await ctx.send(f"Successfully un-shuffled the playlist for you! {ctx.author.name}-sama!")
            elif lang(ctx) == "cn":
                await ctx.send(f"成功为您关闭了随机播放！{ctx.author.name}様！")
        else:
            player.set_shuffle(True)
            if lang(ctx) == "en":
                await ctx.send(f"Successfully shuffled the playlist for you! {ctx.author.name}-sama!")
            elif lang(ctx) == "cn":
                await ctx.send(f"成功为您开启了随机播放！{ctx.author.name}様！")

    @commands.command()
    async def loop(self, ctx):
        player = self.maid.lavalink.player_manager.get(ctx.guild.id)
        if not player.is_connected:
            # We can't disconnect, if we're not connected.
            return await ctx.send('MAID ERROR: Not connected!')

        if not ctx.author.voice or (player.is_connected and ctx.author.voice.channel.id != int(player.channel_id)):
            # Abuse prevention. Users not in voice channels, or not in the same voice channel as the maid
            # may not disconnect the maid.
            return await ctx.send('MAID ERROR: Not in my voicechannel!')
        embed = nextcord.Embed(color=nextcord.Color.dark_red())
        embed.title = player.current.title
        embed.url = player.current.uri
        embed.set_author(name=player.current.author)
        if player.repeat:
            player.set_repeat(False)
            if lang(ctx) == "en":
                embed.description = f"I will stop looping \"{player.current.title}\" for you! {ctx.author.name}-sama!"
            elif lang(ctx) == "cn":
                embed.description = f"成功为您关闭了《{player.current.title}》的洗脑循环！{ctx.author.name}様！"
        else:
            player.set_repeat(True)
            if lang(ctx) == "en":
                embed.description = f"I will start looping \"{player.current.title}\" for you! {ctx.author.name}-sama!"
            elif lang(ctx) == "cn":
                embed.description = f"成功为您开启了《{player.current.title}》的洗脑循环！{ctx.author.name}様！"
        await ctx.send(embed=embed)


def lang(ctx):
    return ConfigManager.instance().get_server_config(ctx.guild.id).get_main().get("lang")


def setup(maid):
    maid.add_cog(Music())
