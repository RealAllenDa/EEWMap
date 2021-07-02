# For people who need to set proxy
PROXY = {
    "http": "",
    "https": ""
}
# Debugging
ENABLE_EEW = True
ENABLE_P2P_TSUNAMI = True
ENABLE_SHAKE = True
ENABLE_QUAKE = True

DEBUG_EEW = False
DEBUG_EEW_OVRD = {
    "start_time": 20210501102730,
    "origin_timestamp": 1623483035
}

DEBUG_EEW_IMAGE = False
DEBUG_EEW_IMAGE_OVRD = "./misc/demo/image.gif"

DEBUG_TSUNAMI = False
DEBUG_TSUNAMI_OVRD = {
    "file": "./misc/demo/demo_tsunami.xml"
}

DEBUG_P2P_TSUNAMI = False
DEBUG_P2P_OVRD = {
    "file": "./misc/demo/p2p_tsunami.json"
}

DEBUG_TSUNAMI_WATCH = False
DEBUG_TSUNAMI_WATCH_OVRD = "./misc/demo/demo_watch.xml"
