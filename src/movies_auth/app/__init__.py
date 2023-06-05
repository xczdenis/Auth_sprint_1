from flask import Flask

from movies_auth.app.contrib import jaeger, jwt, limiter, ma, swagger
from movies_auth.app.contrib.orjson import OrJSONProvider
from movies_auth.app.db.pg import db, migrate
from movies_auth.app.db.redis import redis_db
from movies_auth.app.middleware.request_id import request_id_middleware
from movies_auth.app.oauth2 import google_oauth, mail_oauth, oauth_manager, yandex_oauth
from movies_auth.app.services.permissions import PermissionService
from movies_auth.app.services.users import UserService
from movies_auth.app.settings import app_settings

user_service: UserService = UserService()
permission_service: PermissionService = PermissionService()


@jwt.token_in_blocklist_loader
def check_if_token_is_revoked(jwt_header, jwt_payload: dict):
    jti = jwt_payload["jti"]
    token_in_redis = redis_db.get(jti)
    return token_in_redis is not None


def create_app():
    app = Flask(__name__)
    app.config.from_object(app_settings)

    db.init_app(app)
    migrate.init_app(app, db)

    jwt.init_app(app)

    if app_settings.ENABLE_TRACER:
        jaeger.init_app(app)

    swagger.init_app(app)

    limiter.init_app(app)

    ma.init_app(app)

    oauth_manager.init_app(app, cache=redis_db)
    oauth_manager.register_provider(yandex_oauth)
    oauth_manager.register_provider(mail_oauth)
    oauth_manager.register_provider(google_oauth)

    from movies_auth.app.api import bp as api_bp

    app.register_blueprint(api_bp)

    app.json = OrJSONProvider(app)

    request_id_middleware(app)

    return app
