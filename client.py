# client.py
from retry import retry
from circuit_breaker import CircuitBreaker
from rate_limiter import TokenBucket

breaker = CircuitBreaker()
bucket = TokenBucket()

def call_ai_api(request_id):
    if not breaker.allow():
        print(f"Circuit open. Dropping request {request_id}")
        return

    # Wait for token
    allowed = False
    while not allowed:
        allowed = bucket._refill() or bucket.tokens >= 1
        if allowed:
            bucket.tokens -= 1
            break
        # short sleep to avoid busy loop
        import time; time.sleep(0.01)

    # Wrap fake API call with retry
    def fake_request():
        # simulate intermittent failure
        import random
        if random.random() < 0.2:
            raise Exception("API fail")
        return f"Response for {request_id}"

    try:
        result = retry(fake_request)
        breaker.record_success()
        print(f"Success: {result}")
    except Exception as e:
        breaker.record_failure()
        print(f"Failed: {request_id} -> {e}")