"""
 EEWMap - App
 Used to start the whole program.
"""
import logging
import os
from logging.handlers import RotatingFileHandler

from flask import Flask
from flask_compress import Compress
from flask_cors import CORS
from requests.packages import urllib3
from urllib3.exceptions import InsecureRequestWarning

from api import api_bp, init_api
from config import CURRENT_CONFIG
from debug import debug_bp
from index import index_bp
from map import map_bp
from modules.area import init_geojson_instance
from modules.centroid import init_centroid_instance
from modules.intensity import init_intensity2color
from modules.pswave import init_pswave
from modules.sdk import relpath
from shake_level import shake_level_bp
from tsunami import tsunami_bp

app = Flask("EEWMap")
app.config["COMPRESS_MIMETYPES"] = (
    'text/html',
    'text/css',
    'text/xml',
    'application/json',
    'application/javascript',
    'text/plain')
Compress(app)


# noinspection SpellCheckingInspection
def config_logger():
    """
    Configure the flask logger's format, file store location, etc.
    """
    if not os.path.exists(relpath("./logs/")):
        os.mkdir("logs")
    app.logger.handlers.clear()
    app.logger.setLevel("DEBUG")

    console_handler = logging.StreamHandler()
    console_formatter = logging.Formatter(fmt="[%(asctime)s] [%(levelname)s] [%(module)s] %(funcName)s: %(message)s")
    console_handler.setFormatter(console_formatter)
    app.logger.addHandler(console_handler)

    file_handler = RotatingFileHandler(filename=relpath("logs/main.log"), maxBytes=100 * 1024 * 1024, backupCount=10)
    file_formatter = logging.Formatter(
        fmt="[%(asctime)s] [%(levelname)s] [%(filename)s %(module)s:%(lineno)d] %(funcName)s: %(message)s")
    file_handler.setFormatter(file_formatter)
    file_handler.setLevel("DEBUG")
    app.logger.addHandler(file_handler)


if CURRENT_CONFIG.ENABLE_CORS:
    cors = CORS(app, resources={"*": {"origins": "*"}})
urllib3.disable_warnings(InsecureRequestWarning)
config_logger()
# Register module blueprints
app.register_blueprint(api_bp)
app.register_blueprint(shake_level_bp)
app.register_blueprint(index_bp)
app.register_blueprint(map_bp)
app.register_blueprint(tsunami_bp)
app.register_blueprint(debug_bp)
app.logger.info("App initialization completed successfully. Initializing modules...")
# Initialize APIs & assets
init_geojson_instance(app)
init_centroid_instance(app)
init_api(app)
init_intensity2color(app)
init_pswave(app)
app.logger.info("Modules initialization completed successfully.")
if __name__ == "__main__":
    app.run()
