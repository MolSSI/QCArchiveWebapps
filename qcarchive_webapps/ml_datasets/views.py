from flask import render_template

from . import ml_datasets_bp
from ..portal_client import get_client


def _get_qcarchive_collections():
    """Get Machine Learning datasets from QCArchive server"""

    # connection client to MolSSI server
    client = get_client()

    collection_types = ["dataset", "reactiondataset"]

    payload = {
        "meta": {
            "exclude": ["records", "contributed_values"],
        },
        "data": {"collection": None},
    }

    results = []
    for type in collection_types:
        payload["data"]["collection"] = type
        res = client._automodel_request("collection", "get", payload, full_return=False)
        results.extend(res)

    data = []
    for r in results:
        if "machine learning" in r["tags"]:
            r["tags"].remove("machine learning")
        else:  # skip non ML datasets
            continue

        if r["metadata"]:  # add metadata attributes
            r.update(r.pop("metadata"))

        r["data_points"] = f'{r["data_points"]:,}'

        if r["view_metadata"]:  # add metadata attributes
            r.update(r.pop("view_metadata"))
            # sizes from bytes to MB
            r["plaintext_size"] = int(r["plaintext_size"]) // 1024**2
            r["plaintext_size"] = f'{r["plaintext_size"]:,}'

            r["hdf5_size"] = int(r["hdf5_size"]) // 1024**2
            r["hdf5_size"] = f'{r["hdf5_size"]:,}'

        data.append(r)

    return data


@ml_datasets_bp.route("/list/")
def ml_datasets_list():

    data = _get_qcarchive_collections()

    return {"data": data}


@ml_datasets_bp.route("/")
def ml_datasets():
    return render_template("ml_datasets/index.html")
