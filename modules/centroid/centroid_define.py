import csv
import time
import json

class Centroid:
    """A centroid class that contains area & city centroids."""
    def __init__(self, logger):
        """
        Initializes the instance.

        :param logger: The Flask app logger.
        """
        self.logger = logger
        self._area_centroid = {}
        self._station_centroid = {}
        self._eq_station_centroid = {}
        start_initialize_time = time.perf_counter()
        self.logger.debug("Initializing Centroid library...")
        self._init_area_centroid()
        self._init_earthquake_station_centroid()
        self._init_station_centroid()
        self.logger.debug("Successfully initialized centroid library in {:.3f} seconds.".format(time.perf_counter() - start_initialize_time))

    def _init_area_centroid(self):
        """
        Initializes the centroid for the areas.
        """
        start_initialize_time = time.perf_counter()
        with open("./modules/centroid/jma_area_centroid.csv", "r", encoding="utf-8") as f:
            fieldnames = ("name", "latitude", "longitude")
            reader = csv.DictReader(f, fieldnames)
            for row in reader:
                self._area_centroid[row["name"]] = (row["latitude"], row["longitude"])
            f.close()
        self.logger.debug("Successfully initialized centroid for areas in {:.3f} seconds.".format(time.perf_counter() - start_initialize_time))

    def _init_station_centroid(self):
        """
        Initializes the centroid for intensity stations.
        """
        start_initialize_time = time.perf_counter()
        with open("./modules/centroid/intensity_stations.csv", "r", encoding="utf-8") as f:
            fieldnames = ("name", "latitude", "longitude")
            reader = csv.DictReader(f, fieldnames)
            for row in reader:
                self._station_centroid[row["name"]] = (row["latitude"], row["longitude"])
            f.close()
        self.logger.debug("Successfully initialized centroid for stations in {:.3f} seconds.".format(time.perf_counter() - start_initialize_time))

    def _init_earthquake_station_centroid(self):
        """
        Initializes the centroid for observation stations.
        """
        start_initialize_time = time.perf_counter()
        with open("./modules/centroid/observation_points.json", "r", encoding="utf-8") as f:
            self._eq_station_centroid = json.loads(f.read())
            for i in self._eq_station_centroid:
                if i["Point"] is None or i["IsSuspended"]:
                    self._eq_station_centroid.remove(i)
        self.logger.debug("Successfully initialized centroid for observation stations in {:.3f} seconds.".format(time.perf_counter() - start_initialize_time))

    @property
    def station_centroid(self):
        return self._station_centroid

    @property
    def area_centroid(self):
        return self._area_centroid

    @property
    def earthquake_station_centroid(self):
        return self._eq_station_centroid