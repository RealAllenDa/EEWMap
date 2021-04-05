import re
import time

import requests
import xmltodict

# Comment these three lines if needed
proxies = {
    "http": "http://localhost:7890",
    "https": "http://localhost:7890",
}


def response_verify(resp: requests.Response):
    """
     Verify if the response's status code is 200 or not.
    """
    if resp.status_code != 200:
        return False
    else:
        return True


def get_shake_level():
    """
     Get the shaking level.
    """
    try:
        response = requests.get(url="http://kwatch-24h.net/EQLevel.json?" + str(int(time.time())),
                                timeout=3.5, proxies=proxies)
        response.encoding = 'utf-8'
        if not response_verify(response):
            return {"status": -1}
    except:
        return {"status": -1}
    return {"status": 0, "shake_level": response.json()["l"]}


def get_jma_info():
    """
     Get the JMA XML.
    """
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
    # If response_url_ids[0] == .. (EEW / Tsunami Warning, etc)
    print(response_url_ids[0])
    resp_id = response_url_ids[0].split("_")[2]
    # resp_id = "VXSE51"
    if resp_id == "VXSE51":
        resp = get_intensity_report("http://www.data.jma.go.jp/developer/xml/data/" + response_url_ids[0])
        # resp = get_intensity_report("http://www.data.jma.go.jp/developer/xml/data/20210404112940_0_VXSE51_010000.xml")
        if resp == 0:
            return {"status": -1}
        else:
            return {"status": 1, "content": resp}
    elif resp_id == "VXSE52":
        resp = get_hypocenter_report("http://www.data.jma.go.jp/developer/xml/data/" + response_url_ids[0])
        # resp = get_hypocenter_report("http://www.data.jma.go.jp/developer/xml/data/20210404212455_0_VXSE52_010000.xml")
        if resp == 0:
            return {"status": -1}
        else:
            return {"status": 2, "content": resp}
    elif resp_id == "VXSE53":
        resp = get_last_earthquake(False)
        if resp[0] == 1:
            return {"status": 0, "content": resp[1]}
        else:
            return {"status": -1}
    elif resp_id == "VXSE41":
        pass
    elif resp_id == "VXSE40":
        pass
    elif resp_id == "VTSE51":
        pass
    else:
        # Else: Display earthquake last time
        resp = get_last_earthquake(True)
        if resp[0] == 1:
            return {"status": 0, "content": resp[1]}
        else:
            return {"status": -1}


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


def get_hypocenter_intensity_report(xml_addr):
    """
     Get the Earthquake Information (VXSE53).
    """
    try:
        # xml_addr = "http://www.data.jma.go.jp/developer/xml/data/20210401214209_0_VXSE53_270000.xml"
        response = requests.get(url=xml_addr,
                                proxies=proxies)
        response.encoding = 'utf-8'
        if not response_verify(response):
            return 0
    except:
        return 0
    """
    '
    with open("test.xml", encoding="utf-8") as f:
        test = f.read()
        f.close()
    converted_response = xmltodict.parse(test)
    """
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


