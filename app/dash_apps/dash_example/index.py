"""Create a Dash app within a Flask app."""
from pathlib import Path
import dash_table
import dash_html_components as html
import pandas as pd
from ..dash_base import DashAppBase


class DashExampleApp(DashAppBase):
    """Create a Dash app."""

    def __init__(self, server, path, **kwargs):
        # override default
        external_stylesheets = ['/static/dist/css/styles.css',
                                'https://fonts.googleapis.com/css?family=Lato',
                                'https://use.fontawesome.com/releases/v5.8.1/css/all.css']
        external_scripts = ['/static/dist/js/includes/jquery.min.js',
                            '/static/dist/js/main.min.js']
        super().__init__(server, path,
                         external_stylesheets=external_stylesheets,
                         external_scripts=external_scripts)

    def get_layout(self, dashapp):
        return html.Div(
        children=get_datasets(),
        id='dash-container'
      )

    def register_callbacks(self, dashapp):
        return

def get_datasets():
    """Return previews of all CSVs saved in /data directory."""
    p = Path('.')
    data_filepath = list(p.glob('data/*.csv'))
    arr = ['This is an example Plot.ly Dash App.']
    for index, csv in enumerate(data_filepath):
        df = pd.read_csv(data_filepath[index]).head(10)
        table_preview = dash_table.DataTable(
            id='table_' + str(index),
            columns=[{"name": i, "id": i} for i in df.columns],
            data=df.to_dict("rows"),
            sort_action="native",
            sort_mode='single'
        )
        arr.append(table_preview)
    return arr