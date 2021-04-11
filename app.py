from flask import Flask, render_template
from assets.export_api.get_shake_level import get_shake_level
from assets.export_api.get_jma_info import get_jma_info

app = Flask("EEWMap")
# Renderers
@app.route("/shake_level")
def shake_level_render():
    return render_template("shaking_level.html")
@app.route("/map")
def map_render():
    return render_template("map.html")
@app.route("/")
def index_render():
    return render_template("index.html")
# APIs
@app.route("/api/get_shake_level")
def shake_level_get():
    return get_shake_level()
@app.route("/api/get_jma_xml")
def xml_info_get():
    return get_jma_info()
if __name__ == '__main__':
    app.run()
