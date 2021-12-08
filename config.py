"""
 EEWMap - Config
 The configuration file for all modules.
"""
from modules.sdk import relpath

# Version
VERSION = "1.0.1-Build1 Release"

# Proxy Settings
PROXY = {
    "http": "127.0.0.1:7890",
    "https": "127.0.0.1:7890"
}

# Module enable
ENABLE_EEW = True
ENABLE_P2P_TSUNAMI = True
ENABLE_SHAKE = True
ENABLE_QUAKE = True

# Debugging
DEBUG_EEW = True
DEBUG_EEW_OVRD = {
    "start_time": 20210213230800,
    "origin_timestamp": 1638808716
}

DEBUG_EEW_IMAGE = True
DEBUG_EEW_IMAGE_OVRD = relpath("./tests/test_intensity_to_color.gif")

DEBUG_TSUNAMI = False
DEBUG_TSUNAMI_OVRD = {
    "file": relpath("./misc/demo/demo_tsunami.xml")
}

DEBUG_P2P_TSUNAMI = False
DEBUG_P2P_OVRD = {
    "file": relpath("./misc/demo/p2p_earthquake.json")
}

DEBUG_TSUNAMI_WATCH = False
DEBUG_TSUNAMI_WATCH_OVRD = relpath("./misc/demo/demo_watch.xml")
