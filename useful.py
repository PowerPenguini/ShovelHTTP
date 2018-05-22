"""
useful - a few useful Python functions.
Python 2.7 module created just to be useful.
"""


import os
import sys
import ConfigParser

def non():
    """Do nothing - placeholder"""
    pass

DEBUG = True
ERROR_ENABLE = True
ALERT_ENABLE = True
SUCCESS_ENABLE = True
EXIT_ON_ERROR = False
ERROR_FUNC = non
ALERT_FUNC = non
SUCCESS_FUNC = non
UNKNOWN_ERR = "Unknown error"

def error(msg, err_ret=UNKNOWN_ERR):
    """
    Returns message to stderr.
    Uage:
        error(msg)
    or ----------------------------------------
        error(msg, err_ret="my_own_error")
    """
    if not ERROR_ENABLE or not DEBUG:
        return
    msg = str(msg)
    err_ret = str(err_ret)
    err = "[-] {} - {} \n".format(msg, err_ret)
    sys.stderr.write(err)
    if ERROR_FUNC != non:
        ERROR_FUNC()
    if EXIT_ON_ERROR:
        sys.exit()

def alert(msg):
    """
    Returns message to stdout.
    Uage:
        alert(msg)
    """
    if not ALERT_ENABLE or not DEBUG:
        return
    msg = str(msg)
    alrt = "[*] {} \n".format(msg)
    sys.stdout.write(alrt)
    if ALERT_FUNC != non:
        ALERT_FUNC()

def succ(msg):
    """
    Returns message to stdout.
    Uage:
        alert(msg)
    """
    if not ALERT_ENABLE or not DEBUG:
        return
    msg = str(msg)
    alrt = "[+] {} \n".format(msg)
    sys.stdout.write(alrt)
    if ALERT_FUNC != non:
        ALERT_FUNC()

def clear():
    """
    Clear terminal.
    Usage:
        clear()
    """
    system = sys.platform.lower()
    if "linux" in system or "darwin" in system:
        os.system("clear")
    elif "win" in system:
        os.system("cls")
    else:
        os.system("clear")

def parse_conf(cfg):
    """
    Parse each section to global variable in useful as dictionary.
    Usage:
        parse_conf(file)
	print useful.MyConfigSection
    """
    if not os.path.isfile(cfg):
        error("Config file loading filed.")
    try:
        config = ConfigParser.ConfigParser()
        config.read(cfg)
        secs = config.sections()
        for sec in secs:
            globals()[sec] = dict()
            opts = config.options(sec)
            for opt in opts:
                val = config.get(sec, opt)
                globals()[sec].update({opt: val})
        succ("Config parsing succeed.")
    except Exception as msg:
        error("Configuration file parsing filed.", msg)