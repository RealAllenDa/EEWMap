from flask import Flask, render_template
from get_info import get_shake_level, get_jma_info

app = Flask("EEWMap")
# Renderers
@app.route("/shake_level")
def shake_level_render():
    return render_template("shaking_level.html")
@app.route("/map")
def map_render():
    return render_template("map.html")
# APIs
@app.route("/get_shake_level")
def shake_level_get():
    return get_shake_level()
@app.route("/get_jma_xml")
def xml_info_get():
    return get_jma_info()
if __name__ == '__main__':
    app.run()
