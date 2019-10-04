from flask import render_template, redirect, url_for, abort, flash, request,\
    current_app, make_response

from . import main


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
