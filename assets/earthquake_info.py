import re
import traceback

from assets.area.area_define import fetch_intensity_report_json

def response_verify(resp):
    """
     Verify if the response's status code is 200 or not.
    """
    if resp.status_code != 200:
        return False
    else:
        return True

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
            earthquake_match_a = re.split(r"[-](.*)[-](.*)[-](.*)/", earthquake_hc_coordinate)
            earthquake_match_b = re.split(r"[+](.*)[-](.*)[-](.*)/", earthquake_hc_coordinate)
            earthquake_match_c = re.split(r"[+](.*)[+](.*)[-](.*)/", earthquake_hc_coordinate)
            earthquake_match_d = re.split(r"[-](.*)[+](.*)[-](.*)/", earthquake_hc_coordinate)
            earthquake_match_if_shallow = re.split(r"[+](.*)[+](.*)[+](.*)/", earthquake_hc_coordinate)
            print(earthquake_match_a, earthquake_match_b, earthquake_match_c, earthquake_match_d)
            try:
                earthquake_match_depth = re.split(r'[+-](.*)[+-](.*)[+-](.*)/', earthquake_hc_coordinate)[3]
            except:
                earthquake_match_depth = "Unknown"
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
            elif len(earthquake_match_if_shallow) == 5:
                # +1+2+3
                earthquake_hypocenter["latitude"] = earthquake_match_if_shallow[1]
                earthquake_hypocenter["longitude"] = earthquake_match_if_shallow[2]
            if earthquake_match_depth == "":
                earthquake_hypocenter["depth"] = "Unknown"
                earthquake_match_if_unknown_a = re.split(r"[-](.*)[-](.*)/", earthquake_hc_coordinate)
                earthquake_match_if_unknown_b = re.split(r"[-](.*)[+](.*)/", earthquake_hc_coordinate)
                earthquake_match_if_unknown_c = re.split(r"[+](.*)[+](.*)/", earthquake_hc_coordinate)
                earthquake_match_if_unknown_d = re.split(r"[+](.*)[-](.*)/", earthquake_hc_coordinate)
                if len(earthquake_match_if_unknown_a) == 4:
                    # -1-2
                    earthquake_hypocenter["latitude"] = "-" + earthquake_match_if_unknown_a[1]
                    earthquake_hypocenter["longitude"] = "-" + earthquake_match_if_unknown_a[2]
                elif len(earthquake_match_if_unknown_b) == 4:
                    # -1+2
                    earthquake_hypocenter["longitude"] = earthquake_match_if_unknown_b[1]
                    earthquake_hypocenter["latitude"] = "-" + earthquake_match_if_unknown_b[2]
                elif len(earthquake_match_if_unknown_c) == 4:
                    # +1+2
                    earthquake_hypocenter["latitude"] = earthquake_match_if_unknown_c[1]
                    earthquake_hypocenter["longitude"] = earthquake_match_if_unknown_c[2]
                elif len(earthquake_match_if_unknown_d) == 4:
                    # +1-2
                    earthquake_hypocenter["latitude"] = earthquake_match_if_unknown_d[1]
                    earthquake_hypocenter["longitude"] = "-" + earthquake_match_if_unknown_d[2]
            elif earthquake_match_depth == "0":
                earthquake_hypocenter["depth"] = "Shallow"
            elif earthquake_match_depth == "Unknown":
                earthquake_hypocenter["depth"] = "Unknown"
            else:
                earthquake_hypocenter["depth"] = str(int(earthquake_match_depth) / 1000) + "km"
    except:
        earthquake_hypocenter["depth"] = "Unknown"
        traceback.print_exc()
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
    from assets.centroid.centroid_define import fetch_area_centroid
    earthquake_area_intensity = {}
    to_fetch_area_color = []
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
                        to_fetch_area_color.append(j["Code"])
                else:
                    earthquake_area_intensity[i["Area"]["Code"]] = {
                        "name": i["Area"]["Name"],
                        "intensity": i["Area"]["MaxInt"],
                        "latitude": fetch_area_centroid()[i["Area"]["Code"]][0],
                        "longitude": fetch_area_centroid()[i["Area"]["Code"]][1]
                    }
                    to_fetch_area_color.append(i["Area"]["Code"])
        else:
            if type(response_intensity["Pref"]["Area"]) == list:
                for i in response_intensity["Pref"]["Area"]:
                    earthquake_area_intensity[i["Code"]] = {
                        "name": i["Name"],
                        "intensity": i["MaxInt"],
                        "latitude": fetch_area_centroid()[i["Code"]][0],
                        "longitude": fetch_area_centroid()[i["Code"]][1]
                    }
                    to_fetch_area_color.append(i["Code"])
            else:
                earthquake_area_intensity[response_intensity["Pref"]["Area"]["Code"]] = {
                    "name": response_intensity["Pref"]["Area"]["Name"],
                    "intensity": response_intensity["Pref"]["Area"]["MaxInt"],
                    "latitude": fetch_area_centroid()[response_intensity["Pref"]["Area"]["Code"]][0],
                    "longitude": fetch_area_centroid()[response_intensity["Pref"]["Area"]["Code"]][1]
                }
                to_fetch_area_color.append(response_intensity["Pref"]["Area"]["Code"])
    except:
        pass
    return_geojson = fetch_intensity_report_json(to_fetch_area_color, earthquake_area_intensity)
    return {
        "intensity": earthquake_area_intensity,
        "geojson": return_geojson
    }


def get_city_intensity(response_intensity):
    """
     Get earthquake area intensity.
    """
    from assets.centroid.centroid_define import fetch_city_centroid
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
    except:
        # Downgrade to area intensity
        print("Downgrade")
        import traceback
        traceback.print_exc()
        return get_area_intensity(response_intensity)["intensity"]
    return earthquake_city_intensity
