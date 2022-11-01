from functools import wraps
from http import HTTPStatus
from typing import Any

from flask import current_app, jsonify, request
from flask_jwt_extended import get_jwt

from app.pagination import get_pagination_params, paginate_list


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


def paginate(page_size: int | None = None) -> Any:
    def wrapper(fn):
        @wraps(fn)
        def decorator(*args, **kwargs):
            fn_result = current_app.ensure_sync(fn)(*args, **kwargs)
            if isinstance(fn_result, list):
                _page_size, _page_number = get_pagination_params(request, page_size=page_size)
                paginated_page = paginate_list(
                    page_size=int(_page_size),
                    page_number=int(_page_number),
                    results=fn_result,
                )
                return jsonify(paginated_page.dict())
            return fn_result

        return decorator

    return wrapper
