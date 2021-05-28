"""
 EEWMap - Modules - Centroid
 ---------------------------
 Gets the coordinate definition for earthquake reports.
"""
from modules.centroid.centroid_define import Centroid

# noinspection PyTypeChecker
centroid_instance: Centroid = None


def init_centroid_instance(app):
    """
    Initializes the centroid instance for app.

    :param app: The Flask app instance
    """
    global centroid_instance
    app.logger.debug("Initializing Centroid instance...")
    centroid_instance = Centroid(app.logger)
