from flask import Blueprint

NAMESPACE = "healthcheck"

bp = Blueprint(NAMESPACE, __name__, url_prefix=f"/{NAMESPACE}")

from movies_auth.app.api.v1.healthcheck import routes
