"""
 EEWMap - API - shake_level - Get_Shake
 Gets shake level, etc. from kmoni API.
"""
import time
import traceback

from config import PROXY
from modules.sdk import make_web_request

return_dict = {}


def get_shake_level(app):
    """
     Get the shaking level and green/yellow/red point count.

     :return: The status and the shaking level
     :rtype: dict
    """
    global return_dict
    try:
        response = make_web_request(url="http://kwatch-24h.net/EQLevel.json?" + str(int(time.time())),
                                timeout=3.5, proxies=PROXY, to_json=True)
        if not response[0]:
            app.logger.warn(f"Failed to fetch shake level: {response[1]}.")
            return
    except:
        app.logger.warn("Failed to fetch shake level. Exception occurred: \n" + traceback.format_exc())
        return
    return_dict = {
        "status": 0,
        "shake_level": response[1]["l"],
        "green": response[1]["g"],
        "yellow": response[1]["y"],
        "red": response[1]["r"]
    }
