import re
import time

logger = None
pswave_list = []


def init_pswave(app):
    """
    Initializes the PSWave module.
    :param app: The Flask app instance.
    :return:
    """
    global logger, pswave_list
    logger = app.logger
    logger.debug("Initializing PSWave...")
    start_time = time.perf_counter()
    with open("./modules/pswave/tjma2001", "r") as f:
        temp_file = f.read()
        f.close()
    file_parsed = re.sub(r"\x20+", " ", temp_file)
    pswave_split_1 = file_parsed.split("\n")
    for i in pswave_split_1:
        temp_2 = i.split(" ")
        if len(temp_2) != 5:
            continue
        pswave_list.append([float(temp_2[1]), float(temp_2[2]), int(temp_2[3]), int(temp_2[4])])
    logger.debug(f"Successfully initialized PSWave in {(time.perf_counter() - start_time):.3f} seconds.")


# noinspection PyUnresolvedReferences
def parse_swave(depth, time_passed):
    """
    Parses the SWave time from tjma2001.
    :param depth: The depth of the earthquake
    :param time_passed: The passed time of the earthquake
    :return: The S wave time.
    """
    logger.debug(f"Parsing S wave time -> depth:{depth}, time:{time_passed}...")
    start_time = time.perf_counter()
    if depth > 700 or time_passed > 2000:
        logger.warn("Failed to parse S wave time (Time too long or depth too high).")
        return None
    depth_correspond = list(filter(lambda d: d[2] == depth, pswave_list))
    if len(depth_correspond) == 0:
        logger.warn("Failed to parse S wave time (No depth corresponding).")
        return None
    # the last one => s1, the first one => s2
    s1 = list(filter(lambda s_p: s_p[1] <= time_passed, depth_correspond))
    s2 = list(filter(lambda s_p: s_p[1] >= time_passed, depth_correspond))
    if s1 == [] or s2 == []:
        logger.warn("Failed to parse S wave time (No depth s1, s2 corresponding).")
        return None
    s1 = s1[-1]
    s2 = s2[0]
    s = (time_passed - s1[1]) / (s2[1] - s1[1]) * (s2[3] - s1[3]) + s1[3]
    logger.debug(f"Successfully parsed S wave time in {(time.perf_counter() - start_time):.3f} seconds.")
    return s
