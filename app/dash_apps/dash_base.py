from dash import Dash
import dash_core_components as dcc
import dash_bootstrap_components as dbc
import dash_html_components as html
from abc import ABC, abstractmethod


class DashAppBase(ABC):

    # defaults
    # external_stylesheets = [
    #     'https://codepen.io/chriddyp/pen/bWLwgP.css',
    #     'https://cdn.rawgit.com/plotly/dash-app-stylesheets/0e463810ed36927caf20372b6411690692f94819/dash-drug-discovery-demo-stylesheet.css'
    # ]
    external_stylesheets = [dbc.themes.BOOTSTRAP,
                            "/static/dist/css/hugo_styles.css"]
    external_scripts = ["https://cdnjs.cloudflare.com/ajax/libs/iframe-resizer/4.2.1/iframeResizer.contentWindow.min.js"]

    default_layout = html.Div([
            dcc.Location(id='url', refresh=False),
            html.H1('Default view'),
            html.Div(id='page-content')
    ])

    def __init__(self, server, path, **kwargs):
        """Initialize a dash app in the given flask server using the path prefix"""

        external_stylesheets = kwargs.pop('external_stylesheets', self.external_stylesheets)
        external_scripts = kwargs.pop('external_scripts', self.external_scripts)

        dashapp = Dash(server=server,
                       url_base_pathname=path,  # will set both routes and requests pathname_prefix
                       external_stylesheets=external_stylesheets,
                       external_scripts=external_scripts,
                       # don't include all js and css in all apps, only when needed
                       # assets_folder='static/dist',
                       # routes_pathname_prefix=path,
                       # requests_pathname_prefix=path,  # for middleware dispatcher
                       suppress_callback_exceptions=True,
                       **kwargs)

        dashapp.server.config.from_mapping(QCPORTAL_URI=None)

        # TODO: Override the underlying HTML template
        # dashapp.index_string = html_layout

        dashapp.layout = self.get_layout(dashapp)

        self.register_callbacks(dashapp)


    @abstractmethod
    def get_layout(self, dashapp):
        """Override it to define specific app layout"""
        return self.default_layout

    @abstractmethod
    def register_callbacks(self, dashapp):
        """Override it to Define callback methods"""
        pass


