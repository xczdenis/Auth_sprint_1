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
    class TestClient:
        def __init__(self):
            self.client = app.test_client()
            self.base_url = "/api/v1"

        def get(self, url, params: dict | None = None, headers: dict | None = None):
            return self.client.get(self.base_url + url, query_string=params, headers=headers)

        def post(self, url: str, json: dict | None = None, headers: dict | None = None):
            return self.client.post(self.base_url + url, json=json, headers=headers)

    return TestClient()


@dataclass
class HTTPResponse:
    body: dict | list
    headers: CIMultiDictProxy[str]
    status: int


@pytest.fixture
def make_request(test_client):
    def inner(
        url: str, method: str, params: dict | None = None, data: dict | None = None
    ) -> HTTPResponse:
        params = params or {}
        data = data or {}
        if method.upper() == "GET":
            return test_client.get(url, query_string=params)
        if method.upper() == "POST":
            return test_client.post(url, json=data)

    return inner
