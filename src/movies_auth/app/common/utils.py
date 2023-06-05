import json
import urllib.parse
from http import HTTPStatus
from typing import Any

import orjson
from flask import abort, jsonify, make_response, request
from flask_jwt_extended import create_access_token, create_refresh_token, get_jti

from movies_auth.app.common.types import Tokens


def obtain_auth_tokens(identity: str, is_superuser: bool = False) -> Tokens:
    additional_claims = {"is_superuser": is_superuser}
    refresh_token = create_refresh_token(identity=identity, additional_claims=additional_claims)

    additional_claims["refresh_token_jti"] = get_jti(refresh_token)
    access_token = create_access_token(identity=identity, additional_claims=additional_claims)

    return {"access_token": access_token, "refresh_token": refresh_token}


def get_parameter_from_request(key: str, default: Any | None = None, silent: bool = False):
    if request.method == "GET":
        storage = request.args
    else:
        if request.is_json:
            storage = request.json
        else:
            storage = request.form
    value = storage.get(key, default)
    if not silent and not value:
        abort_json("Parameter not provided: '%s'" % key, HTTPStatus.BAD_REQUEST)
    return value


def abort_json(msg: str, status_code: int = HTTPStatus.BAD_REQUEST):
    abort(make_response(jsonify(msg=msg), status_code))


def build_url(url, params: dict | None = None):
    if params:
        url += "?" if url.endswith("/") else "/?"
        url += urllib.parse.urlencode(params)
    return url


def make_key_from_args(*args, **kwargs) -> str:
    for k, v in kwargs.items():
        if hasattr(v, "__name__"):
            kwargs[k] = v.__name__
        kwargs[k] = str(kwargs[k])
    return f"{args}-{json.dumps({'kwargs': kwargs}, sort_keys=True)}"


def orjsonify(data: Any, status_code: int = HTTPStatus.OK):
    return make_response(orjson.dumps(data), status_code, {"Content-Type": "application/json"})
