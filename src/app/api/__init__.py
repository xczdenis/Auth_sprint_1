from flask import Blueprint

from app.api.v1 import bp as api_v1

bp = Blueprint("api", __name__, url_prefix="/api")

bp.register_blueprint(api_v1)
