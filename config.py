"""
 EEWMap - Config
 The configuration file for all modules.
"""
import time

from modules.sdk import relpath

# Version
VERSION = "2.1.3 Release"


class _BaseConfig:
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
    ENABLE_UPDATING_CENTROID = True
    ENABLE_GLOBAL_EARTHQUAKE = True
    ENABLE_CORS = False

    # EEW Settings
    USE_SVIR_LEVEL = 5
    USE_SVIR_EEW = True

    # CEIC Settings
    CEIC_LIST_COUNT = 5

    # Debugging
    DEBUG_EEW = False
    DEBUG_EEW_OVRD = {
        "start_time": 20210213230800,
        "origin_timestamp": int(time.time())
    }

    DEBUG_IGNORE_EEW_OUTDATE = False

    DEBUG_SVIR_EEW = False
    DEBUG_SVIR_EEW_OVRD = relpath("./misc/svir_eew.json")

    DEBUG_IEDRED_EEW = False
    DEBUG_IEDRED_EEW_OVRD = None

    DEBUG_EEW_IMAGE = False
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

    DEBUG_CEIC_EARTHQUAKE = False
    DEBUG_CEIC_EARTHQUAKE_OVRD = None


class DevelopmentConfig(_BaseConfig):
    PROXY = {
        "http": "127.0.0.1:7890",
        "https": "127.0.0.1:7890"
    }
    ENABLE_UPDATING_CENTROID = False
    ENABLE_CORS = True


class ProductionConfig(_BaseConfig):
    pass


class TestingEEWConfig(DevelopmentConfig):
    DEBUG_EEW = True
    DEBUG_EEW_OVRD = {
        "start_time": 20211209110520,
        # "start_time": 20210213230800,
        "origin_timestamp": int(time.time())
    }


class TestingTsunamiConfig(DevelopmentConfig):
    DEBUG_TSUNAMI = True
    DEBUG_TSUNAMI_WATCH = True
    DEBUG_P2P_TSUNAMI = True


class TestingCEICConfig(DevelopmentConfig):
    CEIC_LIST_COUNT = 0


CURRENT_CONFIG = TestingEEWConfig()
