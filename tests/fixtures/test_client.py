import pytest

from tests.utils.api_client import APIClient


@pytest.fixture(scope="session")
def test_client(test_app):
    return APIClient(test_client=test_app.test_client())
