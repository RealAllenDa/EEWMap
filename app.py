"""
 EEWMap
 ------------------
 Used to start the whole program.
"""
import logging
import os
from logging.handlers import RotatingFileHandler
from flask import Flask

from map import map_bp
from shake_level import shake_level_bp
from index import index_bp
from history import history_bp
from api import api_bp, initialize_api
from modules.area import init_geojson_instance
from modules.centroid import init_centroid_instance
from modules.intensity import init_intensity2color

app = Flask("EEWMap")


# noinspection SpellCheckingInspection
def config_logger():
    """
    Configure the flask logger's format, file store location, etc.
    :return: None
    """
    if not os.path.exists("./logs/"):
        os.mkdir("logs")
    flask_logger = app.logger
    flask_logger.setLevel("DEBUG")
    console_handler = logging.StreamHandler()
    console_formatter = logging.Formatter(fmt="[%(asctime)s] [%(levelname)s] [%(module)s] %(funcName)s: %(message)s")
    console_handler.setFormatter(console_formatter)
    flask_logger.addHandler(console_handler)
    file_handler = RotatingFileHandler(filename="logs/main.log", maxBytes=100*1024*1024, backupCount=10)
    file_formatter = logging.Formatter(fmt="[%(asctime)s] [%(levelname)s] [%(filename)s %(module)s:%(lineno)d] %(funcName)s: %(message)s")
    file_handler.setFormatter(file_formatter)
    file_handler.setLevel("DEBUG")
    flask_logger.addHandler(file_handler)
config_logger()
# Register module blueprints
app.register_blueprint(api_bp)
app.register_blueprint(shake_level_bp)
app.register_blueprint(index_bp)
app.register_blueprint(history_bp)
app.register_blueprint(map_bp)
app.logger.info("App initialization completed successfully. Initializing modules...")
# Initialize APIs & assets
init_geojson_instance(app)
init_centroid_instance(app)
initialize_api(app)
init_intensity2color(app)
app.logger.info("Modules initialization completed successfully.")
if __name__ == "__main_":
    app.run()
