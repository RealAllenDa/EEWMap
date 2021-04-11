import time
import traceback

import requests

from assets.area.area_define import fetch_intensity_report_json
from assets.centroid.centroid_define import fetch_area_centroid
from assets.config import proxies
from assets.earthquake_info import response_verify

def get_eew_info():
    """
     Get EEW information.
     Result: 0 - Success
             1 - No EEW
             -1 - Failed
    """
    try:
        response = requests.get(url="https://api.iedred7584.com/eew/json/",
                                     proxies=proxies)
        response.encoding = 'utf-8'
        if not response_verify(response):
            return get_degraded_eew_info()
    except:
        traceback.print_exc()
        return get_degraded_eew_info()
    converted_response = response.json()
    is_final = False
    if converted_response["ParseStatus"] == "Error":
        return get_degraded_eew_info()
    if converted_response["Type"]["Code"] != 0:
        is_final = True
        # Outdated report
        if int(time.time()) - converted_response["AnnouncedTime"]["UnixTime"] >= 180:
            # >= 1min
            return {
                "status": 1
            }
    if converted_response["Title"]["String"] == "緊急地震速報（警報）":
        report_flag = 4
    else:
        report_flag = 3
    if converted_response["Status"]["String"] != "通常":
        is_train = True
    else:
        is_train = False
    report_time = converted_response["AnnouncedTime"]["String"]
    if converted_response["Type"]["String"] != "発表":
        return {
            "status": 0,
            "is_degraded": False,
            "is_cancel": True
        }
    hypocenter_info = {
        "name": converted_response["Hypocenter"]["Name"],
        "longitude": converted_response["Hypocenter"]["Location"]["Long"],
        "latitude": converted_response["Hypocenter"]["Location"]["Lat"],
        "depth": str(converted_response["Hypocenter"]["Location"]["Depth"]["Int"]) + "km"
    }
    report_num = converted_response["Serial"]
    magnitude = converted_response["Hypocenter"]["Magnitude"]["Float"]
    max_intensity = converted_response["MaxIntensity"]["From"]
    if report_flag == 4:
        area_intensity = {}
        to_fetch_area_color = []
        for i in converted_response["Forecast"]:
            if i["Intensity"]["From"] in ["1", "2", "3", "4", "7"]:
                area_intensity[str(i["Intensity"]["Code"])] = {
                    "name": i["Intensity"]["Name"],
                    "intensity": i["Intensity"]["From"]
                }
            elif i["Intensity"]["From"] == "5強":
                area_intensity[str(i["Intensity"]["Code"])] = {
                    "name": i["Intensity"]["Name"],
                    "intensity": "5+"
                }
            elif i["Intensity"]["From"] == "5弱":
                area_intensity[str(i["Intensity"]["Code"])] = {
                    "name": i["Intensity"]["Name"],
                    "intensity": "5-"
                }
            elif i["Intensity"]["From"] == "6強":
                area_intensity[str(i["Intensity"]["Code"])] = {
                    "name": i["Intensity"]["Name"],
                    "intensity": "6+"
                }
            elif i["Intensity"]["From"] == "6弱":
                area_intensity[str(i["Intensity"]["Code"])] = {
                    "name": i["Intensity"]["Name"],
                    "intensity": "6-"
                }
            area_intensity[str(i["Intensity"]["Code"])]["latitude"] = fetch_area_centroid()[str(i["Intensity"]["Code"])][0]
            area_intensity[str(i["Intensity"]["Code"])]["longitude"] = fetch_area_centroid()[str(i["Intensity"]["Code"])][1]
            to_fetch_area_color.append(str(i["Intensity"]["Code"]))
        geojson = fetch_intensity_report_json(to_fetch_area_color, area_intensity)
    else:
        area_intensity = {}
        geojson = {}
    return {
        "status": 0,
        "is_degraded": False,
        "is_cancel": False,
        "is_test": is_train,
        "last_time": int(time.time()) - converted_response["AnnouncedTime"]["UnixTime"],
        "max_intensity": max_intensity,
        "report_time": report_time,
        "report_num": report_num,
        "report_flag": report_flag,
        "is_final": is_final,
        "magnitude": magnitude,
        "hypocenter": hypocenter_info,
        "area_intensity": {
            "intensity": area_intensity,
            "geojson": geojson
        }
    }
def get_degraded_eew_info():
    try:
        response_time = requests.get(url="http://www.kmoni.bosai.go.jp/webservice/server/pros/latest.json",
                                     proxies=proxies)
        response_time.encoding = 'utf-8'
        if not response_verify(response_time):
            return {"status": -1}
        request_time = time.strptime(response_time.json()["latest_time"], "%Y/%m/%d %H:%M:%S")
        req_timestamp = int(time.mktime(request_time))
        response = requests.get(url="http://www.kmoni.bosai.go.jp/webservice/hypo/eew/{}.json".format(req_timestamp))
        response.encoding = 'utf-8'
        if not response_verify(response):
            return {"status": -1}
    except:
        return {"status": -1}
    converted_response = response.json()
    if converted_response["result"]["message"] != "":
        # No EEW Available
        return {"status": 1}
    else:
        # EEW Available
        if converted_response["alertflg"] == "予報":
            report_flag = 3
        else:
            report_flag = 4
        return {
            "status": 0,
            "is_degraded": True,
            "is_cancel": converted_response["is_cancel"],
            "is_test": converted_response["is_training"],
            "max_intensity": int(converted_response["calcintensity"]),
            "last_time": 0,
            "report_time": converted_response["report_time"],
            "report_num": converted_response["report_num"],
            "report_flag": report_flag,
            "is_final": converted_response["is_final"],
            "magnitude": converted_response["magunitude"],
            "hypocenter": {
                "name": converted_response["region_name"],
                "longitude": converted_response["longitude"],
                "latitude": converted_response["latitude"],
                "depth": converted_response["depth"]
            },
            "area_intensity": {}
        }