from dataclasses import dataclass
from typing import Optional

import pytest
from multidict import CIMultiDictProxy

from app import create_app


@pytest.fixture(scope="session")
def app():
    app = create_app()
    app.config.update(
        {
            "TESTING": True,
        }
    )

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


@pytest.fixture
def make_request(test_client):
    def inner(
        url: str, method: str, params: Optional[dict] = None, data: Optional[dict] = None
    ) -> HTTPResponse:
        method_upper = method.upper()
        if method_upper == "GET":
            params = params or {}
            with test_client.get(url, params=params) as response:
                return HTTPResponse(
                    body=response.json() if response.ok else {},
                    headers=response.headers,
                    status=response.status,
                )

    return inner
