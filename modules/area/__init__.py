"""
 EEWMap - Modules - Area
 ---------------------------
 Gets the geojson area definitions.
"""
from modules.area.area_define import GeoJson

geojson_instance: GeoJson = None
def init_geojson_instance(app):
    """
    Initializes the GeoJson instance for app.

    :param app: The Flask app instance
    """
    global geojson_instance
    app.logger.debug("Initializing GeoJson instance...")
    geojson_instance = GeoJson(app.logger)
