"""
 EEWMap - Tsunami Map - Views
 The main view controller for the tsunami map.
"""
from flask import render_template, Blueprint

tsunami_bp = Blueprint("tsunami", __name__, template_folder="templates")


@tsunami_bp.route("/tsunami_info")
def tsunami_info_render():
    """
    Renders the tsunami info index.
    """
    return render_template("tsunami_info.html")


@tsunami_bp.route("/tsunami_map")
def tsunami_map_render():
    """
    Renders the tsunami map index.
    """
    return render_template("tsunami_map.html")


@tsunami_bp.route("/tsunami_watch")
def tsunami_watch_render():
    """
    Renders the tsunami watch index.
    """
    return render_template("tsunami_watch.html")


@tsunami_bp.route("/tsunami_banner")
def tsunami_banner_render():
    """
    Renders the tsunami banner index.
    """
    return render_template("tsunami_banner.html")

@tsunami_bp.route("/tsunami_forecast")
def tsunami_forecast_render():
    """
    Renders the tsunami forecast index.
    """
    return render_template("tsunami_forecast.html")
