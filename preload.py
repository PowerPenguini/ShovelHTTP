import os
import json
import useful
import load_config

CACHE_CONFIG_PATH = "cache/cache_files.json"
PUBLIC_WWW_DIR = load_config.loadConfigFiles()["location"]["FILES_LOCATION"]


def loadPreloadLits():
    try:
        preload_list = []
        with open(CACHE_CONFIG_PATH) as f:
            data = f.read()
            data = json.loads(data)
            for pre_file in data["PRELOAD_FILES"]:
                preload_list.append(pre_file)
        return preload_list
    except Exception as e:
        useful.error("Preload filed.", e)


def getPreloadFiles(file_list):
    try:
        preload_dict = {}
        for pre_file in file_list:
            path = "{}/{}".format(PUBLIC_WWW_DIR, pre_file)
            with open(path, "rb") as f:
                data = f.read()
                preload_dict.update({pre_file: data})
        return preload_dict
    except Exception as e:
        useful.error("Preload filed.", e)