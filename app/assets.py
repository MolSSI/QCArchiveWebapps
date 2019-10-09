from flask_assets import Environment, Bundle


def compile_assets(app):
    """Configure authorization asset bundles."""
    assets = Environment(app)
    Environment.auto_build = True
    Environment.debug = False

    less_bundle = Bundle('src/less/*.less',
                         filters='less,cssmin',
                         output='dist/css/styles.css',
                         extra={'rel': 'stylesheet/less' if app.debug else 'stylesheet'})

    scss_bundle = Bundle('src/scss/style.scss', 'src/scss/dashapps.scss',
                         depends='**/*.scss',
                         filters='pyscss',
                         output='dist/css/hugo_styles.css')

    js_bundle = Bundle('src/js/*.js',
                       filters='jsmin',
                       output='dist/js/main.min.js')

    # to run less files directly from the browser
    app.config['LESS_RUN_IN_DEBUG'] = False  # True by default
    # if app.debug:
    #     js_bundle.contents += 'http://lesscss.googlecode.com/files/less-1.3.0.min.js'

    assets.register('less_all', less_bundle)
    assets.register('scss_all', scss_bundle)
    assets.register('js_all', js_bundle)

    # if app.env == 'development':
    # less_bundle.build(force=True)
    scss_bundle.build(force=True)
    js_bundle.build()
