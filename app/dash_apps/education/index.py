"""Create a Dash app within a Flask app."""
from ..dash_base import DashAppBase
from .layout import layout
from dash.dependencies import Input, Output


class EducationApp(DashAppBase):
    """Create a Dash app."""

    def __init__(self, server, path, **kwargs):
        # override default
        external_stylesheets = ['/static/dist/css/education.css',
                                'https://fonts.googleapis.com/css?family=Lato',
                                'https://use.fontawesome.com/releases/v5.8.1/css/all.css']
        external_scripts = ['/static/dist/js/education.min.js']
        super().__init__(server, path,
                         external_stylesheets=external_stylesheets,
                         external_scripts=external_scripts)

    def get_layout(self, dashapp):
        return layout

    def register_callbacks(self, dashapp):
        # TODO: replace with the app call backs

        @dashapp.callback([
            Output('rds-display-value', 'children'),
        ], [Input('available-rds', 'value')])
        def display_value(value):
            """Add docs"""
            display_value = 'You have selected "{}"'.format(value)

            return display_value


        @dashapp.callback(Output('primary-graph', 'figure'), [
            Input('available-rds', 'value'),
        ])
        def build_graph(dataset):
            """Add docs"""

            return 'test'

