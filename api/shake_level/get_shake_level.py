"""
 EEWMap - API - shake_level - Get_Shake
 Gets shake level, etc. from kmoni API.
"""
import traceback

from config import CURRENT_CONFIG
from model.shake_level import ReturnShakeLevelJSON, ShakeLevelJSON
from modules.sdk import make_web_request

return_shake_level = None


def get_shake_level(app):
    """
     Get the shaking level and green/yellow/red point count.

     :return: The status and the shaking level
     :rtype: dict
    """
    global return_shake_level
    try:
        response = make_web_request(url="http://kwatch-24h.net/EQLevel.json",
                                    timeout=3.5,
                                    proxies=CURRENT_CONFIG.PROXY,
                                    add_time=True,
                                    to_dataclass=ShakeLevelJSON)
        if not response[0]:
            app.logger.warn(f"Failed to fetch shake level: {response[1]}.")
            return
    except Exception:
        app.logger.warn("Failed to fetch shake level. Exception occurred: \n" + traceback.format_exc())
        return
    if CURRENT_CONFIG.DEBUG_SHAKE_LEVEL:
        import random
        return_shake_level = ReturnShakeLevelJSON(
            status=0,
            shake_level=random.randint(50, 8000),
            green=random.randint(100, 300),
            yellow=random.randint(100, 300),
            red=random.randint(100, 300)
        )
    else:
        return_shake_level = ReturnShakeLevelJSON(
            status=0,
            shake_level=response[1].l,
            green=response[1].g,
            yellow=response[1].y,
            red=response[1].r
        )
