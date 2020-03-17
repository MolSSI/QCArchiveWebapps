import logging
import time
from textwrap import dedent
import traceback
from contextlib import contextmanager

import dash_bio as dashbio
import dash_core_components as dcc
import dash_html_components as html
from dash import Dash
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate

import dash_bootstrap_components as dbc

from ... import cache
from ...models import save_access
from ..dash_base import DashAppBase
from ..dash_converters import molecule_to_d3moljs
from .connection import get_client

logger = logging.getLogger(__name__)

SHOW_TIME = False
CACHE_TIMEOUT = 3600 * 24 * 60  # Two months, effectively no timeout

CARD_HEADER_STYLE = {"background": "rgba(0,126,255,.08)"}


def list_collections():
    client = get_client()

    names = list(client.list_collections("reactiondataset").reset_index()["name"])
    return [{"label": k, "value": k} for k in names]


@cache.memoize(timeout=CACHE_TIMEOUT)
def get_collection_metadata(dataset):
    """This is the function to use if you don't want ds.df.
    Since the return only has metadata, no `ds.df` will be returned.
    """
    client = get_client()
    ds = client.get_collection("reactiondataset", dataset)

    return ds


@contextmanager
def collection_df_manager(dataset):
    t = time.time()
    key = f"rd_df_dataset_cache_{dataset}"

    # Specialized caching code to be used when the ds.df is needed
    if cache.get(key) is not None:
        ds = cache.get(key)
        logger.debug(f"Pulled {dataset} from cache in {time.time() - t}s.")
    else:
        ds = get_collection_metadata(dataset)
        logger.debug(f"Pulled {dataset} from remote in {time.time() - t}s.")

    current_cols = set(ds.df.columns)

    yield ds

    # Save this back if columns are updated from ds.visualize
    if set(ds.df.columns) != current_cols:
        t = time.time()
        cache.set(key, ds, timeout=CACHE_TIMEOUT)
        logger.debug(f"Set {dataset} cache in {time.time() - t}s.")
    else:
        logger.debug(f"{dataset} did not change, no cache update required.")


def get_history_values(name, category):

    ds = get_collection_metadata(name)

    methods = ds.list_values(native=True).reset_index()[category].unique()
    if category == "method":
        return [{"label": k.upper(), "value": k} for k in methods]
    else:
        return [{"label": k, "value": k} for k in methods]


