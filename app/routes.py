from flask import render_template
from . import root_blueprint

@root_blueprint.route("/")
def index():
    return render_template("index.html")
