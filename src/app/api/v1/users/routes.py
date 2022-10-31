from flasgger import swag_from
from flask import jsonify, request
from flask_jwt_extended import get_jwt_identity, jwt_required

from app import db
from app.api.v1.users import bp
from app.decorators import is_superuser_required
from app.models import Permission, User


@bp.route("/", methods=["GET"])
@jwt_required()
@is_superuser_required()
def users():
    return jsonify([item.to_dict() for item in User.query.all()])


@bp.route("/access_log/")
@jwt_required()
@swag_from("docs/access_log.yml")
def access_log():
    identity = get_jwt_identity()
    data = []

    user = User.query.filter_by(id=identity).first()
    if user:
        data = user.entry_records

    return jsonify(data=[item.to_dict() for item in data])


@bp.route("/change_password/", methods=["POST"])
@jwt_required()
@swag_from("docs/change_password.yml")
def change_password():
    old_password = request.json.get("old_password")
    new_password = request.json.get("new_password")

    if not old_password or not new_password:
        return jsonify(msg="Old password or new password was not provided"), 400

    identity = get_jwt_identity()
    user = User.query.filter_by(id=identity).first()
    if not user:
        return jsonify(msg="Token is incorrect"), 401

    if not user.check_password(raw_password=old_password):
        return jsonify(msg="Old password is incorrect"), 401

    user.set_password(new_password)

    db.session.commit()

    return jsonify(msg="The password has been changed"), 200


@bp.route("/permissions/", methods=["PUT", "DELETE"])
@jwt_required()
@is_superuser_required()
@swag_from("docs/users_permissions_put.yml", methods=["PUT"])
@swag_from("docs/users_permissions_delete.yml", methods=["DELETE"])
def users_permissions():
    users_permissions_data = request.json.get("users_permissions")
    if users_permissions_data is None:
        return jsonify(msg="The 'users_permissions' parameter was not provided"), 400
    elif not users_permissions_data:
        return jsonify(msg="The 'users_permissions' parameter is empty"), 400
    elif not isinstance(users_permissions_data, dict):
        return jsonify(msg="The 'users_permissions' parameter should be a dict"), 400

    for k, v in users_permissions_data.items():
        if not isinstance(v, list):
            return jsonify(msg="The 'permissions' should be an array"), 400
        for permission_id in set(v):
            if not isinstance(permission_id, str):
                return jsonify(msg="The 'permission id' should be a string"), 400

    for user_id, permissions_ids in users_permissions_data.items():
        user = User.query.filter_by(id=user_id).first()
        if not user:
            return jsonify(msg="User not found"), 404

        updated_user_permissions = user.permissions[:]
        permissions_from_request = (
            db.session.query(Permission).filter(Permission.id.in_(permissions_ids)).all()
        )
        if request.method == "PUT":
            updated_user_permissions += permissions_from_request
        elif request.method == "DELETE":
            updated_user_permissions = list(
                set(user.permissions[:]) - set(permissions_from_request)
            )

        user.permissions = list(set(updated_user_permissions))

        db.session.commit()

    return jsonify(msg="Users permissions updated successfully"), 200


@bp.route("/has_perms/", methods=["POST"])
@jwt_required()
@swag_from("docs/has_perms_post.yml", methods=["POST"])
def has_perms():
    permissions_codenames = request.json.get("permissions")
    condition = request.json.get("condition", "AND")
    if permissions_codenames is None:
        return jsonify(msg="The 'permissions' parameter was not provided"), 400
    elif not permissions_codenames:
        return jsonify(msg="The 'permissions' parameter is empty"), 400
    elif not isinstance(permissions_codenames, list):
        return jsonify(msg="The 'permissions' parameter should be an array"), 400

    for i in range(len(permissions_codenames)):
        if not isinstance(permissions_codenames[i], str):
            return jsonify(msg="The 'permission codename' should be a string"), 400
        permissions_codenames[i] = permissions_codenames[i].lower()

    identity = get_jwt_identity()
    user = User.query.filter_by(id=identity).first()
    if not user:
        return jsonify(msg="Token is incorrect"), 401

    permissions = (
        Permission.query.join(Permission.users)
        .filter(User.id == identity, Permission.codename.in_(permissions_codenames))
        .all()
    )

    user_has_perms = False
    if condition.upper() == "AND":
        user_has_perms = len(permissions_codenames) == len(permissions)
    elif condition.upper() == "OR":
        user_has_perms = len(permissions) > 0

    return jsonify(has_perms=user_has_perms), 200
