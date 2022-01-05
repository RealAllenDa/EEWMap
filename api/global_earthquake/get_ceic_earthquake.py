"""
 EEWMap - API - GlobalEarthquake - CEIC
 Gets information from CEIC API.
"""
import json
import time
import traceback

from config import CURRENT_CONFIG
from modules.sdk import make_web_request

return_earthquake = []


def get_ceic_info(app):
    """
     Gets CEIC's latest earthquake telegram.

     :param app: The Flask app instance
    """
    if not CURRENT_CONFIG.DEBUG_CEIC_EARTHQUAKE:
        try:
            response = make_web_request(url=f"https://www.ceic.ac.cn/ajax/google?rand={time.time()}",
                                        proxies=CURRENT_CONFIG.PROXY, timeout=3.5, to_json=True, verify=False)
            if not response[0]:
                app.logger.warn(f"Failed to fetch CEIC data: {response[1]}.")
                return
        except Exception:
            app.logger.warn("Failed to fetch CEIC data. Exception occurred: \n" + traceback.format_exc())
            return
        parse_ceic_info(response[1], app)
    else:
        with open(CURRENT_CONFIG.DEBUG_P2P_OVRD["file"], "r", encoding="utf-8") as f:
            parse_ceic_info(json.loads(f.read()), app)


def parse_ceic_info(response, app):
    """
     Parses CEIC's latest earthquake telegram.

     :param response: The response dict
     :param app: The Flask app instance
    """
    global return_earthquake
    try:
        # Clear return_earthquake
        list_count = CURRENT_CONFIG.CEIC_LIST_COUNT * -1
        return_earthquake = []
        converted_response = response[list_count:]
        for i in reversed(converted_response):
            earthquake_temp = {
                "epicenter": {
                    "name": i["LOCATION_C"],
                    "depth": i["EPI_DEPTH"],
                    "latitude": float(i["EPI_LAT"]),
                    "longitude": float(i["EPI_LON"])
                },
                "magnitude": i["M"],
                "mmi": m_to_mmi(i["M"]),
                "occur_time": i["O_TIME"],
                "receive_time": i["SYNC_TIME"]
            }
            return_earthquake.append(earthquake_temp)
    except Exception:
        app.logger.error("Failed to parse CEIC data. Exception occurred: \n" + traceback.format_exc())


def m_to_mmi(m):
    """
    Converts Richter scale to Mercalli scale.

    :param m: Richter magnitude
    :return: Mercalli magnitude
    """
    m = float(m)
    if m < 3.5:
        return 1
    elif 3.5 <= m < 4.2:
        return 2
    elif 4.2 <= m < 4.5:
        return 3
    elif 4.5 <= m < 4.8:
        return 4
    elif 4.8 <= m < 5.4:
        return 5
    elif 5.4 <= m < 6.1:
        return 6
    elif 6.1 <= m < 6.5:
        return 7
    elif 6.5 <= m < 6.9:
        return 8
    elif 6.9 <= m < 7.3:
        return 9
    elif m >= 7.3:
        return 10
