from ..dash_base import DashAppBase
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output


class TestViewerApp(DashAppBase):

    def get_layout(self, dashapp):
        return html.Div([
                html.H3('Test app'),
                dcc.Dropdown(
                    id='app-2-dropdown',
                    options=[
                        {'label': 'App 2 - {}'.format(i), 'value': i} for i in [
                            'NYC', 'MTL', 'LA'
                        ]
                    ]
                ),
                html.Div(id='app-2-display-value'),
                dcc.Link('Go to App 1', href='/reaction_viewer/app1'),
                dcc.Link('Go to App 2', href='/reaction_viewer/app2'),
                dcc.Link('Go home', href='/')
            ])


    def register_callbacks(self, dashapp):

        @dashapp.callback(
            Output('app-2-display-value', 'children'),
            [Input('app-2-dropdown', 'value')])
        def display_value(value):
            return 'You have selected "{}"'.format(value)
