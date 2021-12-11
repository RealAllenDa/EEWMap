import time
import traceback

from config import CURRENT_CONFIG
from modules.pswave import parse_pswave
from modules.sdk import make_web_request

return_dict_svir = {}


def get_svir_eew_info(app):
    """
     Gets EEW information from svir.
    """
    global return_dict_svir
    try:
        response = make_web_request(url="https://api.iedred7584.com/eew/json/",
                                    proxies=CURRENT_CONFIG.PROXY, to_json=True)
        if not response[0]:
            app.logger.warn("Failed to fetch EEW info (failed to get svir json).")
        converted_response = response[1]
    except Exception:
        app.logger.warn("Failed to fetch EEW info. Exception occurred: \n" + traceback.format_exc())
        return

    if converted_response["ParseStatus"] == "Error":
        app.logger.warn("Failed to fetch EEW info (parse status is error).")
        return

    is_final = False
    if converted_response["Type"]["Code"] != 0:
        is_final = True

    if is_final:
        timespan = int(time.time()) - 3600 - converted_response["AnnouncedTime"]["UnixTime"]
        # Outdated report
        if not (-12 < timespan < 180):
            # >= 1min
            if not CURRENT_CONFIG.DEBUG_IGNORE_SVIR_OUTDATE:
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

    if converted_response["Title"]["String"] == "緊急地震速報（警報）":
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
        from modules.area import geojson_instance
        for i in converted_response["Forecast"]:
            if i["Intensity"]["From"] in ["1", "2", "3", "4", "7"]:
                area_intensity[str(i["Intensity"]["Code"])] = {
                    "name": i["Intensity"]["Name"],
                    "intensity": i["Intensity"]["From"],
                    "is_area": True
                }
            elif i["Intensity"]["From"] == "5強":
                area_intensity[str(i["Intensity"]["Code"])] = {
                    "name": i["Intensity"]["Name"],
                    "intensity": "5+",
                    "is_area": True
                }
            elif i["Intensity"]["From"] == "5弱":
                area_intensity[str(i["Intensity"]["Code"])] = {
                    "name": i["Intensity"]["Name"],
                    "intensity": "5-",
                    "is_area": True
                }
            elif i["Intensity"]["From"] == "6強":
                area_intensity[str(i["Intensity"]["Code"])] = {
                    "name": i["Intensity"]["Name"],
                    "intensity": "6+",
                    "is_area": True
                }
            elif i["Intensity"]["From"] == "6弱":
                area_intensity[str(i["Intensity"]["Code"])] = {
                    "name": i["Intensity"]["Name"],
                    "intensity": "6-",
                    "is_area": True
                }
            area_intensity[str(i["Intensity"]["Code"])]["latitude"] = \
                centroid_instance.area_centroid.get(str(i["Intensity"]["Code"]))[0]
            area_intensity[str(i["Intensity"]["Code"])]["longitude"] = \
                centroid_instance.area_centroid.get(str(i["Intensity"]["Code"]))[1]
        geojson = geojson_instance.get_intensity_json(area_intensity)
    else:
        area_intensity = {}
        geojson = {}
    try:
        origin_timestamp = converted_response["OriginTime"]["UnixTime"]
        if CURRENT_CONFIG.DEBUG_EEW:
            origin_timestamp = CURRENT_CONFIG.DEBUG_EEW_OVRD["origin_timestamp"]
        depth = int(converted_response["depth"].replace("km", ""))
        s_wave_time, p_wave_time = parse_pswave(depth, float(
                time.time() + (3600 if not CURRENT_CONFIG.DEBUG_EEW else 0) - origin_timestamp))  # Japanese time
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
            "geojson": geojson,
            "recommended_areas": True
        },
        "s_wave": s_wave_time,
        "p_wave": p_wave_time
    }
