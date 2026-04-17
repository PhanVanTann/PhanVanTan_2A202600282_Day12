import time
import redis
from app.config import settings

r = redis.from_url(settings.REDIS_URL, decode_responses=True)

class RateLimiter:
    def __init__(self, limit_per_minute: int):
        self.limit = limit_per_minute

    def is_allowed(self, user_id: str) -> bool:
        key = f"rate:{user_id}"
        now = int(time.time())

        window = now // 60
        redis_key = f"{key}:{window}"

        current = r.get(redis_key)
        if current and int(current) >= self.limit:
            return False

        pipe = r.pipeline()
        pipe.incr(redis_key, 1)
        pipe.expire(redis_key, 60)
        pipe.execute()

        return True