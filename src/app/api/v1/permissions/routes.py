from http import HTTPStatus

from flasgger import swag_from
from flask import jsonify, request
from flask_jwt_extended import jwt_required

from app import db
from app.api.v1.permissions import bp
from app.decorators import superuser_required
from app.models import Permission


@bp.route("/", methods=["GET", "POST"])
@jwt_required()
@superuser_required()
@swag_from("docs/permissions_get.yml", methods=["GET"])
@swag_from("docs/permissions_post.yml", methods=["POST"])
def permissions():
    if request.method == "POST":
        name = request.json.get("name")
        codename = request.json.get("codename")

        if not name or not codename:
            return (
                jsonify(msg="The 'name' or 'codename' parameters was not provided"),
                HTTPStatus.BAD_REQUEST,
            )

        if Permission.query.filter_by(codename=codename).first():
            return (
                jsonify(
                    msg="Permission with codename '{codename}' already exists".format(
                        codename=codename
                    )
                ),
                HTTPStatus.CONFLICT,
            )

        new_permission = Permission()
        new_permission.name = name
        new_permission.codename = codename

        db.session.add(new_permission)
        db.session.commit()

        return jsonify(new_permission.to_dict()), HTTPStatus.CREATED

    return jsonify([item.to_dict() for item in Permission.query.all()])


@bp.route("/<id>/", methods=["GET", "DELETE", "PATCH"])
@jwt_required()
@superuser_required()
@swag_from("docs/permission_detail_get.yml", methods=["GET"])
@swag_from("docs/permission_detail_delete.yml", methods=["DELETE"])
@swag_from("docs/permission_detail_patch.yml", methods=["PATCH"])
def permission_detail(id):
    permission = Permission.query.filter_by(id=id).first()
    if not permission:
        return jsonify(msg="Permission not found"), HTTPStatus.NOT_FOUND

    if request.method == "DELETE":
        db.session.delete(permission)
        db.session.commit()
        return jsonify(msg="Permission deleted successfully")

    elif request.method == "PATCH":
        name = request.json.get("name")
        codename = request.json.get("codename")

        if not name and not codename:
            return (
                jsonify(msg="The 'name' or 'codename' parameters was not provided"),
                HTTPStatus.BAD_REQUEST,
            )

        if codename:
            if (
                db.session.query(Permission)
                .filter(Permission.id != id, Permission.codename == codename)
                .first()
            ):
                return (
                    jsonify(
                        msg="Permission with codename '{codename}' already exists".format(
                            codename=codename
                        )
                    ),
                    HTTPStatus.CONFLICT,
                )
            permission.codename = codename
        if name:
            permission.name = name

        db.session.commit()
        return jsonify(permission.to_dict())

    return jsonify(permission.to_dict())
