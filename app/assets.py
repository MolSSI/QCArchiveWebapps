from flask_assets import Environment, Bundle


def compile_assets(app):
    """Configure authorization asset bundles."""
    assets = Environment(app)
    Environment.auto_build = True
    Environment.debug = False

    # less_bundle = Bundle('src/less/*.less',
    #                      filters='less,cssmin',
    #                      output='dist/css/styles.css',
    #                      extra={'rel': 'stylesheet/less' if app.debug else 'stylesheet'})

    scss_bundle = Bundle('src/scss/hugo/style.scss', 'src/scss/hugo/dashapps.scss',
                         depends='**/*.scss',
                         filters='libsass',
                         output='dist/css/hugo_styles.css')

    ml_datasets_css = Bundle('src/scss/ml_datasets/ml_datasets_bootstrap4.scss',
                         depends='**/*.scss',
                         filters='libsass',
                         output='dist/css/ml_datasets_bootstrap4.css')

    js_bundle = Bundle('src/js/*.js',
                       filters='jsmin',
                       output='dist/js/main.min.js')

    # to run less files directly from the browser
    app.config['LESS_RUN_IN_DEBUG'] = True  # True by default

    # assets.register('less_all', less_bundle)
    assets.register('scss_all', scss_bundle)
    assets.register('ml_datasets_css', ml_datasets_css)
    assets.register('js_all', js_bundle)

    # if app.env == 'development':
    # less_bundle.build(force=True)
    scss_bundle.build(force=True)
    js_bundle.build()
