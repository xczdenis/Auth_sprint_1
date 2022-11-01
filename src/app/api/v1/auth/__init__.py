from flask import Blueprint

bp = Blueprint("auth", __name__, url_prefix="/auth")

from app.api.v1.auth import routes
