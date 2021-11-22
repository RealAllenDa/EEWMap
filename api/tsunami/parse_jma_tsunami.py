"""
 EEWMap - API - Tsunami - JMA_Tsunami
 Parses tsunami information (Expected arrival time) from JMA XML.
"""
import time
import traceback

import xmltodict

from api.tsunami.parse_jma_watch import preparse_tsunami_watch
from config import PROXY, DEBUG_TSUNAMI, DEBUG_TSUNAMI_OVRD, DEBUG_TSUNAMI_WATCH
from modules.sdk import generate_list, make_web_request

last_jma_info = {}
last_jma_tsunami_watch = []
return_dict = {}


def parse_jma_tsunami(response, app):
    """
    Parses JMA XML and gets tsunami info.

    :param response: The raw response from requests
    :param app: The Flask app instance
    :return: A tsunami info
    :rtype: list
    """
    global last_jma_info, return_dict, last_jma_tsunami_watch
    app.logger.debug("Start splitting JMA XML...")
    start_split_time = time.perf_counter()
    response_urls_info = {}
    response_urls_watch = {}
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
        # store in: {(url): yyMMddhhmmss}
        if i["id"].split("/")[-1].split("_")[2] == "VTSE41":
            response_urls_info[i["id"]] = int(i["id"].split("/")[-1].split("_")[0])
        elif i["id"].split("/")[-1].split("_")[2] == "VTSE51":
            if not i["id"] in last_jma_tsunami_watch:
                response_urls_watch[i["id"]] = int(i["id"].split("/")[-1].split("_")[0])
                last_jma_tsunami_watch.append(i["id"])
    if (not response_urls_info) and (not DEBUG_TSUNAMI) and (not response_urls_watch) and (not DEBUG_TSUNAMI_WATCH):
        app.logger.debug("No tsunami warning in effect.")
        return_dict = {}
        return
    if not DEBUG_TSUNAMI and not DEBUG_TSUNAMI_WATCH:
        latest_information_url = max(response_urls_info, key=lambda x: response_urls_info[x])
    else:
        latest_information_url = "TEST"
    app.logger.debug(f"Split JMA XML in {(time.perf_counter() - start_split_time):.3f} seconds. "
                     f"Parsing: {latest_information_url}...")
    # First parse regular tsunami info, then parse watch info
    parse_current_tsunami_info(latest_information_url, app)
    if response_urls_watch or DEBUG_TSUNAMI_WATCH:
        # Have watch information
        if not DEBUG_TSUNAMI_WATCH:
            watch_information_urls = sorted(response_urls_watch, key=lambda x: response_urls_watch[x])
        else:
            watch_information_urls = ["TEST"]
        preparse_tsunami_watch(watch_information_urls, app)


def parse_current_tsunami_info(information_url, app):
    """
    Parses current tsunami info.

    :param information_url: The information url
    :param app: The Flask app instance
    """
    if not DEBUG_TSUNAMI:
        try:
            response = make_web_request(url=information_url,
                                        proxies=PROXY, timeout=3.5)
            if not response[0]:
                app.logger.error(f"Failed to fetch tsunami data: {response[1]}.")
                return
        except:
            app.logger.warn("Failed to fetch tsunami data. Exception occurred: \n" + traceback.format_exc())
            return
        converted_response = xmltodict.parse(response.text, encoding="utf-8")
    else:
        with open(DEBUG_TSUNAMI_OVRD["file"], encoding="utf-8") as f:
            converted_response = xmltodict.parse(f.read(), encoding="utf-8")
    if converted_response["Report"]["Control"]["Status"] != "通常":
        app.logger.info("Drill/Other tsunami message. Skipped.")
        return
    parse_tsunami_information(converted_response, app)


def parse_tsunami_information(converted_response, app, origin="TE"):
    """
    Parses tsunami basic information.

    :param converted_response: The converted JSON of the XML
    :param app: The Flask app instance
    :param origin: Where does the report come from: TE=Tsunami Expectation Message, TW=Tsunami Watch Message
    """
    global return_dict
    return_dict = {}
    app.logger.debug("Start parsing tsunami info...")
    start_parse_time = time.perf_counter()
    response_items = generate_list(converted_response["Report"]["Body"]["Tsunami"]["Forecast"]["Item"])
    receive_time = time.strptime(converted_response["Report"]["Control"]["DateTime"], "%Y-%m-%dT%H:%M:%SZ")
    receive_time_formatted = time.strftime("%Y/%m/%d %H:%M:%S", receive_time)
    return_dict["receive_time"] = receive_time_formatted
    return_dict["areas"] = parse_tsunami_areas(response_items, app)
    return_dict["origin"] = origin
    app.logger.debug(f"Successfully parsed tsunami info "
                     f"in {(time.perf_counter() - start_parse_time):.3f} seconds.")


def parse_tsunami_areas(response_items, app):
    """
    Parses tsunami areas.

    :param response_items: The items in forecast section
    :param app: The Flask app instance
    :return: A list containing areas
    """
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
                        "time": "Tsunami Will Arrive Soon",
                        "status": 0
                    }
                elif first_time_estimation["Condition"] == "津波到達中と推測":
                    area_time = {
                        "type": "no_time",
                        "time": "Tsunami Arrival Expected",
                        "status": 1
                    }
                elif first_time_estimation["Condition"] == "第１波の到達を確認":
                    area_time = {
                        "type": "no_time",
                        "time": "Arrival of Initial Tsunami Confirmed",
                        "status": 2
                    }
            else:
                time_transformed = time.strptime(first_time_estimation["ArrivalTime"][:19], "%Y-%m-%dT%H:%M:%S")
                area_time = {
                    "type": "time",
                    "time": time.strftime("%m-%d %H:%M", time_transformed),
                    "timestamp": time.mktime(time_transformed)
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
    return area_list
