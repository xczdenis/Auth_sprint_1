from http import HTTPStatus

from flasgger import swag_from
from flask import current_app, jsonify, request
from flask_jwt_extended import create_access_token, get_jwt, get_jwt_identity, jwt_required
from flask_pydantic import validate

from movies_auth.app import user_service
from movies_auth.app.api.v1.auth import bp
from movies_auth.app.api.v1.auth.schemas import SignInRequestBody, SignUpRequestBody, user_response
from movies_auth.app.common.enums import AuthenticationMethods
from movies_auth.app.db.redis import redis_db


@bp.route("/signup", methods=["POST"])
@validate()
@swag_from("docs/signup.yml")
def signup(body: SignUpRequestBody):
    new_user = user_service.create_user(body.login, body.password)
    return user_response.dump(new_user), HTTPStatus.CREATED


@bp.route("/signin", methods=["POST"])
@validate()
@swag_from("docs/signin.yml")
def signin(body: SignInRequestBody):
    user, tokens = user_service.signin(
        AuthenticationMethods.jwt, body.login, body.password, **request.headers
    )
    return jsonify(**tokens), HTTPStatus.CREATED


@bp.route("/logout", methods=["POST"])
@jwt_required()
@swag_from("docs/logout.yml")
def logout():
    user = user_service.get_user_from_jwt()

    claims = get_jwt()
    jti = claims.get("jti")
    refresh_token_jti = claims.get("refresh_token_jti")
    redis_db.set(jti, "", ex=current_app.config.get("JWT_ACCESS_TOKEN_EXPIRES"))
    redis_db.set(refresh_token_jti, "", ex=current_app.config.get("JWT_REFRESH_TOKEN_EXPIRES"))

    user.remove_entry(**request.headers)

    return jsonify(msg="Access and refresh tokens revoked")


@bp.route("/refresh", methods=["POST"])
@jwt_required(refresh=True)
@swag_from("docs/refresh.yml")
def refresh():
    identity = get_jwt_identity()
    claims = get_jwt()
    additional_claims = {"is_superuser": claims.get("is_superuser"), "refresh_token_jti": claims.get("jti")}
    access_token = create_access_token(identity=identity, additional_claims=additional_claims)
    return jsonify(access_token=access_token), HTTPStatus.CREATED
