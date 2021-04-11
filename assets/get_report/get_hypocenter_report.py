import xmltodict
import requests
from assets.config import proxies
from assets.earthquake_info import response_verify, get_basic_information


def get_hypocenter_report(xml_addr):
    try:
        # xml_addr = "http://www.data.jma.go.jp/developer/xml/data/20210404172142_0_VXSE51_010000.xml"
        response = requests.get(url=xml_addr,
                                proxies=proxies)
        response.encoding = 'utf-8'
        if not response_verify(response):
            return 0
    except:
        return 0
    converted_response = xmltodict.parse(response.text)
    response_earthquake, response_comment = converted_response["Report"]["Body"]["Earthquake"], \
                                            converted_response["Report"]["Body"]["Comments"]
    earthquake_info = get_basic_information(response_earthquake, response_comment)
    return {
        "is_test": True if converted_response["Report"]["Control"]["Status"] != "通常" else False,
        "occur_time": earthquake_info["occur_time"],
        "magnitude": earthquake_info["magnitude"],
        "tsunami_comments": {
            "text": earthquake_info["T_text"],
            "code": earthquake_info["T_code"]
        },
        "hypocenter": earthquake_info["hypocenter"]
    }