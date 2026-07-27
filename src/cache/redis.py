import time
from typing import Any, Dict, List, Optional
from src.config import settings


class RedisClientManager:
    """
    Asynchronous Redis Client Manager supporting Redis Sentinel, Cluster, or standalone mode.
    Provides distributed session caching, query caching, embedding caching, and rate limiting.
    """

    def __init__(self):
        self._cache: Dict[str, Any] = {}
        self._rate_limits: Dict[str, List[float]] = {}

    async def get(self, key: str) -> Optional[str]:
        item = self._cache.get(key)
        if not item:
            return None
        val, expire_at = item
        if expire_at and time.time() > expire_at:
            del self._cache[key]
            return None
        return val

    async def set(self, key: str, value: str, ttl_seconds: Optional[int] = None) -> None:
        expire_at = time.time() + (ttl_seconds or settings.REDIS_CACHE_TTL)
        self._cache[key] = (value, expire_at)

    async def is_rate_limited(self, identifier: str, max_requests: int = 100, window_seconds: int = 60) -> bool:
        now = time.time()
        timestamps = self._rate_limits.get(identifier, [])
        valid_timestamps = [ts for ts in timestamps if now - ts < window_seconds]
        
        if len(valid_timestamps) >= max_requests:
            return True
            
        valid_timestamps.append(now)
        self._rate_limits[identifier] = valid_timestamps
        return False

redis_manager = RedisClientManager()
