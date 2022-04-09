"""
 EEWMap - Debug - Views
 The main view controller for debugging.
"""
import time
from functools import wraps

from flask import render_template, Blueprint

from config import CURRENT_CONFIG

debug_bp = Blueprint("debug", __name__, template_folder="templates", url_prefix="/debug")


def debug_error():
    return "Debugging not enabled"


def check_debug(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if CURRENT_CONFIG.DEBUG_WEB:
            return func(*args, **kwargs)
        else:
            return debug_error()

    return wrapper


@debug_bp.route("/index")
@check_debug
def debug_index():
    """
    Returns debug page.
    :return: Debug page
    """
    return render_template("debug_index.html")


@debug_bp.route("/p2p/send_message/<info_type>")
@check_debug
def debug_p2p_send_info(info_type):
    """
    Gives out p2p information.
    :return: None
    """
    CURRENT_CONFIG.DEBUG_P2P_TSUNAMI = True
    info = CURRENT_CONFIG.DEBUG_WEB_P2P_FILES.get(info_type, "Unknown")
    if info == "Unknown":
        return "Unknown type"
    else:
        CURRENT_CONFIG.DEBUG_P2P_OVRD["file"] = info
        return "OK"


@debug_bp.route("/p2p/enable")
@check_debug
def debug_p2p_enable():
    """
    Gives out p2p information.
    :return: None
    """
    CURRENT_CONFIG.DEBUG_P2P_TSUNAMI = True
    return "OK"


@debug_bp.route("/p2p/disable")
@check_debug
def debug_p2p_disable():
    """
    Gives out p2p information.
    :return: None
    """
    CURRENT_CONFIG.DEBUG_P2P_TSUNAMI = False
    return "OK"


@debug_bp.route("/p2p/status")
@check_debug
def debug_p2p_status():
    """
    Gives out p2p information.
    :return: None
    """
    return str(CURRENT_CONFIG.DEBUG_P2P_TSUNAMI)


@debug_bp.route("/eew/set_time/<eew_time>")
@check_debug
def debug_eew_set_time(eew_time):
    """
    Sets eew time.
    :param eew_time: EEW time to be set.
    """
    try:
        _ = time.strptime(eew_time, "%Y%m%d%H%M%S")
    except ValueError:
        return "Time format incorrect"
    except Exception as e:
        return f"Unknown error: {e}"
    CURRENT_CONFIG.DEBUG_EEW_OVRD["start_time"] = eew_time
    return "OK"


@debug_bp.route("/eew/start")
@check_debug
def debug_eew_start():
    """
    Starts EEW.
    """
    CURRENT_CONFIG.DEBUG_EEW = True
    CURRENT_CONFIG.DEBUG_EEW_OVRD["origin_timestamp"] = int(time.time())
    return "OK"


@debug_bp.route("/eew/end")
@check_debug
def debug_eew_end():
    """
    Ends EEW.
    """
    CURRENT_CONFIG.DEBUG_EEW = False
    return "OK"


@debug_bp.route("/eew/status")
@check_debug
def debug_eew_status():
    """
    Returns EEW Status.
    """
    return str(CURRENT_CONFIG.DEBUG_EEW)
