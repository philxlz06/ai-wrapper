import time
import asyncio
from config import REQUESTS_PER_MINUTE, REFILL_INTERVAL


class TokenBucket:
    def __init__(self):
        self.capacity = REQUESTS_PER_MINUTE
        self.tokens = REQUESTS_PER_MINUTE
        self.last_refill = time.monotonic()
        self.lock = asyncio.Lock()

    def _refill(self):
        now = time.monotonic()
        elapsed = now - self.last_refill

        refill_amount = (elapsed / REFILL_INTERVAL) * self.capacity
        if refill_amount > 0:
            self.tokens = min(self.capacity, self.tokens + refill_amount)
            self.last_refill = now

    async def acquire(self):
        async with self.lock:
            self._refill()

            if self.tokens >= 1:
                self.tokens -= 1
                return True

            return False