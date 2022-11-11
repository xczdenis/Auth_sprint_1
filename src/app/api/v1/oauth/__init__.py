from flask import Blueprint

bp = Blueprint("oauth", __name__, url_prefix="/oauth")

from app.api.v1.oauth import routes
