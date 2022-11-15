from flask import current_app
from qcportal import FractalClient

_portal_client = None


def get_client():
    global _portal_client
    if _portal_client is None:
        uri = current_app.config["QCFRACTAL_URI"]
        _portal_client = FractalClient(uri)

    return _portal_client
