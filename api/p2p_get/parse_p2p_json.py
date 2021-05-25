import time

last_response_list = []
return_list = []
tsunami_warning_in_effect = "0"
tsunami_return = {}
INTENSITIES = {
    -1: "-1",
    10: "1",
    20: "2",
    30: "3",
    40: "4",
    45: "5-",
    46: "5?",
    50: "5+",
    55: "6-",
    60: "6+",
    70: "7"
}


def parse_p2p_info(raw_json, app):
    """
    Parses the P2P JSON from the getting module.

    :param app: The Flask app instance.
    :param raw_json: The JSON from the module.
    :return: Earthquake information
    :rtype: dict
    """
    from modules.area import geojson_instance
    from modules.centroid import centroid_instance
    global last_response_list, return_list, tsunami_return, tsunami_warning_in_effect
    app.logger.debug("Start parsing P2P JSON...")
    start_split_time = time.perf_counter()
    if not last_response_list:
        # First time parsing
        parsing_list = [raw_json[0]]
        app.logger.debug("First time parsing. Defaulted to the first message.")
    elif last_response_list != raw_json:
        app.logger.debug("New earthquake information incoming, parsing message...")
        parsing_list = [y for y in raw_json if y not in last_response_list]
        end_split_time = time.perf_counter()
        app.logger.debug("Split the message in {:.3f} seconds.".format(end_split_time - start_split_time))
    else:
        # In this situation, we assume that return_list is not blank (because of the logic above).
        app.logger.debug("No new earthquake information.")
        return
    last_response_list = raw_json
    return_list = []
    tsunami_return = {}
    i: dict
    for i in reversed(parsing_list):
        app.logger.debug("Parsing ID: {}-{}".format(i["code"], i["id"]))
        start_parse_time = time.perf_counter()
        if i["code"] == 551:
            # Earthquake information
            earthquake_info_type = i["issue"]["type"]
            if earthquake_info_type == "Other":
                continue
            earthquake_info_receive_time = i["time"]
            earthquake_time = i["earthquake"]["time"]
            earthquake_raw_hypocenter = i["earthquake"]["hypocenter"]
            earthquake_hypocenter = {
                "name": earthquake_raw_hypocenter["name"],
                "latitude": earthquake_raw_hypocenter["latitude"],
                "longitude": earthquake_raw_hypocenter["longitude"],
                "depth": str(earthquake_raw_hypocenter["depth"])
            }
            if int(earthquake_hypocenter["depth"]) == 0:
                earthquake_hypocenter["depth"] = "Shallow"
            elif int(earthquake_hypocenter["depth"]) != -1:
                earthquake_hypocenter["depth"] += "km"
            else:
                earthquake_hypocenter["depth"] = "Unknown"
            earthquake_magnitude = earthquake_raw_hypocenter["magnitude"]
            earthquake_max_intensity = INTENSITIES.get(i["earthquake"]["maxScale"], 99999)
            """
                001: Tsunami Warning in effect
                002: Tsunami Risk Evaluating
                003: Light Sea Changes Expected
                004: No Tsunami Expected
            """
            if i["earthquake"]["domesticTsunami"] in ["Unknown", "Checking"]:
                earthquake_tsunami_comment = "002"
            elif i["earthquake"]["domesticTsunami"] == "None":
                earthquake_tsunami_comment = "004"
            elif i["earthquake"]["domesticTsunami"] == "NonEffective":
                earthquake_tsunami_comment = "003"
            elif i["earthquake"]["domesticTsunami"] in ["Watch", "Warning"]:
                earthquake_tsunami_comment = "001"
            else:
                earthquake_tsunami_comment = "000"
            app.logger.debug("Successfully parsed basic information in {:.3f} seconds. "
                             "Parsing station information...".format(time.perf_counter() - start_parse_time))
            if earthquake_info_type != "Foreign":
                station_start_time = time.perf_counter()
                to_fetch_geojson_areas = []
                earthquake_area_intensity = {}
                for j in i["points"]:
                    if j["isArea"]:
                        point_long_lat = centroid_instance.area_centroid.get(j["addr"], (99999, 99999))
                        if point_long_lat[0] == 99999:
                            continue
                        earthquake_area_intensity[j["addr"]] = {
                            "name": j["addr"],
                            "intensity": INTENSITIES.get(j["scale"]),
                            "latitude": point_long_lat[0],
                            "longitude": point_long_lat[1],
                            "is_area": "true"
                        }
                        to_fetch_geojson_areas.append(j["addr"])
                    else:
                        point_long_lat = centroid_instance.station_centroid.get(j["addr"], (99999, 99999))
                        if point_long_lat[0] == 99999:
                            continue
                        earthquake_area_intensity[j["addr"]] = {
                            "name": j["addr"],
                            "intensity": INTENSITIES.get(j["scale"]),
                            "latitude": point_long_lat[0],
                            "longitude": point_long_lat[1],
                            "is_area": "false"
                        }
            else:
                app.logger.debug("Earthquake is foreign. Skipped area intensity coloring.")
                earthquake_area_intensity = {}
                to_fetch_geojson_areas = []
                station_start_time = 0
            return_temp = {
                "type": earthquake_info_type,
                "occur_time": earthquake_time,
                "receive_time": earthquake_info_receive_time,
                "magnitude": earthquake_magnitude,
                "max_intensity": earthquake_max_intensity,
                "tsunami_comments": earthquake_tsunami_comment,
                "hypocenter": earthquake_hypocenter,
                "area_intensity": {
                    "areas": earthquake_area_intensity,
                    "geojson": "null"
                }
            }
            if earthquake_hypocenter["latitude"] == -200 or \
                    earthquake_hypocenter["longitude"] == -200 or \
                    earthquake_hypocenter["depth"] == -1 or \
                    earthquake_magnitude == -1 or \
                    earthquake_info_type == "ScalePrompt":
                if earthquake_info_type != "Foreign":
                    # Intensity Report
                    return_temp["hypocenter"] = {}
                    # noinspection PyTypeChecker
                    return_temp["area_intensity"]["geojson"] = geojson_instance.get_intensity_json(to_fetch_geojson_areas,
                                                                                               earthquake_area_intensity)
                    app.logger.debug("Successfully parsed area intensity in {:.3f} seconds.".format(
                        time.perf_counter() - station_start_time
                    ))
            app.logger.debug("Successfully parsed earthquake information in {:.3f} seconds.".format(
                time.perf_counter() - start_parse_time
            ))
            return_list.append(return_temp)
        elif i["code"] == 552:
            # Tsunami information
            if i["issue"]["type"] != "Focus":
                app.logger.warn("RARE: Tsunami information type isn't focus. "
                                "Beware of potential API changes.")
                continue
            if i["cancelled"]:
                tsunami_return = {}
                tsunami_warning_in_effect = "0"
                continue
            tsunami_warning_in_effect = "1"
            to_parse_geojson_areas = []
            tsunami_areas_warn = {}
            tsunami_return = {}
            for j in i["areas"]:
                to_parse_geojson_areas.append(j["name"])
                tsunami_areas_warn[j["name"]] = {
                    "name": j["name"],
                    "immediate": j["immediate"],
                    "grade": j["grade"]
                }
            from modules.area import geojson_instance
            tsunami_return = {
                "time": i["time"],
                "areas": geojson_instance.get_tsunami_json(to_parse_geojson_areas, tsunami_areas_warn)
            }