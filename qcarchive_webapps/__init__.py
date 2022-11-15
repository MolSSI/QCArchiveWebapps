import logging

from flask import Flask
from flask_bootstrap import Bootstrap
from flask_cors import CORS

from .config import config

logger = logging.getLogger(__name__)

bootstrap = Bootstrap()
cors = CORS()


def create_app(config_name):
    logger.info(f"logger: Creating flask app with config {config_name}")

    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    bootstrap.init_app(app)
    cors.init_app(app)

    with app.app_context():

        # The main application entry
        from .main import main_bp

        app.register_blueprint(main_bp)

        # ml datasets app
        from .ml_datasets import ml_datasets_bp

        app.register_blueprint(ml_datasets_bp)

        # Register dash apps
        from qcarchive_webapps.reaction_viewer.index import ReactionViewerApp

        ReactionViewerApp(app, "/reaction_viewer/")

        # Compile assets (JS, SCSS)
        from .assets import compile_assets

        compile_assets(app)

        return app
