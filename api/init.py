"""
 EEWMap - API - Init
 ---------------------------
 Initializes the APIs.
"""
import time
import traceback

from apscheduler.executors.pool import ThreadPoolExecutor
from apscheduler.jobstores.memory import MemoryJobStore
from apscheduler.schedulers.background import BackgroundScheduler

from config import ENABLE_P2P_TSUNAMI, ENABLE_EEW, ENABLE_SHAKE, ENABLE_QUAKE
from .eew import get_eew_info
from .p2p_get import get_p2p_json
from .shake_level import get_shake_level
from .tsunami import get_jma_tsunami


def refresh_p2p_info(app):
    """
    Refreshes the P2P JSON.
    """
    try:
        start_time = time.perf_counter()
        get_p2p_json(app)
        app.logger.debug(f"Refreshed P2P info in {(time.perf_counter() - start_time):.3f} seconds.")
    except:
        app.logger.error("Failed to refresh shaking level. \n" + traceback.format_exc())


def refresh_eew(app):
    """
    Refreshes the EEW.
    """
    try:
        start_time = time.perf_counter()
        get_eew_info(app)
        app.logger.debug(f"Refreshed EEW in {(time.perf_counter() - start_time):.3f} seconds.")
    except:
        app.logger.error("Failed to refresh shaking level. \n" + traceback.format_exc())


def refresh_shake_level(app):
    """
    Refreshes the Shaking Level.
    """
    try:
        start_time = time.perf_counter()
        get_shake_level(app)
        app.logger.debug(f"Refreshed shaking level in {(time.perf_counter() - start_time):.3f} seconds.")
    except:
        app.logger.error("Failed to refresh shaking level. \n" + traceback.format_exc())


def refresh_jma_tsunami(app):
    """
    Refreshes the JMA tsunami info.
    """
    try:
        start_time = time.perf_counter()
        get_jma_tsunami(app)
        app.logger.debug(f"Refreshed tsunami info in {(time.perf_counter() - start_time):.3f} seconds.")
    except:
        app.logger.error("Failed to refresh tsunami info. \n" + traceback.format_exc())


def initialize_api(app):
    """
    Initializes the APIs.
    """
    app.logger.debug("Initializing API Timers...")
    job_stores = {
        "default": MemoryJobStore()
    }
    executors = {
        "default": ThreadPoolExecutor(30)
    }
    job_defaults = {
        "coalesce": False,
        "max_instances": 5
    }
    scheduler = BackgroundScheduler(jobstores=job_stores, executors=executors,
                                    job_defaults=job_defaults)
    if ENABLE_QUAKE: scheduler.add_job(func=refresh_p2p_info, args=(app,), trigger="interval", seconds=2, id="p2p")
    if ENABLE_SHAKE: scheduler.add_job(func=refresh_shake_level, args=(app,), trigger="interval", seconds=2,
                                       id="shake_level")
    if ENABLE_EEW: scheduler.add_job(func=refresh_eew, args=(app,), trigger="interval", seconds=2, id="eew")
    if ENABLE_P2P_TSUNAMI: scheduler.add_job(func=refresh_jma_tsunami, args=(app,), trigger="interval", seconds=4,
                                             id="tsunami")
    scheduler.start()
    app.logger.debug("Successfully initialized API!")
