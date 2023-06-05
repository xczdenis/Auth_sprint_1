from flask import Blueprint

NAMESPACE = "auth"

bp = Blueprint(NAMESPACE, __name__, url_prefix=f"/{NAMESPACE}")

from movies_auth.app.api.v1.auth import routes  # noqa: E402
