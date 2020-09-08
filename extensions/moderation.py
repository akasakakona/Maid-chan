import json



def modSet(modType, modData, modAction = None):
    with open('config.json') as f:
        config_dict = json.load(f)
    f.close()
    if(modAction is not None):
        if(modAction == "del"):
            config_dict[modType].pop(config_dict[modType].index(modData))
        else:
            config_dict[modType].append(modData)
    else:
        config_dict[modType] = modData
    with open('config.json', 'w') as json_file:
        json.dump(config_dict, json_file, indent = 1)
    json_file.close()