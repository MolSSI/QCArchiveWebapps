from dash import Dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
from . import reaction_viewer, app2


def Add_Dash(server, path):
    """Create a Dash app."""

    external_stylesheets = [
        'https://codepen.io/chriddyp/pen/bWLwgP.css',
        'https://cdn.rawgit.com/plotly/dash-app-stylesheets/0e463810ed36927caf20372b6411690692f94819/dash-drug-discovery-demo-stylesheet.css'
    ]
    # external_scripts = ['/static/dist/js/includes/jquery.min.js',
    #                     '/static/dist/js/main.min.js']

    dashapp = Dash(server=server,
                    external_stylesheets=external_stylesheets,
                    # external_scripts=external_scripts,
                    url_base_pathname=path,  # will set both routes and requests pathname_prefix
                    # routes_pathname_prefix=path,
                    # requests_pathname_prefix=path,  # for middleware dispatcher
                    suppress_callback_exceptions=True)

    dashapp.server.config.from_mapping(QCPORTAL_URI=None)

    # Override the underlying HTML template
    # dashapp.index_string = html_layout

    dashapp.layout = html.Div([
        dcc.Location(id='url', refresh=False),
        html.Div(id='page-content')
    ])

    @dashapp.callback(Output('page-content', 'children'),
                  [Input('url', 'pathname')])
    def display_page(pathname):
        if pathname and pathname.endswith('/'):
            pathname = pathname[:-1]
        base = dashapp.config.url_base_pathname
        if pathname == base + 'app1':
            return reaction_viewer.layout()
        elif pathname == base + 'app2':
            return app2.layout
        else:
            return html.Div([dcc.Link('Reaction Viewer', href=base+'app1')])

    # Must register callbacks
    app2.register_callbacks(dashapp)
    reaction_viewer.register_callbacks(dashapp)

    return dashapp.server



