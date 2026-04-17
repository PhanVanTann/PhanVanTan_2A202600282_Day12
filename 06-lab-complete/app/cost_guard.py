import datetime
import redis
from app.config import settings

r = redis.from_url(settings.REDIS_URL, decode_responses=True)

class CostGuard:
    def __init__(self, monthly_limit: float):
        self.limit = monthly_limit

    def add_cost(self, cost: float):
        month = datetime.datetime.utcnow().strftime("%Y-%m")
        key = f"cost:{month}"

        current = float(r.get(key) or 0)
        new_total = current + cost

        r.set(key, new_total)

        if new_total > self.limit:
            raise Exception("Monthly cost limit exceeded")

    def get_cost(self):
        month = datetime.datetime.utcnow().strftime("%Y-%m")
        return float(r.get(f"cost:{month}") or 0)