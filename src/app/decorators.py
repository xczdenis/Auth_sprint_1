from functools import wraps
from http import HTTPStatus
from typing import Any

from flask import current_app, jsonify, request
from flask_jwt_extended import get_jwt


def superuser_required(request_methods: list[str] | None = None) -> Any:
    def wrapper(fn):
        @wraps(fn)
        def decorator(*args, **kwargs):
            if not request_methods or request.method in request_methods:
                claims = get_jwt()
                is_superuser = claims.get("is_superuser")
                if not is_superuser:
                    return jsonify(msg="Permission denied"), HTTPStatus.FORBIDDEN
            return current_app.ensure_sync(fn)(*args, **kwargs)

        return decorator

    return wrapper
