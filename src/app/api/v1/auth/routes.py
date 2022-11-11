from http import HTTPStatus

from flasgger import swag_from
from flask import current_app, jsonify, request
from flask_jwt_extended import (
    create_access_token,
    get_jwt,
    get_jwt_identity,
    jwt_required,
)

from app import db, redis_db
from app.api.v1.auth import bp
from app.models import User
from app.utils import obtain_auth_tokens


@bp.route("/signup/", methods=["POST"])
@swag_from("docs/signup.yml")
def signup():
    login = request.json.get("login")
    password = request.json.get("password")

    if not login or not password:
        return jsonify(msg="Login or password was not provided"), HTTPStatus.BAD_REQUEST

    user = User.query.filter_by(login=login).first()
    if user:
        return jsonify(msg="The user with the provided login already exists"), HTTPStatus.CONFLICT

    new_user = User()
    new_user.login = login
    new_user.set_password(password)

    db.session.add(new_user)
    db.session.commit()

    return jsonify(new_user.to_dict()), HTTPStatus.CREATED


@bp.route("/signin/", methods=["POST"])
@swag_from("docs/signin.yml")
def signin():
    login = request.json.get("login")
    password = request.json.get("password")

    if not login or not password:
        return jsonify(msg="Login or password was not provided"), HTTPStatus.BAD_REQUEST

    user = User.query.filter_by(login=login).first()
    if not user or not user.check_password(raw_password=password):
        return jsonify(msg="Login or password is incorrect"), HTTPStatus.UNAUTHORIZED

    tokens = obtain_auth_tokens(user.id, user.is_superuser)
    user.log_entry(**request.headers)

    return jsonify(**tokens), HTTPStatus.CREATED


@bp.route("/refresh/", methods=["POST"])
@jwt_required(refresh=True)
@swag_from("docs/refresh.yml")
def refresh():
    identity = get_jwt_identity()
    claims = get_jwt()
    additional_claims = {
        "is_superuser": claims.get("is_superuser"),
        "refresh_token_jti": claims.get("jti"),
    }
    access_token = create_access_token(identity=identity, additional_claims=additional_claims)
    return jsonify(access_token=access_token), HTTPStatus.CREATED


@bp.route("/logout/", methods=["POST"])
@jwt_required()
@swag_from("docs/logout.yml")
def logout():
    identity = get_jwt_identity()

    user = User.query.filter_by(id=identity).first()
    if not user:
        return jsonify(msg="Token is incorrect"), HTTPStatus.UNAUTHORIZED

    claims = get_jwt()
    jti = claims.get("jti")
    refresh_token_jti = claims.get("refresh_token_jti")
    redis_db.set(jti, "", ex=current_app.config.get("JWT_ACCESS_TOKEN_EXPIRES"))
    redis_db.set(refresh_token_jti, "", ex=current_app.config.get("JWT_REFRESH_TOKEN_EXPIRES"))

    user.remove_entry(**request.headers)

    return jsonify(msg="Access and refresh tokens revoked")
