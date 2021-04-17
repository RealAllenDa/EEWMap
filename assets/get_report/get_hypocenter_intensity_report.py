import requests
import xmltodict

from assets.earthquake_info import get_basic_information, get_city_intensity
from assets.config import proxies
from assets.earthquake_info import response_verify
from assets.debug import DEBUG

def get_hypocenter_intensity_report(xml_addr):
    """
     Get the Earthquake Information (VXSE53).
    """
    try:
        response = requests.get(url=xml_addr,
                                proxies=proxies)
        response.encoding = 'utf-8'
        if not response_verify(response):
            return 0
    except:
        return 0
    if DEBUG:
        with open("./tests/eqinfo.xml", encoding="utf-8") as f:
            test = f.read()
            f.close()
        converted_response = xmltodict.parse(test)
    else:
        converted_response = xmltodict.parse(response.text)
    response_earthquake, response_comment = converted_response["Report"]["Body"]["Earthquake"], \
                                            converted_response["Report"]["Body"]["Comments"]
    if converted_response["Report"]["Head"]["Title"] == "遠地地震に関する情報":
        earthquake_info = get_basic_information(response_earthquake, response_comment)
        return {
        "is_test": True if converted_response["Report"]["Control"]["Status"] != "通常" else False,
        "is_overseas": True,
        "occur_time": earthquake_info["occur_time"],
        "magnitude": earthquake_info["magnitude"],
        "tsunami_comments": {
            "text": earthquake_info["T_text"],
            "code": earthquake_info["T_code"]
        },
        "hypocenter": earthquake_info["hypocenter"]
        }
    earthquake_max_intensity = converted_response["Report"]["Body"]["Intensity"]["Observation"]["MaxInt"]
    earthquake_info = get_basic_information(response_earthquake, response_comment)
    return {
        "is_test": True if converted_response["Report"]["Control"]["Status"] != "通常" else False,
        "occur_time": earthquake_info["occur_time"],
        "is_overseas": False,
        "magnitude": earthquake_info["magnitude"],
        "max_intensity": earthquake_max_intensity,
        "tsunami_comments": {
            "text": earthquake_info["T_text"],
            "code": earthquake_info["T_code"]
        },
        "hypocenter": earthquake_info["hypocenter"],
        "area_intensity": get_city_intensity(converted_response["Report"]["Body"]["Intensity"]["Observation"])
    }