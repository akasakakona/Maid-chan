# Maid-chan Introuction
<a href = "https://discord.gg/6qKGErK">
    <img src="https://raw.githubusercontent.com/akasakakona/akasakakona.github.io/master/img/f5uq0NV.png" alt="Join Discord" style="width:42px;height:42px;" class="center" >
</a>


She is based on Python, using Discord.py (Rewrite).

She is being updated slowly.

BUT she is getting better and better with every update!

![alt text](https://raw.githubusercontent.com/akasakakona/akasakakona.github.io/master/img/maid_chan.jpg "Maid-chan")


# Dependencies
- [nextcord[voice]](https://discordpy.readthedocs.io/en/latest/index.html)
- [pixivpy3](https://pypi.org/project/PixivPy/)
- [gTTS](https://pypi.org/project/gTTS/)
- [lavalink](https://github.com/Devoxin/Lavalink.py)

# Before You Start
You will need to create a configuration file and name it `config.json`. 

For more information on formatting of the json file, see: `Sample Config.json`.

**NOTE:** Because Pixiv no longer allows password authentication, Maid-chan has moved to `TOKEN` authentication as a temporary login method. Please refer to [this method](https://gist.github.com/ZipFile/c9ebedb224406f4f11845ab700124362) provided by @ZipFile to get your `TOKEN`! Thank you so much for your contribution!

# Current Version
1.1.0

# Features
* React when new members join the server.
* Some fun little reaction to messages.
* Assign/Remove roles based to the reaction added to a certain message.
* `!ping` for debugging feature.
* `!hi` for fun lol.
* `!play [youtube url]` for playing music
* `!skip` for skipping music.
* `!loop [single/all]` for looping music.
* `!playlist` to view the current playlist.
* `!remove [music number]` for removing musics in the playlist.
* `!pause` for pausing music.
* `!resume` for resuming music.
* `!stop` for stopping music and clearing playlist
* `!RR` for playing Russia Roulette
* `!setVol [0-1]` to set volume for the bot when playing music. 0.1 is 10%, 0.2 is 20%... and so on **(NOTE: One place decimal ONLY)**.
* `!picsearch [keyword]` or `!色图 [keyword]` to search for pictures on Pixiv.
* `!setGuild [cn/en]` to set language preference for gthe current server.
* `!delGuild` to clear the guild's language preference.
* `!delete [messageID]` to delete a message by its ID **(NOTE: Permission needed!)**.
* `!say [a language supported by gTTS] [text]` to have the bot pronounce the text in voice channel using your preferred language **(NOTE: You can find the list of languages supported by gTTS here: https://pypi.org/project/gTTS/1.2.1/)**
* `!shutdown` to safely shut down the bot and save its settings. **(NOTE: Remember to change the ID so it reacts to you!)**.

# Future Planning
* Finish `!assign` command.
* Finish `!removeRole` command.
* Debug and optimize `!play` and music related command.

# Update Log
```
-08/19/2019 ---Progress Report & Future Planning---
    @Current Version:
        0.0.1
    @This Update Includes:
        -Ability to react to basic greetings & commands
        -Unstable music player that requires further testing
    @Future Planning:
        -A more stable music player
        -Add 'loop', 'stop', and 'queue' feature into the music player
        -Move to a newer version of Discord API
        -Ability to greet new members of the server
        -Ability to assign roles to a member

-10/07/2019 ---Progress Report & Future Planning---
    @Current Version:
        0.1.0
    @This Update Includes:
        -Ability to spam @Reaily#6672
        -Ability to assign roles to a member via command (Beta)
        -Multi-language support between different servers
        -Move to a newer version of Discord API
        -Ability to greet new members of the server
    @Future Planning:
        -A more stable music player
        -Add 'loop', 'stop', 'skip', 'pause' , and 'queue' feature into the music player
        -Unicode support
        -Limit the ability to assign roles via command to certain roles/users only

-10/27/2019 ---Feature Report & Future Planning---
    @Current Version:
        0.1.1
    @Features:
        -Music player(Beta)
        -'pause', 'stop', 'play' added to the player.
    @Future Planning:
        -Add 'loop', 'skip', and 'queue' feature into the music player
        -Limit the ability to assign roles via command to certain roles/users only
        -Ability to conduct normal conversation using models trained by Tensorflow
        -Ability to play music simultaneously on multiple servers

-05/07/2019 ---Feature Report & Future Planning---
    @Current Version:
        1.1.0
    @Features:
        -`!skip` for skipping music
        -`!loop [single/all]` for looping music
        -`!playlist` to view the current playlist
        -`!remove [music number]` for removing musics in the playlist
        -`!setVol [0 - 1]` for setting volume of the bot when playing music
        -'!picsearch [keyword]` or `!色图 [keyword]` to search for pictures on Pixiv
        -`!RR` for playing Russia Roulette
        -`!setGuild [cn/en]` to set language preference for gthe current server
        -`!delGuild` to clear the guild's language preference
        -`!delete [messageID]` to delete a message by its ID (NOTE: Permission needed!）
        -`!say [a language supported by gTTS] [text]` to have the bot pronounce the text in voice channel using your preferred language **(NOTE: You can find the list of languages supported by gTTS here: https://pypi.org/project/gTTS/1.2.1/)**
        -`!shutdown` to safely shut down the bot and save its settings. (NOTE: Remember to change the ID so it reacts to you!)
    @Future Planning:
        -Finish `!assign` command
        -Finish `!removeRole` command
        -Debug and optimize `!play` and music related command
        
-05/17/2019 ---Feature Report & Future Planning---
    @Current Version:
        1.2.0
    @Features:
        -Added JSON support
    @Future Planning:
        -Finish `!assign` command
        -Finish `!removeRole` command
        -Debug and optimize `!play` and music related command
```
