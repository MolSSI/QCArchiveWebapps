from dash import Dash
import dash_core_components as dcc
import dash_bootstrap_components as dbc
import dash_html_components as html
from dash.dependencies import Input, Output
from ..dash_base import DashAppBase
from ... import cache
from .connection import get_client
import dash_bootstrap_components as dbc


def list_collections():
    client = get_client()
    collections = client.list_collections("reactiondataset")

    names = list(client.list_collections("reactiondataset").reset_index()["name"])
    return [{"label": k, "value": k} for k in names]

@cache.memoize()
def get_collection(name):
    client = get_client()
    ds = client.get_collection("reactiondataset", name)

    return ds

def get_history_values(name, category):

    ds = get_collection(name)

    methods = ds.list_values().reset_index()[category].unique()
    if category == "method":
        return [{"label": k.upper(), "value": k} for k in methods]
    else:
        return [{"label": k, "value": k} for k in methods]


class ReactionViewerApp(DashAppBase):
    """Create a Dash app."""

    def __init__(self, server, path, **kwargs):
        # override default
        external_stylesheets = ['/static/dist/css/reactionViewer.css']

        super().__init__(server, path,
                        external_stylesheets=external_stylesheets)

    layout = html.Div(
    [
        dbc.Alert("The app is in a pre-alpha state and is for demonstration purposes only.", color="warning"),
        # Header
        dbc.Row([dbc.Col([
            html.H3('Reaction Dataset Viewer'),
        ])]),

        # Main selection tool
        # html.Div([
        #     html.Div([
        #         html.P('HOVER over a drug in the graph to the right to see its structure to the left.'),
        #         html.P('SELECT a drug in the dropdown to add it to the drug candidates at the bottom.')
        #     ],
        #              style={'margin-left': '10px'}),
        #     dcc.Dropdown(id='available-rds', options=list_collections(), className='twelve columns'),
        # ],
        #          className='row'),
        html.Div([
            html.Div([
                html.P('First select a reaction dataset to get started:'),
                #     html.P('SELECT a drug in the dropdown to add it to the drug candidates at the bottom.')
            ]),
            dcc.Dropdown(id='available-rds', className='dropdown', options=list_collections(), value="S22"),
            html.Div(id='rds-display-value'),
        ]),
        html.Br(),
        html.Div([
            html.Label('Select methods to display:'),
            dcc.Dropdown(id='rds-available-methods', className='dropdown', options=[], multi=True),
            html.Br(),
            html.Label('Select bases to display:'),
            dcc.Dropdown(id='rds-available-basis', className='dropdown', options=[], multi=True),
            # multi=True,
        ]),
        html.Br(),
        html.Div([
            dbc.Row([
                dbc.Col(
                    # dbc.FormGroup([
                    #     dbc.Label('Groupby:'),
                    #     dbc.RadioItems(id='rds-groupby',
                    #        options=[{
                    #            "label": x.title(),
                    #            "value": x
                    #        } for x in ["method", "basis", "d3"]],
                    #        value=None, custom=False),
                    # ]),
                    dbc.FormGroup([
                        dbc.Label('Groupby:'),
                        html.Br(),
                        dbc.DropdownMenu([
                            dbc.DropdownMenuItem("method"),
                            dbc.DropdownMenuItem("basis"),
                            dbc.DropdownMenuItem("d3")],
                            label="method",
                            group=True,
                            id='rds-groupby',
                        ),
                    ]),
                    className='md-4'
                ),
                dbc.Col(
                    dbc.FormGroup([
                        dbc.Label('Metric:'),
                        html.Br(),
                         dbc.ButtonGroup([
                            dbc.Button("UE"), 
                            dbc.Button("URE")
                        ])
                        # dbc.RadioItems(id='rds-metric', 
                        #    options=[{
                        #        "label": "UE",
                        #        "value": "UE"
                        #    }, {
                        #        "label": "URE",
                        #        "value": "URE"
                        #    }],
                        #    value="UE", custom=False),
                    ], id='rds-metric'),
                    className='md-4'
                ),
                dbc.Col(
                    # dbc.FormGroup([
                    #     dbc.Label('Plot type:'),
                    #     dbc.RadioItems(id='rds-kind',
                    #        options=[{
                    #            "label": "Bar",
                    #            "value": "bar"
                    #        }, {
                    #            "label": "Violin",
                    #            "value": "violin"
                    #        }],
                    #        value="bar", custom=False),
                    # ]),
                    dbc.FormGroup([
                        dbc.Label('Plot type:'),
                        html.Br(),
                        dbc.ButtonGroup([
                            dbc.Button("Bar"), 
                            dbc.Button("Violin")
                            ])
                     ], id='rds-kind'),
                    className='md-4'
                ),

                dbc.Col([
                    dbc.Label('Counterpoise Correction:'),
                    dbc.RadioItems(id='rds-stoich',
                                   options=[{
                                       "label": "CP",
                                       "value": "cp"
                                   }, {
                                       "label": "noCP",
                                       "value": "default"
                                   }],
                                   value="cp",
                                   inline=True),
                    ]),

            ]),

    ]),
        dcc.Graph(id='primary-graph')
    ],
    className='container')


    def get_layout(self, dashapp):
        return self.layout


    def register_callbacks(self, dashapp):

        @dashapp.callback([
            Output('rds-display-value', 'children'),
            Output('rds-available-methods', 'options'),
            Output('rds-available-basis', 'options')
        ], [Input('available-rds', 'value')])
        def display_value(value):
            display_value = 'You have selected "{}"'.format(value)

            return display_value, get_history_values(value, "method"), get_history_values(value, "basis")


        @dashapp.callback(Output('primary-graph', 'figure'), [
            Input('available-rds', 'value'),
            Input('rds-available-methods', 'value'),
            Input('rds-available-basis', 'value'),
            Input('rds-groupby', 'value'),
            Input('rds-metric', 'value'),
            Input('rds-kind', 'value'),
            Input('rds-stoich', 'value'),
        ])
        def build_graph(dataset, method, basis, groupby, metric, kind, stoich):

            key = f"rd_df_dataset_cache_{dataset}"
            if cache.get(key) is not None:
                ds = cache.get(key)
            else:
                ds = get_collection(dataset)

            history = ds.list_values(method=method, basis=basis)
            if (method is None) or (basis is None):
                print("")
                return {}

            if groupby == "none":
                groupby = None
            fig = ds.visualize(method=method, basis=basis, groupby=groupby, metric=metric, kind=kind, stoich=stoich, return_figure=True)

            cache.set(key, ds)

            return fig


