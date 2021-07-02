import json
import traceback

import requests

from config import PROXY, DEBUG_P2P_TSUNAMI, DEBUG_P2P_OVRD
from modules.utilities import response_verify
from .parse_p2p_json import parse_p2p_info


def get_p2p_json(app):
    """
     Gets P2PQuake's JSON telegram.
     :param app: The Flask app instance.
    """
    if not DEBUG_P2P_TSUNAMI:
        try:
            response = requests.get(url="https://api.p2pquake.net/v2/history?codes=551&codes=552&limit=5",
                                    proxies=PROXY, timeout=3.5)
            response.encoding = "utf-8"
            if not response_verify(response):
                app.logger.warn("Failed to fetch P2P JSON data. (response code not 200)")
                return
        except:
            app.logger.warn("Failed to fetch P2P JSON data. Exception occurred: \n" + traceback.format_exc())
            return
        parse_p2p_info(response.json(), app)
    else:
        with open(DEBUG_P2P_OVRD["file"], "r", encoding="utf-8") as f:
            parse_p2p_info(json.loads(f.read()), app)
