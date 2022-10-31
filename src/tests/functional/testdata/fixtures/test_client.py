from dataclasses import dataclass

import pytest
from multidict import CIMultiDictProxy

from app import create_app


@pytest.fixture(scope="session")
def app():
    app = create_app()
    app.config.update({"TESTING": True})

    with app.app_context():
        yield app


@pytest.fixture(scope="session")
def test_client(app):
    return app.test_client()


@dataclass
class HTTPResponse:
    body: dict | list
    headers: CIMultiDictProxy[str]
    status: int
