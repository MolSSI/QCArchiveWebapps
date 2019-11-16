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

    ml_js = Bundle('src/js/ml_datasets.js',
                       filters='jsmin',
                       output='dist/js/ml_datasets.min.js')

    js_base = Bundle('src/js/main.js',  # add all site wide JS files
                       filters='jsmin',
                       output='dist/js/main.min.js')

    # to run less files directly from the browser
    app.config['LESS_RUN_IN_DEBUG'] = True  # True by default

    # assets.register('less_all', less_bundle)
    assets.register('scss_all', scss_bundle)
    assets.register('ml_datasets_css', ml_datasets_css)
    assets.register('js_base', js_base)
    assets.register('ml_js', ml_js)

    # if app.env == 'development':
    # less_bundle.build(force=True)
    scss_bundle.build(force=True)
    js_base.build()
    ml_datasets_css.build()
    ml_js.build()
