from http import HTTPStatus

from flask import request

from movies_auth.app.common.exceptions import AppHTTPException


def request_id_middleware(app):
    @app.before_request
    def before_request():
        request_id = request.headers.get("X-Request-Id")
        if not request_id:
            raise AppHTTPException("Request id is required", HTTPStatus.BAD_REQUEST)
