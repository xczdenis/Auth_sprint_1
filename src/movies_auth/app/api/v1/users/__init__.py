from flask import Blueprint

NAMESPACE = "users"

bp = Blueprint(NAMESPACE, __name__, url_prefix=f"/{NAMESPACE}")

from movies_auth.app.api.v1.users import routes
