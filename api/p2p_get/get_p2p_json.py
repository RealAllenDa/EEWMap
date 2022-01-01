"""
 EEWMap - API - P2P - Get_JSON
 Gets JSON from P2PQuake API, limited to:
    - 551 (Earthquake Information)
    - 552 (Tsunami Information)
"""
import json
import traceback

from config import CURRENT_CONFIG
from modules.sdk import make_web_request
from .parse_p2p_json import parse_p2p_info


def get_p2p_json(app):
    parse_p2p_info(_get_p2p_telegram(app), app)


def _get_p2p_telegram(app, limit=5):
    """
     Gets P2PQuake's JSON telegram.

     :param app: The Flask app instance
    """
    if not CURRENT_CONFIG.DEBUG_P2P_TSUNAMI:
        try:
            response = make_web_request(url=f"https://api.p2pquake.net/v2/history?codes=551&codes=552&limit={limit}",
                                        proxies=CURRENT_CONFIG.PROXY, timeout=3.5, to_json=True)
            if not response[0]:
                app.logger.warn(f"Failed to fetch P2P JSON data: {response[1]}.")
                return
        except Exception:
            app.logger.warn("Failed to fetch P2P JSON data. Exception occurred: \n" + traceback.format_exc())
            return
        return response[1]
    else:
        with open(CURRENT_CONFIG.DEBUG_P2P_OVRD["file"], "r", encoding="utf-8") as f:
            return json.loads(f.read())
