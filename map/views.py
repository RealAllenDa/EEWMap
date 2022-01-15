"""
 EEWMap - Map - Views
 The main view controller for the map.
"""
from flask import render_template, Blueprint

map_bp = Blueprint("map", __name__, template_folder="templates")


@map_bp.route("/map")
def map_render():
    """
    Renders the map index.
    :return: None
    """
    return render_template("map.html")


@map_bp.route("/global_list")
def global_earthquake_list_render():
    """
    Renders the global earthquake list.
    :return: None
    """
    return render_template("global.html")
