from flask import Flask

from app.contrib import jaeger, jwt, limiter, swagger
from app.db.pg import db, migrate
from app.db.redis import redis_db
from app.oauth2 import google_oauth, mail_oauth, oauth_manager, yandex_oauth
from config import settings


@jwt.token_in_blocklist_loader
def check_if_token_is_revoked(jwt_header, jwt_payload: dict):
    jti = jwt_payload["jti"]
    token_in_redis = redis_db.get(jti)
    return token_in_redis is not None


def create_app():
    app = Flask(__name__)
    app.config.from_object(settings)

    db.init_app(app)
    migrate.init_app(app, db)

    jwt.init_app(app)

    jaeger.init_app(app)

    oauth_manager.init_app(app, cache=redis_db)
    oauth_manager.register_provider(yandex_oauth)
    oauth_manager.register_provider(mail_oauth)
    oauth_manager.register_provider(google_oauth)

    swagger.init_app(app)

    limiter.init_app(app)

    from app.api import bp as api_bp

    app.register_blueprint(api_bp)

    return app


from app import models
