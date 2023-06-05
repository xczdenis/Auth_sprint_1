from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

from movies_auth.app.settings import app_settings, redis_settings

limiter = Limiter(
    key_func=get_remote_address,
    storage_uri=f"redis://{redis_settings.REDIS_HOST}:{redis_settings.REDIS_PORT}",
    strategy="fixed-window",
    default_limits=[f"{app_settings.RPS_LIMIT} per second"],
)
