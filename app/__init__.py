from flask import Flask
from flask_bootstrap import Bootstrap
from flask_mail import Mail
from flask_moment import Moment
#from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_pagedown import PageDown
from config import config
from flask_caching import Cache
from flask_cors import CORS
from flask_mongoengine import MongoEngine
from flask_admin import Admin


db = MongoEngine()
# db = SQLAlchemy()
app_admin = Admin(name='QCArchive Logging Admin', template_mode='bootstrap3',
                  base_template='admin/custom_base.html')


bootstrap = Bootstrap()
mail = Mail()
moment = Moment()
pagedown = PageDown()
cache = Cache(config={'CACHE_TYPE': 'simple'})
cors = CORS()

login_manager = LoginManager()
login_manager.login_view = 'auth.login'


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    bootstrap.init_app(app)
    mail.init_app(app)
    moment.init_app(app)
    db.init_app(app)
    login_manager.init_app(app)
    pagedown.init_app(app)
    cache.init_app(app)
    cors.init_app(app)


    if app.config['SSL_REDIRECT']:
        from flask_sslify import SSLify
        sslify = SSLify(app)

    with app.app_context():

        # The main application entry
        from .main import main as main_blueprint
        app.register_blueprint(main_blueprint)

        # For authentication
        from .auth import auth as auth_blueprint
        app.register_blueprint(auth_blueprint, url_prefix='/auth')

        # # API if needed
        # from .api import api as api_blueprint
        # app.register_blueprint(api_blueprint, url_prefix='/api/v1')

        # create user roles
        from .models.users import update_roles
        update_roles()

        # To avoid circular import
        from app.admin import add_admin_views
        add_admin_views()

        # Then init the app
        app_admin.init_app(app)

        # Register dash apps
        register_dashapps(flask_server=app)

        # Compile assets (JS, SCSS, less)
        from .assets import compile_assets
        compile_assets(app)

        return app

    return app


def register_dashapps(flask_server):
    """Register dash apps using the flask server

        Add any new apps here
    """

    # from .dash_apps.education.index import EducationApp
    # EducationApp(flask_server, '/education/')

    from .dash_apps.dash_example.index import DashExampleApp
    DashExampleApp(flask_server, '/dash_example/')

    from .dash_apps.reaction_viewer.index import ReactionViewerApp
    ReactionViewerApp(flask_server, '/reaction_viewer/')

    from .dash_apps.reaction_viewer_mulipage.index import ReactionViewerAppMuli
    ReactionViewerAppMuli(flask_server, '/reaction_multi/')

    from .dash_apps.test_app.index import TestViewerApp
    TestViewerApp(flask_server, '/test/')


    return flask_server