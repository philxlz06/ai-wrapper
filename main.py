# main.py
from collections import deque
from client import call_ai_api
import threading
import time

# ----------------------
# Setup
# ----------------------
request_queue = deque()

def worker():
    while True:
        try:
            req = request_queue.popleft()
        except IndexError:
            break
        call_ai_api(req, prompt=f"Hello from request {req}")

# ----------------------
# First run: 10 requests
# ----------------------
for i in range(10):
    request_queue.append(i)

threads = []
for _ in range(3):  # 3 concurrent workers
    t = threading.Thread(target=worker)
    t.start()
    threads.append(t)

for t in threads:
    t.join()

print("\n✅ First run complete.\n")

time.sleep(2)  # short pause before next run

# ----------------------
# Second run: 50 requests
# ----------------------
request_queue = deque()
for i in range(50):
    request_queue.append(i)

threads = []
for _ in range(3):
    t = threading.Thread(target=worker)
    t.start()
    threads.append(t)

for t in threads:
    t.join()

print("\n✅ Second run complete.\n")