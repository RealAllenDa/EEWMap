"""
 EEWMap - Modules - Centroid - Centroid_Define
 The main entry point of this module.
"""
import csv
import json
import time
import traceback

from config import PROXY
from modules.sdk import relpath, make_web_request


class Centroid:
    """A centroid class that contains area & city centroids."""

    def __init__(self, logger):
        """
        Initializes the instance.

        :param logger: The Flask app logger
        """
        self.logger = logger
        self._area_centroid = {}
        self._station_centroid = {}
        self._eq_station_centroid = {}
        self._area_to_position_centroid = {}
        start_initialize_time = time.perf_counter()
        self.logger.debug("Initializing Centroid library...")
        self.refresh_stations()
        self._init_area_centroid()
        self._init_earthquake_station_centroid()
        self._init_station_centroid()
        self._init_area_to_position_centroid()
        self.logger.debug(f"Successfully initialized centroid library "
                          f"in {(time.perf_counter() - start_initialize_time):.3f} seconds.")

    def refresh_stations(self):
        """
        Updates intensity station names using DM-S.S.S, and refreshes the stations.
        NOTE: The refresh station information are fetched using a bad/borrowed key.
        For commercial uses, please change the key to a self-obtained one.
        """
        self.logger.info("Updating intensity station names...")
        try:
            response = make_web_request(
                url="https://api.dmdata.jp/v2/parameter/earthquake/station?key=1603dbeeac99a4df6b61403626b9decc19850c571809edc1",
                proxies=PROXY, timeout=10, to_json=False
            )
            if not response[0]:
                self.logger.error(f"Failed to update intensity stations: {response[1]}.")
                return
            response = response[1].json()
        except:
            self.logger.error("Failed to update intensity stations. Exception occurred: \n" + traceback.format_exc())
            return
        if response.get("status", "") == "error":
            self.logger.error("Failed to update intensity stations. (response status error)")
            return
        to_write = ""
        for i in response["items"]:
            if i["status"] == "廃止":
                continue
            name = i["name"]
            latitude = i["latitude"]
            longitude = i["longitude"]
            region_code = i["region"]["code"]
            region_name = i["region"]["name"]
            to_write += f"{name},{region_code},{region_name},{latitude},{longitude}\n"
        with open(relpath("./intensity_stations.csv"), "w+", encoding="utf-8") as f:
            f.write(to_write)
            f.close()
        self.logger.info("Successfully updated intensity station names!")
        self._init_station_centroid()

    def _init_area_centroid(self):
        """
        Initializes the centroid for the areas.
        """
        start_initialize_time = time.perf_counter()
        with open(relpath("./jma_area_centroid.csv"), "r", encoding="utf-8") as f:
            fieldnames = ("name", "latitude", "longitude")
            reader = csv.DictReader(f, fieldnames)
            for row in reader:
                self._area_centroid[row["name"]] = (row["latitude"], row["longitude"])
            f.close()
        self.logger.debug(f"Successfully initialized centroid for areas "
                          f"in {(time.perf_counter() - start_initialize_time):.3f} seconds.")

    def _init_station_centroid(self):
        """
        Initializes the centroid for intensity stations.
        """
        start_initialize_time = time.perf_counter()
        with open(relpath("./intensity_stations.csv"), "r", encoding="utf-8") as f:
            fieldnames = ("name", "region_code", "region_name", "latitude", "longitude")
            reader = csv.DictReader(f, fieldnames)
            for row in reader:
                self._station_centroid[row["name"]] = {
                    "location": (row["latitude"], row["longitude"]),
                    "region": {
                        "code": row["region_code"],
                        "name": row["region_name"]
                    }
                }
            f.close()
        self.logger.debug(f"Successfully initialized centroid for stations "
                          f"in {(time.perf_counter() - start_initialize_time):.3f} seconds.")

    def _init_earthquake_station_centroid(self):
        """
        Initializes the centroid for observation stations.
        """
        start_initialize_time = time.perf_counter()
        with open(relpath("./observation_points.json"), "r", encoding="utf-8") as f:
            self._eq_station_centroid = json.loads(f.read())
            for i in self._eq_station_centroid:
                if i["Point"] is None or i["IsSuspended"]:
                    self._eq_station_centroid.remove(i)
        self.logger.debug(f"Successfully initialized centroid for observation stations "
                          f"in {(time.perf_counter() - start_initialize_time):.3f} seconds.")

    def _init_area_to_position_centroid(self):
        """
        Initializes the centroid for sub region codes & position conversion.
        """
        start_initialize_time = time.perf_counter()
        with open(relpath("./area_position.json"), "r", encoding="utf-8") as f:
            self._area_to_position_centroid = json.loads(f.read())
        self.logger.debug(f"Successfully initialized centroid for area to position "
                          f"in {(time.perf_counter() - start_initialize_time):.3f} seconds.")


    @property
    def station_centroid(self):
        return self._station_centroid

    @property
    def area_centroid(self):
        return self._area_centroid

    @property
    def earthquake_station_centroid(self):
        return self._eq_station_centroid

    @property
    def area_position_centroid(self):
        return self._area_to_position_centroid