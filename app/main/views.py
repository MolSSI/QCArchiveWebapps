from flask import render_template, redirect, url_for, abort, flash, request,\
    current_app, make_response

from . import main
import json
import os
from random import randint


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

@main.route('/ml_datasets_list/')
def ml_datasets_list():

    # data_path = os.path.join(current_app.root_path, 'data', 'table_example.json')
    data_path = os.path.join(current_app.root_path, 'data', 'matt_sample.json')
    data_one = json.load(open(data_path))

    data = {}
    data['data'] = [data_one.copy() for i in range(30)]

    for i, d in enumerate(data['data']):
        d['name'] = d['name'] + ' - ' + str(i)
        d['data_points'] = randint(100, 1000)
        if d['data_points'] < 500:
            d['view_url_plaintext'] = 'molssi.org';

    return data