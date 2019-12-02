import dash_html_components as html

# TODO: add custom layout of the Dash app here
layout = html.Div(
    [
        # Header
        html.Div(
            [
                html.H3('Education Dash app',
                         className='app-title'),
            ]),
    ],
    className='container')