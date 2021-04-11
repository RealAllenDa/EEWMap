import json
import traceback

MAP_COLOR = {
    "0": "#666666",
    "1": "#46646E",
    "2": "#1E6EE6",
    "3": "#00C8C8",
    "4": "#FAFA64",
    "5-": "#FFB400",
    "5+": "#FF7800",
    "6-": "#E60000",
    "6+": "#A00000",
    "7": "#960096"
}
def fetch_tsunami_area_json():
    # TODO
    pass
def fetch_intensity_report_json(area_codes, area_intensities):
    with open("./assets/area/IntReport.json", encoding="utf-8") as f:
        areas = json.loads(f.read())
        f.close()
    return_areas = {
        "type":"FeatureCollection",
        "features": []
    }
    for i in areas["features"]:
        if i["properties"]["code"] in area_codes:
            try:
                i["properties"]["intensity"] = area_intensities[i["properties"]["code"]]["intensity"]
            except:
                traceback.print_exc()
                i["properties"]["intensity"] = "0"
            i["properties"]["intensity_color"] = MAP_COLOR[i["properties"]["intensity"]]
            return_areas["features"].append(i)
    return return_areas