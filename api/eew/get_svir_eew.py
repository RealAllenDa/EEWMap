import json
import time
import traceback

from config import CURRENT_CONFIG
from modules.pswave import parse_pswave
from modules.sdk import make_web_request

return_dict_svir = {}

INTENSITY_TRANSFORM_DICT = {
    "1": "1",
    "2": "2",
    "3": "3",
    "4": "4",
    "5-": "5弱",
    "5+": "5強",
    "6-": "6弱",
    "6+": "6強",
    "7": "7",
    "不明": "0"
}


def get_svir_iedred_eew_info(app):
    if CURRENT_CONFIG.USE_SVIR_EEW:
        get_svir_eew_info(app)
    else:
        get_iedred_eew_info(app)


def get_iedred_eew_info(app):
    try:
        if not CURRENT_CONFIG.DEBUG_IEDRED_EEW:
            response = make_web_request(url="https://api.iedred7584.com/eew/json/",
                                        proxies=CURRENT_CONFIG.PROXY, to_json=True)
            if not response[0]:
                app.logger.warn("Failed to fetch EEW info (failed to get iedred json).")
            converted_response = response[1]
        else:
            with open(CURRENT_CONFIG.DEBUG_IEDRED_EEW_OVRD, "r", encoding="utf-8") as f:
                converted_response = json.loads(f.read())
                f.close()
        parse_iedred_eew_info(app, converted_response)
    except Exception:
        app.logger.warn("Failed to fetch EEW info. Exception occurred: \n" + traceback.format_exc())
        return


def get_svir_eew_info(app):
    try:
        if not CURRENT_CONFIG.DEBUG_SVIR_EEW:
            response = make_web_request(url="https://svir.jp/eew/data.json",
                                        proxies=CURRENT_CONFIG.PROXY, to_json=True)
            if not response[0]:
                app.logger.warn("Failed to fetch EEW info (failed to get svir json).")
                return
            converted_response = response[1]
        else:
            with open(CURRENT_CONFIG.DEBUG_SVIR_EEW_OVRD, "r", encoding="utf-8") as f:
                converted_response = json.loads(f.read())
                f.close()
        parse_iedred_eew_info(app, transform_svir_to_iedred(converted_response))
    except Exception:
        app.logger.warn("Failed to fetch EEW info. Exception occurred: \n" + traceback.format_exc())
        return


# noinspection PyTypeChecker
def transform_svir_to_iedred(content):
    return_content = {
        "ParseStatus": "Success",
        "Status": {
            "String": ""
        },
        "AnnouncedTime": {
            "String": "",
            "UnixTime": -1
        },
        "OriginTime": {
            "String": "",
            "UnixTime": -1
        },
        "EventID": "",
        "Type": {
            "Code": -1,
            "String": ""
        },
        "Serial": -1,
        "Hypocenter": {
            "Code": -1,
            "Name": "",
            "isAssumption": -1,
            "Location": {
                "Lat": -1,
                "Long": -1,
                "Depth": {
                    "Int": -1
                }
            },
            "Magnitude": {
                "Float": -1
            }
        },
        "MaxIntensity": {
            "From": -1
        },
        "Warn": False
    }

    if content["Head"]["Title"] != "緊急地震速報（予報）":
        return_content = {
            "ParseStatus": "Error"
        }
        return return_content

    return_content["Status"]["String"] = content["Head"]["Status"]

    # AnnouncedTime Parsing
    announced_time = time.strptime(content["Head"]["DateTime"][:19], "%Y-%m-%dT%H:%M:%S")
    return_content["AnnouncedTime"]["String"] = time.strftime("%Y/%m/%d %H:%M:%S", announced_time)
    return_content["AnnouncedTime"]["UnixTime"] = int(time.mktime(announced_time))

    # OriginTime Parsing
    origin_time = time.strptime(content["Body"]["Earthquake"]["OriginTime"][:19], "%Y-%m-%dT%H:%M:%S")
    return_content["OriginTime"]["String"] = time.strftime("%Y/%m/%d %H:%M:%S", origin_time)
    return_content["OriginTime"]["UnixTime"] = int(time.mktime(origin_time))

    return_content["EventID"] = content["Head"]["EventID"]

    if content["Body"]["EndFlag"] == "1":
        return_content["Type"]["Code"] = 9  # Final EEW
    else:
        return_content["Type"]["Code"] = 0  # Not Final EEW
    if content["Head"]["Status"] == "取消":
        return_content["Type"]["String"] = "取消"
        return return_content
    else:
        return_content["Type"]["String"] = "発表"

    return_content["Serial"] = content["Head"]["Serial"]

    magnitude = content["Body"]["Earthquake"]["Magnitude"]
    return_content["Hypocenter"] = {
        "Code": content["Body"]["Earthquake"]["Hypocenter"]["Code"],
        "Name": content["Body"]["Earthquake"]["Hypocenter"]["Name"],
        "isAssumption": content["Body"]["PLUMFlag"] == "1",
        "Location": {
            "Lat": content["Body"]["Earthquake"]["Hypocenter"]["Lat"],
            "Long": content["Body"]["Earthquake"]["Hypocenter"]["Lon"],
            "Depth": {
                "Int": int(content["Body"]["Earthquake"]["Hypocenter"]["Depth"])
            }
        },
        "Magnitude": {
            "Float": float(magnitude) if magnitude != "/./" else "Unknown"
        }
    }

    return_content["MaxIntensity"]["From"] = content["Body"]["Intensity"]["MaxInt"]
    return_content["Warn"] = (content["Body"]["WarningFlag"] == "1")

    if return_content["Warn"]:
        return_content["Forecast"] = []
        for i in content["Body"]["Intensity"]["Areas"]:
            arrival_time = {}
            if i["Kind"]["Code"][1] == "9":
                arrival_time = {
                    "Flag": False,
                    "Condition": "PLUM",
                    "Time": "Unknown"
                }
            elif i["Kind"]["Code"][1] == "0":
                arrival_time = {
                    "Flag": False,
                    "Condition": i.get("Condition", "未到達と推測"),
                    "Time": i.get("ArrivalTime", "00:00:00")
                }
            return_content["Forecast"].append({
                "Intensity": {
                    "Code": i["Code"],
                    "Name": i["Name"],
                    "From": INTENSITY_TRANSFORM_DICT.get(i["ForecastInt"]["From"], "0"),
                    "To": INTENSITY_TRANSFORM_DICT.get(i["ForecastInt"]["To"], "0"),
                    "Description": i["TextInt"]
                },
                "Warn": (i["Kind"]["Code"][0] == "1"),
                "Arrival": arrival_time
            })

    return return_content


