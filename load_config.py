import os
import json
import useful
CONFIG_DIRECTORY = "config"
LIST_OF_SECTIONS = os.listdir(CONFIG_DIRECTORY)

def loadConfigFiles():
    conf = {}
    try:
        for section in LIST_OF_SECTIONS:
            path = "{}/{}".format(CONFIG_DIRECTORY, section)
            name, _ = os.path.splitext(section)
            with open(path, "r") as f:
                data = f.read()
                data = json.loads(data)
                conf.update({name: data})
    except Exception as e:
        useful.error("Config loading filed.", e)
    return conf