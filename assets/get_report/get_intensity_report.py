import requests
import xmltodict
from assets.config import proxies
from assets.earthquake_info import response_verify, get_area_intensity
from assets.debug import DEBUG

def get_intensity_report(xml_addr):
    """
     Get the Earthquake Information (VXSE51).
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
        with open("./tests/test.xml", encoding="utf-8") as f:
            converted_response = xmltodict.parse(f.read())
            f.close()
    else:
        converted_response = xmltodict.parse(response.text)
    response_head, response_intensity = converted_response["Report"]["Head"], \
                                                          converted_response["Report"]["Body"]["Intensity"][
                                                              "Observation"]
    try:
        earthquake_tsunami_comment_text = converted_response["Report"]["Body"]["Comments"]["ForecastComment"]["Text"]
        earthquake_tsunami_comment_code = converted_response["Report"]["Body"]["Comments"]["ForecastComment"]["Code"]
    except:
        earthquake_tsunami_comment_text = "NO INFO AVAIL"
        earthquake_tsunami_comment_code = "0217"
    # Earthquake time transform
    earthquake_parse_time = response_head["TargetDateTime"]
    earthquake_date = earthquake_parse_time.split("T")[0]
    earthquake_time = earthquake_parse_time.split("T")[1].split("+")[0]
    earthquake_transformed_time = earthquake_date + " " + earthquake_time
    earthquake_max_intensity = response_intensity["MaxInt"]

    return {
        "is_test": True if converted_response["Report"]["Control"]["Status"] != "通常" else False,
        "occur_time": earthquake_transformed_time,
        "max_intensity": earthquake_max_intensity,
        "tsunami_comments": {
            "text": earthquake_tsunami_comment_text,
            "code": earthquake_tsunami_comment_code
        },
        "area_intensity": get_area_intensity(response_intensity)
    }


