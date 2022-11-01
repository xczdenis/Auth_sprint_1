import redis
from flasgger import Swagger
from flask import Blueprint, Flask
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

from app.swagger import swagger_config, swagger_template
from config import settings

db = SQLAlchemy()
migrate = Migrate()

jwt = JWTManager()
jwt_redis_blocklist = redis.Redis(host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=0)


@jwt.token_in_blocklist_loader
def check_if_token_is_revoked(jwt_header, jwt_payload: dict):
    jti = jwt_payload["jti"]
    token_in_redis = jwt_redis_blocklist.get(jti)
    return token_in_redis is not None


swagger = Swagger()
swagger.config.update(swagger_config)


def create_app():
    app = Flask(__name__)
    app.config.from_object(settings)

    db.init_app(app)
    migrate.init_app(app, db)

    jwt.init_app(app)

    swagger.init_app(app)
    swagger.template = swagger_template

    from app.api.v1 import bp as api_v1_bp

    api = Blueprint("api", __name__, url_prefix="/api")
    api.register_blueprint(api_v1_bp)

    app.register_blueprint(api)

    return app


from app import models
