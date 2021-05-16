"""
 EEWMap - Modules - StationToEnglish
 ---------------------------
 Transforms the report Japanese name to English name.
 Unused now (Maybe used in the future versions).
"""
from modules.stationtoenglish.station_to_english import EpicenterName

epicenter_name_instance = None
def init_epicenter_name_instance(app):
    """
    Initializes the GeoJson instance for app.

    :param app: The Flask app instance
    """
    global epicenter_name_instance
    app.logger.debug("Initializing GeoJson instance...")
    epicenter_name_instance = EpicenterName(app.logger)
