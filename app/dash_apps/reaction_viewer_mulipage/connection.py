
from flask import current_app, g
import qcportal as ptl

def get_client():
    if 'connection' not in g:
        uri = current_app.config['QCPORTAL_URI']

        if uri:
            g.connection = ptl.FractalClient(uri)
        else:
            g.connection = ptl.FractalClient()

    return g.connection
