from flask import Blueprint

bp = Blueprint("users", __name__, url_prefix="/users")

from app.api.v1.users import routes
