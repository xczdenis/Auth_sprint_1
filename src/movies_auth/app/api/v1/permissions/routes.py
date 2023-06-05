from http import HTTPStatus

from flasgger import swag_from
from flask import jsonify
from flask.views import MethodView
from flask_jwt_extended import jwt_required
from flask_pydantic import validate

from movies_auth.app import permission_service
from movies_auth.app.api.v1.permissions.schemas import PermissionCreate, PermissionUpdate, permission_response
from movies_auth.app.common.decorators import paginate, superuser_required
from movies_auth.app.common.exceptions import EntityDoesntExists
from movies_auth.app.common.pagination import get_pagination_params
from movies_auth.app.models import Permission


class PermissionsList(MethodView):
    decorators = [superuser_required(), jwt_required()]

    @paginate(ma_schema=permission_response)
    @swag_from("docs/permissions_get.yml")
    def get(self):
        page_number, page_size = get_pagination_params()
        return Permission.query.paginate(page=page_number, per_page=page_size)

    @validate()
    @swag_from("docs/permissions_post.yml")
    def post(self, body: PermissionCreate):
        new_permission = permission_service.create_permission(body.name, body.codename)
        return permission_response.dump(new_permission), HTTPStatus.CREATED


class PermissionDetail(MethodView):
    decorators = [superuser_required(), jwt_required()]

    @swag_from("docs/permission_detail_get.yml")
    def get(self, permission_id):
        permission = permission_service.get_permission_by_id(permission_id)
        if not permission:
            raise EntityDoesntExists("Permission not found")
        return permission_response.dump(permission)

    @swag_from("docs/permission_detail_delete.yml")
    def delete(self, permission_id):
        permission_service.delete_permission_by_id(permission_id)
        return jsonify(msg="Permission deleted successfully")

    @validate()
    @swag_from("docs/permission_detail_patch.yml")
    def patch(self, body: PermissionUpdate, permission_id):
        permission = permission_service.update_permission_by_id(permission_id, **body.dict())
        return permission_response.dump(permission)
