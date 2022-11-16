from flasgger import Swagger
from flask_jwt_extended import JWTManager
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

from app.contrib.jaeger import JaegerManager
from app.contrib.swagger import swagger_config, swagger_template
from config import settings

jaeger = JaegerManager(host=settings.JAEGER_HOST, port=settings.JAEGER_UDP_PORT)

swagger = Swagger()
swagger.config.update(swagger_config)
swagger.template = swagger_template

limiter = Limiter(
    key_func=get_remote_address,
    storage_uri=f"redis://{settings.REDIS_HOST}:{settings.REDIS_PORT}",
    strategy="fixed-window",
    default_limits=[f"{settings.RPS_LIMIT} per second"],
)

jwt = JWTManager()
