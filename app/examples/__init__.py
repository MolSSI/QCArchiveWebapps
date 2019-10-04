from flask import Blueprint

examples = Blueprint('examples', __name__)

from . import views, errors
from ..models import Permission


@examples.app_context_processor
def inject_permissions():
    return dict(Permission=Permission)
