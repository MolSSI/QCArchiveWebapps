from flask_assets import Environment, Bundle


def compile_assets(app):
    """Configure asset bundles."""
    assets = Environment(app)
    Environment.auto_build = True
    Environment.debug = False

    bundles = {}
    bundles["ml_datasets_css"] = Bundle(
        "src/scss/ml_datasets/ml_datasets_bootstrap4.scss",
        depends="**/*.scss",
        filters="libsass",
        output="dist/css/ml_datasets_bootstrap4.css",
    )

    bundles["ml_js"] = Bundle("src/js/ml_datasets.js", filters="jsmin", output="dist/js/ml_datasets.min.js")

    for name, bundle in bundles.items():
        assets.register(name, bundle)
        bundle.build()
