from dash import Dash
import dash_core_components as dcc
import dash_bootstrap_components as dbc
import dash_html_components as html
from dash.dependencies import Input, Output, State
from ..dash_base import DashAppBase
from ... import cache
from qc_time_estimator.processing.input_utils.categorical_data import list_basis_sets
from qc_time_estimator.predict import make_prediction
from qc_time_estimator.processing.data_management import current_model_exists
from qc_time_estimator.train_pipeline import run_training
from qcelemental.models import DriverEnum
import threading
import logging
import natural.date

logger = logging.getLogger(__name__)

# Error msgs
REQUIRED_MSG = "Please enter required fields with valid values"


def create_model():
    # Create the model only if doesn't exist
    # will download data from zenodo if the data file doesn't exist
    run_training(overwrite=False)


@cache.memoize()
def get_basis_sets_options():
    return [{"label": k, "value": v} for k, v in list_basis_sets()]


def required_tag():
    return html.Span("*", className="text-danger")


class QCTimeEstimatorApp(DashAppBase):
    """Create a Dash app."""

    def __init__(self, *args, **kwargs):

        # Run async
        if not current_model_exists():
            logger.info("Model doesn't exist yet, Calling create model thread...")
            threading.Thread(target=create_model).start()

        super().__init__(*args, **kwargs)

    layout = html.Div(
        [
            # dbc.Alert(
            #     "The app is in a pre-alpha state and is for demonstration purposes only.",
            #     color="warning",
            # ),
            ### Header
            dbc.Row(
                [dbc.Col([html.H3("QC Execution Time Estimator")])], className="mb-5"
            ),
            dbc.Alert(
                REQUIRED_MSG,
                id="error-msg",
                color="danger",
                is_open=False,
                dismissable=True,
            ),
            ### Main selectors
            dbc.Row(
                [
                    dbc.Col(
                        [
                            dbc.Label("Molecule (Formula, SMILES or InChI)"),
                            required_tag(),
                        ],
                        width=3,
                    ),
                    dbc.Col(
                        dcc.Input(id="molecule", type="text", size=50, value="H2O"),
                    ),
                ],
                className="mb-2",
            ),
            dbc.Row(
                [
                    dbc.Col([dbc.Label("Choose method"), required_tag()], width=3),
                    dbc.Col([dcc.Input(id="method", size=50, value="B3LYP")]),
                ],
                className="mb-2",
            ),
            dbc.Row(
                [
                    dbc.Col([dbc.Label("Choose Basis Set"), required_tag()], width=3),
                    dbc.Col(
                        [
                            dcc.Dropdown(
                                id="basis-set",
                                value="6-31G",
                                options=get_basis_sets_options(),
                            )
                        ]
                    ),
                ],
                className="mb-2",
            ),
            dbc.Row(
                [
                    dbc.Col([dbc.Label("Select Driver:"), required_tag()], width=3),
                    dbc.Col(
                        [
                            dcc.Dropdown(
                                id="driver",
                                options=[{"label": k, "value": k} for k in DriverEnum if k != "properties"],
                                value="energy",
                            ),
                        ]
                    ),
                ],
                className="mb-2",
            ),
            dbc.Row(
                [
                    dbc.Col([], width=3),
                    dbc.Col(
                        dcc.Checklist(
                            id="restricted",
                            options=[{"label": "Restricted", "value": "restricted"},],
                            value=["restricted"],
                            inputClassName="mr-2",
                        ),
                    ),
                ],
                className="mb-2",
            ),
            dbc.Row(
                [
                    dbc.Col([dbc.Label("Number of threads:")], width=3),
                    dbc.Col([dcc.Input(id="nthreads",
                                       value=1,
                                       type="number",
                                       min=1,
                                       max=32,
                                       step=1,
                                       size=25
                                       ),]),
                ],
                className="mb-2",
            ),
            dbc.Row(
                [
                    dbc.Col(
                        [dbc.Label("CPU Clock Speed (GHz):"), required_tag()], width=3
                    ),
                    dbc.Col(
                        [
                            dcc.Input(
                                id="cpu-clock-speed",
                                type="number",
                                min=1,
                                max=4,
                                step=0.1,
                                value=2.2,
                                size=25,  # TODO: Does not work!!
                                required=True
                            )
                            # options=[{"label": f'{k/1000} GHz', "value": k} for k in range(500, 7500, 500)]),
                        ],
                        width=2,
                    ),
                    html.Span("GHz"),
                ],
                className="mb-2",
            ),
            dbc.Row(
                [
                    dbc.Col([dbc.Label("CPU Launch Year:"), required_tag()], width=3),
                    dbc.Col(
                        [
                            dcc.Dropdown(
                                id="cpu-launch-year",
                                options=[
                                    {"label": k, "value": k}
                                    for k in range(2020, 2000, -1)
                                ],
                                value=2019,
                            ),
                        ]
                    ),
                ],
                className="mb-5",
            ),
            html.Hr(),
            dbc.Row(
                [
                    dbc.Col(
                        [
                            html.Button(
                                "Submit",
                                id="submit",
                                className="float-right btn-primary",
                            ),
                        ],
                    ),
                ],
                className="mb-5",
            ),
            html.Hr(),
            dbc.Card(
                [
                    dcc.Loading(
                        id="loading-1",
                        children=[
                            html.P(
                                [
                                    "Estimated Execution Time: ",
                                    html.Span(id="wall-time"),
                                ]
                            ),
                            html.P(["Model Version: ", html.Span(id="model-version"),]),
                            # dcc.Graph(id="primary-graph")
                        ],
                        type="default",
                        className="p-3",
                    )
                ]
            ),
        ],
        className="container",
    )

    def get_layout(self, dashapp):
        return self.layout

    def register_callbacks(self, dashapp):
        @dashapp.callback(
            [
                Output("wall-time", "children"),
                Output("model-version", "children"),
                Output("error-msg", "is_open"),
                Output("error-msg", "children"),
            ],
            [Input("submit", "n_clicks")],
            [
                State("molecule", "value"),
                State("method", "value"),
                State("basis-set", "value"),
                State("driver", "value"),
                State("restricted", "value"),
                State("nthreads", "value"),
                State("cpu-clock-speed", "value"),
                State("cpu-launch-year", "value"),
            ],
        )
        def update_output(
            n_clicks,
            molecule,
            method,
            basis_set,
            driver,
            restricted,
            nthreads,
            cpu_clock_speed,
            cpu_launch_year,
        ):

            if not n_clicks:
                return ["", "", False, ""]

            data = dict(
                molecule=molecule,
                method=method,
                basis_set=basis_set,
                driver=driver,
                restricted=True if "restricted" in restricted else False,
                nthreads=nthreads,
                cpu_clock_speed=cpu_clock_speed * 1000 if cpu_clock_speed else None,
                cpu_launch_year=cpu_launch_year,
            )

            logger.info(f"Running prediction for input: {data}")

            for k, v in data.items():
                # skip boolean variables
                if k == 'restricted':
                    continue
                if not v:
                    return ["", "", True, f"{REQUIRED_MSG} ({k})"]

            if not current_model_exists():
                return ["(running model training, please try again later)", "", False]

            try:
                ret = make_prediction(input_data=[data])
                return [
                    f'{natural.date.compress(ret["predictions"][0] * 3600)} ({ret["predictions"][0] * 3600:.4f})',
                    ret["version"],
                    False, "",
                ]
            except Exception as err:
                logger.error(f"Error in make_prediction.\n{err}")
                return ["", "", True, str(err)]
