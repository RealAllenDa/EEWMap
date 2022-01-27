"""
 EEWMap - EEW - Middleware
 The middleware, which will be applied every time when
 getting /earthquake_info.
"""


def combine_intensity_areas(info1: dict, info2: dict) -> dict:
    """
    Combines the intensity areas with both of the info.
    :param info1: A EEW Info (SVIR)
    :param info2: A EEW Info (Kmoni)
    :return: Combined area_intensity Info
    """
    combined_areas = info1["area_coloring"]["areas"]
    try:
        for i in info2["area_coloring"]["areas"].keys():
            if i not in combined_areas:
                combined_areas[i] = info2["area_coloring"]["areas"][i]
        return combined_areas
    except Exception:
        return combined_areas


def use_svir_or_kmoni(return_dict, return_dict_svir):
    """
    Determines whether to use kmoni eew or svir eew.
    :param return_dict: Kmoni eew
    :param return_dict_svir: Svir eew
    :return: Only an eew
    :rtype: dict
    """
    svir_on = return_dict_svir.get("status", -1) != -1
    kmoni_on = return_dict.get("status", -1) != -1
    if (not svir_on) and (not kmoni_on):
        return {}
    elif (not svir_on) and kmoni_on:
        return return_dict
    elif svir_on and (not kmoni_on):
        return return_dict_svir
    elif svir_on and kmoni_on:
        try:
            if int(return_dict_svir["hypocenter"]["depth"][:-2]) >= 150:
                return return_dict_svir
            else:
                if return_dict_svir["report_flag"] == 1:
                    return_dict_svir["area_coloring"]["areas"] = combine_intensity_areas(
                        return_dict_svir, return_dict
                    )
                    return return_dict_svir
                else:
                    return return_dict
        except Exception:
            return return_dict
