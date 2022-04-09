"""
 EEWMap - shake_level - Views
 The main view controller for shake level.
"""
from flask import render_template, Blueprint

shake_level_bp = Blueprint("shake_level", __name__, template_folder="templates")


@shake_level_bp.route("/shake_level")
def shake_level_render():
    """
    Renders shaking level display page.
    """
    return render_template("shaking_level.html")


@shake_level_bp.route("/shake_indicator")
def shake_indicator_render():
    """
    Renders shaking indicator (warning, caution).
    """
    return render_template("shake_indicator.html")
