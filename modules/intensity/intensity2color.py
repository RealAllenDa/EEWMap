import json
import time

from PIL import Image
from io import BytesIO

INTENSITY_DICT = {}
logger = None
def init_intensity2color(app):
    """
    Initializes intensity2color.
    :param app: The Flask app instance.
    """
    global INTENSITY_DICT, logger
    start_initialize_time = time.perf_counter()
    logger = app.logger
    logger.debug("Initializing intensity2color...")
    with open("./modules/intensity/intensity2color.json", "r") as f:
        temp_dict = json.loads(f.read())
        f.close()
    for i in temp_dict.keys():
        temp_string = ",".join(temp_dict[i])
        INTENSITY_DICT[temp_string] = float(i)
    logger.debug("Successfully initialized intensity2color in {:.3f} seconds!".format(time.perf_counter() - start_initialize_time))


# noinspection PyUnresolvedReferences
def intensity2color(response_handle):
    """
    Parses the image into a intensity array using centroids.
    :param response_handle: The raw response from requests
    :return: A dict containing latitude, longitude and intensities
    :rtype: dict
    """
    # Preparation
    start_time = time.perf_counter()
    logger.debug("Parsing EEW coloring...")
    intensities = {}
    image_fp = Image.open(BytesIO(response_handle.content))
    image = image_fp.convert("RGBA").load()
    from modules.centroid import centroid_instance
    for i in centroid_instance.earthquake_station_centroid:
        pixel_color = image[int(i["Point"]["X"]), int(i["Point"]["Y"])][0:3]
        pixel_string = ",".join('%s' %list_id for list_id in pixel_color)
        pixel_intensity = INTENSITY_DICT.get(pixel_string, 0)
        if pixel_intensity != 0:
            # Have expected intensity
            intensities[i["Name"]] = {
                "latitude": i["Location"]["Latitude"],
                "longitude": i["Location"]["Longitude"],
                "intensity": pixel_intensity
            }
    logger.debug("Successfully parsed EEW coloring in {:.3f} seconds!".format(
        time.perf_counter() - start_time
    ))
    return intensities