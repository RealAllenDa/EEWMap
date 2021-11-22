"""
 EEWMap - API - P2P - Get_JSON
 Gets JSON from P2PQuake API, limited to:
    - 551 (Earthquake Information)
    - 552 (Tsunami Information)
"""
import json
import traceback

from config import PROXY, DEBUG_P2P_TSUNAMI, DEBUG_P2P_OVRD
from modules.sdk import make_web_request
from .parse_p2p_json import parse_p2p_info


def get_p2p_json(app):
    """
     Gets P2PQuake's JSON telegram.

     :param app: The Flask app instance
    """
    if not DEBUG_P2P_TSUNAMI:
        try:
            response = make_web_request(url="https://api.p2pquake.net/v2/history?codes=551&codes=552&limit=5",
                                        proxies=PROXY, timeout=3.5, to_json=True)
            if not response[0]:
                app.logger.warn(f"Failed to fetch P2P JSON data: {response[1]}.")
                return
        except:
            app.logger.warn("Failed to fetch P2P JSON data. Exception occurred: \n" + traceback.format_exc())
            return
        parse_p2p_info(response[1], app)
    else:
        with open(DEBUG_P2P_OVRD["file"], "r", encoding="utf-8") as f:
            parse_p2p_info(json.loads(f.read()), app)
