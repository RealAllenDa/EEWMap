"""
 EEWMap - History - Views
 ------------------------------
 The main view controller for history module.
"""
from flask import render_template, Blueprint

history_bp = Blueprint("history", __name__, template_folder="templates")
@history_bp.route("/history_earthquake")
def history_render():
    """
    Renders the history page.
    """
    return render_template("previous_earthquake.html")