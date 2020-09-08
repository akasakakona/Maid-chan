import json

def loadSet(filename):
    global ENGuilds
    global CNGuilds
    global PID
    global PPASS
    global MUSIC_VOLUME
    global DEV_KEY
    global ADMIN
    
        for gid in config_dict['ENGuilds']:
          ENGuilds.append(gid)
        for gid in config_dict['CNGuilds']:
          CNGuilds.append(gid)
        MUSIC_VOLUME = config_dict['volume']
        PID = config_dict['PID']
        PPASS = config_dict['PPASS']
        DEV_KEY = config_dict['DEV_KEY']
        
        print(type(ADMIN))
        
    except FileNotFoundError:
        print("File not found!")

DEV_KEY = ""
PID = ""
PPASS = ""
ADMIN = 0
MUSIC_VOLUME = 0.0
ENGuilds = []
CNGuilds = []
queque = {}
players = {}
prevMessage = ""
messageRepeat = 0

loadSet('config.json')