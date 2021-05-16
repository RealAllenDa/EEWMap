"""
 EEWMap - API - Init
 ---------------------------
 Initializes the APIs.
"""
import time
from threading import Timer

from .eew.get_eew import get_eew_info
from .p2p_get import get_p2p_json
from .shake_level import get_shake_level

TIMERS = {}

def refresh_p2p_info(app):
    """
    Refreshes the P2P JSON.
    """
    app.logger.debug("Refreshing P2P info...")
    start_time = time.perf_counter()
    get_p2p_json(app)
    app.logger.debug("Refreshed P2P info in {:.3f} seconds.".format(time.perf_counter() - start_time))
    # Recursion
    TIMERS["p2p"] = Timer(3, refresh_p2p_info, args=(app,))
    TIMERS["p2p"].start()

def refresh_eew(app):
    """
    Refreshes the EEW.
    """
    app.logger.debug("Refreshing EEW...")
    start_time = time.perf_counter()
    get_eew_info(app)
    app.logger.debug("Refreshed EEW in {:.3f} seconds.".format(time.perf_counter() - start_time))
    # Recursion
    TIMERS["eew"] = Timer(3, refresh_eew, args=(app,))
    TIMERS["eew"].start()

def refresh_shake_level(app):
    """
    Refreshes the Shaking Level.
    """
    app.logger.debug("Refreshing shaking level...")
    start_time = time.perf_counter()
    get_shake_level(app)
    app.logger.debug("Refreshed shaking level in {:.3f} seconds.".format(time.perf_counter() - start_time))
    # Recursion
    TIMERS["shake_level"] = Timer(3, refresh_shake_level, args=(app,))
    TIMERS["shake_level"].start()

def initialize_api(app):
    """
    Initializes the APIs.
    """
    global TIMERS
    app.logger.debug("Initializing API Timers...")
    TIMERS["p2p"] = Timer(3, refresh_p2p_info, args=(app,))
    TIMERS["p2p"].start()
    TIMERS["shake_level"] = Timer(3, refresh_shake_level, args=(app,))
    TIMERS["shake_level"].start()
    TIMERS["eew"] = Timer(3, refresh_eew, args=(app,))
    TIMERS["eew"].start()
    app.logger.debug("Successfully initialized API!")