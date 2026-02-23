# retry.py
#Goal

#If a request fails, don’t retry instantly → retry safely.

import time
import random

def retry(fn, max_retries=5):
    delay = 0.1
    for attempt in range(max_retries):
        try:
            return fn()
        except Exception as e:
            time.sleep(delay + random.random() * delay)
            delay *= 2
    raise Exception("Retry limit hit")