def get_basic_information(response_earthquake, response_comment):
    """
     Get basic information (time, M, tsunami comments) for VXSE53, VXSE52.
    """
    earthquake_tsunami_comment_text = response_comment["ForecastComment"]["Text"]
    earthquake_tsunami_comment_code = response_comment["ForecastComment"]["Code"]
    # Earthquake time transform
    earthquake_parse_time = response_earthquake["OriginTime"]
    earthquake_date = earthquake_parse_time.split("T")[0]
    earthquake_time = earthquake_parse_time.split("T")[1].split("+")[0]
    earthquake_transformed_time = earthquake_date + " " + earthquake_time
    earthquake_M = response_earthquake["jmx_eb:Magnitude"]["#text"]
    # In case of a earthquake with M8+, the intensity will be NaN
    if earthquake_M == "NaN" and response_earthquake["jmx_eb:Magnitude"]["@description"] == "Ｍ８を超える巨大地震":
        earthquake_M = "Major earthquake with M8+"
    elif earthquake_M == "NaN" and response_earthquake["jmx_eb:Magnitude"]["@description"] == "Ｍ不明":
        earthquake_M = "Unknown"
    # Hypocenter information (name, codename, latitude, longitude, depth)
    earthquake_hypocenter = {
        "name": response_earthquake["Hypocenter"]["Area"]["Name"],
        "code_name": response_earthquake["Hypocenter"]["Area"]["Code"]["#text"]
    }
    # Convert coordinates like +<latitude>+<longitude>-<depth>/
    try:
        if response_earthquake["Hypocenter"]["Area"]["jmx_eb:Coordinate"]["@description"] == "震源要素不明":
            earthquake_hypocenter["depth"] = "Unknown"
        else:
            earthquake_hc_coordinate = response_earthquake["Hypocenter"]["Area"]["jmx_eb:Coordinate"]["#text"]
            earthquake_match_a =  re.split(r"[-](.*)[-](.*)[-](.*)/", earthquake_hc_coordinate)
            earthquake_match_b =  re.split(r"[+](.*)[-](.*)[-](.*)/", earthquake_hc_coordinate)
            earthquake_match_c =  re.split(r"[+](.*)[+](.*)[-](.*)/", earthquake_hc_coordinate)
            earthquake_match_d =  re.split(r"[-](.*)[+](.*)[-](.*)/", earthquake_hc_coordinate)
            print(earthquake_match_a, earthquake_match_b, earthquake_match_c, earthquake_match_d)
            earthquake_match_depth = re.split(r'[+-](.*)[+-](.*)[+-](.*)/', earthquake_hc_coordinate)[3]
            print(earthquake_match_depth)
            if len(earthquake_match_a) == 5:
                # -1-2
                earthquake_hypocenter["latitude"] = "-" + earthquake_match_a[1]
                earthquake_hypocenter["longitude"] = "-" + earthquake_match_a[2]
            elif len(earthquake_match_b) == 5:
                # +1-2
                earthquake_hypocenter["latitude"] = earthquake_match_b[1]
                earthquake_hypocenter["longitude"] = "-" + earthquake_match_b[2]
            elif len(earthquake_match_c) == 5:
                # +1+2
                earthquake_hypocenter["latitude"] = earthquake_match_c[1]
                earthquake_hypocenter["longitude"] = earthquake_match_c[2]
            elif len(earthquake_match_d) == 5:
                # -1+2
                earthquake_hypocenter["latitude"] = "-" + earthquake_match_d[1]
                earthquake_hypocenter["longitude"] = earthquake_match_d[2]
            if earthquake_match_depth == "":
                earthquake_hypocenter["depth"] = "Unknown"
            elif earthquake_match_depth == "0":
                earthquake_hypocenter["depth"] = "Shallow"
            else:
                earthquake_hypocenter["depth"] = str(int(earthquake_match_depth) / 1000)
    except:
        earthquake_hypocenter["depth"] = "Unknown"
    return {
        "occur_time": earthquake_transformed_time,
        "magnitude": earthquake_M,
        "T_text": earthquake_tsunami_comment_text,
        "T_code": earthquake_tsunami_comment_code,
        "hypocenter": earthquake_hypocenter
    }


def get_area_intensity(response_intensity):
    """
     Get earthquake area intensity.
    """
    from assets.centroid_define import fetch_area_centroid
    earthquake_area_intensity = {}
    try:
        if type(response_intensity["Pref"]) == list:
            for i in response_intensity["Pref"]:
                if type(i["Area"]) == list:
                    for j in i["Area"]:
                        earthquake_area_intensity[j["Code"]] = {
                            "name": j["Name"],
                            "intensity": j["MaxInt"],
                            "latitude": fetch_area_centroid()[j["Code"]][0],
                            "longitude": fetch_area_centroid()[j["Code"]][1]
                        }
                else:
                    earthquake_area_intensity[i["Area"]["Code"]] = {
                        "name": i["Area"]["Name"],
                        "intensity": i["Area"]["MaxInt"],
                        "latitude": fetch_area_centroid()[i["Area"]["Code"]][0],
                        "longitude": fetch_area_centroid()[i["Area"]["Code"]][1]
                    }
        else:
            if type(response_intensity["Pref"]["Area"]) == list:
                for i in response_intensity["Pref"]["Area"]:
                    earthquake_area_intensity[i["Code"]] = {
                        "name": i["Name"],
                        "intensity": i["MaxInt"],
                        "latitude": fetch_area_centroid()[i["Code"]][0],
                        "longitude": fetch_area_centroid()[i["Code"]][1]
                    }
            else:
                earthquake_area_intensity[response_intensity["Pref"]["Area"]["Code"]] = {
                    "name": response_intensity["Pref"]["Area"]["Name"],
                    "intensity": response_intensity["Pref"]["Area"]["MaxInt"],
                    "latitude": fetch_area_centroid()[response_intensity["Pref"]["Area"]["Code"]][0],
                    "longitude": fetch_area_centroid()[response_intensity["Pref"]["Area"]["Code"]][1]
                }
    except:
        pass
    return earthquake_area_intensity


