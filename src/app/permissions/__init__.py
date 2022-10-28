from flask import Blueprint

bp = Blueprint("permissions", __name__)

from app.permissions import routes
