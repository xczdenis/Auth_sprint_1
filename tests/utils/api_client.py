from dataclasses import dataclass

from flask.testing import FlaskClient
from werkzeug.datastructures import Headers


@dataclass
class HTTPResponse:
    body: dict | list
    headers: Headers
    status_code: int


@dataclass
class APIClient:
    test_client: FlaskClient

    def get(self, url: str, **kwargs) -> HTTPResponse:
        return self.request("get", url, **kwargs)

    def post(self, url: str, **kwargs) -> HTTPResponse:
        return self.request("post", url, **kwargs)

    def delete(self, url: str, **kwargs) -> HTTPResponse:
        return self.request("delete", url, **kwargs)

    def put(self, url: str, **kwargs) -> HTTPResponse:
        return self.request("put", url, **kwargs)

    def request(self, method: str, url: str, **kwargs) -> HTTPResponse:
        kwargs["method"] = method.upper()

        headers = kwargs.pop("headers", {})
        headers["X-Request-ID"] = "test-request-id"

        response = self.test_client.open(url, headers=headers, **kwargs)
        return HTTPResponse(
            body=response.get_json(),
            headers=response.headers,
            status_code=response.status_code,
        )