class ReactionViewerApp(DashAppBase):
    """Create a Dash app."""

    layout = html.Div(
        [
            dbc.Alert(
                "The app is in an alpha state and may contain incorrect results.",
                color="warning",
            ),
            ### Header
            dbc.Row([dbc.Col([html.H3("Benchmark Dataset Viewer")])]),
            ### Main selectors
            dbc.Row(
                [
                    dbc.Col([dbc.Label("Choose a dataset:")], width=3),
                    dbc.Col(
                        [
                            dcc.Dropdown(
                                id="available-rds",
                                options=list_collections(),
                                value="S22",
                            )
                        ]
                    ),
                ]
            ),
            dbc.Row(
                [
                    dbc.Col([dbc.Label("Select methods to display:")], width=3),
                    dbc.Col(
                        [
                            dcc.Dropdown(
                                id="rds-available-methods", options=[], multi=True
                            )
                        ]
                    ),
                ]
            ),
            dbc.Row(
                [
                    dbc.Col([dbc.Label("Select basis sets to display:")], width=3),
                    dbc.Col(
                        [dcc.Dropdown(id="rds-available-basis", options=[], multi=True)]
                    ),
                    # multi=True,
                ]
            ),
            ### Radio Options
            dbc.Row(
                [
                    dbc.Col(
                        [
                            dbc.Label("Group by:"),
                            # dbc.ButtonGroup(
                            #    [
                            #        dbc.Button("None", color="primary", active=True),
                            #        dbc.Button("Method", color="primary"),
                            #        dbc.Button("Basis", color="primary"),
                            #        dbc.Button("D3", color="primary"),
                            #    ]
                            # ),
                            dbc.RadioItems(
                                id="rds-groupby",
                                options=[
                                    {"label": "None", "value": "none"},
                                    {"label": "Method", "value": "method"},
                                    {"label": "Basis", "value": "basis"},
                                    {"label": "D3", "value": "d3"},
                                ],
                                # className="btn-group btn-group-toggle",
                                # inputClassName="form-check-input",
                                # labelClassName="btn btn-primary form-check-label",
                                # labelCheckedClassName="active",
                                # custom=False,
                                switch=True,
                                value="none",
                                # inline=True,
                            ),
                        ]
                    ),
                    dbc.Col(
                        [
                            dbc.Label("Metric:"),
                            dbc.RadioItems(
                                id="rds-metric",
                                options=[
                                    {"label": "UE", "value": "UE"},
                                    {"label": "URE", "value": "URE"},
                                ],
                                value="UE",
                                switch=True,
                                # inline=True,
                            ),
                        ]
                    ),
                    dbc.Col(
                        [
                            dbc.Label("Plot type:"),
                            dbc.RadioItems(
                                id="rds-kind",
                                options=[
                                    {"label": "Bar", "value": "bar"},
                                    {"label": "Violin", "value": "violin"},
                                ],
                                value="bar",
                                # inline=True,
                                switch=True,
                            ),
                        ]
                    ),
                    dbc.Col(
                        [
                            dbc.Label("Counterpoise correction:"),
                            dbc.RadioItems(
                                id="rds-stoich",
                                options=[
                                    {"label": "CP", "value": "cp"},
                                    {"label": "noCP", "value": "default"},
                                ],
                                value="cp",
                                # inline=True,
                                switch=True,
                            ),
                        ]
                    ),
                ],
                className="my-3",
            ),
            ### Primary data visualizer
            dbc.Card(
                [
                    dbc.CardHeader(id="info-dataset-name", style=CARD_HEADER_STYLE),
                    dbc.Toast(
                        [html.P(id="graph-toast-error-message")],
                        id="graph-toast-error",
                        header="An error occured!",
                        icon="danger",
                        dismissable=True,
                        is_open=False,
                        style={"max-width": "100%"},
                    ),
                    dcc.Loading(
                        id="loading-1",
                        children=[dcc.Graph(id="primary-graph")],
                        type="default",
                        style={"height": "450px"},
                    ),
                ],
                className="mb-3",
            ),
            ### Molecule Explorer
            dbc.Card(
                [
                    dbc.CardHeader("Molecule Explorer", style=CARD_HEADER_STYLE),
                    dcc.Dropdown(
                        id="available-molecules",
                        options=[],
                        multi=False,
                        className="p-2",
                    ),
                    dbc.Toast(
                        [html.P(id="molecule-toast-error-message")],
                        id="molecule-toast-error",
                        header="An error occured!",
                        icon="danger",
                        dismissable=True,
                        is_open=False,
                        style={"max-width": "100%"},
                    ),
                    dcc.Loading(
                        id="loading-2",
                        children=[
                            dashbio.Molecule3dViewer(
                                id="dash-bio-3d",
                                styles={},
                                modelData={"atoms": [], "bonds": []},
                            )
                        ],
                        type="default",
                        style={"height": "500px"}
                        # styles=styles_data, modelData=model_data)
                    ),
                ],
                className="mb-3",
            ),
            ### Info
            dbc.Card(
                [
                    dbc.CardHeader("Database Information", style=CARD_HEADER_STYLE),
                    dbc.ListGroup(id="dataset-information", flush=True),
                ]
            ),
        ],
        className="container py-3",
    )

    def get_layout(self, dashapp):
        return self.layout

    def register_callbacks(self, dashapp):
        @dashapp.callback(
            [
                Output("rds-available-methods", "options"),
                Output("rds-available-basis", "options"),
                Output("info-dataset-name", "children"),
                Output("available-molecules", "options"),
                Output("available-molecules", "value"),
                Output("dataset-information", "children"),
            ],
            [Input("available-rds", "value")],
        )
        def display_value(value):
            ds = get_collection_metadata(value)

            bases = get_history_values(value, "basis")
            try:
                bases.remove({"label": "None", "value": "None"})
            except:
                pass

            try:
                tmp = ds.data.metadata["citations"][0]["acs_citation"]
                tmp = tmp.replace("&amp", "&")

                authors, second = tmp.split("<em>")
                emph, remaining = second.split("</em>")

                bold, remaining = remaining.replace("<b>", "").split("</b>")
                italics, remaining = remaining.replace("<i>", "").split("</i>")

                doi = ds.data.metadata["citations"][0]["doi"]
                citation = html.P(
                    [
                        html.H5("Citation:"),
                        html.P(
                            [
                                authors,
                                html.Em(emph),
                                html.B(bold),
                                html.I(italics),
                                remaining,
                            ]
                        ),
                        html.P(
                            [
                                html.B("DOI: "),
                                html.A(
                                    doi, href=f"https://doi.org/{doi}", target="_blank"
                                ),
                            ]
                        ),
                    ]
                )
                # citation = citation.replace("</em>", "*").replace(
                #     "<em>", "*"
                # )  # Italics 1
                # citation = citation.replace("</i>", "*").replace(
                #     "<i>", "*"
                # )  # Italics 2
                # citation = citation.replace("</b>", "**").replace("<b>", "**")  # Bold
                # citation = citation.replace(", ***", "*, **").replace(
                #     "***, ", "**, *"
                # )  # HTML vs Markdown corrections

            except Exception as exc:
                logger.error(str(exc))
                citation = html.P(
                    [html.H5("Citation:"), html.I("No information available.")]
                )

                # dedent(
                #     f"""
                #     ## Citation:
                #     *No information available.*
                #     """
                # )

            mqcas_help = html.P(
                [
                    "We are still filling in data and expanding these Webapps. If you have features suggestions or bug reports please file them ",
                    html.A(
                        "here",
                        href="https://github.com/MolSSI/QCArchiveWebapps/issues/new/choose",
                        target="_blank",
                    ),
                    " or if you wish to expand the datasets, methods, or bases please open an issue ",
                    html.A(
                        "here",
                        href="https://github.com/MolSSI/MQCAS/issues/new/choose",
                        target="_blank",
                    ),
                    ".",
                ]
            )

            dataset_info = [dbc.ListGroupItem(x) for x in [citation, mqcas_help]]

            save_access(
                page="reaction_datasets",
                access_type="dataset_query",
                dataset_name=value,
            )
            mol_index = [{"label": x, "value": x} for x in ds.get_index()]

            return (
                get_history_values(value, "method"),
                bases,
                f"{ds.data.name}: {ds.data.tagline}",
                mol_index,
                mol_index[0]["value"],
                dataset_info,
            )

        @dashapp.callback(
            [
                Output("primary-graph", "figure"),
                Output("graph-toast-error", "is_open"),
                Output("graph-toast-error-message", "children"),
            ],
            [
                Input("available-rds", "value"),
                Input("rds-available-methods", "value"),
                Input("rds-available-basis", "value"),
                Input("rds-groupby", "value"),
                Input("rds-metric", "value"),
                Input("rds-kind", "value"),
                Input("rds-stoich", "value"),
            ],
        )
        def show_graph(dataset, method, basis, groupby, metric, kind, stoich):

            # Incomplete data, nothing to return
            if (method is None) or (basis is None):
                print("")
                return {}, False, None

            save_access(
                page="reaction_datasets",
                access_type="graph_query",
                dataset_name=dataset,
                method=method,
                basis=basis,
                groupby=groupby,
                metric=metric,
                kind=kind,
                stoich=stoich,
            )

            try:

                with collection_df_manager(dataset) as ds:

                    if groupby == "none":
                        groupby = None

                    t = time.time()
                    fig = ds.visualize(
                        method=method,
                        basis=basis + ["None"],
                        groupby=groupby,
                        metric=metric,
                        kind=kind,
                        stoich=stoich,
                        return_figure=True,
                    )
                    fig.update_layout(title_text=None, margin={"t": 25, "b": 25})
                    logger.debug(f"Built {dataset} graph in {time.time() - t}s.")

                return fig, False, None
            except Exception as exc:
                print(traceback.format_exc())
                tb = "\n".join(
                    traceback.format_exc(limit=0, chain=False).splitlines()[1:]
                )
                return {}, True, tb

        @dashapp.callback(
            [Output("rds-stoich", "options"), Output("rds-stoich", "value")],
            [Input("available-rds", "value")],
            [State("rds-stoich", "value")],
        )
        def toggle_counterpoise(dataset, current_stoich):
            ds = get_collection_metadata(dataset)

            if "cp" in ds.valid_stoich():
                return (
                    [
                        {"label": "CP", "value": "cp"},
                        {"label": "noCP", "value": "default"},
                    ],
                    current_stoich,
                )
            else:
                return (
                    [{"label": "N/A", "value": "default", "disabled": True}],
                    "default",
                )

        @dashapp.callback(
            [
                Output("dash-bio-3d", "modelData"),
                Output("dash-bio-3d", "styles"),
                Output("molecule-toast-error", "is_open"),
                Output("molecule-toast-error-message", "children"),
            ],
            [Input("available-molecules", "value")],
            [State("available-rds", "value")],
        )
        def show_molecule(molecule, dataset):

            blank_return = ({"atoms": [], "bonds": []}, {})

            if molecule is None:
                return blank_return + (False, None)

            try:
                key = f"rd_df_molecule_cache_{dataset}_{molecule}"
                d3moljs_data = cache.get(key)
                if d3moljs_data is None:
                    ds = get_collection_metadata(dataset)

                    mol = ds.get_molecules(subset=molecule).iloc[0, 0]
                    d3moljs_data = molecule_to_d3moljs(mol)
                    cache.set(key, d3moljs_data, timeout=CACHE_TIMEOUT)

                model_data, style_data = d3moljs_data
                return model_data, style_data, False, None
            except:
                print(traceback.format_exc())
                tb = "\n".join(
                    traceback.format_exc(limit=0, chain=False).splitlines()[1:]
                )
                return blank_return + (True, tb)
