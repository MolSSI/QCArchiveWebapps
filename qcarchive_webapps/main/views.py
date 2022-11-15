from flask import render_template

from . import main_bp


@main_bp.route("/")
def index():
    apps = [
        {"name": "Machine Learning Datasets", "link": "/ml_datasets/"},
        {"name": "Reaction Viewer", "link": "/reaction_viewer/"},
    ]
    return render_template("main/index.html", apps=apps)
