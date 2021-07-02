import time
import traceback

import requests

from config import PROXY, DEBUG_EEW_OVRD, DEBUG_EEW, DEBUG_EEW_IMAGE, DEBUG_EEW_IMAGE_OVRD
from modules.intensity import intensity2color
from modules.pswave import parse_swave
from modules.utilities import response_verify

return_dict = {}


def get_eew_info(app):
    global return_dict
    try:
        response_time = requests.get(url="http://www.kmoni.bosai.go.jp/webservice/server/pros/latest.json",
                                     proxies=PROXY, timeout=3.5)
        response_time.encoding = 'utf-8'
        if not response_verify(response_time):
            app.logger.warn("Failed to fetch EEW info (failed to get time).")
            return
        request_time = time.strptime(response_time.json()["latest_time"], "%Y/%m/%d %H:%M:%S")
        req_date = time.strftime("%Y%m%d", request_time)
        req_time = time.strftime("%Y%m%d%H%M%S", request_time)
        if DEBUG_EEW:
            time_offset = int(time.time()) - DEBUG_EEW_OVRD["origin_timestamp"]
            req_date = str(DEBUG_EEW_OVRD["start_time"])[:8]
            time_struct = time.strptime(str(DEBUG_EEW_OVRD["start_time"]), "%Y%m%d%H%M%S")
            req_timestamp = time.mktime(time_struct) + time_offset
            req_time_transformed = time.localtime(req_timestamp)
            req_time = time.strftime("%Y%m%d%H%M%S", req_time_transformed)
        response = requests.get(
            url=f"http://www.kmoni.bosai.go.jp/webservice/hypo/eew/{req_time}.json",
            proxies=PROXY, timeout=3.5)
        response.encoding = 'utf-8'
        if not response_verify(response):
            app.logger.warn(f"Failed to fetch EEW info (response code isn't 200). -> {response.status_code}")
            return
    except:
        app.logger.warn("Failed to fetch EEW info. Exception occurred: \n" + traceback.format_exc())
        return
    converted_response = response.json()
    if converted_response["result"]["message"] != "":
        # No EEW Available
        return_dict = {
            "status": -1
        }
    else:
        # EEW Available
        app.logger.info("EEW available. Parsing...")
        if converted_response["alertflg"] == "予報":
            report_flag = 0
        elif converted_response["alertflg"] == "警報":
            report_flag = 1
        else:
            report_flag = 2
        if converted_response["calcintensity"] in ["1", "2", "3", "4", "7"]:
            parsed_intensity = converted_response["calcintensity"]
        elif converted_response["calcintensity"] == "5強":
            parsed_intensity = "5+"
        elif converted_response["calcintensity"] == "5弱":
            parsed_intensity = "5-"
        elif converted_response["calcintensity"] == "6強":
            parsed_intensity = "6+"
        elif converted_response["calcintensity"] == "6弱":
            parsed_intensity = "6-"
        else:
            parsed_intensity = "0"
        intensities = {}
        try:
            if not DEBUG_EEW_IMAGE:
                response = requests.get(
                    url=f"http://www.kmoni.bosai.go.jp/data/map_img/EstShindoImg/eew/{req_date}/{req_time}.eew.gif",
                    proxies=PROXY, timeout=3.5)
                resp_raw = response.content
            else:
                with open(DEBUG_EEW_IMAGE_OVRD, "rb") as f:
                    resp_raw = f.read()
                    f.close()
            if not response_verify(response):
                app.logger.warn("Failed to fetch EEW image (response code isn't 200).")
            else:
                intensities = intensity2color(resp_raw)
        except:
            app.logger.warn("Failed to fetch EEW image. Exception occurred: \n" + traceback.format_exc())
        try:
            origin_time = time.strptime(converted_response["origin_time"], "%Y%m%d%H%M%S")
            origin_timestamp = float(time.mktime(origin_time))
            if DEBUG_EEW:
                origin_timestamp = DEBUG_EEW_OVRD["origin_timestamp"]
            depth = int(converted_response["depth"].replace("km", ""))
            s_wave_time = parse_swave(depth, float(
                time.time() + (3600 if not DEBUG_EEW else 0) - origin_timestamp))  # Japanese time
        except:
            app.logger.warn("Failed to get S wave time. Exception occurred: \n" + traceback.format_exc())
            s_wave_time = None
        return_dict = {
            "status": 0,
            "is_cancel": converted_response["is_cancel"],
            "is_test": converted_response["is_training"],
            "max_intensity": parsed_intensity,
            "report_time": converted_response["report_time"],
            "report_num": converted_response["report_num"],
            "report_flag": report_flag,
            "report_id": converted_response["report_id"],
            "is_final": converted_response["is_final"],
            "magnitude": converted_response["magunitude"],
            "hypocenter": {
                "name": converted_response["region_name"],
                "longitude": converted_response["longitude"],
                "latitude": converted_response["latitude"],
                "depth": converted_response["depth"]
            },
            "area_intensity": intensities,
            "s_wave": s_wave_time
        }
