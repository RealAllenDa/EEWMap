"""
 EEWMap - Modules - Intensity - Main
 The main entry point of this module.
"""
import json
import time
from io import BytesIO

from PIL import Image

from modules.sdk import relpath

INTENSITY_DICT = {}
AREA_INTENSITY_CORRESPOND = {
    1: "1",
    2: "2",
    3: "3",
    4: "4",
    5: "5-",
    6: "5+",
    7: "6-",
    8: "6+",
    9: "7"
}
logger = None


def init_intensity2color(app):
    """
    Initializes intensity2color.

    :param app: The Flask app instance
    """
    global INTENSITY_DICT, logger
    start_initialize_time = time.perf_counter()
    logger = app.logger
    logger.debug("Initializing intensity2color...")
    with open(relpath("./intensity2color.json"), "r") as f:
        temp_dict = json.loads(f.read())
        f.close()
    for i in temp_dict.keys():
        temp_string = ",".join(temp_dict[i])
        INTENSITY_DICT[temp_string] = float(i)
    logger.debug(f"Successfully initialized intensity2color "
                 f"in {(time.perf_counter() - start_initialize_time):.3f} seconds!")


# noinspection PyUnresolvedReferences
def intensity2color(raw_response):
    """
    Parses the image into a intensity array using centroids.

    :param raw_response: The raw response from requests
    :return: A dict containing latitude, longitude and intensities
    :rtype: dict
    """
    # Preparation
    start_time = time.perf_counter()
    logger.debug("Parsing EEW coloring...")
    intensities = {}
    area_intensities = {}
    image_fp = Image.open(BytesIO(raw_response))
    image = image_fp.convert("RGBA").load()
    from modules.centroid import centroid_instance
    for i in centroid_instance.earthquake_station_centroid:
        if i["Point"] is None:
            continue
        try:
            pixel_color = image[int(i["Point"]["X"]), int(i["Point"]["Y"])][0:3]
        except Exception:
            continue
        pixel_string = ",".join('%s' % list_id for list_id in pixel_color)
        pixel_intensity = INTENSITY_DICT.get(pixel_string, 0)
        if pixel_intensity != 0:
            # Have expected intensity
            if 0.5 < pixel_intensity < 1.5:
                parsed_intensity = "1", 1
            elif 1.5 <= pixel_intensity < 2.5:
                parsed_intensity = "2", 2
            elif 2.5 <= pixel_intensity < 3.5:
                parsed_intensity = "3", 3
            elif 3.5 <= pixel_intensity < 4.5:
                parsed_intensity = "4", 4
            elif 4.5 <= pixel_intensity < 5.0:
                parsed_intensity = "5-", 5
            elif 5.0 <= pixel_intensity < 5.5:
                parsed_intensity = "5+", 6
            elif 5.5 <= pixel_intensity < 6.0:
                parsed_intensity = "6-", 7
            elif 6.0 <= pixel_intensity < 6.5:
                parsed_intensity = "6+", 8
            elif pixel_intensity >= 6.5:
                parsed_intensity = "7", 9
            else:
                continue
            # Area
            if i["SubRegionCode"] not in area_intensities:
                area_intensities[i["SubRegionCode"]] = 0
            if area_intensities[i["SubRegionCode"]] < parsed_intensity[1]:
                area_intensities[i["SubRegionCode"]] = parsed_intensity[1]
            # Station
            full_name = i["Region"] + i["Name"]
            intensities[full_name] = {
                "name": full_name,
                "area_code": i["RegionCode"],
                "sub_area_code": i["SubRegionCode"],
                "latitude": i["Location"]["Latitude"],
                "longitude": i["Location"]["Longitude"],
                "intensity": parsed_intensity[0],
                "detail_intensity": pixel_intensity,
                "is_area": False
            }
    parsed_area_intensities, recommend_area_coloring = parse_area_intensities(area_intensities)
    from modules.area import geojson_instance
    parsed_area_coloring = geojson_instance.get_intensity_json(parsed_area_intensities)
    logger.debug(f"Successfully parsed EEW intensities in {(time.perf_counter() - start_time):.3f} seconds!")
    return intensities, parsed_area_intensities, parsed_area_coloring, recommend_area_coloring


def parse_area_intensities(area_intensities):
    parsed_area_int = {}
    recommend_areas = False
    from modules.centroid import centroid_instance
    for i in area_intensities.keys():
        try:
            intensity = AREA_INTENSITY_CORRESPOND[area_intensities[i]]
            position_name = centroid_instance.area_position_centroid.get(i)
            position = position_name["position"]
            name = position_name["name"]
            if area_intensities[i] >= 4:
                recommend_areas = True
        except Exception:
            continue
        parsed_area_int[name] = {
            "name": name,
            "intensity": intensity,
            "is_area": True,
            "latitude": position[0],
            "longitude": position[1]
        }
    return parsed_area_int, recommend_areas
