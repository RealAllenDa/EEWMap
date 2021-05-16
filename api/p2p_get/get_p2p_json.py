import requests
from flask import current_app

from config import PROXY
from modules.utilities import response_verify
from .parse_p2p_json import parse_p2p_info

def get_p2p_json(app):
    """
     Gets P2PQuake's JSON telegram.
     :param app: The Flask app instance.
    """
    try:
        response = requests.get(url="https://api.p2pquake.net/v2/history?codes=551&codes=552&limit=5",
                                proxies=PROXY)
        response.encoding = "utf-8"
        if not response_verify(response):
            current_app.logger.warn("Failed to fetch P2P JSON data. (response code not 200)")
            return
    except:
        current_app.logger.warn("Failed to fetch P2P JSON data. (exception occurred)")
        return
    parse_p2p_info(response.json(), app)