import time
from collections import defaultdict, deque

_store = defaultdict(deque)

def check_rate_limit(key: str, limit: int):
    now = time.time()
    q = _store[key]

    while q and q[0] < now - 60:
        q.popleft()

    if len(q) >= limit:
        return False

    q.append(now)
    return True