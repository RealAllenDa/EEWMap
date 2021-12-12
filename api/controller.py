"""
 EEWMap - API - Views
 The controller (blueprint) for APIs.
"""
import json

from flask import Blueprint, abort

from modules.sdk import relpath

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


def use_svir_or_kmoni(return_dict, return_dict_svir):
    """
    Determines whether to use kmoni eew or svir eew.
    :param return_dict: Kmoni eew
    :param return_dict_svir: Svir eew
    :return: Only an eew
    :rtype: dict
    """
    svir_on = return_dict_svir.get("status", -1) != -1
    kmoni_on = return_dict.get("status", -1) != -1
    if (not svir_on) and (not kmoni_on):
        return {}
    elif (not svir_on) and kmoni_on:
        return return_dict
    elif svir_on and (not kmoni_on):
        return return_dict_svir
    elif svir_on and kmoni_on:
        try:
            if int(return_dict_svir["hypocenter"]["depth"][:-2]) >= 150:
                return return_dict_svir
            else:
                return return_dict_svir if return_dict_svir["report_flag"] == 1 else return_dict
        except Exception:
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
    from .eew.get_svir_eew import return_dict_svir
    return {
        "info": return_list,
        "eew": use_svir_or_kmoni(return_dict, return_dict_svir)
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
    from .tsunami.parse_jma_tsunami import return_dict, tsunami_watch_in_effect
    from .p2p_get.parse_p2p_json import tsunami_warning_in_effect
    from .tsunami.parse_jma_watch import watch_return
    return {
        "status": tsunami_warning_in_effect,
        "status_forecast": tsunami_watch_in_effect,
        "map": tsunami_return,
        "info": return_dict,
        "watch": watch_return
    }


@api_bp.route("/web/index_nav")
def index_arrangement():
    """
    Returns the index items list.

    :return: Index items JSON
    :rtype: dict
    """
    # Open file dynamically so it can be updated realtime.
    try:
        with open(relpath("../modules/web/index.json"), "r") as f:
            content = json.loads(f.read())
            f.close()
        return content
    except Exception:
        abort(500)
