from aioredis import Redis

redis: Redis = None  # type: ignore


async def get_redis() -> Redis:
    return redis
