from http import HTTPStatus

from flask import jsonify
from werkzeug.exceptions import UnsupportedMediaType

from movies_auth.app.common import exceptions


def make_error_response(msg: str):
    return jsonify(error=str(msg))


def register_handler(app, code_or_exception: type[Exception] | int, status_code: int | None = None):
    @app.errorhandler(code_or_exception)
    def handle_error(e):
        code = status_code
        if not code:
            if isinstance(code_or_exception, int):
                code = code_or_exception
            elif hasattr(e, "code"):
                code = e.code
        if hasattr(e, "description"):
            return make_error_response(e.description), code
        elif hasattr(e, "message"):
            return make_error_response(e.message), code
        return make_error_response(str(e)), code


def register(app):
    exception_status_code_map = {
        UnsupportedMediaType: HTTPStatus.UNSUPPORTED_MEDIA_TYPE,
        exceptions.AppHTTPException: None,
        exceptions.EntityAlreadyExists: HTTPStatus.CONFLICT,
        exceptions.AuthenticationError: HTTPStatus.UNAUTHORIZED,
        exceptions.EntityDoesntExists: HTTPStatus.NOT_FOUND,
        exceptions.Forbidden: HTTPStatus.FORBIDDEN,
        exceptions.OldPasswordIsIncorrect: HTTPStatus.UNAUTHORIZED,
    }

    for exception, status_code in exception_status_code_map.items():
        register_handler(app, exception, status_code)

    status_codes = [HTTPStatus.METHOD_NOT_ALLOWED, HTTPStatus.BAD_REQUEST, HTTPStatus.NOT_FOUND]

    for status_code in status_codes:
        register_handler(app, status_code)
