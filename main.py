import asyncio
from rate_limiter import TokenBucket


async def test():
    bucket = TokenBucket()
    success = 0

    for _ in range(1100):
        if await bucket.acquire():
            success += 1

    print("Allowed:", success)


asyncio.run(test())
