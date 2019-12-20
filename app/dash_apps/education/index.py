"""Create a Dash app within a Flask app."""
from ..dash_base import DashAppBase
from .layout import layout
from dash.dependencies import Input, Output, State
import dash
import dash_bootstrap_components as dbc
import dash_html_components as html
import dash_core_components as dcc
import dash_bio as dashbio
import six.moves.urllib.request as urlreq
from six import PY3
import json
import qcedu as edu
import os


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

        path1 = os.path.abspath('.')
        path2 = os.path.join(path1, 'app/static/src/js/education/model_data.js')
        path3 = os.path.join(path1, 'app/static/src/js/education/styles_data.js')

        model_data = open(path2).read()

        styles_data = open(path3).read()

        # if PY3:
        #     model_data = model_data.decode('utf-8')
        #     styles_data = styles_data.decode('utf-8')

        model_data = json.loads(model_data)
        styles_data = json.loads(styles_data)

        layout = html.Div([
                html.Div([
                    html.Div([
                        dbc.Row([
                            dbc.Col([
                                    dbc.Input(id="text_ide", placeholder="Explore molecules", type="text", list="molecular", style={'height': '60px', 'font-size': '20px'}),						
                                
                                    html.Table([
                                        html.Td(edu.datalist(id="molecular"))
                                    ], style={'table-layout': 'fixed', 'WORD-BREAK': 'break-all'})
                                ], width=5),
                        ], className='align-items-center', style={'padding-top': '70px'},  justify="center"),
                        dbc.Row([
                            dbc.Col(
                                html.P(html.H5("Search by common name, scienfic name, or formula"), className='text-secondary text-center'),
                            ),
                        ], className='align-items-center pt-3')
                    ], className='container')
                ], style={'background-image': 'url("https://mdbootstrap.com/img/Photos/Others/images/91.jpg")', 'height': '250px'}),

                html.Div([
                    dbc.Row([
                        dbc.Col(
                            edu.eduside(),
                                                
                            width={"size": 3},
                            className='pl-0 pr-0 .bg-white',
                            ),
                        dbc.Col(
                            html.Div([
                                dashbio.Molecule3dViewer(
                                    id='my-dashbio-molecule3d',
                                    styles=styles_data,
                                    modelData=model_data
                                ),
                                html.Hr(),
                                html.Div(id='molecule3d-output')
                            ]),
                            width={"size": 6},
                            className='pl-0 pr-0'
                        ),
                        dbc.Col(
                            dbc.ListGroup(
                                [
                                    dbc.ListGroupItem(
                                        [
                                            dbc.ListGroupItemHeading([
                                                html.P(html.H4("Information"), className='text-center')
                                                
                                            ]),
                                        ]
                                    ),
                                    dbc.ListGroupItem(
                                        [
                                            dbc.Row([
                                                dbc.Col(dbc.ListGroupItemText([
                                                    html.P(html.H6("Molecular Formula:"), className='text-center')
                                                ]),
                                                    width={"size": 5},
                                                ),
                                                dbc.Col(dbc.ListGroupItemText([
                                                    html.P("H20", id="data1", className='text-center')
                                                ]),
                                                    width={"size": 7},
                                                ),

                                            ])
                                        ]
                                    ),
                                    dbc.ListGroupItem(
                                        [
                                            dbc.Row([
                                                dbc.Col(dbc.ListGroupItemText([
                                                    html.Br(),
                                                    html.Br(),
                                                    html.P(html.H6("Chemical Names:"), className='text-center'),
                                                ]),
                                                    width={"size": 5},
                                                ),
                                                dbc.Col(dbc.ListGroupItemText([
                                                    html.P("water", className='text-center'),
				                		            html.P("dihydrgen oxide", className='text-center'),
				                		            html.P("purfied water", className='text-center'),
                                                ]),
                                                    width={"size": 7},
                                                ),

                                            ])
                                        ]
                                    ),
                                    dbc.ListGroupItem(
                                        [
                                            dbc.Row([
                                                dbc.Col(dbc.ListGroupItemText([
                                                    html.P(html.H6("Molecular Weight:"), className='text-center')
                                                ]),
                                                    width={"size": 5},
                                                ),
                                                dbc.Col(dbc.ListGroupItemText([
                                                    html.P("18.05 g/mol", className='text-center')
                                                ]),
                                                    width={"size": 7},
                                                ),

                                            ])
                                        ]
                                    ),
                                    dbc.ListGroupItem(
                                        [
                                            dbc.Row([
                                                dbc.Col(dbc.ListGroupItemText([
                                                    html.P(html.H6("PubChem CID (?):"), className='text-center')
                                                ]),
                                                    width={"size": 5},
                                                ),
                                                dbc.Col(dbc.ListGroupItemText([
                                                    html.P("962", className='text-center')
                                                ]),
                                                    width={"size": 7},
                                                ),

                                            ])
                                        ]
                                    ),
                                    dbc.ListGroupItem(
                                        [
                                            dbc.Row([
                                                dbc.Col(dbc.ListGroupItemText([
                                                    html.Br(),
                                                    html.Br(),
                                                    html.Br(),
                                                    html.P(html.H6("Physical Properties:"), className='text-center')
                                                ]),
                                                    width={"size": 5},
                                                ),
                                                dbc.Col(dbc.ListGroupItemText([
                                                    html.P("clear", className='text-center'),
				                		            html.P("colorless", className='text-center'),
				                		            html.P("odorless", className='text-center'),
				                		            html.P("tasteless", className='text-center'),
				                		            html.P("freezes below 0 ℃", className='text-center'),
				                		            html.P("boils above 100 ℃", className='text-center'),
                                                ]),
                                                    width={"size": 7},
                                                ),

                                            ])
                                        ]
                                    ),
                                    dbc.ListGroupItem(
                                        [
                                            dbc.Row([
                                                dbc.Col(dbc.ListGroupItemText([
                                                    html.Br(),
                                                    html.P(html.H6("Chemical Safety:"), className='text-center')
                                                ]),
                                                    width={"size": 5},
                                                ),
                                                dbc.Col(dbc.ListGroupItemText([
                                                    html.P((html.A(html.H6("Laboratory"), href='#')), className='text-center'),
                                                    html.P((html.A(html.H6("Safety Summary"), href='#')), className='text-center'),
                                                    html.P((html.A(html.H6("(LCSS) Datasheet"), href='#')), className='text-center'),
                                                ]),
                                                    width={"size": 7},
                                                ),

                                            ])
                                        ]
                                    ),
                                ]),
                            width={"size": 3},
                            style={'background-color':'white'},
                            className='pl-0 pr-0'
                            ),
                    ]),
                ], className='container-fluid')

        ])

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
        
        #TODO: replace data in right table
        @dashapp.callback(Output('data1', 'children'), [
            Input('text_ide', 'value'),
        ])
        def update_right_table(input_value):
	        if input_value is None:
		        return "H2O"
	        else:
		        return input_value

        #TODO replace the 3D model
        @dashapp.callback(Output('my-dashbio-molecule3d', 'modelData'), [
            Input('text_ide', 'value'),
        ])
        def update_graph(value):
            """Add docs"""

            pass


