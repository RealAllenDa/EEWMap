import traceback

import requests
import time
from modules.utilities import response_verify
from config import PROXY

return_dict = {}
def get_shake_level(app):
    """
     Get the shaking level.

     :return: The status and the shaking level.
     :rtype: dict
    """
    global return_dict
    try:
        response = requests.get(url="http://kwatch-24h.net/EQLevel.json?" + str(int(time.time())),
                                timeout=3.5, proxies=PROXY)
        response.encoding = 'utf-8'
        if not response_verify(response):
            app.logger.warn("Failed to fetch shake level (response code != 200).")
            return
    except:
        app.logger.warn("Failed to fetch shake level. Exception occurred: \n" + traceback.format_exc())
        return
    return_dict = {
        "status": 0,
        "shake_level": response.json()["l"],
        "green": response.json()["g"],
        "yellow": response.json()["y"],
        "red": response.json()["r"]
    }

