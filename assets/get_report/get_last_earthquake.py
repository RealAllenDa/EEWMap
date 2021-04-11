import requests
import xmltodict
from assets.config import proxies
from assets.earthquake_info import response_verify
from assets.get_report.get_hypocenter_intensity_report import get_hypocenter_intensity_report

def get_last_earthquake(isLongtime):
    """
     Get the last earthquake information.
    """
    if isLongtime:
        url = "http://www.data.jma.go.jp/developer/xml/feed/eqvol_l.xml"
    else:
        url = "http://www.data.jma.go.jp/developer/xml/feed/eqvol.xml"
    try:
        # Not necessary to be real-time, don't need to add timeout
        response = requests.get(url=url,
                                proxies=proxies)
        response.encoding = 'utf-8'
        if not response_verify(response):
            return 0, 0
    except:
        return 0, 0
    converted_response = xmltodict.parse(response.text)
    response_entries = converted_response["feed"]["entry"]
    response_url_ids = []
    for i in response_entries:
        # Ids like yyyyMMddhhmmss_n_id_n.xml
        response_url_ids.append(i["id"].split("/")[-1])
    for i in response_url_ids:
        if i.split("_")[2] == "VXSE53":
            # Hypocenter + Intensity Report
            detailed_response = get_hypocenter_intensity_report("http://www.data.jma.go.jp/developer/xml/data/" + i)
            if detailed_response == 0:
                return 0, 0
            else:
                return 1, detailed_response




