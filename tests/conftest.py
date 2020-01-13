import pytest
from app import create_app


@pytest.fixture(scope="session")
def app():
    app = create_app(config_name='testing')

    with app.app_context():
        yield app


@pytest.fixture(scope="module")
def flask_test_client(app):
    with app.test_client() as test_client:
        yield test_client
