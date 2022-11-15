from flask import Blueprint

ml_datasets_bp = Blueprint(
    "ml_dataset",
    __name__,
    url_prefix="/ml_datasets",
)

from . import views
