import pytest

from movies_auth.app import app_settings
from movies_auth.main import app


@pytest.fixture(scope="session")
def test_app():
    app.config["SERVER_NAME"] = "{host}:{port}".format(host=app_settings.APP_HOST, port=app_settings.APP_PORT)
    app.config["APPLICATION_ROOT"] = "/"
    app.config["PREFERRED_URL_SCHEME"] = "http"
    app.config["TESTING"] = True

    with app.app_context():
        yield app
