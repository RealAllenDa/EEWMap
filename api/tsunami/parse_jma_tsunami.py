import time
import traceback

import requests
import xmltodict

from config import PROXY, DEBUG_TSUNAMI, DEBUG_TSUNAMI_OVRD
from modules.utilities import generate_list, response_verify

last_jma_info = {}
return_dict = {}


def parse_jma_tsunami(response, app):
    """
    Parses JMA XML and gets tsunami info.
    :param response: The raw response from requests
    :param app: The Flask app instance
    :return: A tsunami info
    :rtype: list
    """
    global last_jma_info, return_dict
    app.logger.debug("Start splitting JMA XML...")
    start_split_time = time.perf_counter()
    response_urls = {}
    converted_response = xmltodict.parse(response.text, encoding="utf-8")
    response_entries = converted_response["feed"]["entry"]
    if last_jma_info != converted_response:
        app.logger.debug("New JMA XML updated. Parsing messages...")
        last_jma_info = converted_response
    elif not DEBUG_TSUNAMI:
        app.logger.debug("No new JMA XML info.")
        return
    for i in response_entries:
        # Ids like yyyyMMddhhmmss_n_id_n.xml
        if i["id"].split("/")[-1].split("_")[2] == "VTSE41":
            response_urls[i["id"]] = int(i["id"].split("/")[-1].split("_")[0])
    if (not response_urls) and (not DEBUG_TSUNAMI):
        app.logger.debug("No tsunami warning in effect.")
        return_dict = {}
        return
    if not DEBUG_TSUNAMI:
        latest_information_url = max(response_urls, key=lambda x: response_urls[x])
    else:
        latest_information_url = "TEST"
    app.logger.debug("Split JMA XML in {:.3f} seconds. Parsing tsunami info...".format(
        time.perf_counter() - start_split_time
    ))
    parse_current_tsunami(latest_information_url, app)


def parse_current_tsunami(information_url, app):
    """
    Parses current tsunami info.
    :param information_url: The information url.
    :param app: The Flask app instance.
    """
    global return_dict
    app.logger.debug("Start parsing tsunami info...")
    start_parse_time = time.perf_counter()
    return_dict = {}
    if not DEBUG_TSUNAMI:
        try:
            response = requests.get(url=information_url,
                                    proxies=PROXY, timeout=3500)
            response.encoding = "utf-8"
            if not response_verify(response):
                app.logger.error("Failed to fetch tsunami data. (response code not 200)")
                return
        except:
            app.logger.warn("Failed to fetch tsunami data. Exception occurred: \n" + traceback.format_exc())
            return
        converted_response = xmltodict.parse(response.text, encoding="utf-8")
    else:
        with open(DEBUG_TSUNAMI_OVRD["file"], encoding="utf-8") as f:
            converted_response = xmltodict.parse(f.read(), encoding="utf-8")
    if converted_response["Report"]["Control"]["Status"] != "通常":
        app.logger.info("Drill tsunami message. Skipped.")
        return
    response_items = generate_list(converted_response["Report"]["Body"]["Tsunami"]["Forecast"]["Item"])
    receive_time = time.strptime(converted_response["Report"]["Control"]["DateTime"], "%Y-%m-%dT%H:%M:%SZ")
    receive_time_formatted = time.strftime("%Y-%m-%d %H:%M:%S", receive_time)
    area_list = []
    for i in response_items:
        if i["Category"]["Kind"]["Name"] in ["津波予報（若干の海面変動）", "津波注意報解除", "警報解除"]:
            continue
        area_name = i["Area"]["Name"]
        if "大津波警報" in i["Category"]["Kind"]["Name"]:
            area_grade = "MajorWarning"
        elif "津波警報" in i["Category"]["Kind"]["Name"]:
            area_grade = "Warning"
        elif "津波注意報" in i["Category"]["Kind"]["Name"]:
            area_grade = "Watch"
        else:
            area_grade = "Unknown"
        area_height = "Unknown"
        area_time = {
            "type": "no_time",
            "time": "Unknown"
        }
        if not area_grade in ["Forecast", "Unknown"]:
            first_time_estimation = i["FirstHeight"]
            if "Condition" in first_time_estimation:
                if first_time_estimation["Condition"] == "ただちに津波来襲と予測":
                    area_time = {
                        "type": "no_time",
                        "time": "Tsunami Will Arrive Soon"
                    }
                elif first_time_estimation["Condition"] == "津波到達中と推測":
                    area_time = {
                        "type": "no_time",
                        "time": "Tsunami Arrival Expected"
                    }
                elif first_time_estimation["Condition"] == "第１波の到達を確認":
                    area_time = {
                        "type": "no_time",
                        "time": "Arrival of Initial Tsunami Confirmed"
                    }
            else:
                time_transformed = time.strptime(first_time_estimation["ArrivalTime"][:19], "%Y-%m-%dT%H:%M:%S")
                area_time = {
                    "type": "time",
                    "time": time.strftime("%Y-%m-%d %H:%M:%S", time_transformed)
                }
            try:
                max_height = i["MaxHeight"]["jmx_eb:TsunamiHeight"]
                if max_height["@description"] == "巨大":
                    area_height = "HUGE"
                elif max_height["@description"] == "高い":
                    area_height = "HIGH"
                elif max_height["@description"] == "１０ｍ超":
                    area_height = "10m+"
                elif max_height["@description"] == "１０ｍ":
                    area_height = "10m"
                elif max_height["@description"] == "５ｍ":
                    area_height = "5m"
                elif max_height["@description"] == "３ｍ":
                    area_height = "3m"
                elif max_height["@description"] == "１ｍ":
                    area_height = "1m"
                else:
                    area_height = "Unknown"
            except:
                app.logger.warn("Failed to parse tsunami area height."
                                " Exception occurred: \n" + traceback.format_exc())
                area_height = "Unknown"
        area_list.append({
            "name": area_name,
            "grade": area_grade,
            "height": area_height,
            "time": area_time
        })
    return_dict["receive_time"] = receive_time_formatted
    return_dict["areas"] = area_list
    app.logger.debug("Successfully parsed tsunami info in {:.3f} seconds.".format(
        time.perf_counter() - start_parse_time
    ))
