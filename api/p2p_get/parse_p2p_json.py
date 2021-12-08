"""
 EEWMap - API - P2P - Parse_JSON
 Parses P2P API Json from the response, including:
    - Earthquake information
        - Intensity Report
        - Hypocenter Report
        - Hypocenter and Intensity Report
        - Detailed Intensity Report
        - Foreign Earthquake Report
    - Tsunami information (Goes into tsunami map)
        - Tsunami Expected Grade
"""
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

    :param app: The Flask app instance
    :param raw_json: The JSON from the module
    :return: Earthquake information
    :rtype: dict
    """
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
        app.logger.debug(f"Split the message in {(end_split_time - start_split_time):.3f} seconds.")
    else:
        # In this situation, we assume that return_list is not blank (because of the logic above).
        app.logger.debug("No new earthquake information.")
        return
    last_response_list = raw_json
    return_list = []
    tsunami_return = {}
    i: dict
    for i in reversed(parsing_list):
        app.logger.debug(f"Parsing ID: {i['code']}-{i['id']}")
        start_parse_time = time.perf_counter()

        if i["code"] == 551:
            # Earthquake information
            if i["issue"]["source"] == "TR.tr(\\":
                # Training
                app.logger.debug("Training message. Skipped.")
                continue
            earthquake_info_type = i["issue"]["type"]
            if earthquake_info_type == "Other":
                app.logger.debug("Other message. Skipped.")
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
            earthquake_magnitude = str(round(float(earthquake_raw_hypocenter["magnitude"]), 1))
            earthquake_max_intensity = INTENSITIES.get(i["earthquake"]["maxScale"], 99999)
            earthquake_tsunami_comment = {
                "foreign": "",
                "domestic": ""
            }
            if i["earthquake"]["foreignTsunami"] not in ["None", "Unknown"]:
                earthquake_tsunami_comment["foreign"] = i["earthquake"]["foreignTsunami"]
            else:
                earthquake_tsunami_comment["foreign"] = "None"
            if i["earthquake"]["domesticTsunami"] in ["Unknown", "Checking"]:
                earthquake_tsunami_comment["domestic"] = "Checking"
            elif i["earthquake"]["domesticTsunami"] == "None":
                earthquake_tsunami_comment["domestic"] = "None"
            elif i["earthquake"]["domesticTsunami"] == "NonEffective":
                earthquake_tsunami_comment["domestic"] = "NonEffective"
            elif i["earthquake"]["domesticTsunami"] in ["Watch", "Warning"]:
                earthquake_tsunami_comment["domestic"] = "Warning"
            else:
                earthquake_tsunami_comment["domestic"] = i["earthquake"]["domesticTsunami"]
            app.logger.debug(
                f"Successfully parsed basic information in {(time.perf_counter() - start_parse_time):.3f} seconds. "
                "Parsing station information...")

            if earthquake_info_type != "Foreign":
                station_start_time = time.perf_counter()
                geojson_areas_earthquake = []
                earthquake_area_intensity = {}
                for j in i["points"]:
                    if j["isArea"]:
                        point = centroid_instance.area_centroid.get(j["addr"], None)
                        if point is None:
                            continue
                        earthquake_area_intensity[j["addr"]] = {
                            "name": j["addr"],
                            "intensity": INTENSITIES.get(j["scale"]),
                            "latitude": point[0],
                            "longitude": point[1],
                            "is_area": "true",
                            "intensity_code": j["scale"]
                        }
                        geojson_areas_earthquake.append(j["addr"])
                    else:
                        point = centroid_instance.station_centroid.get(j["addr"], None)
                        if point is None:
                            continue
                        point_region = point["region"]
                        point_long_lat = point["location"]
                        earthquake_area_intensity[j["addr"]] = {
                            "name": j["addr"],
                            "intensity": INTENSITIES.get(j["scale"]),
                            "latitude": point_long_lat[0],
                            "longitude": point_long_lat[1],
                            "is_area": "false",
                            "region_code": point_region["code"],
                            "region_name": point_region["name"],
                            "intensity_code": j["scale"]
                        }
                parsed_intensities = parse_intensities(earthquake_area_intensity)
            else:
                app.logger.debug("Earthquake is foreign. Skipped area intensity parsing.")
                station_start_time = 0
                parsed_intensities = {}

            return_temp = {
                "type": earthquake_info_type,
                "occur_time": earthquake_time,
                "receive_time": earthquake_info_receive_time,
                "magnitude": earthquake_magnitude,
                "max_intensity": earthquake_max_intensity,
                "tsunami_comments": earthquake_tsunami_comment,
                "hypocenter": earthquake_hypocenter,
                "area_intensity": {
                    "areas": parsed_intensities["area"]["intensity"],
                    "geojson": parsed_intensities["area"]["geojson"],
                    "station": parsed_intensities["station"]
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
                    app.logger.debug(f"Successfully parsed area intensity in "
                                     f"{(time.perf_counter() - station_start_time):.3f} seconds.")

            app.logger.debug(f"Successfully parsed earthquake information "
                             f"in {(time.perf_counter() - start_parse_time):.3f} seconds.")
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
            geojson_areas_tsunami = []
            tsunami_areas_warn = {}
            tsunami_return = {}
            for j in i["areas"]:
                geojson_areas_tsunami.append(j["name"])
                tsunami_areas_warn[j["name"]] = {
                    "name": j["name"],
                    "immediate": j["immediate"],
                    "grade": j["grade"]
                }
            from modules.area import geojson_instance
            tsunami_return = {
                "time": i["time"],
                "areas": geojson_instance.get_tsunami_json(geojson_areas_tsunami, tsunami_areas_warn)
            }


def parse_intensities(eq_intensities_list: dict):
    area_intensities = {}
    station_intensities = {}
    area_names = []
    for i in eq_intensities_list.keys():
        content = eq_intensities_list[i]
        if content["is_area"] == "true":
            area_intensities[content["name"]] = content
        else:
            station_intensities[content["name"]] = content
            if content["region_name"] not in area_intensities:
                from modules.centroid import centroid_instance
                position = centroid_instance.area_position_centroid[content["region_code"]]["position"]
                area_intensities[content["region_name"]] = {
                    "name": content["region_name"],
                    "intensity": INTENSITIES.get(content["intensity_code"]),
                    "latitude": position[0],
                    "longitude": position[1],
                    "is_area": "true",
                    "intensity_code": content["intensity_code"]
                }
            else:
                if content["intensity_code"] > area_intensities[content["region_name"]]["intensity_code"]:
                    area_intensities[content["region_name"]]["intensity_code"] = content["intensity_code"]
                    # TODO: more optimization
                    area_intensities[content["region_name"]]["intensity"] = INTENSITIES.get(content["intensity_code"])
            if content["region_name"] not in area_names:
                area_names.append(content["region_name"])
    from modules.area import geojson_instance
    area_geojson = geojson_instance.get_intensity_json(area_names, area_intensities)
    return {
        "area": {
            "intensity": area_intensities,
            "geojson": area_geojson
        },
        "station": station_intensities
    }