"""
 EEWMap - Index - Views
 The main view controller for index page.
"""
from flask import render_template, Blueprint

index_bp = Blueprint("index", __name__, template_folder="templates")


@index_bp.route("/")
def index_render():
    """
    Renders the index page.
    """
    return render_template("index.html")
