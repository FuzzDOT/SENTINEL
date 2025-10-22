import os
import redis
from ..core.settings import settings


def get_redis_client():
    """Return a redis client from REDIS_URL env or settings, or None if not configured."""
    url = os.getenv("REDIS_URL") or settings.REDIS_URL
    if not url:
        return None
    return redis.from_url(str(url))