def get_city_intensity(response_intensity):
    """
     Get earthquake area intensity.
    """
    from assets.centroid_define import fetch_city_centroid
    earthquake_city_intensity = {}
    try:
        if type(response_intensity["Pref"]) == list:
            for i in response_intensity["Pref"]:
                if type(i["Area"]) == list:
                    for j in i["Area"]:
                        if type(j["City"]) == list:
                            for k in j["City"]:
                                k["Code"] = str(int(k["Code"]))
                                earthquake_city_intensity[k["Code"]] = {
                                    "name": k["Name"],
                                    "intensity": k["MaxInt"],
                                    "latitude": fetch_city_centroid()[k["Code"]][0],
                                    "longitude": fetch_city_centroid()[k["Code"]][1]
                                }
                        else:
                            j["City"]["Code"] = str(int(j["City"]["Code"]))
                            earthquake_city_intensity[j["City"]["Code"]] = {
                                "name": j["City"]["Name"],
                                "intensity": j["City"]["MaxInt"],
                                "latitude": fetch_city_centroid()[j["City"]["Code"]][0],
                                "longitude": fetch_city_centroid()[j["City"]["Code"]][1]
                            }
                else:
                    if type(i["Area"]["City"]) == list:
                        for j in i["Area"]["City"]:
                            j["Code"] = str(int(j["Code"]))
                            earthquake_city_intensity[j["Code"]] = {
                                "name": j["Name"],
                                "intensity": j["MaxInt"],
                                "latitude": fetch_city_centroid()[j["Code"]][0],
                                "longitude": fetch_city_centroid()[j["Code"]][1]
                            }
                    else:
                        i["Area"]["City"]["Code"] = str(int(i["Area"]["City"]["Code"]))
                        earthquake_city_intensity[i["Area"]["City"]["Code"]] = {
                            "name": i["Area"]["City"]["Name"],
                            "intensity": i["Area"]["City"]["MaxInt"],
                            "latitude": fetch_city_centroid()[i["Area"]["City"]["Code"]][0],
                            "longitude": fetch_city_centroid()[i["Area"]["City"]["Code"]][1]
                        }
        else:
            if type(response_intensity["Pref"]["Area"]) == list:
                for i in response_intensity["Pref"]["Area"]:
                    if type(i["City"]) == list:
                        for j in i["City"]:
                            j["Code"] = str(int(j["Code"]))
                            earthquake_city_intensity[j["Code"]] = {
                                "name": j["Name"],
                                "intensity": j["MaxInt"],
                                "latitude": fetch_city_centroid()[j["Code"]][0],
                                "longitude": fetch_city_centroid()[j["Code"]][1]
                            }
                    else:
                        i["City"]["Code"] = str(int(i["City"]["Code"]))
                        earthquake_city_intensity[i["City"]["Code"]] = {
                            "name": i["City"]["Name"],
                            "intensity": i["City"]["MaxInt"],
                            "latitude": fetch_city_centroid()[i["City"]["Code"]][0],
                            "longitude": fetch_city_centroid()[i["City"]["Code"]][1]
                        }
            else:
                if type(response_intensity["Pref"]["Area"]["City"]) == list:
                    for i in response_intensity["Pref"]["Area"]["City"]:
                        i["Code"] = str(int(i["Code"]))
                        earthquake_city_intensity[i["Code"]] = {
                            "name": i["Name"],
                            "intensity": i["MaxInt"],
                            "latitude": fetch_city_centroid()[i["Code"]][0],
                            "longitude": fetch_city_centroid()[i["Code"]][1]
                        }
                else:
                    response_intensity["Pref"]["Area"]["City"]["Code"] = str(
                        int(response_intensity["Pref"]["Area"]["City"]["Code"]))
                    earthquake_city_intensity[response_intensity["Pref"]["Area"]["City"]["Code"]] = {
                        "name": response_intensity["Pref"]["Area"]["City"]["Name"],
                        "intensity": response_intensity["Pref"]["Area"]["City"]["MaxInt"],
                        "latitude": fetch_city_centroid()[response_intensity["Pref"]["Area"]["City"]["Code"]][0],
                        "longitude": fetch_city_centroid()[response_intensity["Pref"]["Area"]["City"]["Code"]][1]
                    }
    except Exception as e:
        # Downgrade to area intensity
        print("Downgrade")
        import traceback
        traceback.print_exc()
        return get_area_intensity(response_intensity)
    return earthquake_city_intensity


def get_intensity_report(xml_addr):
    """
     Get the Earthquake Information (VXSE51).
    """
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
    response_head, response_intensity, response_comment = converted_response["Report"]["Head"], \
                                                          converted_response["Report"]["Body"]["Intensity"][
                                                              "Observation"], \
                                                          converted_response["Report"]["Body"]["Comments"]
    earthquake_tsunami_comment_text = response_comment["ForecastComment"]["Text"]
    earthquake_tsunami_comment_code = response_comment["ForecastComment"]["Code"]
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
