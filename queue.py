# queue.py
import time
from collections import deque

class RequestQueue:
    def __init__(self, rate_limiter):
        self.queue = deque()
        self.rate_limiter = rate_limiter

    def submit(self, request_id):
        self.queue.append(request_id)

    def run(self):
        while self.queue:
            if self.rate_limiter.allow():
                req = self.queue.popleft()
                print(f"Processed request {req}")
            else:
                time.sleep(0.05)