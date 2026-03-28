from redis import Redis

from loodation.config import settings

cache = Redis(
    host=settings.redis.host,
    port=settings.redis.port,
    db=settings.redis.db,
    username=settings.redis.username,
    password=settings.redis.password.get_secret_value(),
    decode_responses=True,
)
