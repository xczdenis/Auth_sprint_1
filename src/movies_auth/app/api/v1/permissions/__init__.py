from flask import Blueprint

bp = Blueprint("permissions", __name__, url_prefix="/permissions")

from movies_auth.app.api.v1.permissions import routes

bp.add_url_rule("/<permission_id>", view_func=routes.PermissionDetail.as_view("permission_detail"))
bp.add_url_rule("", view_func=routes.PermissionsList.as_view("permissions_list"))
