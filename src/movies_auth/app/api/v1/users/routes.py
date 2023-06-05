from http import HTTPStatus

from flasgger import swag_from
from flask import jsonify, request
from flask_jwt_extended import get_jwt_identity, jwt_required
from flask_pydantic import validate

from movies_auth.app import permission_service, user_service
from movies_auth.app.api.v1.users import bp
from movies_auth.app.api.v1.users.schemas import (
    HasPermRequest,
    PasswordUpdate,
    PermissionsUpdate,
    access_log_item_response,
    user_detail_response,
    user_list_item_response,
)
from movies_auth.app.common.decorators import paginate, superuser_required
from movies_auth.app.common.pagination import get_pagination_params
from movies_auth.app.models import EntryRecord, User


@bp.route("", methods=["GET"])
@jwt_required()
@superuser_required()
@paginate(ma_schema=user_list_item_response)
def users():
    page_number, page_size = get_pagination_params()
    return User.query.paginate(page=page_number, per_page=page_size)


@bp.route("/<user_id>", methods=["GET"])
@jwt_required()
@superuser_required()
def user_detail(user_id):
    user = user_service.get_user_by_id(user_id)
    return user_detail_response.dump(user)


@bp.route("/access_log")
@jwt_required()
@paginate(ma_schema=access_log_item_response)
@swag_from("docs/access_log.yml")
def access_log():
    user = user_service.get_user_from_jwt()
    page_number, page_size = get_pagination_params()
    return (
        EntryRecord.query.join(User).filter(User.id == user.id).paginate(page=page_number, per_page=page_size)
    )


@bp.route("/change_password", methods=["POST"])
@jwt_required()
@validate()
@swag_from("docs/change_password.yml")
def change_password(body: PasswordUpdate):
    user = user_service.get_user_from_jwt()
    user_service.change_password(user, body.old_password, body.new_password)
    return jsonify(msg="The password has been changed"), HTTPStatus.OK


@bp.route("/permissions", methods=["PUT", "DELETE"])
@jwt_required()
@validate()
@superuser_required()
@swag_from("docs/users_permissions_put.yml", methods=["PUT"])
@swag_from("docs/users_permissions_delete.yml", methods=["DELETE"])
def users_permissions(body: PermissionsUpdate):
    all_users_permissions = body.data
    for user_permissions in all_users_permissions:
        user = user_service.get_user_by_id(user_permissions.user_id)
        permissions_from_db = permission_service.get_permissions_by_codenames(user_permissions.permissions)
        if request.method == "PUT":
            user_service.add_user_permissions(user, permissions_from_db)
        elif request.method == "DELETE":
            user_service.remove_user_permissions(user, permissions_from_db)

    return jsonify(msg="Users permissions updated successfully"), HTTPStatus.OK


@bp.route("/has_perms", methods=["POST"])
@jwt_required()
@validate()
@swag_from("docs/has_perms_post.yml", methods=["POST"])
def has_perms(body: HasPermRequest):
    identity = get_jwt_identity()
    user_has_perms = user_service.has_perms(identity, body.permissions, body.condition)
    return jsonify(has_perms=user_has_perms), HTTPStatus.OK
