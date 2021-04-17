import requests
import xmltodict
from assets.config import proxies
from assets.earthquake_info import response_verify
from assets.debug import DEBUG, resp_id_override, DEBUG_EEW
from assets.get_report.get_eew import get_eew_info

from assets.get_report.get_hypocenter_report import get_hypocenter_report
from assets.get_report.get_last_earthquake import get_last_earthquake
from assets.get_report.get_intensity_report import get_intensity_report


def get_jma_info():
    """
     Get the JMA XML.
    """
    eew_status = get_eew_info()
    try:
        # Not necessary to be real-time, don't need to add timeout
        response = requests.get(url="http://www.data.jma.go.jp/developer/xml/feed/eqvol.xml",
                                proxies=proxies)
        response.encoding = 'utf-8'
        if not response_verify(response):
            return {"status": -1}
    except:
        return {"status": -1}
    converted_response = xmltodict.parse(response.text)
    response_entries = converted_response["feed"]["entry"]
    response_url_ids = []
    for i in response_entries:
        # Ids like yyyyMMddhhmmss_n_id_n.xml
        response_url_ids.append(i["id"].split("/")[-1])
    # Debugging
    if DEBUG:
        resp_id = resp_id_override
        information_id = "DO_" + resp_id_override
    else:
        resp_id = response_url_ids[0].split("_")[2]
        information_id = response_url_ids[0].split("_")[0]
    # If response_url_ids[0] == .. (EEW / Tsunami Warning, etc)
    print(response_url_ids[0])
    if eew_status["status"] == 0 and eew_status["last_time"] <= 150:
        # EEW Issuing
        return {
            "status": eew_status["report_flag"],
            "content": eew_status
        }
    if DEBUG_EEW:
        # EEW Debugging
        return {
            "status": eew_status["report_flag"],
            "content": eew_status
        }
    if resp_id == "VXSE51":
        resp = get_intensity_report("http://www.data.jma.go.jp/developer/xml/data/" + response_url_ids[0])
        if resp != 0:
            resp["report_id"] = information_id
            return {"status": 1, "content": resp}
        else:
            return {"status": -1}
    elif resp_id == "VXSE52" or resp_id == "VXSE61":
        # Hypocenter Report or Significant Earthquake Factor Update
        resp = get_hypocenter_report("http://www.data.jma.go.jp/developer/xml/data/" + response_url_ids[0])
        if resp != 0:
            resp["report_id"] = information_id
            return {"status": 2, "content": resp}
        else:
            return {"status": -1}
    elif resp_id == "VXSE53":
        resp = get_last_earthquake(False)
        if resp[0] == 1:
            return {"status": 0, "content": resp[1]}
        else:
            return {"status": -1}
    else:
        # Else: Display earthquake last time
        resp = get_last_earthquake(True)
        if resp[0] == 1:
            return {"status": 0, "content": resp[1]}
        else:
            return {"status": -1}
