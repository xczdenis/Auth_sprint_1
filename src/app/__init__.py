import redis
from flasgger import Swagger
from flask import Flask
from flask_jwt_extended import JWTManager
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

from app.jaeger import JaegerManager
from app.oauth2 import (
    GoogleOAuthProvider,
    MailOAuthProvider,
    OAuthManager,
    YandexOAuthProvider,
)
from app.swagger import swagger_config, swagger_template
from config import settings

db = SQLAlchemy()
migrate = Migrate()

jwt = JWTManager()
redis_db = redis.Redis(host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=0)

jaeger = JaegerManager(host=settings.JAEGER_HOST, port=settings.JAEGER_UDP_PORT)

swagger = Swagger()
swagger.config.update(swagger_config)

oauth_manager = OAuthManager()
yandex_oauth = YandexOAuthProvider()
mail_oauth = MailOAuthProvider()
google_oauth = GoogleOAuthProvider()

limiter = Limiter(
    key_func=get_remote_address,
    storage_uri=f"redis://{settings.REDIS_HOST}:{settings.REDIS_PORT}",
    strategy="fixed-window",
    default_limits=[f"{settings.RPS_LIMIT} per second"],
)


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
    swagger.template = swagger_template

    limiter.init_app(app)

    from app.api import bp as api_bp

    app.register_blueprint(api_bp)

    return app


from app import models
