"""
 EEWMap - API - Views
 ---------------------------
 The controller (blueprint) for APIs.
"""
from flask import Blueprint

api_bp = Blueprint("api", __name__, url_prefix="/api")


@api_bp.route("/shake_level")
def shake_level_get():
    """
    Gets the level of shaking.

    :return: status=-1 if failed, shake_level=... if success
    :rtype: dict
    """
    from .shake_level.get_shake_level import return_dict
    return return_dict


@api_bp.route("/earthquake_info")
def earthquake_info_get():
    """
    Gets the earthquake infos.

    :return: Earthquake info
    :rtype: dict
    """
    from .eew.get_eew import return_dict
    from .p2p_get.parse_p2p_json import return_list
    return {
        "info": return_list,
        "eew": return_dict
    }


@api_bp.route("/is_tsunami")
def check_if_tsunami_issued():
    """
    Check if the tsunami warning has been issued.

    :return: Issued=1, None=0
    """
    from .p2p_get.parse_p2p_json import tsunami_warning_in_effect
    return str(tsunami_warning_in_effect)


@api_bp.route("/tsunami_info")
def tsunami_info_get():
    """
    Gets the tsunami infos.

    :return: Tsunami info
    :rtype: dict
    """
    from .p2p_get.parse_p2p_json import tsunami_return
    from .tsunami.parse_jma_tsunami import return_dict
    from .p2p_get.parse_p2p_json import tsunami_warning_in_effect
    from .tsunami.parse_jma_watch import watch_return
    return {
        "status": tsunami_warning_in_effect,
        "map": tsunami_return,
        "info": return_dict,
        "watch": watch_return
    }
