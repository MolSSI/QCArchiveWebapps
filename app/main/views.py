from flask import render_template, redirect, url_for, abort, flash, request,\
    current_app, make_response

from . import main
from .. import cache
import json
import os
from random import randint
import qcportal as plt

# @main.after_app_request
# def after_request(response):
#     for query in get_debug_queries():
#         if query.duration >= current_app.config['FLASKY_SLOW_DB_QUERY_TIME']:
#             current_app.logger.warning(
#                 'Slow query: %s\nParameters: %s\nDuration: %fs\nContext: %s\n'
#                 % (query.statement, query.parameters, query.duration,
#                    query.context))
#     return response


@main.route('/shutdown')
def server_shutdown():
    if not current_app.testing:
        abort(404)
    shutdown = request.environ.get('werkzeug.server.shutdown')
    if not shutdown:
        abort(500)
    shutdown()
    return 'Shutting down...'


@main.route('/')
def index():
    apps = [
        {'name': 'Reaction Viewer', 'link': '/reaction_viewer/'},
        {'name': 'App inside an iFrame', 'link': '/app_in_iframe/'},
        {'name': 'Example Dash with different style', 'link': '/dash_example/'},
        {'name': 'App with multiple pages', 'link': '/reaction_multi/'},
    ]
    return render_template('index.html', apps=apps)

@main.route('/app_in_iframe/')
def app_in_iframe():
    return render_template('app_in_iframe.html')

# @main.route('/all')
# @login_required
# def show_all():
#     resp = make_response(redirect(url_for('.index')))
#     resp.set_cookie('show_followed', '', max_age=30*24*60*60)
#     return resp

@main.route('/ml_datasets/')
def ml_datasets():

    return render_template('ml_datasets.html')


@cache.cached()  # timeout in config
def _get_qcarchive_collections():
    """Get Machine Learning datasets from QCArchive server"""

    # connection client to MolSSI server
    client = plt.FractalClient()

    collection_types = ['dataset', 'reactiondataset']

    payload = {
        "meta": {
            "exclude": ["records", "contributed_values"],
        },
        "data": {"collection": None}
    }

    results = []
    for type in collection_types:
        # must have the type to use exclude functionality
        payload['data']['collection'] = type
        # HTTP request to load the data
        res = client._automodel_request("collection", "get", payload, full_return=False)
        results.extend(res)

    print('Total: ', len(results))

    data = []
    for r in results:
        if "machine learning" in r["tags"]:
            r["tags"].remove("machine learning")
        else:   # skip non ML datasets
            continue

        if r['metadata']:  # add metadata attributes
            r.update(r.pop("metadata"))

        data.append(r)

    # data_path = os.path.join(current_app.root_path, 'data', 'server_all_response.json')
    # json.dump(data, open(data_path, 'w'))

    return data


@main.route('/ml_datasets_list/')
def ml_datasets_list():

    data = _get_qcarchive_collections()

    return {'data': data}