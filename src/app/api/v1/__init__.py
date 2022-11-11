from flask import Blueprint

from app.api.v1.auth import bp as auth_bp
from app.api.v1.oauth import bp as oauth_bp
from app.api.v1.permissions import bp as permissions_bp
from app.api.v1.users import bp as users_bp

bp = Blueprint("v1", __name__, url_prefix="/v1")

bp.register_blueprint(auth_bp)
bp.register_blueprint(oauth_bp)
bp.register_blueprint(permissions_bp)
bp.register_blueprint(users_bp)
