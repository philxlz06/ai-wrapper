# client.py
import openai
import os
import time
import random
from retry import retry
from circuit_breaker import CircuitBreaker
from rate_limiter import TokenBucket

openai.api_key = os.getenv("OPENAI_API_KEY")

breaker = CircuitBreaker()
bucket = TokenBucket()


def call_ai_api(request_id, prompt="Hello"):
    # ----------------------
    # Circuit breaker
    # ----------------------
    if not breaker.allow():
        print(f"Circuit open. Dropping request {request_id}")
        return

    # ----------------------
    # Token bucket wait
    # ----------------------
    allowed = False
    while not allowed:
        bucket._refill()
        if bucket.tokens >= 1:
            bucket.tokens -= 1
            allowed = True
        else:
            time.sleep(0.01)

    # ----------------------
    # Retry wrapper
    # ----------------------
    def request_fn():
        # Real API call
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}]
        )
        return response.choices[0].message.content

    try:
        result = retry(request_fn)
        breaker.record_success()
        print(f"✅ Success [{request_id}]: {result[:50]}...")
    except Exception as e:
        breaker.record_failure()
        print(f"❌ Failed [{request_id}]: {e}")
