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


class EducationApp(DashAppBase):
    """Create a Dash app."""

    def __init__(self, server, path, **kwargs):
        # override default
        external_stylesheets = ['/static/dist/css/education.css',
                                'https://fonts.googleapis.com/css?family=Lato',
                                'https://use.fontawesome.com/releases/v5.8.1/css/all.css',
                                'https://codepen.io/chriddyp/pen/bWLwgP.css']
        external_scripts = ['/static/dist/js/education.min.js']

        super().__init__(server, path,
                        external_stylesheets=external_stylesheets,
                        external_scripts=external_scripts)



    def get_layout(self, dashapp):
        model_data = urlreq.urlopen(
            'https://raw.githubusercontent.com/plotly/dash-bio-docs-files/master/' +
            'mol3d/model_data.js'
        ).read()

        styles_data = urlreq.urlopen(
            'https://raw.githubusercontent.com/plotly/dash-bio-docs-files/master/' +
            'mol3d/styles_data.js'
        ).read()

        if PY3:
            model_data = model_data.decode('utf-8')
            styles_data = styles_data.decode('utf-8')

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
                                html.P(html.H2("Search by common name, scienfic name, or formula"), className='text-secondary text-center'),
                            ),
                        ], className='align-items-center', style={'padding-top': '5px'})
                    ], className='container')
                ], style={'background-image': 'url("https://mdbootstrap.com/img/Photos/Others/images/91.jpg")', 'height': '250px'}),

                html.Div([
                    dbc.Row([
                        dbc.Col(
                            edu.eduside(),
                                                
                            width={"size": 3},
                            style={'background-color':'white'},
                            className='pl-0 pr-0',
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
                                                html.P(html.H1("Information"), className='text-center')
                                                
                                            ]),
                                        ]
                                    ),
                                    dbc.ListGroupItem(
                                        [
                                            dbc.Row([
                                                dbc.Col(dbc.ListGroupItemText([
                                                    html.P(html.H4("Molecular Formula:"), className='text-center')
                                                ]),
                                                    width={"size": 5},
                                                ),
                                                dbc.Col(dbc.ListGroupItemText([
                                                    html.P("H20", id="data1", className='text-center', style={'font-size': '12px'})
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
                                                    html.P(html.H4("Chemical Names:"), className='text-center'),
                                                ]),
                                                    width={"size": 5},
                                                ),
                                                dbc.Col(dbc.ListGroupItemText([
                                                    html.P("water", className='text-center', style={'font-size': '12px'}),
				                		            html.P("dihydrgen oxide", className='text-center', style={'font-size': '12px'}),
				                		            html.P("purfied water", className='text-center', style={'font-size': '12px'}),
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
                                                    html.P(html.H4("Molecular Weight:"), className='text-center')
                                                ]),
                                                    width={"size": 5},
                                                ),
                                                dbc.Col(dbc.ListGroupItemText([
                                                    html.P("18.05 g/mol", className='text-center', style={'font-size': '12px'})
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
                                                    html.P(html.H4("PubChem CID (?):"), className='text-center')
                                                ]),
                                                    width={"size": 5},
                                                ),
                                                dbc.Col(dbc.ListGroupItemText([
                                                    html.P("962", className='text-center', style={'font-size': '12px'})
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
                                                    html.P(html.H4("Physical Properties:"), className='text-center')
                                                ]),
                                                    width={"size": 5},
                                                ),
                                                dbc.Col(dbc.ListGroupItemText([
                                                    html.P("clear", className='text-center', style={'font-size': '12px'}),
				                		            html.P("colorless", className='text-center', style={'font-size': '12px'}),
				                		            html.P("odorless", className='text-center', style={'font-size': '12px'}),
				                		            html.P("tasteless", className='text-center', style={'font-size': '12px'}),
				                		            html.P("freezes below 0 ℃", className='text-center', style={'font-size': '12px'}),
				                		            html.P("boils above 100 ℃", className='text-center', style={'font-size': '12px'}),
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
                                                    html.P(html.H4("Chemical Safety:"), className='text-center')
                                                ]),
                                                    width={"size": 5},
                                                ),
                                                dbc.Col(dbc.ListGroupItemText([
                                                    html.P((html.A(html.H4("Laboratory"), href='#')), className='text-center'),
                                                    html.P((html.A(html.H4("Safety Summary"), href='#')), className='text-center'),
                                                    html.P((html.A(html.H4("(LCSS) Datasheet"), href='#')), className='text-center'),
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


