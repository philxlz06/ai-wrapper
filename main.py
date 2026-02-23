# main.py
import threading
import time
from queue import deque
from client import call_ai_api

request_queue = deque()

# simulate 3 concurrent workers
def worker():
    while True:
        if request_queue:
            req = request_queue.popleft()
            call_ai_api(req)
        else:
            time.sleep(0.01)

for _ in range(3):
    t = threading.Thread(target=worker, daemon=True)
    t.start()

# simulate 1100 requests
for i in range(1100):
    request_queue.append(i)

# keep main alive
while True:
    time.sleep(1)