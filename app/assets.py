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

    bundles = {}
    bundles['scss_hugo'] = Bundle('src/scss/hugo/style.scss', 'src/scss/hugo/dashapps.scss',
                         depends='**/*.scss',
                         filters='libsass',
                         output='dist/css/hugo_styles.css')

    bundles['js_base'] = Bundle('src/js/main.js',  # add all site wide JS files
                       filters='jsmin',
                       output='dist/js/main.min.js')

    bundles['ml_datasets_css'] = Bundle('src/scss/ml_datasets/ml_datasets_bootstrap4.scss',
                         depends='**/*.scss',
                         filters='libsass',
                         output='dist/css/ml_datasets_bootstrap4.css')

    bundles['ml_js'] = Bundle('src/js/ml_datasets.js',
                       filters='jsmin',
                       output='dist/js/ml_datasets.min.js')

    bundles['edu_css'] = Bundle('src/scss/education/*.scss', 'src/scss/education/*.css',
                        depends='**/*.scss',
                        filters='libsass',
                        output='dist/css/education.css')

    bundles['edu_js'] = Bundle('src/js/education/*.js',
                       filters='jsmin',
                       output='dist/js/education.min.js')

    # to run less files directly from the browser
    app.config['LESS_RUN_IN_DEBUG'] = True  # True by default

    for name, bundle in bundles.items():
        assets.register(name, bundle)
        # if app.env == 'development':
            # less_bundle.build(force=True)
        # bundle.build(force=True, disable_cache=True)
        bundle.build()

