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