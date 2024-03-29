"""
 EEWMap - Config
 The configuration file for all modules.
"""
import time

from modules.sdk import relpath

# Version
VERSION = "2.3 Release"


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
    DEBUG_WEB = False
    DEBUG_WEB_P2P_FILES = {
        "ScalePrompt": relpath("./debug/p2p/ScalePrompt.json"),
        "Destination": relpath("./debug/p2p/Destination.json"),
        "ScaleAndDestination": relpath("./debug/p2p/ScaleAndDestination.json"),
        "DetailScale": relpath("./debug/p2p/DetailScale.json"),
        "Foreign": relpath("./debug/p2p/Foreign.json")
    }

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

    DEBUG_SHAKE_LEVEL = False


class DevelopmentConfig(_BaseConfig):
    DEBUG_WEB = True
    ENABLE_UPDATING_CENTROID = False
    ENABLE_CORS = True


class ProductionConfig(_BaseConfig):
    pass


class TestingEEWConfig(DevelopmentConfig):
    DEBUG_EEW = True
    DEBUG_EEW_OVRD = {
        "start_time": 20220316233430,
        # "start_time": 20211209110520,
        # "start_time": 20210213230800,
        "origin_timestamp": int(time.time())
    }


class TestingSVIREEWConfig(DevelopmentConfig):
    DEBUG_EEW = True
    DEBUG_IGNORE_EEW_OUTDATE = True
    DEBUG_EEW_OVRD = {
        "start_time": 20211209110520,
        # "start_time": 20210213230800,
        "origin_timestamp": int(time.time())
    }


class TestingTsunamiConfig(DevelopmentConfig):
    DEBUG_TSUNAMI = True
    DEBUG_P2P_OVRD = {
        "file": relpath("./misc/demo/p2p_tsunami.json")
    }
    DEBUG_TSUNAMI_WATCH = True
    DEBUG_P2P_TSUNAMI = True


class TestingCEICConfig(DevelopmentConfig):
    CEIC_LIST_COUNT = 0


class TestingShakeLevelConfig(DevelopmentConfig):
    DEBUG_SHAKE_LEVEL = True


class TestingWebPageConfig(DevelopmentConfig):
    ENABLE_EEW = False
    ENABLE_P2P_TSUNAMI = False
    ENABLE_SHAKE = False
    ENABLE_QUAKE = False
    ENABLE_GLOBAL_EARTHQUAKE = False


CURRENT_CONFIG = ProductionConfig()
