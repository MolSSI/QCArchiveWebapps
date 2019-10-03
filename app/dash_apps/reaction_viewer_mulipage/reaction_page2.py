import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output


layout = html.Div([
    html.H3('App 2'),
    dcc.Dropdown(
        id='app-2-dropdown',
        options=[
            {'label': 'App 2 - {}'.format(i), 'value': i} for i in [
                'NYC', 'MTL', 'LA'
            ]
        ]
    ),
    html.Div(id='app-2-display-value'),
    dcc.Link('Go to App 1', href='/reaction_viewer/app1')
])


def callbacks(dashapp):

    @dashapp.callback(
        Output('app-2-display-value', 'children'),
        [Input('app-2-dropdown', 'value')])
    def display_value(value):
        return 'You have selected "{}"'.format(value)
