"""
 EEWMap - API - Init
 Initializes the APIs (Initializes timers to refresh).
"""
import time
import traceback
from apscheduler.executors.pool import ThreadPoolExecutor
from apscheduler.jobstores.memory import MemoryJobStore
from apscheduler.schedulers.background import BackgroundScheduler

from config import CURRENT_CONFIG
from .eew import get_eew_info
from .eew.get_svir_eew import get_svir_iedred_eew_info
from .p2p_get import get_p2p_json
from .shake_level import get_shake_level
from .tsunami import get_jma_tsunami


def refresh_p2p_info(app):
    """
    Refreshes the P2P JSON.

    :param app: The Flask app instance
    """
    try:
        start_time = time.perf_counter()
        get_p2p_json(app)
        app.logger.debug(f"Refreshed P2P info in {(time.perf_counter() - start_time):.3f} seconds.")
    except Exception:
        app.logger.error("Failed to refresh P2P info. \n" + traceback.format_exc())


def refresh_eew(app):
    """
    Refreshes the EEW.

    :param app: The Flask app instance
    """
    try:
        start_time = time.perf_counter()
        get_eew_info(app)
        app.logger.debug(f"Refreshed EEW in {(time.perf_counter() - start_time):.3f} seconds.")
    except Exception:
        app.logger.error("Failed to refresh EEW. \n" + traceback.format_exc())


def refresh_svir_eew(app):
    """
    Refreshes the SVIR EEW.

    :param app: The Flask app instance
    """
    try:
        start_time = time.perf_counter()
        get_svir_iedred_eew_info(app)
        app.logger.debug(f"Refreshed SVIR EEW in {(time.perf_counter() - start_time):.3f} seconds.")
    except Exception:
        app.logger.error("Failed to refresh SVIR EEW. \n" + traceback.format_exc())


def refresh_shake_level(app):
    """
    Refreshes the Shaking Level.

    :param app: The Flask app instance
    """
    try:
        start_time = time.perf_counter()
        get_shake_level(app)
        app.logger.debug(f"Refreshed shaking level in {(time.perf_counter() - start_time):.3f} seconds.")
    except Exception:
        app.logger.error("Failed to refresh shaking level. \n" + traceback.format_exc())


def refresh_jma_tsunami(app):
    """
    Refreshes the JMA tsunami info.

    :param app: The Flask app instance
    """
    try:
        start_time = time.perf_counter()
        get_jma_tsunami(app)
        app.logger.debug(f"Refreshed tsunami info in {(time.perf_counter() - start_time):.3f} seconds.")
    except Exception:
        app.logger.error("Failed to refresh tsunami info. \n" + traceback.format_exc())


def refresh_stations(app):
    """
    Refreshes the intensity station properties.

    :param app: The Flask app instance
    """
    try:
        from modules.centroid import centroid_instance
        start_time = time.perf_counter()
        centroid_instance.refresh_stations()
        app.logger.debug(f"Refreshed station info in {(time.perf_counter() - start_time):.3f} seconds.")
    except Exception:
        app.logger.error("Failed to refresh station info. \n" + traceback.format_exc())


def init_api(app):
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
    if CURRENT_CONFIG.ENABLE_QUAKE:
        scheduler.add_job(func=refresh_p2p_info, args=(app,), trigger="interval", seconds=2, id="p2p")
        scheduler.add_job(func=refresh_stations, args=(app,), trigger="interval", days=1, id="station_update")
    if CURRENT_CONFIG.ENABLE_SHAKE:
        scheduler.add_job(func=refresh_shake_level, args=(app,), trigger="interval",
                          seconds=2,
                          id="shake_level")
    if CURRENT_CONFIG.ENABLE_EEW:
        scheduler.add_job(func=refresh_eew, args=(app,), trigger="interval", seconds=2,
                          id="eew")
        scheduler.add_job(func=refresh_svir_eew, args=(app,), trigger="interval", seconds=2,
                          id="svir_eew")
    if CURRENT_CONFIG.ENABLE_P2P_TSUNAMI:
        scheduler.add_job(func=refresh_jma_tsunami, args=(app,), trigger="interval",
                          seconds=4,
                          id="tsunami")
    scheduler.start()
    app.logger.debug("Successfully initialized API!")
