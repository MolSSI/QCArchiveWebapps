import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
from . import reaction_viewer, reaction_page2
from ..dash_base import DashAppBase


class ReactionViewerAppMuli(DashAppBase):
    """Create a Dash app."""

    def get_layout(self, dashapp):
        return html.Div([
            dcc.Location(id='url', refresh=False),
            html.Div(id='page-content')
        ])


    def register_callbacks(self, dashapp):
        @dashapp.callback(Output('page-content', 'children'),
                      [Input('url', 'pathname')])
        def display_page(pathname):
            if pathname and pathname.endswith('/'):
                pathname = pathname[:-1]
            base = dashapp.config.url_base_pathname
            if pathname == base + 'app1':
                return reaction_viewer.layout
            elif pathname == base + 'app2':
                return reaction_page2.layout
            else:
                return html.Div([
                    dcc.Link('Link to page 1 (same app)', href=base+'app1'),
                    html.Br(),
                    dcc.Link('Link to page 2 (same app)', href=base+'app2')
                ])

        # Must register callbacks
        reaction_page2.callbacks(dashapp)
        reaction_viewer.callbacks(dashapp)





