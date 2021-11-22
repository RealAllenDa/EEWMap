"""
 EEWMap - Config
 The configuration file for all modules.
"""
from modules.sdk import relpath

# Version
VERSION = "1.0.1-Build1 Release"

# Proxy Settings
PROXY = {
    "http": "",
    "https": ""
}

# Module enable
ENABLE_EEW = True
ENABLE_P2P_TSUNAMI = True
ENABLE_SHAKE = True
ENABLE_QUAKE = True

# Debugging
DEBUG_EEW = False
DEBUG_EEW_OVRD = {
    "start_time": 20210501102730,
    "origin_timestamp": 1631790443
}

DEBUG_EEW_IMAGE = False
DEBUG_EEW_IMAGE_OVRD = relpath("./misc/demo/image.gif")

DEBUG_TSUNAMI = False
DEBUG_TSUNAMI_OVRD = {
    "file": relpath("./misc/demo/demo_tsunami.xml")
}

DEBUG_P2P_TSUNAMI = False
DEBUG_P2P_OVRD = {
    "file": relpath("./misc/demo/p2p_tsunami.json")
}

DEBUG_TSUNAMI_WATCH = False
DEBUG_TSUNAMI_WATCH_OVRD = relpath("./misc/demo/demo_watch.xml")
