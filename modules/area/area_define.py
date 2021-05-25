import json
import traceback
import time


class GeoJson:
    """A GeoJson class that contains earthquake areas and tsunami areas."""

    def __init__(self, logger):
        """
        Initializes the instance.

        :param logger: The Flask app logger.
        """
        self.logger = logger
        self.intensity_color = {
            "0": "#666666",
            "1": "#46646E",
            "2": "#1E6EE6",
            "3": "#00C8C8",
            "4": "#FAFA64",
            "5-": "#FFB400",
            "5+": "#FF7800",
            "5?": "#FFFF00",
            "6-": "#E60000",
            "6+": "#A00000",
            "7": "#960096"
        }
        self.tsunami_color = {
            "MajorWarning": "#AA28AA",
            "Warning": "#DE3329",
            "Watch": "#E5A72C"
        }
        self.return_format = {
            "type": "FeatureCollection",
            "features": []
        }
        self.japan_areas = {}
        self.tsunami_areas = {}
        start_initialize_time = time.perf_counter()
        self.logger.debug("Initializing GeoJson library...")
        self._init_tsunami_json()
        self._init_earthquake_json()
        self.logger.debug("Successfully initialized GeoJson library in {:.3f} seconds.".format(
            time.perf_counter() - start_initialize_time))

    def _init_earthquake_json(self):
        """
        Initializes the earthquake GeoJson.
        """
        try:
            start_initialize_time = time.perf_counter()
            self.logger.debug("Initializing GeoJson for earthquake...")
            with open("./modules/area/japan_areas.json", encoding="utf-8") as f:
                self.japan_areas = json.loads(f.read())
                f.close()
            self.logger.debug("Successfully initialized GeoJson for earthquake in {:.3f} seconds.".format(
                time.perf_counter() - start_initialize_time))
        except:
            self.logger.fatal("Failed to initialize GeoJson for earthquake. \n" + traceback.format_exc())
            raise Exception("Failed to initialize GeoJson for earthquake.")

    def _init_tsunami_json(self):
        """
        Initializes the tsunami GeoJson.
        """
        try:
            start_initialize_time = time.perf_counter()
            self.logger.debug("Initializing GeoJson for tsunami...")
            with open("./modules/area/tsunami_areas.json", encoding="utf-8") as f:
                self.tsunami_areas = json.loads(f.read())
                f.close()
            self.logger.debug("Successfully initialized GeoJson for tsunami in {:.3f} seconds.".format(
                time.perf_counter() - start_initialize_time))
        except:
            self.logger.fatal("Failed to initialize GeoJson for tsunami. \n" + traceback.format_exc())
            raise Exception("Failed to initialize GeoJson for tsunami.")

    def get_intensity_json(self, area_names, area_intensities):
        """
        Tries to get the areas corresponding to the areas in the earthquake,
        then color it with different intensity colours.

        :param area_names: Areas in the earthquake
        :param area_intensities: The intensities of areas in the earthquake
        :return: area-color pair
        :rtype: dict
        """
        start_time = time.perf_counter()
        self.return_format = {
            "type": "FeatureCollection",
            "features": []
        }
        return_areas = self.return_format
        self.logger.debug("Getting GeoJson for intensity reports...")
        for i in self.japan_areas["features"]:
            if i["properties"]["name"] in area_names:
                try:
                    i["properties"]["intensity"] = area_intensities[i["properties"]["name"]]["intensity"]
                except:
                    self.logger.error("Failed to parse intensity coloring for {}.".format(i["properties"]["name"]))
                    traceback.print_exc()
                    i["properties"]["intensity"] = "0"
                i["properties"]["intensity_color"] = self.intensity_color[i["properties"]["intensity"]]
                return_areas["features"].append(i)
        self.logger.debug("Successfully got GeoJson in {:.3f} seconds.".format(time.perf_counter() - start_time))
        return return_areas

    def get_tsunami_json(self, area_names, area_grades):
        """
        Tries to get the areas corresponding to the areas in tsunami warning,
        then color it with different tsunami type colours.

        :param area_names: Tsunami warning areas
        :param area_grades: The area warning grade
        :return: area-color pair
        :rtype: dict
        """
        start_time = time.perf_counter()
        self.return_format = {
            "type": "FeatureCollection",
            "features": []
        }
        return_areas = self.return_format
        self.logger.debug("Getting GeoJson for intensity reports...")
        for i in self.tsunami_areas["features"]:
            if i["properties"]["name"] in area_names:
                try:
                    i["properties"]["grade"] = area_grades[i["properties"]["name"]]["grade"]
                except:
                    self.logger.error("Failed to parse tsunami coloring for {}.".format(i["properties"]["name"]))
                    traceback.print_exc()
                    i["properties"]["grade"] = "Unknown"
                i["properties"]["intensity_color"] = self.tsunami_color[i["properties"]["grade"]]
                return_areas["features"].append(i)
        self.logger.debug("Successfully got GeoJson in {:.3f} seconds.".format(time.perf_counter() - start_time))
        return return_areas