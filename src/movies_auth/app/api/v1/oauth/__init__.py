from flask import Blueprint

bp = Blueprint("oauth", __name__, url_prefix="/oauth")

from movies_auth.app.api.v1.oauth import routes
