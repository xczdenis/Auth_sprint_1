import redis

from movies_auth.app.settings import redis_settings

redis_db = redis.Redis(host=redis_settings.REDIS_HOST, port=redis_settings.REDIS_PORT, db=0)