def parse_iedred_eew_info(app, converted_response):
    """
     Gets EEW information from svir.
    """
    global return_dict_svir

    if converted_response["ParseStatus"] == "Error":
        app.logger.warn("Failed to fetch EEW info (parse status is error).")
        return

    is_final = False
    if converted_response["Type"]["Code"] != 0:
        is_final = True

    if is_final:
        timespan = int(time.time()) + 3600 - converted_response["AnnouncedTime"]["UnixTime"]  # China time
        # Outdated report
        if not (-12 < timespan < 180):
            # >= 1min
            if not CURRENT_CONFIG.DEBUG_IGNORE_EEW_OUTDATE:
                return_dict_svir = {
                    "status": -1
                }
                return

    if converted_response["Type"]["String"] != "発表":
        return_dict_svir = {
            "status": 0,
            "is_cancel": True
        }
        return

    if converted_response["Warn"]:
        report_flag = 1
    else:
        report_flag = 0

    if converted_response["Status"]["String"] != "通常":
        is_test = True
    else:
        is_test = False

    if report_flag == 1:
        area_intensity = {}
        from modules.centroid import centroid_instance
        for i in converted_response["Forecast"]:
            if i["Intensity"]["From"] in ["1", "2", "3", "4", "7"]:
                area_intensity[str(i["Intensity"]["Name"])] = {
                    "name": i["Intensity"]["Name"],
                    "intensity": i["Intensity"]["From"],
                    "is_area": True
                }
            elif i["Intensity"]["From"] == "5強":
                area_intensity[str(i["Intensity"]["Name"])] = {
                    "name": i["Intensity"]["Name"],
                    "intensity": "5+",
                    "is_area": True
                }
            elif i["Intensity"]["From"] == "5弱":
                area_intensity[str(i["Intensity"]["Name"])] = {
                    "name": i["Intensity"]["Name"],
                    "intensity": "5-",
                    "is_area": True
                }
            elif i["Intensity"]["From"] == "6強":
                area_intensity[str(i["Intensity"]["Name"])] = {
                    "name": i["Intensity"]["Name"],
                    "intensity": "6+",
                    "is_area": True
                }
            elif i["Intensity"]["From"] == "6弱":
                area_intensity[str(i["Intensity"]["Name"])] = {
                    "name": i["Intensity"]["Name"],
                    "intensity": "6-",
                    "is_area": True
                }
            area_intensity[str(i["Intensity"]["Name"])]["latitude"] = \
                centroid_instance.area_centroid.get(str(i["Intensity"]["Name"]))[0]
            area_intensity[str(i["Intensity"]["Name"])]["longitude"] = \
                centroid_instance.area_centroid.get(str(i["Intensity"]["Name"]))[1]
    else:
        area_intensity = {}
    try:
        origin_timestamp = converted_response["OriginTime"]["UnixTime"]
        if CURRENT_CONFIG.DEBUG_EEW:
            origin_timestamp = CURRENT_CONFIG.DEBUG_EEW_OVRD["origin_timestamp"] + 3600
        depth = int(converted_response["Hypocenter"]["Location"]["Depth"]["Int"])
        s_wave_time, p_wave_time = parse_pswave(depth, float(
            time.time() + 3600 - origin_timestamp))  # Japanese time
    except Exception:
        app.logger.warn("Failed to get PS wave time. Exception occurred: \n" + traceback.format_exc())
        s_wave_time, p_wave_time = None, None
    return_dict_svir = {
        "status": 0,
        "type": "svir",
        "is_plum": converted_response["Hypocenter"]["isAssumption"],
        "is_cancel": False,
        "is_test": is_test,
        "max_intensity": converted_response["MaxIntensity"]["From"],
        "report_time": converted_response["AnnouncedTime"]["String"],
        "report_num": converted_response["Serial"],
        "report_flag": report_flag,
        "report_id": converted_response["EventID"],
        "is_final": is_final,
        "magnitude": converted_response["Hypocenter"]["Magnitude"]["Float"],
        "hypocenter": {
            "name": converted_response["Hypocenter"]["Name"],
            "longitude": converted_response["Hypocenter"]["Location"]["Long"],
            "latitude": converted_response["Hypocenter"]["Location"]["Lat"],
            "depth": str(converted_response["Hypocenter"]["Location"]["Depth"]["Int"]) + "km"
        },
        "area_intensities": None,
        "area_coloring": {
            "areas": area_intensity,
            "recommended_areas": True
        },
        "s_wave": s_wave_time,
        "p_wave": p_wave_time
    }
