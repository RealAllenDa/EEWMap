"""
 EEWMap - API - Tsunami - JMA_Watch
 Parses tsunami watch information from JMA XML.
"""
import time
import traceback

import xmltodict

from config import CURRENT_CONFIG
from modules.sdk import generate_list, make_web_request

watch_return = {}


def preparse_tsunami_watch(information_urls, app):
    """
    Filters tsunami watch information from other information.

    :param information_urls: The information urls list
    :param app: The Flask app instance
    """
    start_preparse_time = time.perf_counter()
    app.logger.debug("Start pre-parsing tsunami watch information...")
    to_parse_response = ""
    if information_urls != ["TEST"]:
        for i in information_urls:
            try:
                response = make_web_request(url=i,
                                            proxies=CURRENT_CONFIG.PROXY, timeout=3.5, to_json=False)
                if not response[0]:
                    app.logger.warn(f"Failed to fetch tsunami watch information: {response[1]}.")
                    continue
                response = response[1]
            except Exception:
                app.logger.warn(
                    "Failed to fetch tsunami watch information. Exception occurred: \n" + traceback.format_exc())
                continue
            converted_response = xmltodict.parse(response.text, encoding="utf-8")
            if converted_response["Report"]["Head"]["Title"] == "津波観測に関する情報" and \
                    converted_response["Report"]["Control"]["Status"] == "通常" and \
                    converted_response["Report"]["Head"]["InfoType"] == "発表":
                app.logger.debug(f"Parsing watch information url: {i}")
                to_parse_response = converted_response
                break
    else:
        with open(CURRENT_CONFIG.DEBUG_TSUNAMI_WATCH_OVRD, encoding="utf-8") as f:
            to_parse_response = xmltodict.parse(f.read(), encoding="utf-8")
            f.close()
    if not to_parse_response:
        app.logger.info("No tsunami watch information.")
        return
    app.logger.debug(f"Successfully pre-parsed tsunami watch information "
                     f"in {(time.perf_counter() - start_preparse_time):.3f} seconds.")
    from .parse_jma_tsunami import parse_tsunami_information
    parse_tsunami_information(to_parse_response, app, "TW")
    parse_tsunami_watch_information(to_parse_response, app)


def parse_tsunami_watch_information(to_parse_raw_response, app):
    """
    Parses tsunami watch information.

    :param to_parse_raw_response: The raw response waiting to being parsed
    :param app: The Flask app instance
    """
    global watch_return
    watch_return = {"areas": []}
    start_parse_time = time.perf_counter()
    app.logger.debug("Parsing tsunami watch information...")
    receive_time = time.strptime(to_parse_raw_response["Report"]["Control"]["DateTime"], "%Y-%m-%dT%H:%M:%SZ")
    receive_time_formatted = time.strftime("%Y/%m/%d %H:%M:%S", receive_time)
    watch_return["receive_time"] = receive_time_formatted
    report_items = generate_list(to_parse_raw_response["Report"]["Body"]["Tsunami"]["Observation"]["Item"])
    for i in report_items:
        report_stations = generate_list(i["Station"])
        for j in report_stations:
            max_height_record = j["MaxHeight"]
            if "Condition" in max_height_record:
                if max_height_record["Condition"] == "観測中":
                    watch_return["areas"].append({
                        "name": j["Name"],
                        "time": "None",
                        "condition": "Observing",
                        "height": "None",
                        "height_condition": "None",
                        "height_is_max": False
                    })
                    continue
                elif max_height_record["Condition"] == "微弱":
                    time_transformed = time.strptime(max_height_record["DateTime"][:19], "%Y-%m-%dT%H:%M:%S")
                    time_formatted = time.strftime("%m-%d %H:%M", time_transformed)
                    watch_return["areas"].append({
                        "name": j["Name"],
                        "time": time_formatted,
                        "condition": "Weak",
                        "height": "None",
                        "height_condition": "None",
                        "height_is_max": False
                    })
                    continue
            time_transformed = time.strptime(max_height_record["DateTime"][:19], "%Y-%m-%dT%H:%M:%S")
            time_formatted = time.strftime("%m-%d %H:%M", time_transformed)
            try:
                tsunami_height_raw = max_height_record["jmx_eb:TsunamiHeight"]
                if "@condition" in tsunami_height_raw:
                    if tsunami_height_raw["@condition"] == "上昇中":
                        height_condition = "Rising"
                    else:
                        height_condition = "None"
                else:
                    height_condition = "None"
                height = tsunami_height_raw["#text"]
                if "以上" in tsunami_height_raw["@description"]:
                    height_is_max = True
                else:
                    height_is_max = False
            except Exception:
                app.logger.warn("Failed to parse tsunami watch areas."
                                " Exception occurred: \n" + traceback.format_exc())
                continue
            watch_return["areas"].append({
                "name": j["Name"],
                "time": time_formatted,
                "condition": "None",
                "height": height,
                "height_condition": height_condition,
                "height_is_max": height_is_max
            })
    app.logger.debug(f"Successfully parsed tsunami watch information "
                     f"in {(time.perf_counter() - start_parse_time):.3f} seconds.")
