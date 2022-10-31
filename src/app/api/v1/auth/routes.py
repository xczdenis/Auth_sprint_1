from flasgger import swag_from
from flask import current_app, jsonify, request
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    get_jti,
    get_jwt,
    get_jwt_identity,
    jwt_required,
)

from app import db, jwt_redis_blocklist
from app.api.v1.auth import bp
from app.models import User


@bp.route("/signup/", methods=["POST"])
@swag_from("docs/signup.yml")
def signup():
    login = request.json.get("login")
    password = request.json.get("password")

    if not login or not password:
        return jsonify(msg="Login or password was not provided"), 400

    user = User.query.filter_by(login=login).first()
    if user:
        return jsonify(msg="The user with the provided login already exists"), 409

    new_user = User()
    new_user.login = login
    new_user.set_password(password)

    db.session.add(new_user)
    db.session.commit()

    return jsonify(new_user.to_dict()), 201


@bp.route("/signin/", methods=["POST"])
@swag_from("docs/signin.yml")
def signin():
    login = request.json.get("login")
    password = request.json.get("password")

    if not login or not password:
        return jsonify(msg="Login or password was not provided"), 400

    user = User.query.filter_by(login=login).first()
    if not user or not user.check_password(raw_password=password):
        return jsonify(msg="Login or password is incorrect"), 401

    identity = user.id

    additional_claims = {
        "is_superuser": user.is_superuser,
    }
    refresh_token = create_refresh_token(identity=identity, additional_claims=additional_claims)

    additional_claims["refresh_token_jti"] = get_jti(refresh_token)
    access_token = create_access_token(identity=identity, additional_claims=additional_claims)

    user.log_entry(**request.headers)

    return jsonify(access_token=access_token, refresh_token=refresh_token), 201


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
    return jsonify(access_token=access_token), 201


@bp.route("/logout/", methods=["POST"])
@jwt_required()
@swag_from("docs/logout.yml")
def logout():
    identity = get_jwt_identity()

    user = User.query.filter_by(id=identity).first()
    if not user:
        return jsonify(msg="Token is incorrect"), 401

    claims = get_jwt()
    jti = claims.get("jti")
    refresh_token_jti = claims.get("refresh_token_jti")
    jwt_redis_blocklist.set(jti, "", ex=current_app.config.get("JWT_ACCESS_TOKEN_EXPIRES"))
    jwt_redis_blocklist.set(
        refresh_token_jti, "", ex=current_app.config.get("JWT_REFRESH_TOKEN_EXPIRES")
    )

    user.remove_entry(**request.headers)

    return jsonify(msg="Access and refresh tokens revoked")
